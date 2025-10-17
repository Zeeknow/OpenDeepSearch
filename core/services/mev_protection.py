"""
MEV Protection Module
Detects and warns about MEV attacks and sandwich attacks
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class MEVProtection:
    """MEV protection and sandwich attack detection"""
    
    def __init__(self):
        self.etherscan_key = "CMVH5IECZ2KGH3FMU51CJN4J9NNVHH144Z"
        self.flashbots_api = "https://protect.flashbots.net/v1/mev-protection"
        
    def check_mev_risk(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check for MEV risk in a transaction"""
        try:
            logger.info("Checking MEV risk for transaction")
            
            # Analyze transaction for MEV risk factors
            risk_analysis = self._analyze_transaction_risk(transaction_data)
            
            # Generate protection recommendations
            recommendations = self._generate_protection_recommendations(risk_analysis)
            
            return {
                'success': True,
                'data': {
                    'mev_risk_score': risk_analysis.get('risk_score', 5.0),
                    'risk_factors': risk_analysis.get('risk_factors', []),
                    'protection_methods': recommendations,
                    'timestamp': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"MEV protection check error: {e}")
            return {
                'success': False,
                'error': f"Failed to check MEV risk: {str(e)}"
            }
    
    def _analyze_transaction_risk(self, tx_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze transaction for MEV risk factors"""
        risk_factors = []
        risk_score = 0.0
        
        # Check transaction size
        value = float(tx_data.get('value', 0))
        if value > 10:  # Large transactions are more attractive to MEV
            risk_factors.append("Large transaction value - attractive to MEV bots")
            risk_score += 2.0
        
        # Check if it's a swap transaction
        if 'swap' in tx_data.get('function_name', '').lower():
            risk_factors.append("Swap transaction - high MEV risk")
            risk_score += 3.0
            
            # Check slippage tolerance
            slippage = tx_data.get('slippage_tolerance', 0.5)
            if slippage > 2.0:
                risk_factors.append(f"High slippage tolerance ({slippage}%) - vulnerable to sandwich attacks")
                risk_score += 2.0
        
        # Check if it's a DEX interaction
        dex_protocols = ['uniswap', 'sushiswap', 'curve', 'balancer', '1inch']
        if any(dex in tx_data.get('protocol', '').lower() for dex in dex_protocols):
            risk_factors.append("DEX interaction - potential MEV target")
            risk_score += 1.5
        
        # Check gas price
        gas_price = float(tx_data.get('gas_price', 20))
        if gas_price > 50:  # High gas prices indicate competition
            risk_factors.append(f"High gas price ({gas_price} Gwei) - indicates MEV competition")
            risk_score += 1.0
        
        # Check transaction timing
        current_hour = datetime.now().hour
        if 14 <= current_hour <= 18:  # Peak trading hours
            risk_factors.append("Peak trading hours - higher MEV activity")
            risk_score += 0.5
        
        return {
            'risk_score': min(risk_score, 10.0),
            'risk_factors': risk_factors
        }
    
    def _generate_protection_recommendations(self, risk_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate MEV protection recommendations"""
        recommendations = []
        risk_score = risk_analysis.get('risk_score', 5.0)
        
        if risk_score > 7:
            recommendations.append({
                'method': 'Private Mempool',
                'description': 'Use Flashbots Protect or similar private mempool',
                'priority': 'HIGH',
                'implementation': 'Route transaction through Flashbots Protect API'
            })
            
            recommendations.append({
                'method': 'Lower Gas Price',
                'description': 'Use lower gas price to avoid MEV competition',
                'priority': 'MEDIUM',
                'implementation': 'Set gas price 10-20% below current fast price'
            })
        
        if risk_score > 5:
            recommendations.append({
                'method': 'Reduce Slippage',
                'description': 'Lower slippage tolerance to reduce sandwich attack risk',
                'priority': 'MEDIUM',
                'implementation': 'Set slippage to 0.5-1% for stable pairs'
            })
            
            recommendations.append({
                'method': 'Split Transaction',
                'description': 'Split large transactions into smaller ones',
                'priority': 'MEDIUM',
                'implementation': 'Break transaction into 2-3 smaller transactions'
            })
        
        # Always recommend these
        recommendations.append({
            'method': 'Monitor Gas Prices',
            'description': 'Wait for lower gas prices during off-peak hours',
            'priority': 'LOW',
            'implementation': 'Execute during 6-10 AM UTC when gas is typically lower'
        })
        
        recommendations.append({
            'method': 'Use Limit Orders',
            'description': 'Use limit orders instead of market orders when possible',
            'priority': 'LOW',
            'implementation': 'Set specific price targets rather than market execution'
        })
        
        return recommendations
    
    def get_sandwich_attack_alerts(self, wallet_address: str) -> Dict[str, Any]:
        """Get alerts for potential sandwich attacks on a wallet"""
        try:
            # Simulate checking recent transactions for sandwich patterns
            # In production, you'd analyze actual blockchain data
            
            alerts = [
                {
                    'type': 'sandwich_detected',
                    'severity': 'HIGH',
                    'message': 'Potential sandwich attack detected on USDC/ETH swap',
                    'timestamp': datetime.now().isoformat(),
                    'tx_hash': '0x1234...5678',
                    'loss_estimate': '$45.30',
                    'recommendation': 'Use private mempool for future swaps'
                },
                {
                    'type': 'mev_risk_high',
                    'severity': 'MEDIUM',
                    'message': 'High MEV risk detected for pending transaction',
                    'timestamp': datetime.now().isoformat(),
                    'tx_hash': '0xabcd...efgh',
                    'loss_estimate': '$12.50',
                    'recommendation': 'Consider reducing gas price or using Flashbots Protect'
                }
            ]
            
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
            logger.error(f"Error getting sandwich attack alerts: {e}")
            return {
                'success': False,
                'error': f"Failed to get MEV alerts: {str(e)}"
            }
    
    def get_mev_protection_status(self) -> Dict[str, Any]:
        """Get current MEV protection status and recommendations"""
        try:
            # Simulate current MEV protection status
            status = {
                'network_mev_activity': 'HIGH',
                'average_mev_loss': '$23.45',
                'protection_methods': [
                    'Flashbots Protect (Recommended)',
                    'Private Mempool Services',
                    'MEV-Protected RPC Endpoints'
                ],
                'current_gas_conditions': 'Competitive - MEV bots active',
                'recommended_actions': [
                    'Use private mempool for transactions >$100',
                    'Avoid peak trading hours (2-6 PM UTC)',
                    'Consider batching multiple operations'
                ]
            }
            
            return {
                'success': True,
                'data': status,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting MEV protection status: {e}")
            return {
                'success': False,
                'error': f"Failed to get MEV protection status: {str(e)}"
            }

# Global instance
mev_protection = MEVProtection()
