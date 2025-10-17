"""
Sentient Agent API Adapter for DeFi Assistant
Compatible with Sentient Chat ecosystem
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SentientDeFiAgent:
    """Sentient-compatible DeFi Safety Assistant"""
    
    def __init__(self):
        self.agent_id = "defi-safety-assistant"
        self.name = "Safe DeFi Assistant"
        self.description = "Your trusted DeFi safety companion for gas optimization, risk assessment, and market analysis"
        self.capabilities = [
            "gas-optimization",
            "risk-assessment", 
            "market-analysis",
            "portfolio-analysis",
            "liquidation-monitoring",
            "mev-protection",
            "yield-farming-insights"
        ]
        self.version = "1.0.0"
        
    async def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main entry point for Sentient Chat integration
        Processes user queries and returns structured responses
        """
        try:
            logger.info(f"Processing Sentient query: {query}")
            
            # Determine query type and route accordingly
            query_type = self._classify_query(query)
            
            if query_type == "gas_prices":
                return await self._handle_gas_query(query, context)
            elif query_type == "portfolio_analysis":
                return await self._handle_portfolio_query(query, context)
            elif query_type == "risk_assessment":
                return await self._handle_risk_query(query, context)
            elif query_type == "yield_farming":
                return await self._handle_yield_query(query, context)
            elif query_type == "market_data":
                return await self._handle_market_query(query, context)
            else:
                return await self._handle_general_query(query, context)
                
        except Exception as e:
            logger.error(f"Error processing Sentient query: {e}")
            return self._create_error_response(str(e))
    
    def _classify_query(self, query: str) -> str:
        """Classify the type of DeFi query"""
        query_lower = query.lower()
        
        gas_keywords = ["gas", "gwei", "transaction fee", "network fee", "eth fee"]
        portfolio_keywords = ["portfolio", "positions", "holdings", "balance", "wallet"]
        risk_keywords = ["risk", "safe", "dangerous", "secure", "audit", "vulnerability"]
        yield_keywords = ["yield", "farming", "staking", "apy", "reward", "liquidity"]
        market_keywords = ["price", "market", "tvl", "volume", "trend", "analysis"]
        
        if any(keyword in query_lower for keyword in gas_keywords):
            return "gas_prices"
        elif any(keyword in query_lower for keyword in portfolio_keywords):
            return "portfolio_analysis"
        elif any(keyword in query_lower for keyword in risk_keywords):
            return "risk_assessment"
        elif any(keyword in query_lower for keyword in yield_keywords):
            return "yield_farming"
        elif any(keyword in query_lower for keyword in market_keywords):
            return "market_data"
        else:
            return "general"
    
    async def _handle_gas_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle gas price and optimization queries"""
        # Import here to avoid circular imports
        from market_data import GasPriceMonitor
        
        try:
            gas_monitor = GasPriceMonitor()
            gas_data = gas_monitor.get_gas_prices()
            
            if gas_data and gas_data.get('success'):
                eth_gas = gas_data['data']['ethereum']
                
                response_text = f"""⛽ **Current Ethereum Gas Prices**
                
**Gas Price Recommendations:**
• **Slow**: {eth_gas['slow']} Gwei (~{gas_data['data'].get('slow_usd', 'N/A')} USD)
• **Standard**: {eth_gas['standard']} Gwei (~{gas_data['data'].get('standard_usd', 'N/A')} USD)  
• **Fast**: {eth_gas['fast']} Gwei (~{gas_data['data'].get('fast_usd', 'N/A')} USD)
• **Instant**: {eth_gas['instant']} Gwei (~{gas_data['data'].get('instant_usd', 'N/A')} USD)

**Network Status**: {gas_data['data'].get('network_status', 'Normal')}
**Last Updated**: {datetime.now().strftime('%H:%M UTC')}

