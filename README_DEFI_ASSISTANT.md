# Safe DeFi Assistant

A comprehensive DeFi safety companion with real-time market data, risk analysis, and AI-powered insights.

## 🚀 Features

- **Real-Time Gas Prices**: Monitor Ethereum, Polygon, and Arbitrum gas prices
- **DeFi Market Data**: Track TVL changes and protocol performance
- **Yield Farming Detection**: Discover high-yield opportunities
- **AI-Powered Chat**: Get personalized DeFi advice and insights
- **Risk Analysis**: Comprehensive safety assessments for DeFi protocols
- **Multi-Chain Support**: Ethereum, Polygon, Arbitrum, and more

## 📁 Project Structure

```
OpenDeepSearch/
├── defi_assistant_server.py    # Main server application
├── market_data.py              # Market data services (gas, TVL, yields)
├── templates.py                # HTML templates for all pages
├── working_defi_assistant.py   # Legacy single-file version
├── .env                        # Environment variables (API keys)
├── env_template.txt            # Template for environment setup
└── requirements.txt            # Python dependencies
```

## 🛠️ Installation

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd OpenDeepSearch
   python -m venv opendeepsearch_env
   source opendeepsearch_env/bin/activate  # On Windows: opendeepsearch_env\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure API keys**:
   ```bash
   cp env_template.txt .env
   # Edit .env with your actual API keys
   ```

3. **Run the application**:
   ```bash
   python defi_assistant_server.py
   ```

## 🌐 Available Pages

- **Landing Page**: `http://localhost:8080/` - Overview and navigation
- **Gas Prices**: `http://localhost:8080/gas-prices` - Real-time gas monitoring
- **Market Data**: `http://localhost:8080/market-data` - DeFi market intelligence
- **AI Chat**: `http://localhost:8080/chat` - Interactive AI assistant
- **Risk Analysis**: `http://localhost:8080/risk-analysis` - Protocol safety (coming soon)
- **Yield Farming**: `http://localhost:8080/yield-farming` - Yield opportunities (coming soon)

## 🔧 API Endpoints

- `GET /api/gas-prices` - Real-time gas price data
- `GET /api/market-data` - Comprehensive market data
- `GET /api/tvl-data` - DeFi protocol TVL data
- `GET /api/yield-opportunities` - Yield farming opportunities
- `POST /api/chat` - AI chat interface

## 🔑 Required API Keys

Add these to your `.env` file:

```bash
SERPER_API_KEY=your_serper_key
OPENROUTER_API_KEY=your_openrouter_key
JINA_API_KEY=your_jina_key
LITELLM_API_KEY=your_litellm_key
LITELLM_MODEL_ID=openrouter/google/gemini-2.0-flash-001
ETHERSCAN_API_KEY=your_etherscan_key
```

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile
- **Dark Theme**: Modern, easy-on-the-eyes interface
- **Real-Time Updates**: Auto-refreshing data every 30 seconds
- **Interactive Elements**: Hover effects, smooth transitions
- **Markdown Support**: Rich text formatting in chat responses

## 🔄 Auto-Refresh

- Gas prices update every 30 seconds
- Market data refreshes automatically
- Live data widgets in chat sidebar
- Manual refresh buttons available

## 🛡️ Safety Features

- Comprehensive risk analysis
- Real-time market monitoring
- AI-powered safety recommendations
- Multi-source data validation
- Error handling and fallbacks

## 🚀 Quick Start

1. **Start the server**:
   ```bash
   python defi_assistant_server.py
   ```

2. **Open your browser**:
   ```
   http://localhost:8080
   ```

3. **Try the features**:
   - Check gas prices
   - View market data
   - Chat with the AI assistant
   - Explore different pages

## 📱 Mobile Support

The interface is fully responsive and works great on mobile devices. All features are accessible on smartphones and tablets.

## 🔧 Development

To modify or extend the application:

1. **Market Data**: Edit `market_data.py` to add new data sources
2. **Templates**: Modify `templates.py` to change the UI
3. **Server Logic**: Update `defi_assistant_server.py` for new features
4. **Styling**: CSS is embedded in templates for easy customization

## 🐛 Troubleshooting

- **Port conflicts**: Change the port in `defi_assistant_server.py` or set `PORT` environment variable
- **API errors**: Check your `.env` file has valid API keys
- **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

## 📈 Performance

- Lightweight server implementation
- Efficient data caching
- Optimized API calls
- Fast page loads
- Smooth animations

## 🔮 Future Features

- Portfolio tracking and analysis
- Advanced risk scoring algorithms
- Cross-chain arbitrage detection
- DeFi protocol comparison tools
- Historical data analysis
- Alert system for price changes

---

Built with ❤️ for the DeFi community
