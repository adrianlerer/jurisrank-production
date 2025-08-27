"""
JurisRank Data Models
====================

Pydantic models for JurisRank API data structures.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator

class LegalDocument(BaseModel):
    """Legal document model with metadata."""

    id: str = Field(..., description="Unique document identifier")
    title: str = Field(..., description="Document title")
    court: str = Field(..., description="Court name")
    date: str = Field(..., description="Document date (YYYY-MM-DD)")
    authority_score: float = Field(..., ge=0, le=100, description="Authority score (0-100)")
    jurisdiction: Optional[str] = Field(None, description="Legal jurisdiction")
    summary: Optional[str] = Field(None, description="Document summary")

    @validator('authority_score')
    def validate_authority_score(cls, v):
        """Validate authority score is within valid range."""
        if not 0 <= v <= 100:
            raise ValueError('Authority score must be between 0 and 100')
        return v

class AnalysisResult(BaseModel):
    """Legal document analysis result."""

    document_id: str = Field(..., description="Analyzed document ID")
    authority_score: float = Field(..., ge=0, le=100, description="Overall authority score")
    confidence: float = Field(..., ge=0, le=1, description="Analysis confidence (0-1)")
    analysis_summary: str = Field(..., description="Summary of analysis")
    insights: Optional[List[str]] = Field(default_factory=list, description="Key insights")
    similar_cases: Optional[List[LegalDocument]] = Field(default_factory=list, description="Similar cases")

    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "document_id": "doc_123",
                "authority_score": 85.5,
                "confidence": 0.92,
                "analysis_summary": "High authority precedent with strong legal basis",
                "insights": ["Strong precedential value", "Clear legal reasoning"],
                "similar_cases": []
            }
        }

class AuthorityScore(BaseModel):
    """Court/Judge authority scoring model."""

    entity_id: str = Field(..., description="Court or judge identifier")
    entity_type: str = Field(..., description="Type: court or judge")
    name: str = Field(..., description="Entity name")
    authority_score: float = Field(..., ge=0, le=100, description="Authority score")
    jurisdiction: str = Field(..., description="Legal jurisdiction")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

    @validator('entity_type')
    def validate_entity_type(cls, v):
        """Validate entity type."""
        if v not in ['court', 'judge']:
            raise ValueError('Entity type must be either "court" or "judge"')
        return v

class SearchQuery(BaseModel):
    """Legal search query model."""

    query: str = Field(..., min_length=3, description="Search query")
    jurisdiction: str = Field(default="global", description="Target jurisdiction")
    limit: int = Field(default=10, ge=1, le=100, description="Result limit (1-100)")
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional filters")

    @validator('jurisdiction')
    def validate_jurisdiction(cls, v):
        """Validate jurisdiction."""
        valid_jurisdictions = ["global", "argentina", "usa", "eu", "uk", "canada"]
        if v not in valid_jurisdictions:
            raise ValueError(f'Jurisdiction must be one of: {valid_jurisdictions}')
        return v
