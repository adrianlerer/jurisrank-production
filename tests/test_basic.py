"""
Basic tests for JurisRank public API
==================================

Run with: python -m pytest tests/
"""

import pytest
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from jurisrank import JurisRankAPI, get_version, get_api_info
from jurisrank.models import LegalDocument, AnalysisResult, AuthorityScore

class TestJurisRankAPI:
    """Test suite for JurisRank API client."""

    def test_api_client_initialization(self):
        """Test API client can be initialized."""
        client = JurisRankAPI(api_key="test_key")
        assert client.api_key == "test_key"
        assert client.base_url == "https://api.jurisrank.io"

    def test_api_client_custom_url(self):
        """Test API client with custom base URL."""
        custom_url = "https://custom.api.example.com"
        client = JurisRankAPI(base_url=custom_url)
        assert client.base_url == custom_url

    def test_analyze_document(self):
        """Test document analysis method."""
        client = JurisRankAPI()
        result = client.analyze_document("test_document.pdf")

        assert isinstance(result, AnalysisResult)
        assert result.document_id == "sample"
        assert 0 <= result.authority_score <= 100
        assert 0 <= result.confidence <= 1

    def test_search_jurisprudence(self):
        """Test jurisprudence search method."""
        client = JurisRankAPI()
        results = client.search_jurisprudence("contract law")

        assert isinstance(results, list)
        assert len(results) > 0
        assert isinstance(results[0], LegalDocument)

    def test_get_authority_score(self):
        """Test authority score method."""
        client = JurisRankAPI()
        score = client.get_authority_score("Supreme Court")

        assert isinstance(score, float)
        assert 0 <= score <= 100

class TestModels:
    """Test suite for JurisRank data models."""

    def test_legal_document_model(self):
        """Test LegalDocument model validation."""
        doc = LegalDocument(
            id="test_123",
            title="Test Case",
            court="Test Court", 
            date="2024-01-01",
            authority_score=85.5
        )

        assert doc.id == "test_123"
        assert doc.authority_score == 85.5

    def test_legal_document_invalid_score(self):
        """Test LegalDocument model with invalid authority score."""
        with pytest.raises(ValueError):
            LegalDocument(
                id="test_123",
                title="Test Case",
                court="Test Court",
                date="2024-01-01", 
                authority_score=150  # Invalid: > 100
            )

    def test_analysis_result_model(self):
        """Test AnalysisResult model."""
        result = AnalysisResult(
            document_id="doc_123",
            authority_score=88.5,
            confidence=0.95,
            analysis_summary="Test analysis"
        )

        assert result.document_id == "doc_123"
        assert result.confidence == 0.95

class TestUtilities:
    """Test suite for utility functions."""

    def test_get_version(self):
        """Test version information."""
        version = get_version()
        assert isinstance(version, str)
        assert len(version) > 0

    def test_get_api_info(self):
        """Test API information."""
        info = get_api_info()
        assert isinstance(info, dict)
        assert "version" in info
        assert "api_base_url" in info
        assert "free_tier" in info
        assert info["free_tier"] == "unlimited"

if __name__ == "__main__":
    pytest.main([__file__])