**💡 Pro Tips:**
• Use Standard speed for most transactions
• Wait for off-peak hours (6-10 AM UTC) for lower fees
• Consider Layer 2 solutions (Polygon, Arbitrum) for savings
• Monitor gas trends before large transactions"""
                
                return self._create_success_response(
                    response_text,
                    data=gas_data,
                    action_type="gas_analysis"
                )
            else:
                return self._create_error_response("Unable to fetch current gas prices")
                
        except Exception as e:
            logger.error(f"Error in gas query handling: {e}")
            return self._create_error_response("Gas price service temporarily unavailable")
    
    async def _handle_portfolio_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle portfolio analysis queries"""
        try:
            # Extract wallet address from query or context
            wallet_address = self._extract_wallet_address(query, context)
            
            if not wallet_address:
                return self._create_error_response(
                    "Please provide a wallet address for portfolio analysis. "
                    "Example: 'Analyze my portfolio: 0x1234...'"
                )
            
            # Simulate portfolio analysis (in real implementation, connect to blockchain APIs)
            portfolio_data = await self._analyze_portfolio(wallet_address)
            
            response_text = f"""📊 **Portfolio Risk Analysis**
            
**Wallet**: `{wallet_address[:10]}...{wallet_address[-6:]}`
**Total Value**: ${portfolio_data.get('total_value', 'N/A')}
**Risk Score**: {portfolio_data.get('risk_score', 'N/A')}/10

**🔍 Risk Factors:**
{self._format_risk_factors(portfolio_data.get('risk_factors', []))}

**⚠️ Liquidation Risk:**
{self._format_liquidation_risks(portfolio_data.get('liquidation_risks', []))}

**💡 Recommendations:**
{self._format_recommendations(portfolio_data.get('recommendations', []))}"""
            
            return self._create_success_response(
                response_text,
                data=portfolio_data,
                action_type="portfolio_analysis"
            )
            
        except Exception as e:
            logger.error(f"Error in portfolio analysis: {e}")
            return self._create_error_response("Portfolio analysis service unavailable")
    
    async def _handle_risk_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle risk assessment queries"""
        try:
            # Extract protocol or token from query
            protocol = self._extract_protocol_name(query)
            
            if not protocol:
                return self._create_error_response(
                    "Please specify a protocol or token for risk assessment. "
                    "Example: 'Is Uniswap safe?' or 'Assess Aave risks'"
                )
            
            risk_data = await self._assess_protocol_risk(protocol)
            
            response_text = f"""🛡️ **Risk Assessment: {protocol.upper()}**

**Overall Risk Score**: {risk_data.get('risk_score', 'N/A')}/10
**Security Rating**: {risk_data.get('security_rating', 'N/A')}

**🔒 Security Analysis:**
{self._format_security_analysis(risk_data.get('security_analysis', {}))}

**⚠️ Risk Factors:**
{self._format_risk_factors(risk_data.get('risk_factors', []))}

**📋 Audit Status:**
{self._format_audit_status(risk_data.get('audit_status', []))}

**💡 Safety Recommendations:**
{self._format_recommendations(risk_data.get('recommendations', []))}"""
            
            return self._create_success_response(
                response_text,
                data=risk_data,
                action_type="risk_assessment"
            )
            
        except Exception as e:
            logger.error(f"Error in risk assessment: {e}")
            return self._create_error_response("Risk assessment service unavailable")
    
    async def _handle_yield_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle yield farming queries"""
        try:
            from market_data import YieldFarmingDetector
            
            yield_detector = YieldFarmingDetector()
            yield_data = yield_detector.get_yield_opportunities()
            
            if yield_data and yield_data.get('success'):
                opportunities = yield_data['data'].get('top_yields', [])[:5]
                
                response_text = f"""🌾 **Top Yield Farming Opportunities**

**Current Best APYs:**
{self._format_yield_opportunities(opportunities)}

**💡 Yield Farming Tips:**
• Always research protocol security before investing
• Consider impermanent loss risks in AMM pools
• Diversify across multiple protocols
• Monitor gas costs vs. expected returns
• Set up alerts for significant APY changes"""
                
                return self._create_success_response(
                    response_text,
                    data=yield_data,
                    action_type="yield_analysis"
                )
            else:
                return self._create_error_response("Unable to fetch yield opportunities")
                
        except Exception as e:
            logger.error(f"Error in yield farming analysis: {e}")
            return self._create_error_response("Yield farming data unavailable")
    
    async def _handle_market_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle market data queries"""
        try:
            from market_data import DeFiTVLTracker
            
            tvl_tracker = DeFiTVLTracker()
            tvl_data = tvl_tracker.get_protocol_tvl()
            
            if tvl_data and tvl_data.get('success'):
                protocols = tvl_data['data'].get('protocols', [])[:5]
                
                response_text = f"""📈 **DeFi Market Overview**

