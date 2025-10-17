from opendeepsearch import OpenDeepSearchTool
from smolagents import CodeAgent, LiteLLMModel
import os
import gradio as gr
import requests
import json
from typing import Dict, Any

# Set up environment variables for OpenDeepSearch
os.environ["SERPER_API_KEY"] = "your-serper-api-key-here"  # Get from https://serper.dev
os.environ["OPENROUTER_API_KEY"] = "your-openrouter-api-key-here"  # Get from https://openrouter.ai
os.environ["JINA_API_KEY"] = "your-jina-api-key-here"  # Get from https://jina.ai

# You can also set these if you have them:
# os.environ["LITELLM_MODEL_ID"] = "openrouter/google/gemini-2.0-flash-001"
# os.environ["LITELLM_SEARCH_MODEL_ID"] = "openrouter/google/gemini-2.0-flash-001"

class GasPriceTool:
    """Tool to fetch current gas prices from various networks"""
    
    name = "get_gas_prices"
    description = "Get current gas prices for Ethereum and Polygon networks. Use this when users ask about gas fees, transaction costs, or network fees."
    
    def __call__(self, network: str = "ethereum") -> str:
        try:
            if network.lower() == "ethereum":
                response = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle")
                data = response.json()
                if data["status"] == "1":
                    result = {
                        "network": "ethereum",
                        "slow": f"{data['result']['SafeGasPrice']} Gwei",
                        "average": f"{data['result']['ProposeGasPrice']} Gwei",
                        "fast": f"{data['result']['FastGasPrice']} Gwei",
                        "usd_estimate": "$2-4 for simple swaps"
                    }
                    return json.dumps(result, indent=2)
            elif network.lower() == "polygon":
                response = requests.get("https://gasstation.polygon.technology/v2")
                data = response.json()
                result = {
                    "network": "polygon", 
                    "slow": f"{data['standard']['maxFee']} Gwei",
                    "average": f"{data['standard']['maxPriorityFee']} Gwei",
                    "fast": f"{data['fast']['maxFee']} Gwei",
                    "usd_estimate": "$0.01-0.05 for simple swaps"
                }
                return json.dumps(result, indent=2)
            else:
                return f"Unsupported network: {network}. Supported networks: ethereum, polygon"
        except Exception as e:
            return f"Error fetching gas prices: {str(e)}"

class RiskAssessmentTool:
    """Tool to assess risks for DeFi protocols"""
    
    name = "assess_protocol_risk"
    description = "Assess risks and best practices for DeFi protocols like Aave, Uniswap, Compound. Use this when users ask about safety, risks, or security of protocols."
    
    def __call__(self, protocol: str) -> str:
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
        
        protocol_lower = protocol.lower()
        if protocol_lower in risk_data:
            return json.dumps(risk_data[protocol_lower], indent=2)
        else:
            # Use OpenDeepSearch for unknown protocols
            search_tool = OpenDeepSearchTool(
                model_name="openrouter/google/gemini-2.0-flash-001",
                reranker="jina"
            )
            if not search_tool.is_initialized:
                search_tool.setup()
            
            search_query = f"risks security audit {protocol} DeFi protocol 2024"
            search_result = search_tool.forward(search_query)
            return f"Unknown protocol '{protocol}'. Search results:\n{search_result}"

class DeFiAnalysisTool:
    """Tool to analyze complete DeFi actions"""
    
    name = "analyze_defi_action" 
    description = "Analyze DeFi actions with gas costs and risk assessment. Use this when users want to analyze specific actions like staking, swapping, or lending."
    
    def __call__(self, action: str, protocol: str, amount: str = "") -> str:
        # Gas estimates for different actions
        gas_estimates = {
            "swap": {"ethereum": "$3-8", "polygon": "$0.02-0.1"},
            "stake": {"ethereum": "$5-15", "polygon": "$0.05-0.2"},
            "lend": {"ethereum": "$8-20", "polygon": "$0.1-0.3"},
            "borrow": {"ethereum": "$10-25", "polygon": "$0.15-0.4"},
            "provide_liquidity": {"ethereum": "$15-30", "polygon": "$0.2-0.5"}
        }
        
        # Detect action type
        action_lower = action.lower()
        if "swap" in action_lower:
            action_type = "swap"
        elif "stake" in action_lower:
            action_type = "stake" 
        elif "lend" in action_lower:
            action_type = "lend"
        elif "borrow" in action_lower:
            action_type = "borrow"
        elif "liquidity" in action_lower:
            action_type = "provide_liquidity"
        else:
            action_type = "swap"
        
        # Get risk assessment
        risk_tool = RiskAssessmentTool()
        risk_data = risk_tool(protocol)
        
        analysis = {
            "action": action,
            "protocol": protocol,
            "amount": amount,
            "gas_estimate_ethereum": gas_estimates[action_type]["ethereum"],
            "gas_estimate_polygon": gas_estimates[action_type]["polygon"],
            "recommendations": [
                "Check if the protocol has recent security audits",
                "Verify contract addresses from official sources",
                "Consider using testnet first to understand the process",
                "Monitor transaction gas fees before submitting",
                "Start with a small amount to test the process",
                "Use hardware wallets for large amounts"
            ],
            "risk_assessment": json.loads(risk_data) if risk_data.startswith('{') else risk_data
        }
        
        return json.dumps(analysis, indent=2)

