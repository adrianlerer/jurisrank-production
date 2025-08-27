"""
JurisRank: Advanced Legal AI Platform
===================================== 

A revolutionary legal AI platform that democratizes access to jurisprudential
analysis through cutting-edge artificial intelligence.

Copyright (c) 2025 Ignacio Adrián Lerer

This package provides public API access to JurisRank's legal AI capabilities
through a Free Forever API, enabling developers worldwide to integrate
advanced legal intelligence into their applications.
"""

from ._version import __version__
from .api import JurisRankAPI
from .client import JurisRankClient
from .models import LegalDocument, AnalysisResult, AuthorityScore

# Public API exports
__all__ = [
    "__version__",
    "JurisRankAPI", 
    "JurisRankClient",
    "LegalDocument",
    "AnalysisResult", 
    "AuthorityScore"
]

# Package metadata
__author__ = "Ignacio Adrián Lerer"
__author_email__ = "contact@jurisrank.io"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2025 Ignacio Adrián Lerer"
__description__ = "Advanced Legal AI Platform for jurisprudential analysis"
__url__ = "https://jurisrank.io"

def get_version():
    """Get the current version of JurisRank."""
    return __version__

def get_api_info():
    """Get API information for JurisRank Free Forever API."""
    return {
        "version": __version__,
        "api_base_url": "https://api.jurisrank.io",
        "documentation": "https://docs.jurisrank.net", 
        "free_tier": "unlimited",
        "supported_languages": ["en", "es"],
        "supported_jurisdictions": ["global", "argentina", "usa", "eu"]
    }