**Top Protocols by TVL:**
{self._format_tvl_data(protocols)}

**Market Insights:**
• Total DeFi TVL: ${tvl_data['data'].get('total_tvl', 'N/A'):,}
• Market Trend: {tvl_data['data'].get('trend', 'N/A')}
• Dominant Sectors: {', '.join(tvl_data['data'].get('top_sectors', ['N/A']))}"""
                
                return self._create_success_response(
                    response_text,
                    data=tvl_data,
                    action_type="market_analysis"
                )
            else:
                return self._create_error_response("Unable to fetch market data")
                
        except Exception as e:
            logger.error(f"Error in market analysis: {e}")
            return self._create_error_response("Market data service unavailable")
    
    async def _handle_general_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle general DeFi queries using OpenDeepSearch"""
        try:
            # Import here to avoid circular imports
            from opendeepsearch.ods_tool import OpenDeepSearchTool
            
            search_tool = OpenDeepSearchTool()
            if not search_tool.is_initialized:
                search_tool.setup()
            
            # Enhance query with DeFi context
            enhanced_query = f"""You are a DeFi safety assistant. Please provide helpful, accurate information about:
{query}

Focus on:
- Safety considerations and best practices
- Current market conditions and data
- Practical recommendations for DeFi users
- Risk assessment and mitigation strategies"""
            
            response = await search_tool.ask(enhanced_query)
            
            return self._create_success_response(
                response,
                action_type="general_analysis"
            )
            
        except Exception as e:
            logger.error(f"Error in general query handling: {e}")
            return self._create_error_response("Unable to process your DeFi query")
    
    # Helper methods for data formatting and processing
    def _extract_wallet_address(self, query: str, context: Dict[str, Any] = None) -> Optional[str]:
        """Extract wallet address from query or context"""
        import re
        
        # Look for Ethereum address pattern
        eth_pattern = r'0x[a-fA-F0-9]{40}'
        matches = re.findall(eth_pattern, query)
        
        if matches:
            return matches[0]
        
        # Check context for wallet address
        if context and 'wallet_address' in context:
            return context['wallet_address']
        
        return None
    
    def _extract_protocol_name(self, query: str) -> Optional[str]:
        """Extract protocol name from query"""
        query_lower = query.lower()
        
        protocols = ['uniswap', 'aave', 'compound', 'curve', 'maker', 'convex', 'yearn', 'sushi', 'balancer']
        
        for protocol in protocols:
            if protocol in query_lower:
                return protocol
        
        return None
    
    async def _analyze_portfolio(self, wallet_address: str) -> Dict[str, Any]:
        """Analyze portfolio risk (simulated - in real implementation, connect to blockchain APIs)"""
        # This is a simulation - in production, you'd connect to blockchain APIs
        return {
            'total_value': '45,230',
            'risk_score': '6.5',
            'risk_factors': [
                'High concentration in single token (60% ETH)',
                'Active lending positions with 75% collateralization',
                'Multiple yield farming positions'
            ],
            'liquidation_risks': [
                'Aave ETH position at 75% LTV - monitor closely',
                'Compound USDC borrowing approaching limit'
            ],
            'recommendations': [
                'Diversify holdings across multiple assets',
                'Consider reducing LTV ratios for safety',
                'Set up liquidation alerts for active positions'
            ]
        }
    
    async def _assess_protocol_risk(self, protocol: str) -> Dict[str, Any]:
        """Assess protocol risk (simulated)"""
        # This is a simulation - in production, you'd query security databases
        risk_data = {
            'uniswap': {
                'risk_score': '3',
                'security_rating': 'High',
                'security_analysis': {
                    'audits': 'Multiple comprehensive audits',
                    'bug_bounty': 'Active program with $2M+ rewards',
                    'timelock': '24-hour governance timelock'
                },
                'risk_factors': ['Smart contract risk', 'Market volatility'],
                'audit_status': ['Trail of Bits (2023)', 'ConsenSys Diligence (2022)'],
                'recommendations': ['Generally safe for basic swaps', 'Be cautious with new pools']
            },
            'aave': {
                'risk_score': '4',
                'security_rating': 'High',
                'security_analysis': {
                    'audits': 'Regular security audits',
                    'bug_bounty': 'Active program',
                    'insurance': 'Coverage through Nexus Mutual'
                },
                'risk_factors': ['Liquidation risk', 'Oracle manipulation'],
                'audit_status': ['OpenZeppelin (2023)', 'ConsenSys (2022)'],
                'recommendations': ['Safe for established tokens', 'Monitor liquidation thresholds']
            }
        }
        
        return risk_data.get(protocol.lower(), {
            'risk_score': '5',
            'security_rating': 'Medium',
            'security_analysis': {'audits': 'Limited audit history', 'bug_bounty': 'None'},
            'risk_factors': ['Unknown security status'],
            'audit_status': ['No recent audits'],
            'recommendations': ['Research thoroughly before using', 'Start with small amounts']
        })
    
    def _format_risk_factors(self, factors: List[str]) -> str:
        """Format risk factors for display"""
        if not factors:
            return "• No significant risk factors identified"
        
        return '\n'.join([f"• {factor}" for factor in factors])
    
    def _format_liquidation_risks(self, risks: List[str]) -> str:
        """Format liquidation risks for display"""
        if not risks:
            return "• No immediate liquidation risks"
        
        return '\n'.join([f"• {risk}" for risk in risks])
    
    def _format_recommendations(self, recommendations: List[str]) -> str:
        """Format recommendations for display"""
        if not recommendations:
            return "• Continue monitoring your positions"
        
        return '\n'.join([f"• {rec}" for rec in recommendations])
    
    def _format_security_analysis(self, analysis: Dict[str, str]) -> str:
        """Format security analysis for display"""
        if not analysis:
            return "• Limited security information available"
        
        return '\n'.join([f"• **{key}**: {value}" for key, value in analysis.items()])
    
    def _format_audit_status(self, audits: List[str]) -> str:
        """Format audit status for display"""
        if not audits:
            return "• No recent audits available"
        
        return '\n'.join([f"• {audit}" for audit in audits])
    
    def _format_yield_opportunities(self, opportunities: List[Dict]) -> str:
        """Format yield opportunities for display"""
        if not opportunities:
            return "• No current opportunities available"
        
        formatted = []
        for opp in opportunities:
            formatted.append(f"• **{opp.get('protocol', 'Unknown')}**: {opp.get('apy', 'N/A')}% APY")
        
        return '\n'.join(formatted)
    
    def _format_tvl_data(self, protocols: List[Dict]) -> str:
        """Format TVL data for display"""
        if not protocols:
            return "• No protocol data available"
        
        formatted = []
        for protocol in protocols:
            tvl = protocol.get('tvl', 0)
            formatted.append(f"• **{protocol.get('name', 'Unknown')}**: ${tvl:,.0f}M")
        
        return '\n'.join(formatted)
    
    def _create_success_response(self, message: str, data: Dict[str, Any] = None, action_type: str = None) -> Dict[str, Any]:
        """Create standardized success response for Sentient"""
        return {
            'success': True,
            'message': message,
            'data': data or {},
            'action_type': action_type,
            'timestamp': datetime.now().isoformat(),
            'agent_id': self.agent_id,
            'agent_name': self.name
        }
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create standardized error response for Sentient"""
        return {
            'success': False,
            'error': error_message,
            'timestamp': datetime.now().isoformat(),
            'agent_id': self.agent_id,
            'agent_name': self.name
        }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent metadata for Sentient registration"""
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'description': self.description,
            'capabilities': self.capabilities,
            'version': self.version,
            'endpoints': {
                'query': '/api/sentient/query',
                'info': '/api/sentient/info'
            }
        }

# Example usage and testing
async def test_sentient_adapter():
    """Test the Sentient adapter functionality"""
    agent = SentientDeFiAgent()
    
    # Test queries
    test_queries = [
        "What are current gas prices?",
        "Analyze my portfolio: 0x1234567890123456789012345678901234567890",
        "Is Uniswap safe to use?",
        "Show me yield farming opportunities",
        "What's the current DeFi market status?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing query: {query}")
        response = await agent.process_query(query)
        print(f"✅ Response: {response['success']}")
        if response['success']:
            print(f"📝 Message: {response['message'][:200]}...")
        else:
            print(f"❌ Error: {response['error']}")

if __name__ == "__main__":
    asyncio.run(test_sentient_adapter())
