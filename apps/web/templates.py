#!/usr/bin/env python3
"""
HTML Templates for DeFi Assistant
Landing page, feature pages, and components
"""

def get_base_css():
    """Base CSS styles for all pages"""
    return """
:root{
  --bg:#0f1724;
  --card:#0b1220;
  --accent:#7c5cff;
  --accent-2:#3ec6ff;
  --muted:#9aa4b2;
  --glass: rgba(255,255,255,0.04);
  --text:#e6eef8;
  --success:#10b981;
  --warning:#f59e0b;
  --error:#ef4444;
}
*{box-sizing:border-box}
body{
  margin:0;
  background: linear-gradient(180deg, #071022 0%, #081126 60%);
  font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  color:var(--text);
  -webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;
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
}
.btn{
  background: linear-gradient(90deg,var(--accent),var(--accent-2));
  border:none;
  color:white;
  padding:12px 20px;
  border-radius:8px;
  cursor:pointer;
  font-weight:600;
  text-decoration:none;
  display:inline-block;
  transition:transform 0.2s ease;
  box-shadow: 0 8px 24px rgba(124,92,255,0.18);
}
.btn:hover{
  transform:translateY(-2px);
}
.btn-secondary{
  background:rgba(255,255,255,0.1);
  color:var(--text);
}
.btn-secondary:hover{
  background:rgba(255,255,255,0.15);
}
.grid{
  display:grid;
  gap:20px;
}
.grid-2{grid-template-columns:repeat(auto-fit, minmax(300px, 1fr))}
.grid-3{grid-template-columns:repeat(auto-fit, minmax(250px, 1fr))}
.grid-4{grid-template-columns:repeat(auto-fit, minmax(200px, 1fr))}
.feature-card{
  background:var(--glass);
  border-radius:12px;
  padding:20px;
  border:1px solid rgba(255,255,255,0.03);
  transition:transform 0.2s ease, background 0.2s ease;
  text-decoration:none;
  color:inherit;
}
.feature-card:hover{
  transform:translateY(-4px);
  background:rgba(255,255,255,0.06);
}
.feature-icon{
  width:48px;
  height:48px;
  border-radius:12px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:24px;
  margin-bottom:16px;
  background:linear-gradient(135deg,var(--accent), var(--accent-2));
}
.feature-title{
  font-size:18px;
  font-weight:700;
  margin-bottom:8px;
}
.feature-desc{
  color:var(--muted);
  font-size:14px;
  line-height:1.5;
}
.loading{
  text-align:center;
  color:var(--muted);
  padding:20px;
}
.error{
  color:var(--error);
  background:rgba(239,68,68,0.1);
  border:1px solid rgba(239,68,68,0.2);
  padding:12px;
  border-radius:8px;
  margin:10px 0;
}
.success{
  color:var(--success);
  background:rgba(16,185,129,0.1);
  border:1px solid rgba(16,185,129,0.2);
  padding:12px;
  border-radius:8px;
  margin:10px 0;
}
@media (max-width:768px){
  .container{padding:10px}
  .navbar{flex-direction:column;gap:16px}
  .nav-links{flex-wrap:wrap;justify-content:center}
  .grid-2,.grid-3,.grid-4{grid-template-columns:1fr}
}

/* Snackbar notifications */
.snackbar{
  position:fixed;
  left:50%;
  transform:translateX(-50%);
  bottom:26px;
  background:var(--accent);
  color:white;
  padding:12px 20px;
  border-radius:8px;
  box-shadow:0 8px 30px rgba(2,6,23,0.6);
  z-index:9999;
  opacity:0;
  animation:slideUp .3s forwards;
}
@keyframes slideUp{
  from{transform:translateX(-50%) translateY(20px);opacity:0}
  to{transform:translateX(-50%) translateY(0);opacity:1}
}
.snackbar.warning{background:var(--warning)}
.snackbar.error{background:var(--error)}
.snackbar.success{background:var(--success)}
"""

def get_landing_page():
    """Landing page HTML"""
    return f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Safe DeFi Assistant - Your DeFi Safety Companion</title>
