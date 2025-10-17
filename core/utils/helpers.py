"""
Utility functions for Safe DeFi Assistant
"""

import re
from typing import Optional

def validate_ethereum_address(address: str) -> bool:
    """Validate Ethereum address format"""
    pattern = r'^0x[a-fA-F0-9]{40}$'
    return bool(re.match(pattern, address))

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amount"""
    if currency == "USD":
        return f"${amount:,.2f}"
    return f"{amount:,.4f} {currency}"

def format_percentage(value: float) -> str:
    """Format percentage value"""
    return f"{value:.2f}%"

def truncate_address(address: str, start: int = 6, end: int = 4) -> str:
    """Truncate Ethereum address for display"""
    if len(address) <= start + end:
        return address
    return f"{address[:start]}...{address[-end:]}"

def safe_float(value: Optional[str], default: float = 0.0) -> float:
    """Safely convert string to float"""
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int(value: Optional[str], default: int = 0) -> int:
    """Safely convert string to int"""
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
