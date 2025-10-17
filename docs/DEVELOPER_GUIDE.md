# 🛠️ Safe DeFi Assistant - Developer Documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.14+
- Virtual environment (recommended)
- API keys for external services

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd OpenDeepSearch

# Create virtual environment
python3 -m venv opendeepsearch_env
source opendeepsearch_env/bin/activate  # On Windows: opendeepsearch_env\Scripts\activate

# Install dependencies
pip install -e .
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### Environment Setup
Create a `.env` file with your API keys:
```bash
# Core APIs
SERPER_API_KEY=your_serper_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
JINA_API_KEY=your_jina_api_key
LITELLM_API_KEY=your_litellm_api_key
LITELLM_MODEL_ID=openrouter/google/gemini-2.0-flash-001

# Blockchain Data APIs
ETHERSCAN_API_KEY=your_etherscan_api_key
MORALIS_API_KEY=your_moralis_api_key
ALCHEMY_API_KEY=your_alchemy_api_key
DEBANK_API_KEY=your_debank_api_key
```

### Running the Application
```bash
# Start the server
python defi_assistant_server.py

# Access the application
open http://127.0.0.1:8080
```

## 🏗️ Architecture Overview

### Project Structure
```
OpenDeepSearch/
├── defi_assistant_server.py      # Main server application
├── templates.py                  # HTML templates and UI components
├── market_data.py               # Market data integration services
├── portfolio_analyzer.py         # Portfolio analysis logic
├── mev_protection.py            # MEV protection and detection
├── sentient_adapter.py          # Sentient API compatibility
├── .env                         # Environment variables (not in git)
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

### Core Components

#### 1. Server (`defi_assistant_server.py`)
- **HTTP Server**: Custom HTTP server using Python's built-in modules
- **Route Handling**: RESTful API endpoints for all features
- **Error Handling**: Comprehensive error management and logging
- **CORS Support**: Cross-origin resource sharing for web clients

#### 2. Templates (`templates.py`)
- **HTML Templates**: Modular page templates for all features
- **CSS Styling**: Modern dark theme with responsive design
- **JavaScript**: Interactive UI components and API calls
- **Component System**: Reusable UI components

#### 3. Market Data (`market_data.py`)
- **Gas Price Monitor**: Multi-source gas price aggregation
- **TVL Tracker**: DeFi protocol TVL monitoring
- **Yield Detector**: Yield farming opportunity detection
- **Data Validation**: Cross-source verification and fallbacks

#### 4. Portfolio Analyzer (`portfolio_analyzer.py`)
- **Real-time Analysis**: Live portfolio data from Moralis API
- **Risk Scoring**: Comprehensive risk assessment (1-10 scale)
- **Recommendations**: Personalized optimization suggestions
- **Fallback Data**: Simulated data when APIs are unavailable

#### 5. MEV Protection (`mev_protection.py`)
- **Attack Detection**: Sandwich attack identification
- **Risk Assessment**: Transaction-level MEV risk analysis
- **Protection Methods**: Recommended protection strategies
- **Alert System**: Proactive notification system

#### 6. Sentient Adapter (`sentient_adapter.py`)
- **API Compatibility**: Full Sentient platform integration
- **Agent Metadata**: Proper agent configuration and capabilities
- **Query Processing**: Seamless query handling and responses
- **Error Handling**: Graceful degradation and fallbacks

## 🔌 API Endpoints

### Core Application Routes
```bash
GET  /                    # Landing page
GET  /chat               # AI Assistant interface
GET  /gas-prices         # Gas price monitoring
GET  /market-data        # Market data dashboard
GET  /portfolio          # Portfolio analysis
GET  /risk-analysis      # Risk analysis (coming soon)
GET  /yield-farming      # Yield farming (coming soon)
```

### Sentient Integration APIs
```bash
GET  /api/sentient/info           # Agent metadata
POST /api/sentient/query          # Query processing
```

### Advanced Feature APIs
```bash
GET  /api/gas-prices              # Gas price data
GET  /api/market-data             # Market data
GET  /api/tvl-data                # TVL data
GET  /api/yield-opportunities     # Yield opportunities
GET  /api/portfolio/analyze       # Portfolio analysis
GET  /api/mev/status              # MEV protection status
GET  /api/mev/alerts              # MEV alerts
POST /api/mev/check               # MEV risk check
POST /api/chat                    # Chat processing
```

## 🔧 Configuration

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `PORT` | Server port | No | 8080 |
| `SERPER_API_KEY` | Serper search API key | Yes | - |
| `OPENROUTER_API_KEY` | OpenRouter API key | Yes | - |
| `JINA_API_KEY` | Jina AI API key | Yes | - |
| `LITELLM_API_KEY` | LiteLLM API key | Yes | - |
| `LITELLM_MODEL_ID` | LiteLLM model ID | Yes | openrouter/google/gemini-2.0-flash-001 |
| `ETHERSCAN_API_KEY` | Etherscan API key | Yes | - |
| `MORALIS_API_KEY` | Moralis API key | No | - |
| `ALCHEMY_API_KEY` | Alchemy API key | No | - |
| `DEBANK_API_KEY` | DeBank API key | No | - |

### API Rate Limits
- **Etherscan**: 5 calls/second (free tier)
- **Moralis**: 100,000 requests/month (free tier)
- **DeFiLlama**: No rate limits (public API)
- **Serper**: 2,500 requests/month (free tier)

## 🧪 Testing

### Manual Testing
```bash
# Test core endpoints
curl http://127.0.0.1:8080/api/gas-prices
curl http://127.0.0.1:8080/api/market-data
curl "http://127.0.0.1:8080/api/portfolio/analyze?wallet=0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"

