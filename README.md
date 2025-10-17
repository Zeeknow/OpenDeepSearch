# 🚀 Safe DeFi Assistant - Clean Architecture

## 📁 Project Structure

```
OpenDeepSearch/
├── main.py                          # Main entry point
├── apps/                            # Application layer
│   ├── web/                         # Web application
│   │   ├── defi_assistant_server.py # Main server
│   │   ├── templates.py             # HTML templates
│   │   ├── gradio_demo.py          # Gradio demo (legacy)
│   │   └── working_defi_assistant.py # Legacy implementation
│   └── api/                         # API layer
│       └── sentient_adapter.py      # Sentient API integration
├── core/                            # Core business logic
│   ├── services/                    # Business services
│   │   ├── market_data.py          # Market data services
│   │   ├── portfolio_analyzer.py   # Portfolio analysis
│   │   ├── mev_protection.py       # MEV protection
│   │   └── defi_assistant.py       # Core DeFi assistant
│   ├── models/                      # Data models
│   │   └── __init__.py             # Data model definitions
│   └── utils/                       # Utility functions
│       └── helpers.py              # Helper functions
├── infrastructure/                  # Infrastructure layer
│   ├── config/                      # Configuration
│   │   ├── settings.py             # Application settings
│   │   └── env_template.txt        # Environment template
│   └── logging/                     # Logging configuration
│       └── logger.py               # Logging setup
├── docs/                           # Documentation
│   ├── api/                        # API documentation
│   ├── guides/                     # User guides
│   └── architecture/               # Architecture docs
├── tests/                          # Test suite
│   ├── unit/                       # Unit tests
│   ├── integration/                # Integration tests
│   └── e2e/                        # End-to-end tests
├── src/                            # Original OpenDeepSearch source
├── assets/                         # Static assets
├── evals/                          # Evaluation scripts
└── requirements.txt                # Dependencies
```

## 🏗️ Clean Architecture Principles

### **Layers**

#### **1. Apps Layer** (`apps/`)
- **Web Application**: HTTP server, templates, UI components
- **API Layer**: External API integrations (Sentient)
- **Presentation**: User interface and API endpoints

#### **2. Core Layer** (`core/`)
- **Services**: Business logic and domain services
- **Models**: Data models and domain entities
- **Utils**: Pure utility functions

#### **3. Infrastructure Layer** (`infrastructure/`)
- **Configuration**: Environment variables and settings
- **Logging**: Application logging setup
- **External Dependencies**: Database, external APIs

### **Dependencies Flow**
```
Apps → Core → Infrastructure
```

- **Apps** depend on **Core** and **Infrastructure**
- **Core** depends only on **Infrastructure**
- **Infrastructure** has no dependencies on other layers

## 🚀 Quick Start

### **Installation**
```bash
# Clone repository
git clone <repository-url>
cd OpenDeepSearch

# Create virtual environment
python3 -m venv opendeepsearch_env
source opendeepsearch_env/bin/activate

# Install dependencies
pip install -e .
pip install -r requirements.txt
```

### **Configuration**
```bash
# Copy environment template
cp infrastructure/config/env_template.txt .env

# Edit .env with your API keys
nano .env
```

### **Running**
```bash
# Start the application
python main.py

# Or run directly
python apps/web/defi_assistant_server.py
```

## 🔧 Development

### **Adding New Features**

#### **1. Core Services**
```python
# core/services/new_service.py
from core.models import YourModel
from infrastructure.config.settings import config

class NewService:
    def __init__(self):
        self.config = config
    
    def process(self, data: YourModel) -> YourModel:
        # Business logic here
        pass
```

#### **2. API Endpoints**
```python
# apps/web/defi_assistant_server.py
def handle_new_api(self):
    """Handle new API endpoint"""
    try:
        service = NewService()
        result = service.process(data)
        self.send_json_response({"success": True, "data": result})
    except Exception as e:
        self.send_json_response({"success": False, "error": str(e)})
```

#### **3. Data Models**
```python
# core/models/__init__.py
@dataclass
class NewModel:
    field1: str
    field2: int
    timestamp: datetime
```

### **Testing**
```bash
# Run unit tests
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/

# Run all tests
python -m pytest tests/
```

## 📊 Architecture Benefits

### **✅ Separation of Concerns**
- **Business Logic**: Isolated in core services
- **Presentation**: Separated in apps layer
- **Infrastructure**: External concerns isolated

### **✅ Testability**
- **Unit Tests**: Core services can be tested in isolation
- **Integration Tests**: API endpoints can be tested
- **Mocking**: Easy to mock infrastructure dependencies

### **✅ Maintainability**
- **Clear Structure**: Easy to find and modify code
- **Dependency Management**: Clear dependency flow
- **Modularity**: Components can be modified independently

### **✅ Scalability**
- **Horizontal Scaling**: Services can be extracted to microservices
- **Vertical Scaling**: Components can be optimized independently
- **Team Scaling**: Different teams can work on different layers

## 🔒 Security & Best Practices

### **Configuration Management**
- **Environment Variables**: All secrets in `.env` file
- **Validation**: Required keys validation
- **Default Values**: Sensible defaults for optional settings

### **Error Handling**
- **Graceful Degradation**: Fallbacks when services fail
- **Logging**: Comprehensive error logging
- **User Feedback**: Clear error messages to users

### **Code Quality**
- **Type Hints**: Full type annotation support
- **Documentation**: Comprehensive docstrings
- **Linting**: Code quality enforcement

## 📈 Future Enhancements

### **Planned Improvements**
- **Database Layer**: Persistent data storage
- **Caching Layer**: Redis for performance
- **Message Queue**: Async processing
- **Monitoring**: Application metrics and health checks

### **Microservices Migration**
- **Service Extraction**: Extract services to separate applications
- **API Gateway**: Centralized API management
- **Container Orchestration**: Docker and Kubernetes support

---

## 📞 Support

- **Documentation**: `docs/` directory
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

---

*Built with Clean Architecture principles for maintainability and scalability* 🚀
