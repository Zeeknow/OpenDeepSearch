"""
Core data models for Safe DeFi Assistant
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime

@dataclass
class GasPriceData:
    """Gas price data model"""
    slow: int
    standard: int
    fast: int
    instant: int
    sources: List[str]
    timestamp: datetime

@dataclass
class ProtocolTVL:
    """Protocol TVL data model"""
    name: str
    tvl: float
    change_24h: float
    category: str
    chains: List[str]

@dataclass
class YieldOpportunity:
    """Yield farming opportunity model"""
    protocol: str
    token: str
    apy: float
    tvl: float
    risk_score: int
    category: str

@dataclass
class PortfolioPosition:
    """Portfolio position model"""
    protocol: str
    token: str
    amount: str
    value_usd: str
    position_type: str
    health_factor: Optional[float] = None

@dataclass
class PortfolioAnalysis:
    """Portfolio analysis result model"""
    wallet_address: str
    total_value: float
    positions: List[PortfolioPosition]
    risk_score: int
    risk_factors: List[str]
    liquidation_risks: List[str]
    recommendations: List[str]
    data_source: str
    timestamp: datetime

@dataclass
class MEVAlert:
    """MEV alert model"""
    timestamp: datetime
    alert_type: str
    details: str
    severity: str

@dataclass
class MEVRiskAssessment:
    """MEV risk assessment model"""
    risk_score: int
    risk_factors: List[str]
    protection_methods: List[str]
    timestamp: datetime

@dataclass
class SentientQuery:
    """Sentient query model"""
    query: str
    context: Dict[str, Any]
    timestamp: datetime

@dataclass
class SentientResponse:
    """Sentient response model"""
    response: str
    agent_id: str
    timestamp: datetime
    success: bool