<style>{get_base_css()}</style>
</head>
<body>
  <div class="container">
    <nav class="navbar">
      <a href="/" class="logo">
        <div class="logo-icon">DF</div>
        <div>
          <div style="font-size:20px;font-weight:700">Safe DeFi Assistant</div>
          <div style="font-size:12px;color:var(--muted)">DeFi Safety & Intelligence</div>
        </div>
      </a>
      <div class="nav-links">
            <a href="/" class="nav-link active">Home</a>
            <a href="/chat" class="nav-link">AI Assistant</a>
            <a href="/gas-prices" class="nav-link">Gas Prices</a>
            <a href="/market-data" class="nav-link">Market Data</a>
            <a href="/risk-analysis" class="nav-link">Risk Analysis</a>
            <a href="/portfolio" class="nav-link">Portfolio</a>
            <a href="/yield-farming" class="nav-link">Yield Farming</a>
      </div>
    </nav>

    <div class="card" style="text-align:center;padding:40px">
      <h1 style="font-size:48px;margin:0 0 16px 0;background:linear-gradient(135deg,var(--accent),var(--accent-2));-webkit-background-clip:text;-webkit-text-fill-color:transparent">
        Safe DeFi Assistant
      </h1>
      <p style="font-size:20px;color:var(--muted);margin:0 0 32px 0;max-width:600px;margin-left:auto;margin-right:auto">
        Your comprehensive DeFi safety companion with real-time market data, risk analysis, and AI-powered insights
      </p>
      <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap">
        <a href="/chat" class="btn">Start Chatting</a>
        <a href="/market-data" class="btn btn-secondary">View Market Data</a>
      </div>
    </div>

    <div class="grid grid-3">
      <a href="/gas-prices" class="feature-card">
        <div class="feature-icon">⛽</div>
        <div class="feature-title">Real-Time Gas Prices</div>
        <div class="feature-desc">
          Monitor Ethereum, Polygon, and Arbitrum gas prices in real-time. Get optimal transaction timing recommendations.
        </div>
      </a>
      
      <a href="/market-data" class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-title">DeFi Market Data</div>
        <div class="feature-desc">
          Track TVL changes, protocol performance, and market trends across major DeFi protocols.
        </div>
      </a>
      
      <a href="/risk-analysis" class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Risk Analysis</div>
        <div class="feature-desc">
          Comprehensive risk assessments for DeFi protocols including smart contract audits and safety scores.
        </div>
      </a>
      
      <a href="/yield-farming" class="feature-card">
        <div class="feature-icon">🌾</div>
        <div class="feature-title">Yield Opportunities</div>
        <div class="feature-desc">
          Discover high-yield farming opportunities with risk-adjusted returns and safety recommendations.
        </div>
      </a>
      
      <a href="/chat" class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI Assistant</div>
        <div class="feature-desc">
          Chat with our AI-powered assistant for personalized DeFi advice and real-time market insights.
        </div>
      </a>
      
      <a href="/portfolio" class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Portfolio Analysis</div>
        <div class="feature-desc">
          Analyze your DeFi portfolio performance, risks, and optimization opportunities.
        </div>
      </a>
    </div>

    <div class="card">
      <h2 style="margin-top:0">Why Choose Safe DeFi Assistant?</h2>
      <div class="grid grid-2">
        <div>
          <h3>🛡️ Safety First</h3>
          <p>Comprehensive risk analysis and safety recommendations for all major DeFi protocols.</p>
        </div>
        <div>
          <h3>⚡ Real-Time Data</h3>
          <p>Live market data, gas prices, and yield opportunities updated every 30 seconds.</p>
        </div>
        <div>
          <h3>🤖 AI-Powered</h3>
          <p>Advanced AI assistant with access to current web data for accurate, up-to-date advice.</p>
        </div>
        <div>
          <h3>🔍 Multi-Chain</h3>
          <p>Support for Ethereum, Polygon, Arbitrum, and other major DeFi ecosystems.</p>
        </div>
      </div>
    </div>
  </div>

  <script>
    function showComingSoon(feature) {{
      showSnackbar('🚧 ' + feature + ' is coming soon!', 'warning');
    }}

    function showSnackbar(message, type = 'info') {{
      const snackbar = document.createElement('div');
      snackbar.className = 'snackbar ' + type;
      snackbar.textContent = message;
      document.body.appendChild(snackbar);
      
      setTimeout(() => {{
        snackbar.style.opacity = '0';
        setTimeout(() => snackbar.remove(), 300);
      }}, 3000);
    }}
  </script>
