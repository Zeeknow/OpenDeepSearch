"""
Portfolio Risk Analysis Module
Analyzes DeFi positions and provides risk insights
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class PortfolioAnalyzer:
    """Analyzes DeFi portfolio positions and risks"""
    
    def __init__(self):
        self.etherscan_key = "CMVH5IECZ2KGH3FMU51CJN4J9NNVHH144Z"  # Using the same key
        self.debank_api = "https://openapi.debank.com/v1/user/total_balance"
        self.defillama_api = "https://api.llama.fi/protocols"
        
    def analyze_portfolio(self, wallet_address: str) -> Dict[str, Any]:
        """Analyze portfolio for risk factors"""
        try:
            logger.info(f"Analyzing portfolio for wallet: {wallet_address[:10]}...")
            
            # Get portfolio data from multiple sources
            portfolio_data = self._fetch_portfolio_data(wallet_address)
            
            # Analyze risks
            risk_analysis = self._analyze_risks(portfolio_data)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(portfolio_data, risk_analysis)
            
            return {
                'success': True,
                'data': {
                    'wallet_address': wallet_address,
                    'total_value': portfolio_data.get('total_value', 0),
                    'positions': portfolio_data.get('positions', []),
                    'risk_score': risk_analysis.get('overall_risk_score', 5.0),
                    'risk_factors': risk_analysis.get('risk_factors', []),
                    'liquidation_risks': risk_analysis.get('liquidation_risks', []),
                    'recommendations': recommendations,
                    'data_source': portfolio_data.get('data_source', 'unknown'),
                    'last_updated': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Portfolio analysis error: {e}")
            return {
                'success': False,
                'error': f"Failed to analyze portfolio: {str(e)}"
            }
    
    def _fetch_portfolio_data(self, wallet_address: str) -> Dict[str, Any]:
        """Fetch portfolio data from blockchain APIs"""
        try:
            logger.info(f"Starting portfolio data fetch for wallet: {wallet_address[:10]}...")
            # Try to fetch real data from Moralis API first
            real_data = self._fetch_moralis_data(wallet_address)
            if real_data:
                logger.info(f"Successfully got real data from Moralis for wallet: {wallet_address[:10]}...")
                return real_data
            
            # Fallback to simulated data for demo purposes
            logger.info(f"Using simulated data for wallet: {wallet_address[:10]}...")
            return self._get_simulated_portfolio_data(wallet_address)
            
        except Exception as e:
            logger.error(f"Error fetching portfolio data: {e}")
            return self._get_simulated_portfolio_data(wallet_address)
    
    def _fetch_moralis_data(self, wallet_address: str) -> Optional[Dict[str, Any]]:
        """Fetch real portfolio data from Moralis API"""
        try:
            # Check if Moralis API key is available
            moralis_key = os.getenv("MORALIS_API_KEY")
            if not moralis_key:
                logger.info("Moralis API key not found, using simulated data")
                return None
            
            logger.info(f"Attempting to fetch Moralis data for wallet: {wallet_address[:10]}...")
            
            # Moralis API endpoints for DeFi data
            base_url = "https://deep-index.moralis.io/api/v2.2"
            headers = {
                "X-API-Key": moralis_key,
                "Content-Type": "application/json"
            }
            
            # Fetch token balances
            balances_url = f"{base_url}/{wallet_address}/erc20"
            logger.info(f"Making request to: {balances_url}")
            balances_response = requests.get(balances_url, headers=headers, timeout=10)
            
            logger.info(f"Moralis API response status: {balances_response.status_code}")
            if balances_response.status_code == 200:
                balances_data = balances_response.json()
                
                # Process the real data
                positions = []
                total_value = 0
                
                # Moralis returns a list directly, not wrapped in 'result'
                tokens = balances_data if isinstance(balances_data, list) else balances_data.get('result', [])
                
                for token in tokens:
                    balance = float(token.get('balance', 0))
                    if balance > 0:
                        # Moralis doesn't always provide USD price, so we'll use a placeholder
                        # In a real implementation, you'd fetch prices from a separate API
                        usd_price = token.get('usd_price', 0)  # This will be 0 if not provided
                        token_value = float(usd_price) * balance if usd_price else 0
                        
                        # For tokens without USD price, we'll show the raw balance
                        if token_value > 0:
                            value_display = f"{token_value:.2f}"
                        else:
                            value_display = f"{balance:.4f} {token.get('symbol', 'tokens')}"
                        
                        total_value += token_value
                        
                        positions.append({
                            'protocol': 'Native',
                            'token': token.get('symbol', 'Unknown'),
                            'amount': f"{balance:.4f}",
                            'value_usd': value_display,
                            'position_type': 'hold',
                            'health_factor': None
                        })
                
                logger.info(f"Successfully fetched {len(positions)} positions from Moralis")
                return {
                    'total_value': total_value,
                    'positions': positions,
                    'wallet_address': wallet_address,
                    'data_source': 'moralis'
                }
            else:
                logger.warning(f"Moralis API returned status {balances_response.status_code}: {balances_response.text[:200]}")
                return None
            
        except Exception as e:
            logger.error(f"Moralis API error: {e}")
            return None
        
        return None
    
    def _get_simulated_portfolio_data(self, wallet_address: str) -> Dict[str, Any]:
        """Get simulated portfolio data for demo purposes"""
        positions = [
            {
                'protocol': 'Aave',
                'token': 'ETH',
                'amount': '2.5',
                'value_usd': '6250',
                'position_type': 'supply',
                'health_factor': 1.8
            },
            {
                'protocol': 'Aave',
                'token': 'USDC',
                'amount': '1000',
                'value_usd': '1000',
                'position_type': 'borrow',
                'health_factor': 1.8
            },
            {
                'protocol': 'Uniswap V3',
                'token': 'ETH/USDC',
                'amount': '1.0 ETH, 2500 USDC',
                'value_usd': '5000',
                'position_type': 'liquidity',
                'health_factor': None
            },
            {
                'protocol': 'Compound',
                'token': 'WBTC',
                'amount': '0.1',
                'value_usd': '3000',
                'position_type': 'supply',
                'health_factor': 2.1
            }
        ]
        
        total_value = sum(float(pos['value_usd']) for pos in positions)
        
        return {
            'total_value': total_value,
            'positions': positions,
            'wallet_address': wallet_address,
            'data_source': 'simulated'
        }
    
    def _analyze_risks(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze portfolio risks"""
        positions = portfolio_data.get('positions', [])
        risk_factors = []
        liquidation_risks = []
        
        # Analyze concentration risk
        total_value = portfolio_data.get('total_value', 1)
        eth_positions = [pos for pos in positions if 'ETH' in pos.get('token', '')]
        eth_value = sum(float(pos.get('value_usd', 0)) for pos in eth_positions)
        eth_concentration = (eth_value / total_value) * 100 if total_value > 0 else 0
        
        if eth_concentration > 60:
            risk_factors.append(f"High ETH concentration ({eth_concentration:.1f}%) - consider diversifying")
        
        # Analyze lending risks
        lending_positions = [pos for pos in positions if pos.get('position_type') in ['supply', 'borrow']]
        for pos in lending_positions:
            health_factor = pos.get('health_factor')
            if health_factor and health_factor < 2.0:
                risk_factors.append(f"Low health factor ({health_factor:.1f}) for {pos['protocol']} {pos['token']} position")
                
                if health_factor < 1.5:
                    liquidation_risks.append(f"High liquidation risk for {pos['protocol']} {pos['token']} - health factor {health_factor:.1f}")
        
        # Analyze liquidity risks
        lp_positions = [pos for pos in positions if pos.get('position_type') == 'liquidity']
        if lp_positions:
            risk_factors.append(f"{len(lp_positions)} liquidity positions - monitor for impermanent loss")
        
        # Calculate overall risk score (1-10, 10 being highest risk)
        risk_score = 5.0  # Base score
        
        if eth_concentration > 60:
            risk_score += 2.0
        if any(pos.get('health_factor', 10) < 2.0 for pos in lending_positions):
            risk_score += 2.0
        if len(lp_positions) > 2:
            risk_score += 1.0
        if len(positions) > 10:
            risk_score += 1.0  # Complexity risk
        
        risk_score = min(risk_score, 10.0)
        
        return {
            'overall_risk_score': risk_score,
            'risk_factors': risk_factors,
            'liquidation_risks': liquidation_risks
        }
    
    def _generate_recommendations(self, portfolio_data: Dict[str, Any], risk_analysis: Dict[str, Any]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        positions = portfolio_data.get('positions', [])
        risk_score = risk_analysis.get('overall_risk_score', 5.0)
        
        # General recommendations based on risk score
        if risk_score > 7:
            recommendations.append("⚠️ High risk portfolio - consider reducing exposure and diversifying")
        elif risk_score > 5:
            recommendations.append("⚡ Medium risk portfolio - monitor positions closely")
        else:
            recommendations.append("✅ Low risk portfolio - well diversified")
        
        # Specific recommendations
        eth_positions = [pos for pos in positions if 'ETH' in pos.get('token', '')]
        eth_value = sum(float(pos.get('value_usd', 0)) for pos in eth_positions)
        total_value = portfolio_data.get('total_value', 1)
        eth_concentration = (eth_value / total_value) * 100 if total_value > 0 else 0
        
        if eth_concentration > 60:
            recommendations.append(f"💡 Diversify away from ETH ({eth_concentration:.1f}% of portfolio)")
        
        # Lending recommendations
        lending_positions = [pos for pos in positions if pos.get('position_type') in ['supply', 'borrow']]
        low_health_positions = [pos for pos in lending_positions if pos.get('health_factor', 10) < 2.0]
        
        if low_health_positions:
            recommendations.append("🔒 Improve health factors on lending positions to reduce liquidation risk")
        
        # Liquidity recommendations
        lp_positions = [pos for pos in positions if pos.get('position_type') == 'liquidity']
        if lp_positions:
            recommendations.append("🌊 Monitor liquidity positions for impermanent loss and consider rebalancing")
        
        # General DeFi best practices
        recommendations.append("📊 Set up alerts for significant price movements")
        recommendations.append("🔍 Regularly review and rebalance your portfolio")
        recommendations.append("🛡️ Consider using multiple protocols to reduce single points of failure")
        
        return recommendations
    
    def get_liquidation_alerts(self, wallet_address: str) -> Dict[str, Any]:
        """Get liquidation risk alerts for a wallet"""
        try:
            portfolio_data = self._fetch_portfolio_data(wallet_address)
            risk_analysis = self._analyze_risks(portfolio_data)
            
            alerts = []
            positions = portfolio_data.get('positions', [])
            
            for pos in positions:
                health_factor = pos.get('health_factor')
                if health_factor and health_factor < 1.5:
                    alerts.append({
                        'protocol': pos['protocol'],
                        'token': pos['token'],
                        'health_factor': health_factor,
                        'risk_level': 'HIGH' if health_factor < 1.2 else 'MEDIUM',
                        'message': f"Liquidation risk in {pos['protocol']} {pos['token']} position"
                    })
            
            return {
                'success': True,
                'data': {
                    'wallet_address': wallet_address,
                    'alerts': alerts,
                    'total_alerts': len(alerts),
                    'last_checked': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting liquidation alerts: {e}")
            return {
                'success': False,
                'error': f"Failed to get liquidation alerts: {str(e)}"
            }

# Global instance
portfolio_analyzer = PortfolioAnalyzer()
