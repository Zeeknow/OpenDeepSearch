#!/usr/bin/env python3
"""
Safe DeFi Assistant - Main Server
Modular DeFi safety assistant with real-time market data and AI chat
"""

import os
import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import traceback
import time
import logging
from datetime import datetime

# Import our modules with new structure
from core.services.market_data import gas_monitor, tvl_tracker, yield_detector
from apps.web.templates import get_landing_page, get_gas_prices_page, get_market_data_page, get_chat_page, get_portfolio_page, get_yield_farming_page, get_risk_analysis_page
from apps.api.sentient_adapter import SentientDeFiAgent
from core.services.portfolio_analyzer import portfolio_analyzer
from core.services.mev_protection import mev_protection
from infrastructure.config.settings import config
from infrastructure.logging.logger import logger

# Import OpenDeepSearch
try:
    from opendeepsearch.ods_tool import OpenDeepSearchTool
except ImportError as e:
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
            model_name=config.LITELLM_MODEL_ID,
            reranker="jina",
            search_provider="serper",
            serper_api_key=config.SERPER_API_KEY
        )
        if not search_tool.is_initialized:
            search_tool.setup()
        logger.info("OpenDeepSearch tool initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize OpenDeepSearch tool: {e}")
        search_tool = None

# Initialize Sentient Agent
try:
    sentient_agent = SentientDeFiAgent()
    logger.info("Sentient DeFi Agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Sentient agent: {e}")
    sentient_agent = None

class DeFiAssistantHandler(BaseHTTPRequestHandler):
    """Main HTTP request handler for the DeFi Assistant"""
    
    def send_json_response(self, data, status=200):
        """Helper to send JSON responses reliably"""
        try:
            payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)
        except Exception as e:
            logger.error(f"Failed to send JSON response: {e}")
            try:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Internal response error"}).encode("utf-8"))
            except:
                pass

    def send_html_response(self, html, status=200):
        """Helper to send HTML responses"""
        try:
            self.send_response(status)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        except Exception as e:
            logger.error(f"Failed to send HTML response: {e}")

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        parsed = urlparse(self.path)
        path = parsed.path
        logger.info(f"GET request: {path} - Query: {parsed.query}")
        
        try:
            # Route to appropriate handler
            if path == "/":
                self.serve_landing_page()
            elif path == "/gas-prices":
                self.serve_gas_prices_page()
            elif path == "/market-data":
                self.serve_market_data_page()
            elif path == "/chat":
                self.serve_chat_page()
            elif path == "/risk-analysis":
                self.serve_risk_analysis_page()
            elif path == "/yield-farming":
                self.serve_yield_farming_page()
            elif path == "/portfolio":
                self.serve_portfolio_page()
            # API endpoints
            elif path == "/api/gas-prices":
                self.handle_gas_prices_api()
            elif path == "/api/market-data":
                self.handle_market_data_api()
            elif path == "/api/tvl-data":
                self.handle_tvl_data_api()
            elif path == "/api/yield-opportunities":
                self.handle_yield_opportunities_api()
            # Sentient API endpoints
            elif path == "/api/sentient/info":
                self.handle_sentient_info_api()
            # Portfolio and MEV protection endpoints
            elif path == "/api/portfolio/analyze":
                self.handle_portfolio_analysis_api()
            elif path == "/api/mev/status":
                self.handle_mev_status_api()
            elif path == "/api/mev/alerts":
                self.handle_mev_alerts_api()
            else:
                logger.warning(f"GET 404: {path}")
                self.send_json_response({"success": False, "error": "Not found"}, status=404)
        except Exception as e:
            logger.error(f"GET handler exception: {e}")
            traceback.print_exc()
            self.send_json_response({"success": False, "error": str(e)}, status=500)

    def do_POST(self):
        """Handle POST requests"""
        parsed = urlparse(self.path)
        path = parsed.path
        logger.info(f"POST request: {path}")
        
        try:
            if path == "/api/chat" or path == "/chat":
                self.handle_chat_api()
            elif path == "/api/sentient/query":
                self.handle_sentient_query_api()
            elif path == "/api/portfolio/analyze":
                self.handle_portfolio_analysis_post_api()
            elif path == "/api/mev/check":
                self.handle_mev_check_api()
            else:
                logger.warning(f"POST 404: {path}")
                self.send_json_response({"success": False, "error": "Not found"}, status=404)
        except Exception as e:
            logger.error(f"POST handler exception: {e}")
            traceback.print_exc()
            self.send_json_response({"success": False, "error": str(e)}, status=500)

    # Page handlers
    def serve_landing_page(self):
        """Serve the landing page"""
        html = get_landing_page()
        self.send_html_response(html)

    def serve_gas_prices_page(self):
        """Serve the gas prices page"""
        html = get_gas_prices_page()
        self.send_html_response(html)

    def serve_market_data_page(self):
        """Serve the market data page"""
        html = get_market_data_page()
        self.send_html_response(html)

    def serve_chat_page(self):
        """Serve the chat page"""
        html = get_chat_page()
        self.send_html_response(html)

    def serve_risk_analysis_page(self):
        """Serve the risk analysis page (placeholder)"""
        html = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Risk Analysis - Safe DeFi Assistant</title>