</body>
</html>
"""

def get_gas_prices_page():
    """Gas prices page HTML"""
    return f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Gas Prices - Safe DeFi Assistant</title>
<style>{get_base_css()}</style>
</head>
<body>
  <div class="container">
    <nav class="navbar">
      <a href="/" class="logo">
        <div class="logo-icon">DF</div>
        <div>
          <div style="font-size:20px;font-weight:700">Safe DeFi Assistant</div>
          <div style="font-size:12px;color:var(--muted)">Gas Price Monitor</div>
        </div>
      </a>
      <div class="nav-links">
            <a href="/" class="nav-link">Home</a>
            <a href="/chat" class="nav-link">AI Assistant</a>
            <a href="/gas-prices" class="nav-link active">Gas Prices</a>
            <a href="/market-data" class="nav-link">Market Data</a>
            <a href="/risk-analysis" class="nav-link">Risk Analysis</a>
            <a href="/portfolio" class="nav-link">Portfolio</a>
            <a href="/yield-farming" class="nav-link">Yield Farming</a>
      </div>
    </nav>

    <div class="card">
      <h1 style="margin-top:0">⛽ Real-Time Gas Prices</h1>
      <p>Monitor gas prices across multiple networks and get optimal transaction timing recommendations.</p>
      
      <div id="gas-data" class="loading">
        Loading gas price data...
      </div>
      
      <div style="margin-top:20px">
        <button class="btn" onclick="refreshGasPrices()">🔄 Refresh Data</button>
        <button class="btn btn-secondary" onclick="setAutoRefresh()">⏰ Auto Refresh</button>
      </div>
    </div>

    <div class="card">
      <h2>Gas Price Tips</h2>
      <div class="grid grid-2">
        <div>
          <h3>🕐 Best Times to Transact</h3>
          <ul>
            <li>Early morning (UTC): 6-10 AM</li>
            <li>Weekend mornings</li>
            <li>Avoid peak hours: 2-6 PM UTC</li>
          </ul>
        </div>
        <div>
          <h3>💰 Cost Optimization</h3>
          <ul>
            <li>Use Layer 2 solutions (Polygon, Arbitrum)</li>
            <li>Batch multiple transactions</li>
            <li>Monitor gas price trends</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <script>
    async function fetchGasPrices() {{
      try {{
        const response = await fetch('/api/gas-prices');
        const data = await response.json();
        return data.success ? data.data : null;
      }} catch (error) {{
        console.error('Error fetching gas prices:', error);
        return null;
      }}
    }}

    function updateGasDisplay(data) {{
      const container = document.getElementById('gas-data');
      if (!data) {{
        container.innerHTML = '<div class="error">Failed to load gas price data</div>';
        return;
      }}
      
      const eth = data.ethereum;
      let html = '<div class="grid grid-2">';
      html += '<div class="card"><h3>Ethereum Gas Prices</h3>';
      html += '<div style="display:flex;justify-content:space-between;margin:8px 0"><span>Slow</span><span style="font-weight:600">' + eth.slow + ' Gwei</span></div>';
      html += '<div style="display:flex;justify-content:space-between;margin:8px 0"><span>Standard</span><span style="font-weight:600">' + eth.standard + ' Gwei</span></div>';
      html += '<div style="display:flex;justify-content:space-between;margin:8px 0"><span>Fast</span><span style="font-weight:600">' + eth.fast + ' Gwei</span></div>';
      html += '<div style="display:flex;justify-content:space-between;margin:8px 0"><span>Instant</span><span style="font-weight:600">' + Math.round(eth.instant) + ' Gwei</span></div>';
      html += '</div>';
      
      html += '<div class="card"><h3>Last Updated</h3>';
      html += '<p>' + new Date(data.last_updated).toLocaleString() + '</p>';
      html += '<p>Sources: ' + data.sources.join(', ') + '</p>';
      html += '</div>';
      html += '</div>';
      
      container.innerHTML = html;
    }}

    async function refreshGasPrices() {{
      const data = await fetchGasPrices();
      updateGasDisplay(data);
    }}

    function setAutoRefresh() {{
      setInterval(refreshGasPrices, 30000);
      alert('Auto-refresh enabled! Gas prices will update every 30 seconds.');
    }}

    // Initial load
    window.addEventListener('load', refreshGasPrices);
  </script>
</body>
</html>
"""

def get_market_data_page():
    """Market data page HTML"""
    return f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Market Data - Safe DeFi Assistant</title>