# Test Sentient integration
curl http://127.0.0.1:8080/api/sentient/info
curl -X POST http://127.0.0.1:8080/api/sentient/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are current gas prices?", "context": {}}'
```

### Automated Testing
```bash
# Run the test suite
python test_new_features.py
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Ensure virtual environment is activated
source opendeepsearch_env/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. API Key Issues
```bash
# Check .env file exists and has correct keys
cat .env

# Verify API keys are valid
curl -H "X-API-Key: $MORALIS_API_KEY" https://deep-index.moralis.io/api/v2.2/0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6/erc20
```

#### 3. Port Conflicts
```bash
# Kill existing processes
pkill -f "defi_assistant_server.py"

# Use different port
PORT=8081 python defi_assistant_server.py
```

#### 4. Playwright Issues
```bash
# Reinstall Playwright browsers
playwright install
```

## 📊 Performance Optimization

### Caching Strategy
- **API Responses**: 30-second cache for market data
- **Static Assets**: Browser caching for CSS/JS
- **Database Queries**: In-memory caching for frequent requests

### Rate Limiting
- **API Calls**: Respect external API rate limits
- **User Requests**: Implement request throttling
- **Error Handling**: Exponential backoff for failed requests

### Monitoring
- **Logging**: Comprehensive request/response logging
- **Error Tracking**: Detailed error reporting and debugging
- **Performance Metrics**: Response time monitoring

## 🔒 Security Considerations

### API Key Protection
- **Environment Variables**: Never commit API keys to git
- **Key Rotation**: Regular API key updates
- **Access Control**: Limit API key permissions

### Input Validation
- **Wallet Addresses**: Ethereum address format validation
- **Query Sanitization**: Prevent injection attacks
- **Rate Limiting**: Prevent abuse and DoS attacks

### Data Privacy
- **No Storage**: No persistent storage of user data
- **Temporary Processing**: Data processed in memory only
- **Secure Transmission**: HTTPS for all API calls

## 🚀 Deployment

### Local Development
```bash
# Development server with auto-reload
python defi_assistant_server.py
```

### Production Deployment
```bash
# Use production WSGI server
gunicorn -w 4 -b 0.0.0.0:8080 defi_assistant_server:app
```

### Docker Deployment
```dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "defi_assistant_server.py"]
```

## 📈 Scaling Considerations

### Horizontal Scaling
- **Load Balancing**: Multiple server instances
- **API Gateway**: Centralized API management
- **Database**: External database for persistent data

### Vertical Scaling
- **Resource Optimization**: Memory and CPU optimization
- **Caching**: Redis for distributed caching
- **CDN**: Content delivery network for static assets

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Standards
- **Python**: PEP 8 style guide
- **JavaScript**: ES6+ standards
- **CSS**: BEM methodology
- **Documentation**: Comprehensive docstrings

### Testing Requirements
- **Unit Tests**: Test individual components
- **Integration Tests**: Test API endpoints
- **End-to-End Tests**: Test complete user flows

---

## 📞 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: Project Wiki
- **Community**: Discord/Telegram

---

*Happy coding! 🚀*