<style>
:root{
  --bg:#0f1724;
  --card:#0b1220;
  --accent:#7c5cff;
  --accent-2:#3ec6ff;
  --muted:#9aa4b2;
  --glass: rgba(255,255,255,0.04);
  --text:#e6eef8;
}
*{box-sizing:border-box}
body{
  margin:0;
  background: linear-gradient(180deg, #071022 0%, #081126 60%);
  font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  color:var(--text);
  min-height:100vh;
}
.container{
  width:100%;
  max-width:1200px;
  margin:0 auto;
  padding:20px;
}
.navbar{
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border-radius:12px;
  padding:16px 24px;
  margin-bottom:24px;
  border:1px solid rgba(255,255,255,0.03);
  display:flex;
  justify-content:space-between;
  align-items:center;
}
.logo{
  display:flex;
  align-items:center;
  gap:12px;
  text-decoration:none;
  color:inherit;
}
.logo-icon{
  width:40px;
  height:40px;
  border-radius:10px;
  display:flex;
  align-items:center;
  justify-content:center;
  background: linear-gradient(135deg,var(--accent), var(--accent-2));
  font-weight:700;
  box-shadow: 0 6px 18px rgba(124,92,255,0.18);
}
.nav-links{
  display:flex;
  gap:20px;
  align-items:center;
}
.nav-link{
  color:var(--muted);
  text-decoration:none;
  padding:8px 16px;
  border-radius:8px;
  transition:all 0.2s ease;
}
.nav-link:hover{
  color:var(--text);
  background:rgba(255,255,255,0.05);
}
.nav-link.active{
  color:var(--accent);
  background:rgba(124,92,255,0.1);
}
.card{
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border-radius:12px;
  padding:24px;
  border:1px solid rgba(255,255,255,0.03);
  margin-bottom:20px;
  text-align:center;
}
</style>
</head>
<body>
  <div class="container">
    <nav class="navbar">
      <a href="/" class="logo">
        <div class="logo-icon">DF</div>
        <div>
          <div style="font-size:20px;font-weight:700">Safe DeFi Assistant</div>
          <div style="font-size:12px;color:var(--muted)">Risk Analysis</div>
        </div>
      </a>
      <div class="nav-links">
        <a href="/" class="nav-link">Home</a>
        <a href="/chat" class="nav-link">AI Assistant</a>
        <a href="/gas-prices" class="nav-link">Gas Prices</a>
        <a href="/market-data" class="nav-link">Market Data</a>
        <a href="/risk-analysis" class="nav-link active">Risk Analysis</a>
        <a href="/yield-farming" class="nav-link">Yield Farming</a>
      </div>
    </nav>

    <div class="card">
      <h1>🔍 Risk Analysis</h1>
      <p>Comprehensive risk analysis for DeFi protocols coming soon!</p>
      <p>For now, you can ask our AI assistant about specific protocol risks.</p>
      <a href="/chat" style="color:var(--accent);text-decoration:none">→ Go to AI Assistant</a>
    </div>
    
    <div class="card" style="background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.2);">
      <h2 style="color:var(--warning);margin-top:0">🚧 Coming Soon Features</h2>
      <ul>
        <li>Smart contract vulnerability scanning</li>
        <li>Protocol safety scoring system</li>
        <li>Risk comparison between protocols</li>
        <li>Historical risk data analysis</li>
        <li>Automated risk alerts</li>
      </ul>
    </div>
  </div>
</body>
</html>
"""
        html = get_risk_analysis_page()
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def serve_yield_farming_page(self):
        """Serve the yield farming page"""
        html = get_yield_farming_page()
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def serve_portfolio_page(self):
        """Serve the portfolio analysis page"""
        html = get_portfolio_page()
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    # API handlers
    def handle_gas_prices_api(self):
        """Handle gas prices API requests"""
        logger.info("Handling gas prices API request")
        try:
            gas_data = gas_monitor.get_gas_prices()
            self.send_json_response({"success": True, "data": gas_data})
        except Exception as e:
            logger.error(f"handle_gas_prices_api error: {e}")
            self.send_json_response({"success": False, "error": str(e)})

    def handle_market_data_api(self):
        """Handle market data API requests"""
        logger.info("Handling market data API request")
        try:
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
            logger.error(f"handle_market_data_api error: {e}")
            self.send_json_response({"success": False, "error": str(e)})

    def handle_tvl_data_api(self):
        """Handle TVL data API requests"""
        logger.info("Handling TVL data API request")
        try:
            tvl_data = tvl_tracker.get_protocol_tvl()
            self.send_json_response({"success": True, "data": tvl_data})
        except Exception as e:
            logger.error(f"handle_tvl_data_api error: {e}")
            self.send_json_response({"success": False, "error": str(e)})

    def handle_yield_opportunities_api(self):
        """Handle yield opportunities API requests"""
        logger.info("Handling yield opportunities API request")
        try:
            yield_data = yield_detector.get_yield_opportunities()
            self.send_json_response({"success": True, "data": yield_data})
        except Exception as e:
            logger.error(f"handle_yield_opportunities_api error: {e}")
            self.send_json_response({"success": False, "error": str(e)})

    def handle_chat_api(self):
        """Handle chat API requests"""
        logger.info("Handling chat API request")
        try:
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
            
            self.send_json_response(response_payload)
        except Exception as e:
            logger.error(f"handle_chat_api error: {e}")
            traceback.print_exc()
            self.send_json_response({"success": False, "error": str(e)}, status=500)

    def process_message(self, message):
        """Process chat messages and return AI responses"""
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

    def handle_sentient_info_api(self):
        """Handle Sentient agent info requests"""
        try:
            if sentient_agent:
                agent_info = sentient_agent.get_agent_info()
                self.send_json_response(agent_info)
            else:
                self.send_json_response({
                    "success": False, 
                    "error": "Sentient agent not initialized"
                }, status=500)
        except Exception as e:
            logger.error(f"Sentient info API error: {e}")
            self.send_json_response({
                "success": False, 
                "error": "Failed to get agent info"
            }, status=500)

    def handle_sentient_query_api(self):
        """Handle Sentient query requests"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            logger.info(f"Sentient query request: {data}")
            
            query = data.get('query', '')
            context = data.get('context', {})
            
            if not query:
                self.send_json_response({
                    "success": False,
                    "error": "Query parameter is required"
                }, status=400)
                return
            
            if sentient_agent:
                # Process query asynchronously
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(
                    sentient_agent.process_query(query, context)
                )
                loop.close()
                
                self.send_json_response(response)
            else:
                self.send_json_response({
                    "success": False,
                    "error": "Sentient agent not initialized"
                }, status=500)
                
        except json.JSONDecodeError:
            self.send_json_response({
                "success": False,
                "error": "Invalid JSON in request body"
            }, status=400)
        except Exception as e:
            logger.error(f"Sentient query API error: {e}")
            traceback.print_exc()
            self.send_json_response({
                "success": False,
                "error": "Failed to process query"
            }, status=500)

    def handle_portfolio_analysis_api(self):
        """Handle GET portfolio analysis requests"""
        try:
            # Get wallet address from query parameters
            parsed = urlparse(self.path)
            query_params = parse_qs(parsed.query)
            wallet_address = query_params.get('wallet', [None])[0]
            
            if not wallet_address:
                self.send_json_response({
                    "success": False,
                    "error": "Wallet address parameter is required"
                }, status=400)
                return
            
            # Analyze portfolio
            result = portfolio_analyzer.analyze_portfolio(wallet_address)
            self.send_json_response(result)
            
        except Exception as e:
            logger.error(f"Portfolio analysis API error: {e}")
            self.send_json_response({
                "success": False,
                "error": "Failed to analyze portfolio"
            }, status=500)

    def handle_portfolio_analysis_post_api(self):
        """Handle POST portfolio analysis requests"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            wallet_address = data.get('wallet_address')
            if not wallet_address:
                self.send_json_response({
                    "success": False,
                    "error": "wallet_address is required"
                }, status=400)
                return
            
            # Analyze portfolio
            result = portfolio_analyzer.analyze_portfolio(wallet_address)
            self.send_json_response(result)
            
        except json.JSONDecodeError:
            self.send_json_response({
                "success": False,
                "error": "Invalid JSON in request body"
            }, status=400)
        except Exception as e:
            logger.error(f"Portfolio analysis POST API error: {e}")
            self.send_json_response({
                "success": False,
                "error": "Failed to analyze portfolio"
            }, status=500)

    def handle_mev_status_api(self):
        """Handle MEV protection status requests"""
        try:
            result = mev_protection.get_mev_protection_status()
            self.send_json_response(result)
        except Exception as e:
            logger.error(f"MEV status API error: {e}")
            self.send_json_response({
                "success": False,
                "error": "Failed to get MEV protection status"
            }, status=500)

    def handle_mev_alerts_api(self):
        """Handle MEV alerts requests"""
        try:
            parsed = urlparse(self.path)
            query_params = parse_qs(parsed.query)
            wallet_address = query_params.get('wallet', [None])[0]
            
            if not wallet_address:
                self.send_json_response({
                    "success": False,
                    "error": "Wallet address parameter is required"
                }, status=400)
                return
            
            result = mev_protection.get_sandwich_attack_alerts(wallet_address)
            self.send_json_response(result)
            
        except Exception as e:
            logger.error(f"MEV alerts API error: {e}")
            self.send_json_response({
                "success": False,
                "error": "Failed to get MEV alerts"
            }, status=500)

    def handle_mev_check_api(self):
        """Handle MEV risk check requests"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            transaction_data = data.get('transaction_data', {})
            if not transaction_data:
                self.send_json_response({
                    "success": False,
                    "error": "transaction_data is required"
                }, status=400)
                return
            
            result = mev_protection.check_mev_risk(transaction_data)
            self.send_json_response(result)
            
        except json.JSONDecodeError:
            self.send_json_response({
                "success": False,
                "error": "Invalid JSON in request body"
            }, status=400)
        except Exception as e:
            logger.error(f"MEV check API error: {e}")
            self.send_json_response({
                "success": False,
                "error": "Failed to check MEV risk"
            }, status=500)

def main():
    """Main function to start the server"""
    port = config.PORT
    host = config.HOST
    server = HTTPServer((host, port), DeFiAssistantHandler)
    print("🚀 Safe DeFi Assistant running at: http://{}:{}".format(host, port))
    print("📱 Features available:")
    print("   • Landing page: http://{}:{}".format(host, port))
    print("   • Gas prices: http://{}:{}/gas-prices".format(host, port))
    print("   • Market data: http://{}:{}/market-data".format(host, port))
    print("   • AI chat: http://{}:{}/chat".format(host, port))
    print("🤖 Sentient API endpoints:")
    print("   • Agent info: http://{}:{}/api/sentient/info".format(host, port))
    print("   • Query endpoint: http://{}:{}/api/sentient/query".format(host, port))
    print("📊 Advanced Features:")
    print("   • Portfolio analysis: http://{}:{}/api/portfolio/analyze".format(host, port))
    print("   • MEV protection: http://{}:{}/api/mev/status".format(host, port))
    print("   • MEV alerts: http://{}:{}/api/mev/alerts".format(host, port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")

if __name__ == "__main__":
    main()