<style>{get_base_css()}</style>
</head>
<body>
  <div class="container">
    <nav class="navbar">
      <a href="/" class="logo">
        <div class="logo-icon">DF</div>
        <div>
          <div style="font-size:20px;font-weight:700">Safe DeFi Assistant</div>
          <div style="font-size:12px;color:var(--muted)">Market Intelligence</div>
        </div>
      </a>
      <div class="nav-links">
            <a href="/" class="nav-link">Home</a>
            <a href="/chat" class="nav-link">AI Assistant</a>
            <a href="/gas-prices" class="nav-link">Gas Prices</a>
            <a href="/market-data" class="nav-link active">Market Data</a>
            <a href="/risk-analysis" class="nav-link">Risk Analysis</a>
            <a href="/portfolio" class="nav-link">Portfolio</a>
            <a href="/yield-farming" class="nav-link">Yield Farming</a>
      </div>
    </nav>

    <div class="card">
      <h1 style="margin-top:0">📈 DeFi Market Data</h1>
      <p>Real-time TVL tracking, protocol performance, and market trends.</p>
      
      <div id="market-data" class="loading">
        Loading market data...
      </div>
      
      <div style="margin-top:20px">
        <button class="btn" onclick="refreshMarketData()">🔄 Refresh All Data</button>
        <button class="btn btn-secondary" onclick="toggleAutoRefresh()">⏰ Auto Refresh</button>
      </div>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h2>📊 Protocol TVL Rankings</h2>
        <div id="tvl-data" class="loading">Loading TVL data...</div>
      </div>
      
      <div class="card">
        <h2>🌾 Top Yield Opportunities</h2>
        <div id="yield-data" class="loading">Loading yield data...</div>
      </div>
    </div>
  </div>

  <script>
    let autoRefreshInterval = null;

    async function fetchMarketData() {{
      try {{
        const response = await fetch('/api/market-data');
        const data = await response.json();
        return data.success ? data.data : null;
      }} catch (error) {{
        console.error('Error fetching market data:', error);
        return null;
      }}
    }}

    function updateMarketDisplay(data) {{
      if (!data) {{
        document.getElementById('market-data').innerHTML = '<div class="error">Failed to load market data</div>';
        return;
      }}
      
      let html = '<div class="grid grid-3">';
      html += '<div class="card"><h3>Total DeFi TVL</h3><p style="font-size:24px;font-weight:700">$' + (data.tvl_data.total_tvl / 1e9).toFixed(1) + 'B</p></div>';
      html += '<div class="card"><h3>Gas Prices</h3><p style="font-size:24px;font-weight:700">' + data.gas_prices.ethereum.standard + ' Gwei</p></div>';
      html += '<div class="card"><h3>Top Yields</h3><p style="font-size:24px;font-weight:700">' + (data.yield_opportunities.top_yields[0]?.apy || 0) + '% APY</p></div>';
      html += '</div>';
      
      document.getElementById('market-data').innerHTML = html;
    }}

    function updateTVLDisplay(data) {{
      const container = document.getElementById('tvl-data');
      if (!data || !data.protocols) {{
        container.innerHTML = '<div class="error">Failed to load TVL data</div>';
        return;
      }}
      
      let html = '';
      const protocols = Object.values(data.protocols).slice(0, 5);
      protocols.forEach(protocol => {{
        const change = protocol.change_1d > 0 ? '+' : '';
        const changeColor = protocol.change_1d > 0 ? 'var(--success)' : 'var(--error)';
        html += '<div style="display:flex;justify-content:space-between;margin:8px 0;padding:8px;background:rgba(255,255,255,0.02);border-radius:6px">';
        html += '<span>' + protocol.name + '</span>';
        html += '<div style="text-align:right">';
        html += '<div style="font-weight:600">$' + (protocol.tvl/1e9).toFixed(1) + 'B</div>';
        html += '<div style="font-size:12px;color:' + changeColor + '">' + change + protocol.change_1d.toFixed(1) + '%</div>';
        html += '</div></div>';
      }});
      
      container.innerHTML = html;
    }}

    function updateYieldDisplay(data) {{
      const container = document.getElementById('yield-data');
      if (!data || !data.top_yields) {{
        container.innerHTML = '<div class="error">Failed to load yield data</div>';
        return;
      }}
      
      let html = '';
      data.top_yields.slice(0, 5).forEach(yield => {{
        html += '<div style="display:flex;justify-content:space-between;margin:8px 0;padding:8px;background:rgba(255,255,255,0.02);border-radius:6px">';
        html += '<span>' + yield.protocol + '</span>';
        html += '<div style="text-align:right">';
        html += '<div style="font-weight:600;color:var(--success)">' + yield.apy + '% APY</div>';
        html += '<div style="font-size:12px;color:var(--muted)">$' + (yield.tvl/1e6).toFixed(1) + 'M TVL</div>';
        html += '</div></div>';
      }});
      
      container.innerHTML = html;
    }}

    async function refreshMarketData() {{
      const data = await fetchMarketData();
      updateMarketDisplay(data);
      if (data) {{
        updateTVLDisplay(data.tvl_data);
        updateYieldDisplay(data.yield_opportunities);
      }}
    }}

    function toggleAutoRefresh() {{
      if (autoRefreshInterval) {{
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
        alert('Auto-refresh disabled');
      }} else {{
        autoRefreshInterval = setInterval(refreshMarketData, 30000);
        alert('Auto-refresh enabled! Data will update every 30 seconds.');
      }}
    }}

    // Initial load
    window.addEventListener('load', refreshMarketData);
  </script>
