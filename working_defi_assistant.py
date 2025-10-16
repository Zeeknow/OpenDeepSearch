
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

load_dotenv()

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
        try:
            if path == "/":
                self.serve_html()
            elif path == "/gas":
                self.handle_gas_prices()
            elif path == "/risk":
                self.handle_risk_assessment(parsed.query)
            else:
                self.send_json_response({"success": False, "error": "Not found"}, status=404)
        except Exception as e:
            print("GET handler exception:", e)
            traceback.print_exc()
            self.send_json_response({"success": False, "error": str(e)}, status=500)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        try:
            if path == "/chat":
                content_length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(content_length)
                try:
                    data = json.loads(raw.decode("utf-8"))
                except json.JSONDecodeError:
                    self.send_json_response({"success": False, "error": "Invalid JSON"}, status=400)
                    return

                message = data.get("message", "")
                # Process chat synchronously and return structured JSON
                response_payload = self.process_message(message)
                # Always return JSON with success flag
                self.send_json_response(response_payload)
            else:
                self.send_json_response({"success": False, "error": "Not found"}, status=404)
        except Exception as e:
            print("POST handler exception:", e)
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

function createMsgElement(text, cls) {
  const div = document.createElement('div');
  div.className = 'msg ' + cls;
  div.innerHTML = text;
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

// add welcome on load
window.addEventListener('load', function(){
  appendMessage('<div style="font-weight:700">👋 Welcome!</div><div style="margin-top:8px" class="small">I\'m your Safe DeFi Assistant. Try the quick actions or ask a question like "What are current gas prices?"</div>', 'bot');
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
        try:
            r = requests.get(url, timeout=timeout)
            return r.json()
        except Exception as e:
            print(f"safe_get_json error for {url}: {e}")
            return None

    def handle_gas_prices(self):
        try:
            eth_url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle"
            polygon_url = "https://gasstation.polygon.technology/v2"
            eth = self.safe_get_json(eth_url)
            polygon = self.safe_get_json(polygon_url)

            if not eth or not eth.get("result"):
                raise Exception("Ethereum gas API unavailable")
            if not polygon or not polygon.get("standard"):
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

            self.send_json_response({"success": True, "data": result})
        except Exception as e:
            print("handle_gas_prices error:", e)
            traceback.print_exc()
            # fallback estimates
            fallback = {
                "ethereum": {"slow":"20-30 Gwei","average":"30-50 Gwei","fast":"50-80 Gwei"},
                "polygon": {"slow":"30-50 Gwei","average":"50-100 Gwei","fast":"100-200 Gwei"}
            }
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

    # Main dispatcher for message => action
    def process_message(self, message):
        """Return a dict: {'success': bool, 'response': str, 'error': '...'}"""
        try:
            if not message or not isinstance(message, str):
                return {"success": False, "error": "Empty message"}

            text = message.strip().lower()

            # gas-related intents
            if any(w in text for w in ["gas", "fee", "fees", "cost", "price"]):
                # call gas routine and build a friendly text response
                eth_url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle"
                polygon_url = "https://gasstation.polygon.technology/v2"
                eth = self.safe_get_json(eth_url)
                polygon = self.safe_get_json(polygon_url)
                if not eth or not eth.get("result"):
                    # fallback
                    resp = ("⛽ Current (estimated) Ethereum gas prices:\n"
                            "Slow: 20-30 Gwei\nAverage: 30-50 Gwei\nFast: 50-80 Gwei\n\n"
                            "Polygon: very low (approx 0.01-0.05 USD for simple swaps)\n\n"
                            "Tip: use Polygon for cheap swaps and check gas before big txs.")
                else:
                    eth_result = eth.get('result', {})
                    if isinstance(eth_result, dict):
                        resp = (f"⛽ Ethereum Gas (Gwei):\n"
                                f"• Slow: {eth_result.get('SafeGasPrice','-')} Gwei\n"
                                f"• Average: {eth_result.get('ProposeGasPrice','-')} Gwei\n"
                                f"• Fast: {eth_result.get('FastGasPrice','-')} Gwei\n\n")
                    else:
                        resp = (f"⛽ Ethereum Gas (Gwei):\n"
                                f"• Slow: - Gwei\n"
                                f"• Average: - Gwei\n"
                                f"• Fast: - Gwei\n\n")
                    if polygon and polygon.get("standard"):
                        resp += (f"Polygon (Gwei):\n"
                                 f"• Slow: {polygon['standard'].get('maxFee','-')} Gwei\n"
                                 f"• Average: {polygon['standard'].get('maxPriorityFee','-')} Gwei\n"
                                 f"• Fast: {polygon.get('fast',{}).get('maxFee','-')} Gwei\n\n")
                    resp += "Tip: schedule large transactions off-peak or use Polygon for cheap swaps."
                return {"success": True, "response": resp}

            # risk-related intents
            if any(w in text for w in ["risk", "safe", "danger", "audit"]):
                protocols = ["aave", "uniswap", "compound", "maker", "curve", "balancer"]
                found = [p for p in protocols if p in text]
                if found:
                    proto = found[0]
                    # reuse get_protocol_risks
                    detail = self.get_protocol_risks(proto)
                    return {"success": True, "response": detail}
                else:
                    # return general risk advice
                    general_advice = (
                        "🔍 General DeFi Risk Assessment\n\n"
                        "Common risks: Smart contract vulnerabilities, liquidation risk, oracle manipulation, governance and market risk.\n\n"
                        "Best practices: Start small, use audited protocols, diversify, monitor positions, and keep emergency funds separate."
                    )
                    return {"success": True, "response": general_advice}

            # analysis intents
            if any(w in text for w in ["analyze", "analysis", "action", "staking", "stake", "swap"]):
                analysis = (
                    "📊 DeFi Action Analysis\n\n"
                    "Swapping tokens: Ethereum gas ~ $3-8 (varies). Polygon: <$0.1.\n"
                    "Providing liquidity: Higher possibility of impermanent loss; costs vary.\n"
                    "Lending/borrowing: Watch collateral ratios and liquidation thresholds.\n\n"
                    "Recommendation: Test on testnet, start small, and check gas before transaction."
                )
                return {"success": True, "response": analysis}

            # fallback/general response
            general = (
                f"🤖 I understand you're asking about: \"{message}\"\n\n"
                "I can help with:\n"
                "• Gas fees: ask 'What are current gas prices?'\n"
                "• Risk assessment: ask 'Is Aave safe?'\n"
                "• Action analysis: 'Analyze staking 100 USDC on Compound'\n\n"
                "If you'd like protocol-specific risk info, mention the protocol name (e.g., Aave, Uniswap, Compound)."
            )
            return {"success": True, "response": general}

        except Exception as e:
            print("process_message error:", e)
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



# #!/usr/bin/env python3
# """
# Working DeFi Assistant - Web Interface
# This bypasses Gradio compatibility issues with Python 3.14
# """

# import os
# import json
# import requests
# from http.server import HTTPServer, BaseHTTPRequestHandler
# from urllib.parse import urlparse, parse_qs
# from dotenv import load_dotenv
# import threading
# import time

# # Load environment variables
# load_dotenv()

# class DeFiAssistantHandler(BaseHTTPRequestHandler):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
    
#     def do_GET(self):
#         """Handle GET requests"""
#         parsed_path = urlparse(self.path)
        
#         if parsed_path.path == '/':
#             self.serve_html()
#         elif parsed_path.path == '/gas':
#             self.handle_gas_prices()
#         elif parsed_path.path == '/risk':
#             self.handle_risk_assessment(parsed_path.query)
#         else:
#             self.send_error(404)
    
#     def do_POST(self):
#         """Handle POST requests"""
#         if self.path == '/chat':
#             content_length = int(self.headers['Content-Length'])
#             post_data = self.rfile.read(content_length)
#             try:
#                 data = json.loads(post_data.decode('utf-8'))
#                 message = data.get('message', '')
#                 self.handle_chat(message)
#             except json.JSONDecodeError:
#                 self.send_error(400, "Invalid JSON")
#         else:
#             self.send_error(404)
    
#     def serve_html(self):
#         """Serve the HTML interface"""
#         html = """
# <!DOCTYPE html>
# <html>
# <head>
#     <meta charset="UTF-8">
#     <title>Safe DeFi Assistant</title>
#     <style>
#         body { font-family: Arial, sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
#         .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
#         .chat-container { background: white; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
#         .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
#         .user-message { background: #e3f2fd; margin-left: 20px; }
#         .bot-message { background: #f3e5f5; margin-right: 20px; }
#         .input-container { display: flex; gap: 10px; margin-top: 20px; }
#         .message-input { flex: 1; padding: 12px; font-size: 16px; border: 2px solid #ddd; border-radius: 5px; }
#         .send-btn { padding: 12px 24px; font-size: 16px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; }
#         .send-btn:hover { background: #5a6fd8; }
#         .quick-actions { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin-bottom: 20px; }
#         .quick-btn { padding: 15px; background: white; border: 2px solid #667eea; border-radius: 5px; cursor: pointer; text-align: center; transition: all 0.3s; }
#         .quick-btn:hover { background: #667eea; color: white; }
#         .loading { color: #666; font-style: italic; }
#         .error { color: #d32f2f; background: #ffebee; padding: 10px; border-radius: 5px; }
#         .success { color: #2e7d32; background: #e8f5e8; padding: 10px; border-radius: 5px; }
#     </style>
# </head>
# <body>
#     <div class="header">
#         <h1>🛡️ Safe DeFi Assistant</h1>
#         <p>Powered by OpenDeepSearch & AI - Get gas insights, risk assessments, and safe DeFi guidance</p>
#     </div>
    
#     <div class="quick-actions">
#         <div class="quick-btn" onclick="askQuestion('What are current gas prices?')">
#             ⛽ Gas Prices
#         </div>
#         <div class="quick-btn" onclick="askQuestion('What are the risks of using Aave?')">
#             🔍 Aave Risks
#         </div>
#         <div class="quick-btn" onclick="askQuestion('Is Uniswap safe to use?')">
#             🦄 Uniswap Safety
#         </div>
#         <div class="quick-btn" onclick="askQuestion('Analyze staking 100 USDC on Compound')">
#             📊 DeFi Analysis
#         </div>
#     </div>
    
#     <div class="chat-container">
#         <div id="chat-messages"></div>
#         <div class="input-container">
#             <input type="text" id="message-input" class="message-input" placeholder="Ask about gas fees, protocol risks, or analyze DeFi actions..." onkeypress="handleKeyPress(event)">
#             <button type="button" onclick="sendMessage()" class="send-btn">Send 📤</button>
#         </div>
#     </div>
    
#     <script>
#         function addMessage(content, isUser = false) {
#             const messagesDiv = document.getElementById('chat-messages');
#             const messageDiv = document.createElement('div');
#             messageDiv.className = 'message ' + (isUser ? 'user-message' : 'bot-message');
#             messageDiv.innerHTML = content;
#             messagesDiv.appendChild(messageDiv);
#             messagesDiv.scrollTop = messagesDiv.scrollHeight;
#         }
        
#         function askQuestion(question) {
#             console.log('askQuestion called with:', question);
#             document.getElementById('message-input').value = question;
#             sendMessage();
#         }
        
#         function handleKeyPress(event) {
#             if (event.key === 'Enter') {
#                 sendMessage();
#             }
#         }
        
#         function sendMessage() {
#             const input = document.getElementById('message-input');
#             const message = input.value.trim();
            
#             if (!message) {
#                 console.log('No message to send');
#                 return;
#             }
            
#             console.log('Sending message:', message);
#             addMessage(message, true);
#             input.value = '';
            
#             addMessage('<div class="loading">🤔 Thinking...</div>');
            
#             fetch('/chat', {
#                 method: 'POST',
#                 headers: { 'Content-Type': 'application/json' },
#                 body: JSON.stringify({ message: message })
#             })
#             .then(response => {
#                 console.log('Response received:', response.status);
#                 return response.json();
#             })
#             .then(data => {
#                 console.log('Data received:', data);
                
#                 // Remove loading message
#                 const messagesDiv = document.getElementById('chat-messages');
#                 if (messagesDiv.lastChild) {
#                     messagesDiv.removeChild(messagesDiv.lastChild);
#                 }
                
#                 if (data.success) {
#                     addMessage('<div class="success">' + data.response + '</div>');
#                 } else {
#                     addMessage('<div class="error">Error: ' + data.error + '</div>');
#                 }
#             })
#             .catch(error => {
#                 console.error('Fetch error:', error);
                
#                 // Remove loading message
#                 const messagesDiv = document.getElementById('chat-messages');
#                 if (messagesDiv.lastChild) {
#                     messagesDiv.removeChild(messagesDiv.lastChild);
#                 }
                
#                 addMessage('<div class="error">Network error: ' + error.message + '</div>');
#             });
#         }
        
#         // Add welcome message when page loads
#         window.onload = function() {
#             console.log('Page loaded, adding welcome message');
#             addMessage('<div class="success">👋 Welcome! I\'m your Safe DeFi Assistant. Ask me about gas fees, protocol risks, or analyze DeFi actions. Try clicking one of the quick action buttons above!</div>');
#         };
#     </script>
# </body>
# </html>
#         """
        
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html; charset=utf-8')
#         self.end_headers()
#         self.wfile.write(html.encode('utf-8'))
    
#     def handle_gas_prices(self):
#         """Handle gas price requests"""
#         try:
#             # Ethereum gas prices
#             eth_response = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle")
#             eth_data = eth_response.json()
            
#             # Polygon gas prices
#             polygon_response = requests.get("https://gasstation.polygon.technology/v2")
#             polygon_data = polygon_response.json()
            
#             result = {
#                 "ethereum": {
#                     "slow": f"{eth_data['result']['SafeGasPrice']} Gwei",
#                     "average": f"{eth_data['result']['ProposeGasPrice']} Gwei", 
#                     "fast": f"{eth_data['result']['FastGasPrice']} Gwei",
#                     "usd_estimate": "$2-8 for simple swaps"
#                 },
#                 "polygon": {
#                     "slow": f"{polygon_data['standard']['maxFee']} Gwei",
#                     "average": f"{polygon_data['standard']['maxPriorityFee']} Gwei",
#                     "fast": f"{polygon_data['fast']['maxFee']} Gwei", 
#                     "usd_estimate": "$0.01-0.05 for simple swaps"
#                 }
#             }
            
#             self.send_json_response({'success': True, 'data': result})
            
#         except Exception as e:
#             self.send_json_response({'success': False, 'error': str(e)})
    
#     def handle_risk_assessment(self, query_string):
#         """Handle risk assessment requests"""
#         params = parse_qs(query_string)
#         protocol = params.get('protocol', [''])[0]
        
#         risk_data = {
#             "aave": {
#                 "risks": [
#                     "Smart Contract Risk: Code vulnerabilities could lead to fund loss",
#                     "Liquidation Risk: Price volatility may trigger forced liquidations", 
#                     "Oracle Risk: Price feed manipulation could affect positions",
#                     "Interest Rate Risk: Fluctuating borrowing/lending rates"
#                 ],
#                 "best_practices": [
#                     "Only invest what you can afford to lose",
#                     "Monitor your health factor regularly (keep it above 2.0)",
#                     "Use stop-loss strategies for large positions",
#                     "Diversify across multiple protocols"
#                 ],
#                 "audit_status": "Multiple audits by reputable firms",
#                 "tvl": "> $10B (as of 2024)"
#             },
#             "uniswap": {
#                 "risks": [
#                     "Impermanent Loss: Price divergence between paired assets",
#                     "Smart Contract Risk: Potential vulnerabilities in V3 contracts",
#                     "Front-running Risk: MEV bots may extract value", 
#                     "Liquidity Provider Risk: Temporary loss of funds during provision"
#                 ],
#                 "best_practices": [
#                     "Provide liquidity in correlated asset pairs (e.g., ETH/USDC)",
#                     "Monitor pool fees and volume regularly",
#                     "Use reputable front-ends only",
#                     "Start with small amounts to understand impermanent loss"
#                 ],
#                 "audit_status": "Multiple audits, battle-tested over years",
#                 "tvl": "> $3B (as of 2024)"
#             },
#             "compound": {
#                 "risks": [
#                     "Interest Rate Risk: Fluctuating borrowing/lending rates",
#                     "Liquidation Risk: Collateral value dropping below threshold",
#                     "Governance Risk: Protocol parameter changes via COMP tokens",
#                     "Smart Contract Risk: Though extensively audited"
#                 ],
#                 "best_practices": [
#                     "Maintain healthy collateral ratio (keep it conservative)",
#                     "Diversify across multiple protocols", 
#                     "Stay updated on governance proposals",
#                     "Monitor your borrowing positions regularly"
#                 ],
#                 "audit_status": "Extensively audited, one of the original DeFi protocols",
#                 "tvl": "> $2B (as of 2024)"
#             }
#         }
        
#         protocol_lower = protocol.lower()
#         if protocol_lower in risk_data:
#             self.send_json_response({'success': True, 'data': risk_data[protocol_lower]})
#         else:
#             self.send_json_response({'success': False, 'error': f'Unknown protocol: {protocol}'})
    
#     def handle_chat(self, message):
#         """Handle general chat messages"""
#         try:
#             message_lower = message.lower()
            
#             # Route to appropriate handler based on message content
#             if any(word in message_lower for word in ['gas', 'fee', 'cost', 'price']):
#                 self.handle_gas_request()
#             elif any(word in message_lower for word in ['risk', 'safe', 'danger', 'audit']):
#                 self.handle_risk_request(message)
#             elif any(word in message_lower for word in ['analyze', 'analysis', 'action']):
#                 self.handle_analysis_request(message)
#             else:
#                 self.handle_general_request(message)
                
#         except Exception as e:
#             self.send_json_response({'success': False, 'error': str(e)})
    
#     def handle_gas_request(self):
#         """Handle gas-related requests"""
#         try:
#             # Get current gas prices
#             eth_response = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle")
#             eth_data = eth_response.json()
            
#             polygon_response = requests.get("https://gasstation.polygon.technology/v2")
#             polygon_data = polygon_response.json()
            
#             # Check if API responses are valid
#             if eth_data.get("status") != "1":
#                 raise Exception("Ethereum API returned error")
            
#             response_text = f"""
# ⛽ **Current Gas Prices**

# **Ethereum Network:**
# • Slow: {eth_data['result']['SafeGasPrice']} Gwei (~$2-4)
# • Average: {eth_data['result']['ProposeGasPrice']} Gwei (~$3-6) 
# • Fast: {eth_data['result']['FastGasPrice']} Gwei (~$5-8)

# **Polygon Network:**
# • Slow: {polygon_data['standard']['maxFee']} Gwei (~$0.01-0.02)
# • Average: {polygon_data['standard']['maxPriorityFee']} Gwei (~$0.02-0.03)
# • Fast: {polygon_data['fast']['maxFee']} Gwei (~$0.03-0.05)

# 💡 **Tips:**
# • Use Polygon for lower fees on simple transactions
# • Monitor gas prices before large transactions
# • Consider transaction timing (off-peak hours)
#             """
            
#             self.send_json_response({'success': True, 'response': response_text})
            
#         except Exception as e:
#             # Fallback response if APIs fail
#             fallback_response = """
# ⛽ **Gas Price Information**

# **Ethereum Network (Estimated):**
# • Slow: 20-30 Gwei (~$2-4)
# • Average: 30-50 Gwei (~$3-6)
# • Fast: 50-80 Gwei (~$5-8)

# **Polygon Network (Estimated):**
# • Slow: 30-50 Gwei (~$0.01-0.02)
# • Average: 50-100 Gwei (~$0.02-0.03)
# • Fast: 100-200 Gwei (~$0.03-0.05)

# 💡 **Tips:**
# • Use Polygon for lower fees on simple transactions
# • Monitor gas prices before large transactions
# • Consider transaction timing (off-peak hours)

# ⚠️ *Note: Unable to fetch real-time data. Showing estimated ranges.*
#             """
#             self.send_json_response({'success': True, 'response': fallback_response})
    
#     def handle_risk_request(self, message):
#         """Handle risk assessment requests"""
#         # Extract protocol name from message
#         protocols = ['aave', 'uniswap', 'compound', 'maker', 'curve', 'balancer']
#         mentioned_protocols = [p for p in protocols if p in message.lower()]
        
#         if mentioned_protocols:
#             protocol = mentioned_protocols[0]
#             risk_data = self.get_protocol_risks(protocol)
#             self.send_json_response({'success': True, 'response': risk_data})
#         else:
#             general_advice = """
# 🔍 **General DeFi Risk Assessment**

# **Common Risks Across All Protocols:**
# • Smart Contract Risk: Code vulnerabilities
# • Liquidation Risk: Forced position closures
# • Oracle Risk: Price feed manipulation
# • Governance Risk: Protocol parameter changes
# • Market Risk: Asset price volatility

# **Best Practices:**
# • Start with small amounts
# • Use only audited protocols
# • Diversify across multiple protocols
# • Monitor positions regularly
# • Keep emergency funds separate
# • Use hardware wallets for large amounts

# **Recommended Protocols (Well-Audited):**
# • Aave (Lending/Borrowing)
# • Uniswap (DEX)
# • Compound (Lending)
# • MakerDAO (Stablecoins)
#             """
#             self.send_json_response({'success': True, 'response': general_advice})
    
#     def handle_analysis_request(self, message):
#         """Handle DeFi action analysis requests"""
#         analysis_text = """
# 📊 **DeFi Action Analysis**

# **Common DeFi Actions & Estimated Costs:**

# **Swapping Tokens:**
# • Ethereum: $3-8 gas fee
# • Polygon: $0.02-0.1 gas fee
# • Risk: Low (if using reputable DEX)

# **Providing Liquidity:**
# • Ethereum: $15-30 gas fee
# • Polygon: $0.2-0.5 gas fee
# • Risk: Medium (impermanent loss)

# **Lending/Borrowing:**
# • Ethereum: $8-25 gas fee
# • Polygon: $0.1-0.4 gas fee
# • Risk: Medium (liquidation risk)

# **Staking:**
# • Ethereum: $5-15 gas fee
# • Polygon: $0.05-0.2 gas fee
# • Risk: Low-Medium (protocol dependent)

# **Recommendations:**
# • Test on testnet first
# • Start with small amounts
# • Monitor gas fees before transactions
# • Use reputable front-ends only
# • Keep track of your positions
#         """
        
#         self.send_json_response({'success': True, 'response': analysis_text})
    
#     def handle_general_request(self, message):
#         """Handle general DeFi questions"""
#         general_response = f"""
# 🤖 **DeFi Assistant Response**

# I understand you're asking about: "{message}"

# Here's what I can help you with:

# **⛽ Gas Fees:** Ask about current gas prices on Ethereum/Polygon
# **🔍 Risk Assessment:** Ask about safety of specific protocols (Aave, Uniswap, Compound)
# **📊 Action Analysis:** Ask me to analyze specific DeFi actions
# **💡 General Advice:** Ask about DeFi best practices and safety tips

# **Try asking:**
# • "What are current gas prices?"
# • "Is Aave safe to use?"
# • "Analyze staking 100 USDC"
# • "What are DeFi best practices?"

# I'm here to help you navigate DeFi safely! 🛡️
#         """
        
#         self.send_json_response({'success': True, 'response': general_response})
    
#     def get_protocol_risks(self, protocol):
#         """Get risk information for a specific protocol"""
#         risk_data = {
#             "aave": """
# 🛡️ **Aave Protocol Risk Assessment**

# **Main Risks:**
# • Smart Contract Risk: Code vulnerabilities could lead to fund loss
# • Liquidation Risk: Price volatility may trigger forced liquidations
# • Oracle Risk: Price feed manipulation could affect positions
# • Interest Rate Risk: Fluctuating borrowing/lending rates

# **Best Practices:**
# • Only invest what you can afford to lose
# • Monitor your health factor regularly (keep it above 2.0)
# • Use stop-loss strategies for large positions
# • Diversify across multiple protocols

# **Audit Status:** Multiple audits by reputable firms
# **TVL:** > $10B (as of 2024)
# **Overall Risk Level:** Medium (well-established protocol)
#             """,
#             "uniswap": """
# 🦄 **Uniswap Protocol Risk Assessment**

# **Main Risks:**
# • Impermanent Loss: Price divergence between paired assets
# • Smart Contract Risk: Potential vulnerabilities in V3 contracts
# • Front-running Risk: MEV bots may extract value
# • Liquidity Provider Risk: Temporary loss of funds during provision

# **Best Practices:**
# • Provide liquidity in correlated asset pairs (e.g., ETH/USDC)
# • Monitor pool fees and volume regularly
# • Use reputable front-ends only
# • Start with small amounts to understand impermanent loss

# **Audit Status:** Multiple audits, battle-tested over years
# **TVL:** > $3B (as of 2024)
# **Overall Risk Level:** Medium (impermanent loss is main concern)
#             """,
#             "compound": """
# 🏦 **Compound Protocol Risk Assessment**

# **Main Risks:**
# • Interest Rate Risk: Fluctuating borrowing/lending rates
# • Liquidation Risk: Collateral value dropping below threshold
# • Governance Risk: Protocol parameter changes via COMP tokens
# • Smart Contract Risk: Though extensively audited

# **Best Practices:**
# • Maintain healthy collateral ratio (keep it conservative)
# • Diversify across multiple protocols
# • Stay updated on governance proposals
# • Monitor your borrowing positions regularly

# **Audit Status:** Extensively audited, one of the original DeFi protocols
# **TVL:** > $2B (as of 2024)
# **Overall Risk Level:** Low-Medium (very established protocol)
#             """
#         }
        
#         return risk_data.get(protocol, f"Protocol '{protocol}' not found in my database.")
    
#     def send_json_response(self, data):
#         """Send JSON response"""
#         self.send_response(200)
#         self.send_header('Content-type', 'application/json; charset=utf-8')
#         self.end_headers()
#         self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

# def main():
#     """Main function"""
#     print("🚀 Starting Safe DeFi Assistant...")
    
#     # Check if we have the required API keys
#     serper_key = os.getenv("SERPER_API_KEY")
#     if not serper_key:
#         print("⚠️  SERPER_API_KEY not found - some features may be limited")
    
#     # Create server
#     port = 8080
#     server = HTTPServer(('127.0.0.1', port), DeFiAssistantHandler)
    
#     print(f"🌐 DeFi Assistant running at: http://127.0.0.1:{port}")
#     print("📝 Open your browser and start asking DeFi questions!")
#     print("🛑 Press Ctrl+C to stop")
    
#     try:
#         server.serve_forever()
#     except KeyboardInterrupt:
#         print("\n🛑 Server stopped by user")

# if __name__ == "__main__":
#     main()
