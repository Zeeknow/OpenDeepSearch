#!/usr/bin/env python3
"""
Market Data Services for DeFi Assistant
Real-time gas prices, TVL tracking, and yield farming detection
"""

import os
import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class GasPriceMonitor:
    """Real-time gas price monitoring with multiple sources"""
    
    def __init__(self):
        self.sources = {
            'etherscan': 'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={}',
            'gasnow': 'https://www.gasnow.org/api/v3/gas/price',
            'blocknative': 'https://api.blocknative.com/gasprices/blockprices'
        }
        self.etherscan_key = os.getenv("ETHERSCAN_API_KEY")
    
    def get_gas_prices(self) -> Dict:
        """Get current gas prices from multiple sources"""
        gas_data = {
            'ethereum': {'slow': 0, 'standard': 0, 'fast': 0, 'instant': 0},
            'polygon': {'slow': 0, 'standard': 0, 'fast': 0},
            'arbitrum': {'slow': 0, 'standard': 0, 'fast': 0},
            'last_updated': datetime.now().isoformat(),
            'sources': []
        }
        
        try:
            # Ethereum gas prices from Etherscan
            if self.etherscan_key:
                url = self.sources['etherscan'].format(self.etherscan_key)
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == '1':
                        result = data.get('result', {})
                        gas_data['ethereum'] = {
                            'slow': int(result.get('SafeGasPrice', 0)),
                            'standard': int(result.get('ProposeGasPrice', 0)),
                            'fast': int(result.get('FastGasPrice', 0)),
                            'instant': int(result.get('FastGasPrice', 0)) * 1.2
                        }
                        gas_data['sources'].append('etherscan')
            
            # GasNow API (backup)
            try:
                response = requests.get(self.sources['gasnow'], timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == 200:
                        prices = data.get('data', {})
                        gas_data['ethereum'].update({
                            'slow': prices.get('slow', 0) // 1000000000,  # Convert wei to gwei
                            'standard': prices.get('standard', 0) // 1000000000,
                            'fast': prices.get('fast', 0) // 1000000000,
                            'instant': prices.get('rapid', 0) // 1000000000
                        })
                        if 'gasnow' not in gas_data['sources']:
                            gas_data['sources'].append('gasnow')
            except:
                pass
                
        except Exception as e:
            logger.error(f"Error fetching gas prices: {e}")
        
        return gas_data

class DeFiTVLTracker:
    """DeFi protocol TVL tracking and trends"""
    
    def __init__(self):
        self.defillama_api = "https://api.llama.fi/protocols"
        self.protocols = ['aave', 'compound', 'uniswap', 'curve', 'maker', 'convex']
    
    def get_protocol_tvl(self) -> Dict:
        """Get TVL data for major DeFi protocols"""
        tvl_data = {
            'protocols': {},
            'total_tvl': 0,
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            response = requests.get(self.defillama_api, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                for protocol in data:
                    if protocol.get('name', '').lower() in self.protocols:
                        protocol_name = protocol.get('name', '').lower()
                        tvl_data['protocols'][protocol_name] = {
                            'name': protocol.get('name', ''),
                            'tvl': protocol.get('tvl', 0),
                            'change_1d': protocol.get('change_1d', 0),
                            'change_7d': protocol.get('change_7d', 0),
                            'chains': protocol.get('chains', [])
                        }
                        tvl_data['total_tvl'] += protocol.get('tvl', 0)
                        
        except Exception as e:
            logger.error(f"Error fetching TVL data: {e}")
        
        return tvl_data

class YieldFarmingDetector:
    """Yield farming opportunity detection"""
    
    def __init__(self):
        self.apy_sources = {
            'defillama': 'https://yields.llama.fi/pools',
            'coindix': 'https://api.coindix.com/api/v1/pools'
        }
    
    def get_yield_opportunities(self) -> Dict:
        """Get current yield farming opportunities"""
        yield_data = {
            'opportunities': [],
            'top_yields': [],
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            # DeFiLlama yields API
            response = requests.get(self.apy_sources['defillama'], timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Filter for high-yield opportunities
                high_yield_pools = [
                    pool for pool in data.get('data', [])
                    if pool.get('apy', 0) > 10 and pool.get('tvlUsd', 0) > 1000000
                ]
                
                # Sort by APY and take top 10
                high_yield_pools.sort(key=lambda x: x.get('apy', 0), reverse=True)
                
                for pool in high_yield_pools[:10]:
                    yield_data['opportunities'].append({
                        'protocol': pool.get('project', ''),
                        'chain': pool.get('chain', ''),
                        'apy': round(pool.get('apy', 0), 2),
                        'tvl': pool.get('tvlUsd', 0),
                        'tokens': pool.get('symbol', ''),
                        'pool': pool.get('pool', '')
                    })
                
                yield_data['top_yields'] = yield_data['opportunities'][:5]
                
        except Exception as e:
            logger.error(f"Error fetching yield opportunities: {e}")
        
        return yield_data

# Initialize market data services
gas_monitor = GasPriceMonitor()
tvl_tracker = DeFiTVLTracker()
yield_detector = YieldFarmingDetector()