</body>
</html>
"""

def get_chat_page():
    """Chat page HTML"""
    return f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>AI Assistant - Safe DeFi Assistant</title>
<style>{get_base_css()}
.chat-container{{
  display:grid;
  grid-template-columns:300px 1fr;
  gap:20px;
  height:70vh;
}}
.chat-sidebar{{
  background:var(--glass);
  border-radius:12px;
  padding:20px;
  border:1px solid rgba(255,255,255,0.03);
  overflow-y:auto;
}}
.chat-main{{
  background:var(--glass);
  border-radius:12px;
  border:1px solid rgba(255,255,255,0.03);
  display:flex;
  flex-direction:column;
}}
.chat-messages{{
  flex:1;
  padding:20px;
  overflow-y:auto;
  display:flex;
  flex-direction:column;
  gap:12px;
}}
.chat-input{{
  padding:20px;
  border-top:1px solid rgba(255,255,255,0.03);
  display:flex;
  gap:12px;
}}
.chat-input input{{
  flex:1;
  background:rgba(255,255,255,0.05);
  border:1px solid rgba(255,255,255,0.1);
  border-radius:8px;
  padding:12px;
  color:inherit;
  font-size:14px;
}}
.chat-input input:focus{{
  outline:none;
  border-color:var(--accent);
}}
.message{{
  max-width:80%;
  padding:12px 16px;
  border-radius:12px;
  word-wrap:break-word;
}}
.message.user{{
  margin-left:auto;
  background:linear-gradient(135deg,var(--accent),var(--accent-2));
  color:white;
}}
.message.bot{{
  margin-right:auto;
  background:rgba(255,255,255,0.05);
  border:1px solid rgba(255,255,255,0.1);
}}
.quick-action{{
  background:rgba(255,255,255,0.05);
  border:1px solid rgba(255,255,255,0.1);
  border-radius:8px;
  padding:12px;
  margin-bottom:8px;
  cursor:pointer;
  transition:background 0.2s ease;
}}
.quick-action:hover{{
  background:rgba(255,255,255,0.1);
}}
@media (max-width:768px){{
  .chat-container{{grid-template-columns:1fr}}
  .chat-sidebar{{display:none}}
}}
</style>
</head>
<body>
  <div class="container">
    <nav class="navbar">
      <a href="/" class="logo">
        <div class="logo-icon">DF</div>
        <div>
          <div style="font-size:20px;font-weight:700">Safe DeFi Assistant</div>
          <div style="font-size:12px;color:var(--muted)">AI Chat Assistant</div>
        </div>
      </a>
      <div class="nav-links">
            <a href="/" class="nav-link">Home</a>
            <a href="/chat" class="nav-link active">AI Assistant</a>
            <a href="/gas-prices" class="nav-link">Gas Prices</a>
            <a href="/market-data" class="nav-link">Market Data</a>
            <a href="/risk-analysis" class="nav-link">Risk Analysis</a>
            <a href="/portfolio" class="nav-link">Portfolio</a>
            <a href="/yield-farming" class="nav-link">Yield Farming</a>
      </div>
    </nav>

    <div class="chat-container">
      <div class="chat-sidebar">
        <h3 style="margin-top:0">Quick Actions</h3>
        <div class="quick-action" onclick="askQuestion('What are current gas prices?')">
          ⛽ Gas Prices
        </div>
        <div class="quick-action" onclick="askQuestion('What are the risks of using Aave?')">
          🔍 Aave Risks
        </div>
        <div class="quick-action" onclick="askQuestion('Is Uniswap safe to use?')">
          🦄 Uniswap Safety
        </div>
        <div class="quick-action" onclick="askQuestion('Analyze staking 100 USDC on Compound')">
          📊 DeFi Analysis
        </div>
        
        <h3 style="margin-top:24px">Live Data</h3>
        <div id="live-gas" class="loading">Loading gas data...</div>
        <div id="live-tvl" class="loading">Loading TVL data...</div>
      </div>
      
      <div class="chat-main">
        <div class="chat-messages" id="chat-messages">
          <div class="message bot">
            <strong>👋 Welcome!</strong><br>
            I'm your Safe DeFi Assistant. Ask me about gas prices, protocol risks, yield farming opportunities, or any DeFi-related questions!
          </div>
        </div>
        
        <div class="chat-input">
          <input type="text" id="message-input" placeholder="Ask about DeFi..." onkeydown="handleKey(event)">
          <button class="btn" onclick="sendMessage()">Send</button>
        </div>
      </div>
    </div>
  </div>

  <script>
    function markdownToHtml(text) {{
      return text
        .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
        .replace(/\\*(.*?)\\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/\\n/g, '<br>');
    }}

    function addMessage(text, type) {{
      const container = document.getElementById('chat-messages');
      const message = document.createElement('div');
      message.className = 'message ' + type;
      message.innerHTML = markdownToHtml(text);
      container.appendChild(message);
      container.scrollTop = container.scrollHeight;
    }}

    function askQuestion(question) {{
      document.getElementById('message-input').value = question;
      sendMessage();
    }}

    function handleKey(e) {{
      if (e.key === 'Enter') sendMessage();
    }}

    async function sendMessage() {{
      const input = document.getElementById('message-input');
      const text = input.value.trim();
      if (!text) return;

      addMessage('<strong>You:</strong><br>' + text, 'user');
      input.value = '';

      // Show loading
      const loadingMsg = document.createElement('div');
      loadingMsg.className = 'message bot';
      loadingMsg.innerHTML = '<strong>Assistant:</strong><br>Thinking...';
      document.getElementById('chat-messages').appendChild(loadingMsg);

      try {{
        const response = await fetch('/api/chat', {{
          method: 'POST',
          headers: {{'Content-Type': 'application/json'}},
          body: JSON.stringify({{message: text}})
        }});

        const data = await response.json();
        loadingMsg.remove();

        if (data.success) {{
          addMessage('<strong>Assistant:</strong><br>' + data.response, 'bot');
        }} else {{
          addMessage('<strong>Error:</strong><br>' + (data.error || 'Something went wrong'), 'bot');
        }}
      }} catch (error) {{
        loadingMsg.remove();
        addMessage('<strong>Error:</strong><br>Network error: ' + error.message, 'bot');
      }}
    }}

    // Load live data
    async function loadLiveData() {{
      try {{
        const response = await fetch('/api/market-data');
        const data = await response.json();
        if (data.success) {{
          const gas = data.data.gas_prices.ethereum;
          const tvl = data.data.tvl_data.total_tvl;
          document.getElementById('live-gas').innerHTML = '⛽ ETH: ' + gas.standard + ' Gwei';
          document.getElementById('live-tvl').innerHTML = '📈 TVL: $' + (tvl/1e9).toFixed(1) + 'B';
        }}
      }} catch (error) {{
        console.error('Error loading live data:', error);
      }}
    }}

    // Auto-refresh live data
    setInterval(loadLiveData, 30000);
    window.addEventListener('load', loadLiveData);
  </script>
</body>
</html>
"""