def create_defi_assistant():
    """Create the Safe DeFi Assistant using OpenDeepSearch and SmolAgents"""
    
    # Initialize tools
    gas_tool = GasPriceTool()
    risk_tool = RiskAssessmentTool() 
    analysis_tool = DeFiAnalysisTool()
    
    # Initialize OpenDeepSearch tool for general queries
    search_tool = OpenDeepSearchTool(
        model_name="openrouter/google/gemini-2.0-flash-001",
        reranker="jina"
    )
    if not search_tool.is_initialized:
        search_tool.setup()
    
    # Initialize the model
    model = LiteLLMModel(
        model_id="openrouter/google/gemini-2.0-flash-001",
        temperature=0.1,
        api_base="https://openrouter.ai/api/v1"
    )
    
    # Create the agent with all tools
    agent = CodeAgent(
        tools=[gas_tool, risk_tool, analysis_tool, search_tool],
        model=model,
        name="safe_defi_assistant",
        description="An intelligent DeFi assistant that provides gas insights, risk assessments, and action analysis using OpenDeepSearch"
    )
    
    return agent

# Initialize the assistant
try:
    assistant = create_defi_assistant()
    print("✅ Safe DeFi Assistant initialized successfully with OpenDeepSearch!")
except Exception as e:
    print(f"❌ Failed to initialize assistant: {e}")
    assistant = None

def chat_with_assistant(message, history):
    """Chat function for Gradio interface"""
    if assistant is None:
        return "Assistant not available. Please check API keys and initialization."
    
    try:
        # System prompt to guide the assistant
        system_prompt = """
        You are a Safe DeFi Assistant powered by OpenDeepSearch. Your role is to help users navigate decentralized finance safely.

        Core Capabilities:
        1. Gas Fee Insights - Check current gas prices on Ethereum and Polygon
        2. Risk Assessment - Analyze risks for DeFi protocols (Aave, Uniswap, Compound, etc.)
        3. Action Analysis - Provide comprehensive analysis of DeFi actions

        Always:
        - Prioritize user safety and provide accurate information
        - Be transparent about risks and limitations
        - Suggest best practices for DeFi usage
        - Use the available tools to get current information

        When users ask about gas fees, use the gas price tool.
        When users ask about protocol safety, use the risk assessment tool.
        When users want to analyze specific actions, use the analysis tool.
        For other questions, use the search tool to find current information.
        """
        
        full_prompt = f"{system_prompt}\n\nUser: {message}"
        response = assistant.run(full_prompt)
        return response
    except Exception as e:
        return f"Error: {str(e)}"

# Create Gradio interface
def create_gradio_interface():
    with gr.Blocks(theme=gr.themes.Soft(), title="Safe DeFi Assistant") as demo:
        gr.Markdown("# 🛡️ Safe DeFi Assistant")
        gr.Markdown("Powered by OpenDeepSearch & Sentient AGI")
        gr.Markdown("### Get gas insights, risk assessments, and safe DeFi guidance")
        
        with gr.Row():
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(
                    label="DeFi Assistant Chat",
                    height=500,
                    show_copy_button=True,
                    avatar_images=("👤", "🛡️")
                )
                
        with gr.Row():
            with gr.Column(scale=4):
                msg = gr.Textbox(
                    label="Ask about gas fees, protocol risks, or analyze DeFi actions",
                    placeholder="e.g., 'What are current gas fees?', 'Is Aave safe?', 'Analyze staking 100 USDC on Compound'",
                    lines=2,
                    max_lines=4
                )
            with gr.Column(scale=1):
                send_btn = gr.Button("Send 📤", size="lg")
                clear_btn = gr.Button("Clear 🗑️", size="lg")
        
        # Example questions
        gr.Markdown("### 💡 Example Questions")
        gr.Examples(
            examples=[
                "What are the current gas prices on Ethereum?",
                "What risks should I know about before using Aave?",
                "Analyze providing liquidity on Uniswap V3",
                "How much would it cost to swap tokens on Polygon?",
                "Is Compound protocol safe for lending?",
                "What are the best practices for using DeFi safely?",
                "Compare risks between Aave and Compound",
                "Analyze borrowing 1000 USDC on Aave"
            ],
            inputs=msg,
            label="Click any example to try it!"
        )
        
        # Quick action buttons
        gr.Markdown("### ⚡ Quick Actions")
        with gr.Row():
            gas_btn = gr.Button("⛽ Check Gas Fees")
            risk_btn = gr.Button("🔍 Assess Protocol Risks")
            analyze_btn = gr.Button("📊 Analyze DeFi Action")
        
        def quick_gas(history):
            return "What are the current gas prices on Ethereum and Polygon?"
        
        def quick_risk(history):
            return "What are the main risks I should know about for popular DeFi protocols?"
        
        def quick_analyze(history):
            return "Can you analyze a typical DeFi action like staking or lending?"
        
        # Event handlers
        def respond(message, chat_history):
            if not message.strip():
                return "", chat_history
            bot_message = chat_with_assistant(message, chat_history)
            chat_history.append((message, bot_message))
            return "", chat_history
        
        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        send_btn.click(respond, [msg, chatbot], [msg, chatbot])
        clear_btn.click(lambda: [], None, chatbot)
        
        gas_btn.click(quick_gas, chatbot, msg)
        risk_btn.click(quick_risk, chatbot, msg) 
        analyze_btn.click(quick_analyze, chatbot, msg)
        
        return demo

if __name__ == "__main__":
    print("🚀 Starting Safe DeFi Assistant with OpenDeepSearch...")
    print("📋 Make sure you have set these environment variables:")
    print("   - SERPER_API_KEY (from https://serper.dev)")
    print("   - OPENROUTER_API_KEY (from https://openrouter.ai)") 
    print("   - JINA_API_KEY (from https://jina.ai)")
    print("\n🌐 The interface will open at http://localhost:7860")
    
    demo = create_gradio_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )