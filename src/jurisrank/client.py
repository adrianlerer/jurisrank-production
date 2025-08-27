"""
JurisRank Client (Backward Compatibility)
========================================

Alias for JurisRankAPI to maintain backward compatibility.
"""

from .api import JurisRankAPI

# Backward compatibility alias
JurisRankClient = JurisRankAPI

__all__ = ["JurisRankClient"]