def get_portfolio_page():
    return f"""
    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Portfolio Analysis - Safe DeFi Assistant</title>
    <style>{get_base_css()}
    .portfolio-container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }}
    .wallet-input {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 20px;
    }}
    .wallet-input input {{
      width: 100%;
      padding: 12px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--bg);
      color: var(--text);
      font-size: 14px;
    }}
    .wallet-input button {{
      margin-top: 10px;
      width: 100%;
    }}
    .analysis-result {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      margin-top: 20px;
      display: none;
    }}
    .risk-score {{
      display: inline-block;
      padding: 8px 16px;
      border-radius: 20px;
      font-weight: 700;
      font-size: 18px;
    }}
    .risk-low {{ background: #10b981; color: white; }}
    .risk-medium {{ background: #f59e0b; color: white; }}
    .risk-high {{ background: #ef4444; color: white; }}
    .positions-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 15px;
      margin: 20px 0;
    }}
    .position-card {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 15px;
    }}
    .position-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }}
    .protocol-name {{
      font-weight: 700;
      color: var(--primary);
    }}
    .position-value {{
      font-weight: 700;
      color: var(--text);
    }}
    .risk-factors, .recommendations {{
      margin: 15px 0;
    }}
    .risk-factors ul, .recommendations ul {{
      margin: 10px 0;
      padding-left: 20px;
    }}
    .risk-factors li, .recommendations li {{
      margin: 5px 0;
      color: var(--text-secondary);
    }}
    </style>
    </head>
    <body>
      <div class="container">
        <nav class="navbar">
          <a href="/" class="logo">
            <div class="logo-icon">DF</div>
            <div>
              <div style="font-size:20px;font-weight:700">Safe DeFi Assistant</div>
              <div style="font-size:12px;color:var(--muted)">Portfolio Analysis</div>
            </div>
          </a>
          <div class="nav-links">
            <a href="/" class="nav-link">Home</a>
            <a href="/chat" class="nav-link">AI Assistant</a>
            <a href="/gas-prices" class="nav-link">Gas Prices</a>
            <a href="/market-data" class="nav-link">Market Data</a>
            <a href="/risk-analysis" class="nav-link">Risk Analysis</a>
            <a href="/portfolio" class="nav-link active">Portfolio</a>
            <a href="/yield-farming" class="nav-link">Yield Farming</a>
          </div>
        </nav>
        
        <div class="portfolio-container">
          <div class="page-header">
            <h1>📊 Portfolio Risk Analysis</h1>
            <p>Analyze your DeFi portfolio for risks and get personalized recommendations</p>
          </div>
          
          <div class="wallet-input">
            <h3>Enter Wallet Address</h3>
            <input type="text" id="walletInput" placeholder="0x1234567890123456789012345678901234567890" />
            <button class="btn-primary" onclick="analyzePortfolio()">Analyze Portfolio</button>
          </div>
          
          <div id="loadingIndicator" style="display: none; text-align: center; padding: 40px;">
            <div style="font-size: 18px;">🔍 Analyzing portfolio...</div>
            <div style="color: var(--muted); margin-top: 10px;">This may take a few moments</div>
          </div>
          
          <div id="analysisResult" class="analysis-result">
            <div class="analysis-header">
              <h2>📈 Portfolio Analysis Results</h2>
              <div id="riskScore" class="risk-score"></div>
            </div>
            
            <div class="portfolio-summary">
              <h3>💰 Portfolio Summary</h3>
              <div id="portfolioSummary"></div>
            </div>
            
            <div class="positions-section">
              <h3>📋 Positions</h3>
              <div id="positionsGrid" class="positions-grid"></div>
            </div>
            
            <div class="risk-factors">
              <h3>⚠️ Risk Factors</h3>
              <ul id="riskFactorsList"></ul>
            </div>
            
            <div class="recommendations">
              <h3>💡 Recommendations</h3>
              <ul id="recommendationsList"></ul>
            </div>
          </div>
        </div>
      </div>
      
      <script>
        async function analyzePortfolio() {{
          const walletInput = document.getElementById('walletInput');
          const walletAddress = walletInput.value.trim();
          
          if (!walletAddress) {{
            showSnackbar('Please enter a wallet address', 'error');
            return;
          }}
          
          if (!walletAddress.startsWith('0x') || walletAddress.length !== 42) {{
            showSnackbar('Please enter a valid Ethereum address', 'error');
            return;
          }}
          
          // Show loading indicator
          document.getElementById('loadingIndicator').style.display = 'block';
          document.getElementById('analysisResult').style.display = 'none';
          
          try {{
            const response = await fetch(`/api/portfolio/analyze?wallet=${{walletAddress}}`);
            const data = await response.json();
            
            if (data.success) {{
              displayAnalysisResults(data.data);
            }} else {{
              showSnackbar('Analysis failed: ' + data.error, 'error');
            }}
          }} catch (error) {{
            showSnackbar('Error analyzing portfolio: ' + error.message, 'error');
          }} finally {{
            document.getElementById('loadingIndicator').style.display = 'none';
          }}
        }}
        
        function displayAnalysisResults(data) {{
          // Show results
          document.getElementById('analysisResult').style.display = 'block';
          
          // Risk score
          const riskScore = document.getElementById('riskScore');
          const score = data.risk_score;
          riskScore.textContent = `Risk Score: ${{score}}/10`;
          riskScore.className = 'risk-score ' + (score <= 3 ? 'risk-low' : score <= 7 ? 'risk-medium' : 'risk-high');
          
          // Portfolio summary
          document.getElementById('portfolioSummary').innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0;">
              <div style="background: var(--bg); padding: 15px; border-radius: 8px; text-align: center;">
                <div style="font-size: 24px; font-weight: 700; color: var(--primary);">$${{data.total_value.toLocaleString()}}</div>
                <div style="color: var(--muted);">Total Value</div>
              </div>
              <div style="background: var(--bg); padding: 15px; border-radius: 8px; text-align: center;">
                <div style="font-size: 24px; font-weight: 700; color: var(--primary);">${{data.positions.length}}</div>
                <div style="color: var(--muted);">Positions</div>
              </div>
              <div style="background: var(--bg); padding: 15px; border-radius: 8px; text-align: center;">
                <div style="font-size: 24px; font-weight: 700; color: var(--primary);">${{data.liquidation_risks.length}}</div>
                <div style="color: var(--muted);">Liquidation Risks</div>
              </div>
            </div>
          `;
          
          // Positions
          const positionsGrid = document.getElementById('positionsGrid');
          positionsGrid.innerHTML = data.positions.map(pos => `
            <div class="position-card">
              <div class="position-header">
                <div class="protocol-name">${{pos.protocol}}</div>
                <div class="position-value">$${{pos.value_usd}}</div>
              </div>
              <div style="color: var(--text-secondary); margin-bottom: 10px;">${{pos.token}}</div>
              <div style="color: var(--text-secondary); font-size: 14px;">${{pos.amount}}</div>
              ${{pos.health_factor ? `<div style="margin-top: 10px; padding: 4px 8px; background: var(--bg); border-radius: 4px; font-size: 12px;">Health Factor: ${{pos.health_factor}}</div>` : ''}}
            </div>
          `).join('');
          
          // Risk factors
          const riskFactorsList = document.getElementById('riskFactorsList');
          riskFactorsList.innerHTML = data.risk_factors.map(factor => `<li>${{factor}}</li>`).join('');
          
          // Recommendations
          const recommendationsList = document.getElementById('recommendationsList');
          recommendationsList.innerHTML = data.recommendations.map(rec => `<li>${{rec}}</li>`).join('');
        }}
        
        function showSnackbar(message, type = 'info') {{
          const snackbar = document.createElement('div');
          snackbar.className = `snackbar snackbar-${{type}}`;
          snackbar.textContent = message;
          document.body.appendChild(snackbar);
          
          setTimeout(() => {{
            snackbar.classList.add('show');
          }}, 100);
          
          setTimeout(() => {{
            snackbar.classList.remove('show');
            setTimeout(() => document.body.removeChild(snackbar), 300);
          }}, 3000);
        }}
      </script>
    </body>
    </html>
    """

