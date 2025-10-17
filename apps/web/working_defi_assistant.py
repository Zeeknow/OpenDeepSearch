
#!/usr/bin/env python3
"""
Safe DeFi Assistant - Single-file server + modern UI
Run: python safe_defi_assistant.py
"""

import os
import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import traceback
import time
import logging
from datetime import datetime
import asyncio
import aiohttp
from typing import Dict, List, Optional

load_dotenv()

# API keys are now loaded from .env file
# Make sure your .env file contains:
# SERPER_API_KEY=your_serper_key
# OPENROUTER_API_KEY=your_openrouter_key
# JINA_API_KEY=your_jina_key
# LITELLM_API_KEY=your_litellm_key
# LITELLM_MODEL_ID=openrouter/google/gemini-2.0-flash-001
# ETHERSCAN_API_KEY=your_etherscan_key

# Import OpenDeepSearch
try:
    from opendeepsearch.ods_tool import OpenDeepSearchTool
    logger = logging.getLogger(__name__)
    logger.info("OpenDeepSearch imported successfully")
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.error(f"Failed to import OpenDeepSearch: {e}")
    OpenDeepSearchTool = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('defi_assistant.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize OpenDeepSearch tool globally
search_tool = None
if OpenDeepSearchTool:
    try:
        search_tool = OpenDeepSearchTool(
            model_name="openrouter/google/gemini-2.0-flash-001",
            reranker="jina",
            search_provider="serper",
            serper_api_key=os.getenv("SERPER_API_KEY")
        )
        if not search_tool.is_initialized:
            search_tool.setup()
        logger.info("OpenDeepSearch tool initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize OpenDeepSearch tool: {e}")
        search_tool = None

# Market Data Integration Classes
class GasPriceMonitor:
    """Real-time gas price monitoring with multiple sources"""
    
    def __init__(self):
        self.sources = {
            'etherscan': 'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={}',
            'gasnow': 'https://www.gasnow.org/api/v3/gas/price',
            'blocknative': 'https://api.blocknative.com/gasprices/blockprices'
        }
        self.etherscan_key = os.getenv("ETHERSCAN_API_KEY")
    
    def get_gas_prices(self) -> Dict:
        """Get current gas prices from multiple sources"""
        gas_data = {
            'ethereum': {'slow': 0, 'standard': 0, 'fast': 0, 'instant': 0},
            'polygon': {'slow': 0, 'standard': 0, 'fast': 0},
            'arbitrum': {'slow': 0, 'standard': 0, 'fast': 0},
            'last_updated': datetime.now().isoformat(),
            'sources': []
        }
        
        try:
            # Ethereum gas prices from Etherscan
            if self.etherscan_key:
                url = self.sources['etherscan'].format(self.etherscan_key)
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == '1':
                        result = data.get('result', {})
                        gas_data['ethereum'] = {
                            'slow': int(result.get('SafeGasPrice', 0)),
                            'standard': int(result.get('ProposeGasPrice', 0)),
                            'fast': int(result.get('FastGasPrice', 0)),
                            'instant': int(result.get('FastGasPrice', 0)) * 1.2
                        }
                        gas_data['sources'].append('etherscan')
            
            # GasNow API (backup)
            try:
                response = requests.get(self.sources['gasnow'], timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == 200:
                        prices = data.get('data', {})
                        gas_data['ethereum'].update({
                            'slow': prices.get('slow', 0) // 1000000000,  # Convert wei to gwei
                            'standard': prices.get('standard', 0) // 1000000000,
                            'fast': prices.get('fast', 0) // 1000000000,
                            'instant': prices.get('rapid', 0) // 1000000000
                        })
                        if 'gasnow' not in gas_data['sources']:
                            gas_data['sources'].append('gasnow')
            except:
                pass
                
        except Exception as e:
            logger.error(f"Error fetching gas prices: {e}")
        
        return gas_data

class DeFiTVLTracker:
    """DeFi protocol TVL tracking and trends"""
    
    def __init__(self):
        self.defillama_api = "https://api.llama.fi/protocols"
        self.protocols = ['aave', 'compound', 'uniswap', 'curve', 'maker', 'convex']
    
    def get_protocol_tvl(self) -> Dict:
        """Get TVL data for major DeFi protocols"""
        tvl_data = {
            'protocols': {},
            'total_tvl': 0,
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            response = requests.get(self.defillama_api, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                for protocol in data:
                    if protocol.get('name', '').lower() in self.protocols:
                        protocol_name = protocol.get('name', '').lower()
                        tvl_data['protocols'][protocol_name] = {
                            'name': protocol.get('name', ''),
                            'tvl': protocol.get('tvl', 0),
                            'change_1d': protocol.get('change_1d', 0),
                            'change_7d': protocol.get('change_7d', 0),
                            'chains': protocol.get('chains', [])
                        }
                        tvl_data['total_tvl'] += protocol.get('tvl', 0)
                        
        except Exception as e:
            logger.error(f"Error fetching TVL data: {e}")
        
        return tvl_data

class YieldFarmingDetector:
    """Yield farming opportunity detection"""
    
    def __init__(self):
        self.apy_sources = {
            'defillama': 'https://yields.llama.fi/pools',
            'coindix': 'https://api.coindix.com/api/v1/pools'
        }
    
    def get_yield_opportunities(self) -> Dict:
        """Get current yield farming opportunities"""
        yield_data = {
            'opportunities': [],
            'top_yields': [],
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            # DeFiLlama yields API
            response = requests.get(self.apy_sources['defillama'], timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Filter for high-yield opportunities
                high_yield_pools = [
                    pool for pool in data.get('data', [])
                    if pool.get('apy', 0) > 10 and pool.get('tvlUsd', 0) > 1000000
                ]
                
                # Sort by APY and take top 10
                high_yield_pools.sort(key=lambda x: x.get('apy', 0), reverse=True)
                
                for pool in high_yield_pools[:10]:
                    yield_data['opportunities'].append({
                        'protocol': pool.get('project', ''),
                        'chain': pool.get('chain', ''),
                        'apy': round(pool.get('apy', 0), 2),
                        'tvl': pool.get('tvlUsd', 0),
                        'tokens': pool.get('symbol', ''),
                        'pool': pool.get('pool', '')
                    })
                
                yield_data['top_yields'] = yield_data['opportunities'][:5]
                
        except Exception as e:
            logger.error(f"Error fetching yield opportunities: {e}")
        
        return yield_data

# Initialize market data services
gas_monitor = GasPriceMonitor()
tvl_tracker = DeFiTVLTracker()
yield_detector = YieldFarmingDetector()

class DeFiAssistantHandler(BaseHTTPRequestHandler):
    # Helper to write JSON responses reliably
    def send_json_response(self, data, status=200):
        try:
            payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            # CORS for convenience (if you access UI from other host)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)
        except Exception as e:
            # If sending fails, log and try sending minimal error
            print("Failed to send JSON response:", e)
            try:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Internal response error"}).encode("utf-8"))
            except:
                pass

    # Allow preflight for fetch (if needed)
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        logger.info(f"GET request: {path} - Query: {parsed.query}")
        try:
            if path == "/":
                self.serve_html()
            elif path == "/gas":
                self.handle_gas_prices()
            elif path == "/risk":
                self.handle_risk_assessment(parsed.query)
            elif path == "/market-data":
                self.handle_market_data()
            elif path == "/gas-prices":
                self.handle_real_time_gas()
            elif path == "/tvl-data":
                self.handle_tvl_data()
            elif path == "/yield-opportunities":
                self.handle_yield_opportunities()
            else:
                logger.warning(f"GET 404: {path}")
                self.send_json_response({"success": False, "error": "Not found"}, status=404)
        except Exception as e:
            logger.error(f"GET handler exception: {e}")
            traceback.print_exc()
            self.send_json_response({"success": False, "error": str(e)}, status=500)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        logger.info(f"POST request: {path}")
        try:
            if path == "/chat":
                content_length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(content_length)
                try:
                    data = json.loads(raw.decode("utf-8"))
                    logger.info(f"Chat request data: {data}")
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")
                    self.send_json_response({"success": False, "error": "Invalid JSON"}, status=400)
                    return

                message = data.get("message", "")
                logger.info(f"Processing message: '{message}'")
                
                # Process chat synchronously and return structured JSON
                start_time = time.time()
                response_payload = self.process_message(message)
                processing_time = time.time() - start_time
                
                logger.info(f"Response payload: {response_payload}")
                logger.info(f"Processing time: {processing_time:.2f}s")
                
                # Always return JSON with success flag
                self.send_json_response(response_payload)
            else:
                logger.warning(f"POST 404: {path}")
                self.send_json_response({"success": False, "error": "Not found"}, status=404)
        except Exception as e:
            logger.error(f"POST handler exception: {e}")
            traceback.print_exc()
            self.send_json_response({"success": False, "error": str(e)}, status=500)

    def serve_html(self):
        """Serve the single-page modernized UI"""
        html = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Safe DeFi Assistant</title>
<style>
:root{
  --bg:#0f1724;
  --card:#0b1220;
  --accent:#7c5cff;
  --accent-2:#3ec6ff;
  --muted:#9aa4b2;
  --glass: rgba(255,255,255,0.04);
}
*{box-sizing:border-box}
body{
  margin:0;
  background: linear-gradient(180deg, #071022 0%, #081126 60%);
  font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  color:#e6eef8;
  -webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;
  min-height:100vh;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:28px;
}
.container{
  width:100%;
  max-width:980px;
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border-radius:14px;
  padding:18px;
  box-shadow: 0 10px 40px rgba(2,6,23,0.7);
  overflow:hidden;
  display:grid;
  grid-template-columns: 360px 1fr;
  gap:18px;
}

/* Left column - info & quick actions */
.left {
  padding:18px;
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border-radius:10px;
  border:1px solid rgba(255,255,255,0.03);
  height:600px;
  display:flex;
  flex-direction:column;
  gap:12px;
}
.brand {
  display:flex;
  gap:12px;
  align-items:center;
}
.logo {
  width:52px;
  height:52px;
  border-radius:12px;
  display:flex;
  align-items:center;
  justify-content:center;
  background: linear-gradient(135deg,var(--accent), var(--accent-2));
  font-weight:700;
  box-shadow: 0 6px 18px rgba(124,92,255,0.18);
}
.h1 { font-size:18px; margin:0; }
.p { color:var(--muted); font-size:13px; margin-top:2px }

/* Quick actions */
.quick-actions {
  margin-top:8px;
  display:grid;
  grid-template-columns:1fr;
  gap:10px;
}
.quick-btn {
  background:var(--glass);
  border-radius:10px;
  padding:10px;
  cursor:pointer;
  border:1px solid rgba(255,255,255,0.03);
  display:flex;
  gap:10px;
  align-items:center;
  transition:transform .12s ease, background .12s ease;
}
.quick-btn:hover { transform:translateY(-4px); background: rgba(255,255,255,0.02) }
.quick-btn .emoji { font-size:18px; width:36px; height:36px; display:flex; align-items:center; justify-content:center; }

/* Market data widgets */
.market-data {
  margin-top:8px;
  display:grid;
  grid-template-columns:1fr;
  gap:8px;
}
.market-widget {
  background:var(--glass);
  border-radius:8px;
  padding:8px;
  border:1px solid rgba(255,255,255,0.03);
  transition:transform .12s ease, background .12s ease;
}
.market-widget:hover { background: rgba(255,255,255,0.02) }
.widget-header {
  display:flex;
  align-items:center;
  gap:6px;
  margin-bottom:6px;
  font-size:12px;
}
.widget-header .emoji { font-size:14px; }
.refresh-btn {
  margin-left:auto;
  cursor:pointer;
  opacity:0.6;
  transition:opacity .2s ease;
}
.refresh-btn:hover { opacity:1; }
.widget-content {
  font-size:11px;
  color:var(--muted);
}
.widget-content .loading {
  text-align:center;
  opacity:0.7;
}
.gas-item, .tvl-item, .yield-item {
  display:flex;
  justify-content:space-between;
  margin-bottom:2px;
}
.gas-item .value, .tvl-item .value, .yield-item .value {
  font-weight:600;
  color:var(--text);
}

/* Right column - chat */
.right {
  height:600px;
  display:flex;
  flex-direction:column;
  border-radius:10px;
  overflow:hidden;
  background: linear-gradient(180deg, rgba(255,255,255,0.012), rgba(255,255,255,0.01));
  border:1px solid rgba(255,255,255,0.03);
}

/* messages container */
.chat-top {
  padding:18px;
  display:flex;
  gap:12px;
  align-items:center;
  border-bottom:1px solid rgba(255,255,255,0.02);
}
.chat-title { font-size:16px; margin:0 }
.chat-sub { color:var(--muted); font-size:13px }

.messages {
  flex:1;
  padding:18px;
  overflow:auto;
  display:flex;
  flex-direction:column;
  gap:12px;
  background: linear-gradient(180deg, rgba(255,255,255,0.005), transparent);
}

/* message bubbles */
.msg {
  max-width:78%;
  padding:12px 14px;
  border-radius:14px;
  box-shadow: 0 6px 20px rgba(2,6,23,0.5);
  opacity:0;
  transform: translateY(6px) scale(0.995);
  animation: fadeInUp .18s ease forwards;
  word-wrap: break-word;
  line-height:1.4;
}
.user { margin-left:auto; background: linear-gradient(180deg,#0b2037, #082033); border:1px solid rgba(255,255,255,0.02) }
.bot  { margin-right:auto; background: linear-gradient(180deg, rgba(124,92,255,0.08), rgba(62,198,255,0.04)); color:#eaf6ff; border:1px solid rgba(124,92,255,0.06) }

.small { font-size:13px; color:var(--muted); margin-top:6px }

/* input area */
.input-area {
  padding:12px;
  background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.02));
  border-top:1px solid rgba(255,255,255,0.02);
  display:flex;
  gap:10px;
  align-items:center;
}
.input {
  flex:1;
  display:flex;
  gap:8px;
  align-items:center;
  background: rgba(255,255,255,0.02);
  padding:8px;
  border-radius:12px;
  border:1px solid rgba(255,255,255,0.03);
}
.input input {
  flex:1;
  background:transparent;
  border:0;
  color:inherit;
  padding:8px;
  outline:none;
  font-size:15px;
}
.btn {
  background: linear-gradient(90deg,var(--accent),var(--accent-2));
  border:none;
  color:white;
  padding:10px 14px;
  border-radius:10px;
  cursor:pointer;
  font-weight:600;
  box-shadow: 0 8px 24px rgba(124,92,255,0.18);
}

/* loader dots */
.loader {
  display:inline-flex;
  gap:6px;
}
.loader span {
  width:8px;height:8px;border-radius:50%;
  background: rgba(255,255,255,0.7);
  opacity:0.9;
  transform: translateY(0);
  animation: bounce 1s infinite ease-in-out;
}
.loader span:nth-child(2){ animation-delay:0.12s }
.loader span:nth-child(3){ animation-delay:0.24s }

@keyframes bounce {
  0%{ transform: translateY(0); opacity:0.6}
  50%{ transform: translateY(-6px); opacity:1}
  100%{ transform: translateY(0); opacity:0.6}
}
@keyframes fadeInUp {
  to { opacity:1; transform:none; }
}

/* snackbar */
.snack {
  position:fixed;
  left:50%;
  transform:translateX(-50%);
  bottom:26px;
  background:#d32f2f;
  color:white;
  padding:10px 16px;
  border-radius:8px;
  box-shadow:0 8px 30px rgba(2,6,23,0.6);
  z-index:9999;
  opacity:0;
  animation: slideUp .28s forwards;
}
@keyframes slideUp { from { transform: translateX(-50%) translateY(10px); opacity:0 } to { transform: translateX(-50%) translateY(0); opacity:1 } }

/* responsive */
@media (max-width:980px){
  .container{ grid-template-columns: 1fr; padding:10px }
  .left{ order:2; height:auto }
  .right{ order:1; height:70vh }
  .messages { height: 60vh; }
}
</style>
</head>
<body>
  <div class="container">
    <div class="left">
      <div class="brand">
        <div class="logo">DF</div>
        <div>
          <div class="h1">Safe DeFi Assistant</div>
          <div class="p">Gas insights, risk checks and DeFi action analysis — built with OpenDeepSearch</div>
        </div>
      </div>

      <div style="height:8px"></div>

      <div style="font-weight:700; color:var(--muted); font-size:13px">Quick actions</div>
      <div class="quick-actions" id="quick-actions">
        <div class="quick-btn" onclick="askQuestion('What are current gas prices?')">
          <div class="emoji">⛽</div>
          <div>
            <div style="font-weight:700">Gas Prices</div>
            <div class="small">Get current Ethereum & Polygon gas stats</div>
          </div>
        </div>

        <div class="quick-btn" onclick="askQuestion('What are the risks of using Aave?')">
          <div class="emoji">🔍</div>
          <div>
            <div style="font-weight:700">Aave Risks</div>
            <div class="small">Protocol-specific risk summary</div>
          </div>
        </div>

        <div class="quick-btn" onclick="askQuestion('Is Uniswap safe to use?')">
          <div class="emoji">🦄</div>
          <div>
            <div style="font-weight:700">Uniswap Safety</div>
            <div class="small">Checks and best practices</div>
          </div>
        </div>

        <div class="quick-btn" onclick="askQuestion('Analyze staking 100 USDC on Compound')">
          <div class="emoji">📊</div>
          <div>
            <div style="font-weight:700">DeFi Analysis</div>
            <div class="small">Estimate costs & risks for actions</div>
          </div>
        </div>
      </div>

      <div style="height:16px"></div>

      <div style="font-weight:700; color:var(--muted); font-size:13px">Live Market Data</div>
      <div class="market-data" id="market-data">
        <div class="market-widget" id="gas-widget">
          <div class="widget-header">
            <div class="emoji">⛽</div>
            <div style="font-weight:700">Gas Prices</div>
            <div class="refresh-btn" onclick="refreshGasPrices()">🔄</div>
          </div>
          <div class="widget-content" id="gas-content">
            <div class="loading">Loading...</div>
          </div>
        </div>

        <div class="market-widget" id="tvl-widget">
          <div class="widget-header">
            <div class="emoji">📈</div>
            <div style="font-weight:700">DeFi TVL</div>
            <div class="refresh-btn" onclick="refreshTVLData()">🔄</div>
          </div>
          <div class="widget-content" id="tvl-content">
            <div class="loading">Loading...</div>
          </div>
        </div>

        <div class="market-widget" id="yield-widget">
          <div class="widget-header">
            <div class="emoji">🌾</div>
            <div style="font-weight:700">Top Yields</div>
            <div class="refresh-btn" onclick="refreshYieldData()">🔄</div>
          </div>
          <div class="widget-content" id="yield-content">
            <div class="loading">Loading...</div>
          </div>
        </div>
      </div>

      <div style="flex:1"></div>

      <div style="font-size:13px; color:var(--muted);">
        Tip: Use the quick actions to start. For advanced checks, ask detailed protocol/action questions.
      </div>
    </div>

    <div class="right">
      <div class="chat-top">
        <div>
          <div class="chat-title">Safe DeFi Assistant</div>
          <div class="chat-sub">Ask about gas, risks or analyze DeFi actions</div>
        </div>
      </div>

      <div class="messages" id="chat-messages" aria-live="polite"></div>

      <div class="input-area">
        <div class="input">
          <input id="message-input" type="text" placeholder="Ask: What are current gas prices? e.g., 'Is Aave safe?'" onkeydown="handleKey(event)">
        </div>
        <button class="btn" onclick="sendMessage()">Send</button>
      </div>
    </div>
  </div>

<script>
/* Frontend logic: loader, stable removal, snackbar, fetch to /chat */

function markdownToHtml(text) {
  // Convert Markdown to HTML
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Bold text
    .replace(/\*(.*?)\*/g, '<em>$1</em>')              // Italic text
    .replace(/`(.*?)`/g, '<code>$1</code>')            // Inline code
    .replace(/\n/g, '<br>');                           // Line breaks
}

function createMsgElement(text, cls) {
  const div = document.createElement('div');
  div.className = 'msg ' + cls;
  div.innerHTML = markdownToHtml(text);
  return div;
}

function appendMessage(text, type='bot') {
  const container = document.getElementById('chat-messages');
  const cls = type === 'user' ? 'user' : (type === 'error' ? 'bot' : 'bot');
  const msgEl = createMsgElement(text, type === 'user' ? 'user' : (type === 'error' ? 'bot' : 'bot'));
  // if it's an error, style it inline to look red
  if (type === 'error') {
    msgEl.style.background = '#3b1515';
    msgEl.style.border = '1px solid rgba(255,80,80,0.18)';
  }
  container.appendChild(msgEl);
  container.scrollTop = container.scrollHeight;
  return msgEl;
}

function addLoader() {
  // Ensure only one loader exists
  removeLoader();
  const container = document.getElementById('chat-messages');
  const loaderEl = document.createElement('div');
  loaderEl.className = 'msg bot';
  loaderEl.id = 'loader-msg';
  loaderEl.style.display = 'inline-flex';
  loaderEl.style.gap = '10px';
  loaderEl.innerHTML = '<div style="font-weight:700; margin-right:6px">Assistant</div><div class="loader"><span></span><span></span><span></span></div>';
  container.appendChild(loaderEl);
  container.scrollTop = container.scrollHeight;
}

function removeLoader() {
  const el = document.getElementById('loader-msg');
  if (el) el.remove();
}

function showSnack(message, color='#d32f2f') {
  const snack = document.createElement('div');
  snack.className = 'snack';
  snack.style.background = color;
  snack.textContent = message;
  document.body.appendChild(snack);
  setTimeout(()=> {
    snack.style.opacity = '0';
    try { snack.remove(); } catch(e) {}
  }, 3200);
}

function askQuestion(q) {
  document.getElementById('message-input').value = q;
  sendMessage();
}

function handleKey(e) {
  if (e.key === 'Enter') sendMessage();
}

async function sendMessage() {
  const input = document.getElementById('message-input');
  const text = (input.value || '').trim();
  if (!text) return;

  // show user's message
  appendMessage('<strong>You</strong><div style="margin-top:6px">'+escapeHtml(text)+'</div>', 'user');
  input.value = '';
  addLoader();

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({message: text})
    });

    if (!res.ok) {
      removeLoader();
      const errText = `Server error ${res.status}`;
      appendMessage('<strong>Error</strong><div style="margin-top:6px">'+errText+'</div>', 'error');
      showSnack(errText);
      return;
    }

    const data = await res.json();
    removeLoader();

    if (data.success) {
      // Response may contain newlines; convert to HTML
      const safe = nl2br(escapeHtml(String(data.response || '')));
      appendMessage('<div style="white-space:pre-wrap">'+safe+'</div>', 'bot');
    } else {
      const msg = data.error || 'Unsupported request';
      appendMessage('<strong>Error</strong><div style="margin-top:6px">'+escapeHtml(msg)+'</div>', 'error');
      showSnack(msg);
    }

  } catch (err) {
    removeLoader();
    const em = err && err.message ? err.message : 'Network error';
    appendMessage('<strong>Network</strong><div style="margin-top:6px">'+escapeHtml(em)+'</div>', 'error');
    showSnack('Network error: ' + em);
    console.error(err);
  }
}

// small helpers
function escapeHtml(unsafe) {
  return unsafe
    .replaceAll('&','&amp;')
    .replaceAll('<','&lt;')
    .replaceAll('>','&gt;')
    .replaceAll('"','&quot;')
    .replaceAll("'","&#039;");
}
function nl2br(str) {
  return str.replace(/\n/g, "<br>");
}

// Market data functions
async function fetchMarketData(endpoint) {
  try {
    const response = await fetch(endpoint);
    const data = await response.json();
    return data.success ? data.data : null;
  } catch (error) {
    console.error('Error fetching market data:', error);
    return null;
  }
}

function updateGasPrices(data) {
  const container = document.getElementById('gas-content');
  if (!data) {
    container.innerHTML = '<div class="loading">Failed to load</div>';
    return;
  }
  
  const eth = data.ethereum;
  let html = '<div class="gas-item"><span>Ethereum Slow</span><span class="value">' + eth.slow + ' Gwei</span></div>';
  html += '<div class="gas-item"><span>Ethereum Standard</span><span class="value">' + eth.standard + ' Gwei</span></div>';
  html += '<div class="gas-item"><span>Ethereum Fast</span><span class="value">' + eth.fast + ' Gwei</span></div>';
  html += '<div class="gas-item"><span>Ethereum Instant</span><span class="value">' + Math.round(eth.instant) + ' Gwei</span></div>';
  
  container.innerHTML = html;
}

function updateTVLData(data) {
  const container = document.getElementById('tvl-content');
  if (!data || !data.protocols) {
    container.innerHTML = '<div class="loading">Failed to load</div>';
    return;
  }
  
  let html = '';
  const protocols = Object.values(data.protocols).slice(0, 4);
  protocols.forEach(protocol => {
    const change = protocol.change_1d > 0 ? '+' : '';
    html += `<div class="tvl-item"><span>${protocol.name}</span><span class="value">$${(protocol.tvl/1e9).toFixed(1)}B ${change}${protocol.change_1d.toFixed(1)}%</span></div>`;
  });
  
  container.innerHTML = html;
}

function updateYieldData(data) {
  const container = document.getElementById('yield-content');
  if (!data || !data.top_yields) {
    container.innerHTML = '<div class="loading">Failed to load</div>';
    return;
  }
  
  let html = '';
  data.top_yields.slice(0, 3).forEach(yield => {
    html += `<div class="yield-item"><span>${yield.protocol}</span><span class="value">${yield.apy}% APY</span></div>`;
  });
  
  container.innerHTML = html;
}

async function refreshGasPrices() {
  const data = await fetchMarketData('/gas-prices');
  updateGasPrices(data);
}

async function refreshTVLData() {
  const data = await fetchMarketData('/tvl-data');
  updateTVLData(data);
}

async function refreshYieldData() {
  const data = await fetchMarketData('/yield-opportunities');
  updateYieldData(data);
}

// Auto-refresh market data every 30 seconds
setInterval(async () => {
  await refreshGasPrices();
  await refreshTVLData();
  await refreshYieldData();
}, 30000);

// Initial load
window.addEventListener('load', async function(){
  appendMessage('<div style="font-weight:700">👋 Welcome!</div><div style="margin-top:8px" class="small">I\'m your Safe DeFi Assistant. Try the quick actions or ask a question like "What are current gas prices?"</div>', 'bot');
  
  // Load initial market data
  await refreshGasPrices();
  await refreshTVLData();
  await refreshYieldData();
});
</script>
</body>
</html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    # Helpers for backend logic
    def safe_get_json(self, url, timeout=6):
        logger.info(f"Making API request to: {url}")
        try:
            r = requests.get(url, timeout=timeout)
            logger.info(f"API response status: {r.status_code}")
            if r.status_code == 200:
                data = r.json()
                logger.info(f"API response data: {data}")
                return data
            else:
                logger.warning(f"API request failed with status {r.status_code}: {r.text}")
                return None
        except Exception as e:
            logger.error(f"safe_get_json error for {url}: {e}")
            return None

    def handle_gas_prices(self):
        logger.info("Handling gas prices request")
        try:
            eth_url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle"
            polygon_url = "https://gasstation.polygon.technology/v2"
            eth = self.safe_get_json(eth_url)
            polygon = self.safe_get_json(polygon_url)

            logger.info(f"Ethereum API response: {eth}")
            logger.info(f"Polygon API response: {polygon}")

            if not eth or not eth.get("result"):
                logger.warning("Ethereum gas API unavailable, using fallback")
                raise Exception("Ethereum gas API unavailable")
            if not polygon or not polygon.get("standard"):
                logger.warning("Polygon gas API unavailable, using fallback")
                # polygon may not be present - don't raise, fall back to estimates
                polygon = None

            result = {
                "ethereum": {
                    "slow": f"{eth['result'].get('SafeGasPrice','-')} Gwei",
                    "average": f"{eth['result'].get('ProposeGasPrice','-')} Gwei",
                    "fast": f"{eth['result'].get('FastGasPrice','-')} Gwei"
                },
                "polygon": {}
            }
            if polygon:
                result["polygon"] = {
                    "slow": f"{polygon['standard'].get('maxFee','-')} Gwei",
                    "average": f"{polygon['standard'].get('maxPriorityFee','-')} Gwei",
                    "fast": f"{polygon.get('fast',{}).get('maxFee','-')} Gwei"
                }
            else:
                result["polygon"] = {"slow":"-","average":"-","fast":"-"}

            logger.info(f"Gas prices result: {result}")
            self.send_json_response({"success": True, "data": result})
        except Exception as e:
            logger.error(f"handle_gas_prices error: {e}")
            traceback.print_exc()
            # fallback estimates
            fallback = {
                "ethereum": {"slow":"20-30 Gwei","average":"30-50 Gwei","fast":"50-80 Gwei"},
                "polygon": {"slow":"30-50 Gwei","average":"50-100 Gwei","fast":"100-200 Gwei"}
            }
            logger.info(f"Using fallback gas prices: {fallback}")
            self.send_json_response({"success": True, "data": fallback})

    def handle_risk_assessment(self, query_string):
        params = parse_qs(query_string)
        protocol = params.get("protocol", [""])[0].lower()
        # static risk data (same as earlier)
        risk_data = {
            "aave": {
                "risks": [
                    "Smart Contract Risk: Code vulnerabilities could lead to fund loss",
                    "Liquidation Risk: Price volatility may trigger forced liquidations",
                    "Oracle Risk: Price feed manipulation could affect positions",
                    "Interest Rate Risk: Fluctuating borrowing/lending rates"
                ],
                "best_practices": [
                    "Only invest what you can afford to lose",
                    "Monitor your health factor regularly (keep it above 2.0)",
                    "Use stop-loss strategies for large positions",
                    "Diversify across multiple protocols"
                ],
                "audit_status": "Multiple audits by reputable firms",
                "tvl": "> $10B (as of 2024)"
            },
            "uniswap": {
                "risks": [
                    "Impermanent Loss: Price divergence between paired assets",
                    "Smart Contract Risk: Potential vulnerabilities in V3 contracts",
                    "Front-running Risk: MEV bots may extract value",
                    "Liquidity Provider Risk: Temporary loss of funds during provision"
                ],
                "best_practices": [
                    "Provide liquidity in correlated asset pairs (e.g., ETH/USDC)",
                    "Monitor pool fees and volume regularly",
                    "Use reputable front-ends only",
                    "Start with small amounts to understand impermanent loss"
                ],
                "audit_status": "Multiple audits, battle-tested over years",
                "tvl": "> $3B (as of 2024)"
            },
            "compound": {
                "risks": [
                    "Interest Rate Risk: Fluctuating borrowing/lending rates",
                    "Liquidation Risk: Collateral value dropping below threshold",
                    "Governance Risk: Protocol parameter changes via COMP tokens",
                    "Smart Contract Risk: Though extensively audited"
                ],
                "best_practices": [
                    "Maintain healthy collateral ratio (keep it conservative)",
                    "Diversify across multiple protocols",
                    "Stay updated on governance proposals",
                    "Monitor your borrowing positions regularly"
                ],
                "audit_status": "Extensively audited, one of the original DeFi protocols",
                "tvl": "> $2B (as of 2024)"
            }
        }

        if protocol and protocol in risk_data:
            self.send_json_response({"success": True, "data": risk_data[protocol]})
        elif protocol:
            self.send_json_response({"success": False, "error": f"Unknown protocol: {protocol}"})
        else:
            # If no protocol query param provided, return general guidance
            general = {
                "message": "Provide a protocol using ?protocol=aave (or uniswap, compound) to get specific risk details."
            }
            self.send_json_response({"success": True, "data": general})

    def handle_market_data(self):
        """Get comprehensive market data"""
        logger.info("Handling market data request")
        try:
            # Get all market data
            gas_data = gas_monitor.get_gas_prices()
            tvl_data = tvl_tracker.get_protocol_tvl()
            yield_data = yield_detector.get_yield_opportunities()
            
            market_data = {
                "gas_prices": gas_data,
                "tvl_data": tvl_data,
                "yield_opportunities": yield_data,
                "timestamp": datetime.now().isoformat()
            }
            
            self.send_json_response({"success": True, "data": market_data})
        except Exception as e:
            logger.error(f"handle_market_data error: {e}")
            self.send_json_response({"success": False, "error": str(e)})

    def handle_real_time_gas(self):
        """Get real-time gas prices"""
        logger.info("Handling real-time gas prices request")
        try:
            gas_data = gas_monitor.get_gas_prices()
            self.send_json_response({"success": True, "data": gas_data})
        except Exception as e:
            logger.error(f"handle_real_time_gas error: {e}")
            self.send_json_response({"success": False, "error": str(e)})

    def handle_tvl_data(self):
        """Get DeFi protocol TVL data"""
        logger.info("Handling TVL data request")
        try:
            tvl_data = tvl_tracker.get_protocol_tvl()
            self.send_json_response({"success": True, "data": tvl_data})
        except Exception as e:
            logger.error(f"handle_tvl_data error: {e}")
            self.send_json_response({"success": False, "error": str(e)})

    def handle_yield_opportunities(self):
        """Get yield farming opportunities"""
        logger.info("Handling yield opportunities request")
        try:
            yield_data = yield_detector.get_yield_opportunities()
            self.send_json_response({"success": True, "data": yield_data})
        except Exception as e:
            logger.error(f"handle_yield_opportunities error: {e}")
            self.send_json_response({"success": False, "error": str(e)})

    # Main dispatcher for message => action
    def process_message(self, message):
        """Return a dict: {'success': bool, 'response': str, 'error': '...'}"""
        logger.info(f"Processing message: '{message}'")
        try:
            if not message or not isinstance(message, str):
                logger.warning("Empty or invalid message received")
                return {"success": False, "error": "Empty message"}

            # Use OpenDeepSearch for all responses
            if search_tool:
                logger.info("Using OpenDeepSearch for response generation")
                try:
                    # Add DeFi context to the message for better responses
                    enhanced_message = f"""
                    You are a DeFi safety assistant with access to real-time web data. Please provide helpful, accurate information about:
                    {message}
                    
                    IMPORTANT INSTRUCTIONS:
                    - You have access to current web data, so provide real-time information when available
                    - For gas prices: Look for current Ethereum and Polygon gas prices in Gwei, USD costs, and network congestion
                    - For protocol risks: Provide specific risk factors, audit status, and safety recommendations
                    - For DeFi analysis: Include cost estimates, risk assessments, and step-by-step guidance
                    - Always include specific numbers, percentages, and actionable advice
                    - If you find current data, present it clearly with context about what it means
                    - Be practical and helpful for DeFi users making real decisions
                    
                    Focus on:
                    - Current gas prices and transaction costs (Ethereum, Polygon, etc.)
                    - Protocol risks and safety assessments (Aave, Uniswap, Compound, etc.)
                    - DeFi action analysis and recommendations
                    - Best practices for safe DeFi usage
                    
                    Be concise but informative. Include specific data when available from the web search results.
                    """
                    
                    logger.info(f"Enhanced message: {enhanced_message[:200]}...")
                    
                    # Use OpenDeepSearch to get AI-powered response
                    start_time = time.time()
                    result = search_tool.forward(enhanced_message)
                    processing_time = time.time() - start_time
                    
                    logger.info(f"OpenDeepSearch response: {str(result)[:200]}...")
                    logger.info(f"OpenDeepSearch processing time: {processing_time:.2f}s")
                    
                    return {"success": True, "response": str(result)}
                    
                except Exception as e:
                    logger.error(f"OpenDeepSearch error: {e}")
                    traceback.print_exc()
                    # Fallback to basic response
                    return {"success": True, "response": f"I encountered an error processing your request: {message}. Please try rephrasing your question."}
            else:
                logger.warning("OpenDeepSearch not available, using fallback responses")
                # Fallback responses when OpenDeepSearch is not available
                text = message.strip().lower()
                
                if any(w in text for w in ["gas", "fee", "fees", "cost", "price"]):
                    return {"success": True, "response": "⛽ Gas prices vary by network and time. Ethereum: ~$3-8, Polygon: ~$0.01-0.05. Check current prices before transactions."}
                elif any(w in text for w in ["risk", "safe", "danger", "audit"]):
                    return {"success": True, "response": "🔍 DeFi risks include smart contract vulnerabilities, liquidation risk, and impermanent loss. Always start small and use audited protocols."}
                elif any(w in text for w in ["analyze", "analysis", "action", "staking", "stake", "swap"]):
                    return {"success": True, "response": "📊 DeFi actions have varying costs and risks. Test on testnet first, start small, and monitor gas prices."}
                else:
                    return {"success": True, "response": f"I understand you're asking about: {message}. I can help with gas prices, risk assessments, and DeFi analysis."}

        except Exception as e:
            logger.error(f"process_message error: {e}")
            traceback.print_exc()
            return {"success": False, "error": "Internal processing error"}

    def get_protocol_risks(self, protocol):
        protocol = protocol.lower()
        risk_texts = {
            "aave": (
                "🛡️ Aave Risk Summary\n\n"
                "Main risks: Smart contract vulnerabilities, liquidation risk, oracle risk, interest rate risk.\n\n"
                "Best practices: Keep healthy collateral ratios, diversify, and monitor your positions. Aave has multiple audits and is battle-tested."
            ),
            "uniswap": (
                "🦄 Uniswap Risk Summary\n\n"
                "Main risks: Impermanent loss for LPs, smart contract risk, front-running/MEV.\n\n"
                "Best practices: Use reputable front-ends, provide liquidity with caution, and start small."
            ),
            "compound": (
                "🏦 Compound Risk Summary\n\n"
                "Main risks: Interest rate risk, liquidation risk, governance changes. Compound is well-audited and established."
            )
        }
        return risk_texts.get(protocol, f"Protocol '{protocol}' not found in database. Try 'Aave', 'Uniswap' or 'Compound'.")

def main():
    port = int(os.getenv("PORT", 8080))
    host = "127.0.0.1"
    server = HTTPServer((host, port), DeFiAssistantHandler)
    print("🚀 Safe DeFi Assistant running at: http://{}:{}".format(host, port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")

if __name__ == "__main__":
    main()