def get_risk_analysis_page():
    return f"""
    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Risk Analysis - Safe DeFi Assistant</title>
    <style>{get_base_css()}</style>
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
            <a href="/portfolio" class="nav-link">Portfolio</a>
            <a href="/yield-farming" class="nav-link">Yield Farming</a>
          </div>
        </nav>
        
        <div class="page-header">
          <h1>⚠️ Risk Analysis</h1>
          <p>Comprehensive DeFi risk assessment and protocol safety analysis</p>
        </div>
        
        <div class="card">
          <h2>🚧 Coming Soon</h2>
          <p>Our advanced risk analysis feature is currently under development. This will include:</p>
          <ul>
            <li>Smart contract security audits</li>
            <li>Protocol risk scoring</li>
            <li>Liquidation risk analysis</li>
            <li>Market volatility assessment</li>
            <li>Cross-protocol risk comparison</li>
            <li>Real-time risk alerts</li>
          </ul>
          <p>In the meantime, you can use our <a href="/chat">AI Assistant</a> to get personalized risk assessments!</p>
        </div>
      </div>
      
      <script>
        function showSnackbar(message, type = 'info') {{
          const snackbar = document.createElement('div');
          snackbar.className = `snackbar snackbar-${{type}}`;
          snackbar.textContent = message;
          document.body.appendChild(snackbar);
          
          setTimeout(() => {{
            snackbar.classList.add('show');
          }}, 100);
          
          setTimeout(() => {{
            snackbar.classList.remove('show');
            setTimeout(() => document.body.removeChild(snackbar), 300);
          }}, 3000);
        }}
      </script>
    </body>
    </html>
    """

def get_yield_farming_page():
    return f"""
    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Yield Farming - Safe DeFi Assistant</title>
    <style>{get_base_css()}</style>
    </head>
    <body>
      <div class="container">
        <nav class="navbar">
          <a href="/" class="logo">
            <div class="logo-icon">DF</div>
            <div>
              <div style="font-size:20px;font-weight:700">Safe DeFi Assistant</div>
              <div style="font-size:12px;color:var(--muted)">Yield Farming</div>
            </div>
          </a>
          <div class="nav-links">
            <a href="/" class="nav-link">Home</a>
            <a href="/chat" class="nav-link">AI Assistant</a>
            <a href="/gas-prices" class="nav-link">Gas Prices</a>
            <a href="/market-data" class="nav-link">Market Data</a>
            <a href="/risk-analysis" class="nav-link">Risk Analysis</a>
            <a href="/portfolio" class="nav-link">Portfolio</a>
            <a href="/yield-farming" class="nav-link active">Yield Farming</a>
          </div>
        </nav>
        
        <div class="page-header">
          <h1>🌾 Yield Farming Opportunities</h1>
          <p>Discover high-yield farming opportunities with risk-adjusted returns and safety recommendations</p>
        </div>
        
        <div class="card">
          <h2>🚧 Coming Soon</h2>
          <p>Our yield farming analysis feature is currently under development. This will include:</p>
          <ul>
            <li>Real-time yield opportunity detection</li>
            <li>Risk-adjusted return calculations</li>
            <li>Protocol safety assessments</li>
            <li>Impermanent loss analysis</li>
            <li>Automated yield optimization suggestions</li>
          </ul>
          <p>In the meantime, you can use our <a href="/chat">AI Assistant</a> to get personalized yield farming advice!</p>
        </div>
      </div>
      
      <script>
        function showSnackbar(message, type = 'info') {{
          const snackbar = document.createElement('div');
          snackbar.className = `snackbar snackbar-${{type}}`;
          snackbar.textContent = message;
          document.body.appendChild(snackbar);
          
          setTimeout(() => {{
            snackbar.classList.add('show');
          }}, 100);
          
          setTimeout(() => {{
            snackbar.classList.remove('show');
            setTimeout(() => document.body.removeChild(snackbar), 300);
          }}, 3000);
        }}
      </script>
    </body>
    </html>
    """

def get_risk_analysis_page():
    return f"""
    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Risk Analysis - Safe DeFi Assistant</title>
    <style>{get_base_css()}</style>
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
            <a href="/portfolio" class="nav-link">Portfolio</a>
            <a href="/yield-farming" class="nav-link">Yield Farming</a>
          </div>
        </nav>
        
        <div class="page-header">
          <h1>⚠️ Risk Analysis</h1>
          <p>Comprehensive DeFi risk assessment and protocol safety analysis</p>
        </div>
        
        <div class="card">
          <h2>🚧 Coming Soon</h2>
          <p>Our advanced risk analysis feature is currently under development. This will include:</p>
          <ul>
            <li>Smart contract security audits</li>
            <li>Protocol risk scoring</li>
            <li>Liquidation risk analysis</li>
            <li>Market volatility assessment</li>
            <li>Cross-protocol risk comparison</li>
            <li>Real-time risk alerts</li>
          </ul>
          <p>In the meantime, you can use our <a href="/chat">AI Assistant</a> to get personalized risk assessments!</p>
        </div>
      </div>
      
      <script>
        function showSnackbar(message, type = 'info') {{
          const snackbar = document.createElement('div');
          snackbar.className = `snackbar snackbar-${{type}}`;
          snackbar.textContent = message;
          document.body.appendChild(snackbar);
          
          setTimeout(() => {{
            snackbar.classList.add('show');
          }}, 100);
          
          setTimeout(() => {{
            snackbar.classList.remove('show');
            setTimeout(() => document.body.removeChild(snackbar), 300);
          }}, 3000);
        }}
      </script>
    </body>
    </html>
    """
