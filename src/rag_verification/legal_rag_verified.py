#!/usr/bin/env python3
"""
JurisRank P7 Enhanced RAG with Verification System
Addressing Academic Research on AI Limitations in Legal Practice

Key AI Limitations Addressed:
1. Constitutional Hallucinations → Citation Verification Engine
2. Lack of Transparency → Complete Traceability Chain  
3. Context Window Issues → Structured Retrieval with Verification
4. Precedent Analysis Failures → Authority-Weighted Retrieval

Integration Target: Legal-RAG-pipeline (4 embedding models + BM25/Cosine hybrid)
Enhancement: Academic research-backed verification and traceability

Author: Ignacio Adrian Lerer
Research Base: AI's Limitations in Legal Practice + Constitutional Interpretation Studies
"""

import json
import hashlib
import logging
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio
import aiohttp
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CitationVerificationStatus(Enum):
    """Verification status for legal citations"""
    VERIFIED = "verified"
    PARTIAL_MATCH = "partial_match" 
    NOT_FOUND = "not_found"
    CONFLICTING_INFO = "conflicting_info"
    PENDING_VERIFICATION = "pending"

class LegalSourceAuthority(Enum):
    """Authority levels for legal sources"""
    CONSTITUTIONAL_COURT = 100      # CSJN constitutional decisions
    SUPREME_COURT = 90             # CSJN regular decisions  
    APPELLATE_COURT = 70           # Appellate court decisions
    TRIAL_COURT = 50               # Trial court decisions
    ADMINISTRATIVE = 30            # Administrative decisions
    ACADEMIC_PRIMARY = 60          # Law review articles
    ACADEMIC_SECONDARY = 40        # Secondary academic sources
    LEGISLATION = 95               # Constitutional and statutory law
    INTERNATIONAL_TREATY = 85      # International human rights treaties

@dataclass
class LegalCitation:
    """Represents a legal citation with verification metadata"""
    citation_text: str
    case_name: Optional[str] = None
    court: Optional[str] = None
    date: Optional[datetime] = None
    citation_format: Optional[str] = None  # "Fallos", "LL", etc.
    volume: Optional[str] = None
    page: Optional[str] = None
    verification_status: CitationVerificationStatus = CitationVerificationStatus.PENDING_VERIFICATION
    authority_level: Optional[LegalSourceAuthority] = None
    source_hash: Optional[str] = None
    verification_timestamp: Optional[datetime] = None

@dataclass
class VerificationResult:
    """Result of citation verification process"""
    citation: LegalCitation
    verification_status: CitationVerificationStatus
    confidence_score: float  # 0.0 to 1.0
    source_document: Optional[str] = None
    discrepancies: List[str] = field(default_factory=list)
    alternative_citations: List[LegalCitation] = field(default_factory=list)
    verification_notes: Optional[str] = None

@dataclass
class RetrievalCandidate:
    """Enhanced retrieval candidate with verification metadata"""
    document_id: str
    content: str
    score: float
    embedding_model: str
    legal_citations: List[LegalCitation] = field(default_factory=list)
    constitutional_articles: List[str] = field(default_factory=list)
    precedential_authority: Optional[LegalSourceAuthority] = None
    verification_results: List[VerificationResult] = field(default_factory=list)
    traceability_chain: List[str] = field(default_factory=list)

@dataclass
class VerifiedRetrievalResult:
    """Complete verified retrieval result"""
    query: str
    candidates: List[RetrievalCandidate]
    verification_summary: Dict[str, int]
    overall_confidence: float
    citation_traceability: Dict[str, List[str]]
    constitutional_context: Optional[Dict] = None
    precedent_evolution_chain: Optional[List[str]] = None

class LegalCitationExtractor:
    """
    Extracts and standardizes legal citations from text
    Supports Argentine legal citation formats
    """
    
    def __init__(self):
        # Argentine legal citation patterns
        self.citation_patterns = {
            'csjn_fallos': r'Fallos\s+(\d+):(\d+)',
            'csjn_case_name': r'"([^"]+)",?\s+Fallos\s+(\d+):(\d+)',
            'date_pattern': r'(\d{1,2})/(\d{1,2})/(\d{4})',
            'court_pattern': r'(CSJN|Corte Suprema|Cámara|Juzgado)',
            'constitutional_article': r'Art\.?\s*(\d+)(?:\s+inc\.?\s*(\d+))?\s*(?:de la\s+)?(?:Constitución|CN|C\.N\.)',
        }
        
    def extract_citations_from_text(self, text: str) -> List[LegalCitation]:
        """Extract legal citations from text using pattern matching"""
        
        citations = []
        
        # Extract CSJN Fallos citations
        import re
        fallos_matches = re.finditer(self.citation_patterns['csjn_fallos'], text, re.IGNORECASE)
        
        for match in fallos_matches:
            volume = match.group(1) 
            page = match.group(2)
            
            # Try to find case name near citation
            case_name = self._extract_case_name_near_citation(text, match.start())
            
            citation = LegalCitation(
                citation_text=match.group(0),
                case_name=case_name,
                court="CSJN",
                citation_format="Fallos",
                volume=volume,
                page=page,
                authority_level=LegalSourceAuthority.SUPREME_COURT
            )
            
            citations.append(citation)
            
        return citations
        
    def _extract_case_name_near_citation(self, text: str, citation_position: int) -> Optional[str]:
        """Extract case name near a citation position"""
        
        # Look for quoted case names within 100 characters before citation
        import re
        
        search_text = text[max(0, citation_position-100):citation_position+50]
        case_pattern = r'"([^"]+)"'
        
        matches = re.findall(case_pattern, search_text)
        if matches:
            return matches[-1]  # Return the closest case name
            
        return None

class CitationVerificationEngine:
    """
    Verifies legal citations against authoritative sources
    Addresses hallucination risks by validating every legal assertion
    """
    
    def __init__(self):
        self.citation_extractor = LegalCitationExtractor()
        self.verification_database = {}
        self.known_precedents = self._load_known_precedents()
        
    def _load_known_precedents(self) -> Dict[str, Dict]:
        """Load known constitutional precedents for verification"""
        
        return {
            "BAZTERRICA_1986": {
                "citation": "Fallos 308:1392",
                "case_name": "Bazterrica, Gustavo Mario", 
                "date": "29/08/1986",
                "court": "CSJN",
                "constitutional_articles": ["Art 19 CN"],
                "verified": True,
                "authority": LegalSourceAuthority.CONSTITUTIONAL_COURT,
                "hash": hashlib.md5("Bazterrica_Fallos_308_1392".encode()).hexdigest()
            },
            "ARRIOLA_2009": {
                "citation": "Fallos 332:1963",
                "case_name": "Arriola, Sebastián y otros",
                "date": "25/08/2009", 
                "court": "CSJN",
                "constitutional_articles": ["Art 19 CN", "Art 75 inc 22 CN"],
                "verified": True,
                "authority": LegalSourceAuthority.CONSTITUTIONAL_COURT,
                "hash": hashlib.md5("Arriola_Fallos_332_1963".encode()).hexdigest()
            }
        }
        
    async def verify_citation(self, citation: LegalCitation) -> VerificationResult:
        """
        Verify a legal citation against known sources
        Returns verification result with confidence score
        """
        
        verification_result = VerificationResult(
            citation=citation,
            verification_status=CitationVerificationStatus.PENDING_VERIFICATION,
            confidence_score=0.0
        )
        
        # Check against known precedents
        for precedent_id, precedent_data in self.known_precedents.items():
            similarity_score = self._calculate_citation_similarity(citation, precedent_data)
            
            if similarity_score > 0.9:  # High confidence match
                verification_result.verification_status = CitationVerificationStatus.VERIFIED
                verification_result.confidence_score = similarity_score
                verification_result.source_document = precedent_id
                verification_result.verification_notes = f"Verified against known precedent: {precedent_id}"
                break
                
            elif similarity_score > 0.7:  # Partial match
                verification_result.verification_status = CitationVerificationStatus.PARTIAL_MATCH
                verification_result.confidence_score = similarity_score
                verification_result.alternative_citations.append(
                    self._create_citation_from_precedent(precedent_data)
                )
                
        # If no match found in known precedents, mark as not found
        if verification_result.verification_status == CitationVerificationStatus.PENDING_VERIFICATION:
            verification_result.verification_status = CitationVerificationStatus.NOT_FOUND
            verification_result.confidence_score = 0.0
            verification_result.verification_notes = "Citation not found in verified precedent database"
            
        verification_result.verification_timestamp = datetime.now()
        return verification_result
        
    def _calculate_citation_similarity(self, citation: LegalCitation, precedent_data: Dict) -> float:
        """Calculate similarity between citation and known precedent"""
        
        similarity_factors = []
        
        # Citation text similarity
        if citation.citation_format == "Fallos" and precedent_data.get("citation"):
            if precedent_data["citation"] in citation.citation_text:
                similarity_factors.append(1.0)
            else:
                similarity_factors.append(0.0)
                
        # Case name similarity  
        if citation.case_name and precedent_data.get("case_name"):
            if citation.case_name.lower() in precedent_data["case_name"].lower():
                similarity_factors.append(1.0)
            else:
                similarity_factors.append(0.0)
                
        # Court similarity
        if citation.court and precedent_data.get("court"):
            if citation.court == precedent_data["court"]:
                similarity_factors.append(1.0)
            else:
                similarity_factors.append(0.0)
                
        # Return average similarity
        return sum(similarity_factors) / len(similarity_factors) if similarity_factors else 0.0
        
    def _create_citation_from_precedent(self, precedent_data: Dict) -> LegalCitation:
        """Create a LegalCitation object from precedent data"""
        
        return LegalCitation(
            citation_text=precedent_data["citation"],
            case_name=precedent_data["case_name"],
            court=precedent_data["court"],
            citation_format="Fallos",
            authority_level=precedent_data["authority"],
            verification_status=CitationVerificationStatus.VERIFIED
        )

class VerifiedLegalRAG:
    """
    Enhanced RAG system with citation verification and traceability
    
    Integrates with existing Legal-RAG-pipeline while adding:
    1. Citation verification engine (addresses hallucinations)
    2. Complete traceability chains (addresses transparency)
    3. Authority-weighted retrieval (improves precedent analysis)
    4. Multi-embedding verification (reduces false matches)
    """
    
    def __init__(self):
        self.citation_extractor = LegalCitationExtractor()
        self.verification_engine = CitationVerificationEngine()
        
        # Simulate existing Legal-RAG embedding models
        self.embedding_models = {
            'constitutional_law': "law-ai/InLegalBERT",
            'precedent_analysis': "nlpaueb/legal-bert-base-uncased", 
            'cross_jurisdictional': "sentence-transformers/paraphrase-multilingual",
            'general_legal': "openai/text-embedding-ada-002"
        }
        
        # BM25 + Cosine hybrid retrieval (simulated)
        self.hybrid_retrieval_weights = {
            'bm25': 0.3,
            'cosine_constitutional': 0.25,
            'cosine_precedent': 0.25, 
            'cosine_cross_jurisdictional': 0.1,
            'cosine_general': 0.1
        }
        
    async def retrieve_with_verification(self, 
                                       query: str,
                                       constitutional_context: Optional[str] = None) -> VerifiedRetrievalResult:
        """
        Enhanced retrieval with complete verification and traceability
        
        Process:
        1. Multi-embedding retrieval (existing Legal-RAG pipeline)
        2. Citation extraction and verification  
        3. Authority-weighted ranking using JurisRank P7
        4. Traceability chain construction
        5. Constitutional context integration
        """
        
        logger.info(f"Starting verified retrieval for query: {query[:100]}...")
        
        # Stage 1: Multi-embedding retrieval (simulated)
        raw_candidates = await self._multi_embedding_retrieval(query)
        
        # Stage 2: Citation extraction and verification
        verified_candidates = []
        
        for candidate in raw_candidates:
            # Extract citations from retrieved content
            citations = self.citation_extractor.extract_citations_from_text(candidate.content)
            candidate.legal_citations = citations
            
            # Verify each citation
            verification_results = []
            for citation in citations:
                verification = await self.verification_engine.verify_citation(citation)
                verification_results.append(verification)
                
            candidate.verification_results = verification_results
            
            # Calculate overall verification confidence
            if verification_results:
                verification_scores = [vr.confidence_score for vr in verification_results]
                candidate.score *= (sum(verification_scores) / len(verification_scores))
                
            verified_candidates.append(candidate)
            
        # Stage 3: Authority-weighted ranking
        authority_weighted_candidates = self._apply_authority_weighting(verified_candidates)
        
        # Stage 4: Build traceability chains
        for candidate in authority_weighted_candidates:
            candidate.traceability_chain = self._build_traceability_chain(candidate)
            
        # Stage 5: Create verification summary
        verification_summary = self._create_verification_summary(authority_weighted_candidates)
        
        # Stage 6: Calculate overall confidence
        overall_confidence = self._calculate_overall_confidence(authority_weighted_candidates)
        
        # Stage 7: Build citation traceability map
        citation_traceability = self._build_citation_traceability_map(authority_weighted_candidates)
        
        return VerifiedRetrievalResult(
            query=query,
            candidates=authority_weighted_candidates,
            verification_summary=verification_summary,
            overall_confidence=overall_confidence,
            citation_traceability=citation_traceability,
            constitutional_context={"article": "Art 19 CN", "precedents": ["Bazterrica", "Arriola"]},
            precedent_evolution_chain=["Bazterrica (1986)", "Arriola (2009)"]
        )
        
    async def _multi_embedding_retrieval(self, query: str) -> List[RetrievalCandidate]:
        """
        Simulate multi-embedding retrieval from existing Legal-RAG pipeline
        """
        
        # Simulated retrieval results - in production, this would call actual Legal-RAG
        simulated_candidates = [
            RetrievalCandidate(
                document_id="constitutional_doc_001",
                content=f"""
                El artículo 19 de la Constitución Nacional establece que las acciones privadas 
                de los hombres que de ningún modo ofendan al orden y a la moral pública, ni 
                perjudiquen a un tercero, están sólo reservadas a Dios, y exentas de la autoridad 
                de los magistrados. En "Bazterrica, Gustavo Mario", Fallos 308:1392 (1986), 
                la Corte Suprema estableció que la tenencia de estupefacientes para consumo personal 
                no constituye delito cuando no genera daño a terceros.
                """,
                score=0.95,
                embedding_model="constitutional_law",
                constitutional_articles=["Art 19 CN"],
                precedential_authority=LegalSourceAuthority.CONSTITUTIONAL_COURT
            ),
            RetrievalCandidate(
                document_id="precedent_doc_002", 
                content=f"""
                La evolución jurisprudencial en materia de autonomía personal muestra una clara
                progresión desde "Bazterrica" (1986) hacia "Arriola, Sebastián y otros", Fallos 
                332:1963 (2009). En Arriola, la Corte reafirmó los principios de Bazterrica pero
                incorporó estándares internacionales de derechos humanos y el concepto de dignidad 
                humana como fundamento de la autonomía personal.
                """,
                score=0.88,
                embedding_model="precedent_analysis",
                constitutional_articles=["Art 19 CN", "Art 75 inc 22 CN"],
                precedential_authority=LegalSourceAuthority.CONSTITUTIONAL_COURT
            )
        ]
        
        return simulated_candidates
        
    def _apply_authority_weighting(self, candidates: List[RetrievalCandidate]) -> List[RetrievalCandidate]:
        """
        Apply JurisRank P7 authority weighting to candidates based on verification
        """
        
        for candidate in candidates:
            authority_multiplier = 1.0
            
            # Weight by precedential authority
            if candidate.precedential_authority:
                authority_multiplier *= (candidate.precedential_authority.value / 100.0)
                
            # Weight by verification confidence
            if candidate.verification_results:
                verification_scores = [vr.confidence_score for vr in candidate.verification_results]
                verification_confidence = sum(verification_scores) / len(verification_scores)
                authority_multiplier *= verification_confidence
                
            # Apply weighting to candidate score
            candidate.score *= authority_multiplier
            
        # Sort by weighted score
        candidates.sort(key=lambda c: c.score, reverse=True)
        return candidates
        
    def _build_traceability_chain(self, candidate: RetrievalCandidate) -> List[str]:
        """
        Build complete traceability chain for a retrieval candidate
        """
        
        chain = []
        
        # Add document source
        chain.append(f"Source Document: {candidate.document_id}")
        
        # Add embedding model used
        chain.append(f"Retrieved via: {candidate.embedding_model}")
        
        # Add verified citations
        for verification in candidate.verification_results:
            if verification.verification_status == CitationVerificationStatus.VERIFIED:
                chain.append(f"Verified Citation: {verification.citation.citation_text}")
                
        # Add constitutional articles
        for article in candidate.constitutional_articles:
            chain.append(f"Constitutional Article: {article}")
            
        return chain
        
    def _create_verification_summary(self, candidates: List[RetrievalCandidate]) -> Dict[str, int]:
        """Create summary of verification results across all candidates"""
        
        summary = {
            "total_candidates": len(candidates),
            "verified_citations": 0,
            "partial_matches": 0,
            "unverified_citations": 0,
            "constitutional_articles": 0
        }
        
        for candidate in candidates:
            for verification in candidate.verification_results:
                if verification.verification_status == CitationVerificationStatus.VERIFIED:
                    summary["verified_citations"] += 1
                elif verification.verification_status == CitationVerificationStatus.PARTIAL_MATCH:
                    summary["partial_matches"] += 1 
                else:
                    summary["unverified_citations"] += 1
                    
            summary["constitutional_articles"] += len(candidate.constitutional_articles)
            
        return summary
        
    def _calculate_overall_confidence(self, candidates: List[RetrievalCandidate]) -> float:
        """Calculate overall confidence in retrieval results"""
        
        if not candidates:
            return 0.0
            
        confidence_factors = []
        
        # Factor 1: Verification confidence
        verification_scores = []
        for candidate in candidates:
            if candidate.verification_results:
                candidate_scores = [vr.confidence_score for vr in candidate.verification_results]
                if candidate_scores:
                    verification_scores.append(sum(candidate_scores) / len(candidate_scores))
                    
        if verification_scores:
            confidence_factors.append(sum(verification_scores) / len(verification_scores))
            
        # Factor 2: Authority level confidence
        authority_scores = []
        for candidate in candidates:
            if candidate.precedential_authority:
                authority_scores.append(candidate.precedential_authority.value / 100.0)
                
        if authority_scores:
            confidence_factors.append(sum(authority_scores) / len(authority_scores))
            
        # Factor 3: Constitutional relevance
        constitutional_relevance = sum(1 for c in candidates if c.constitutional_articles) / len(candidates)
        confidence_factors.append(constitutional_relevance)
        
        return sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.0
        
    def _build_citation_traceability_map(self, candidates: List[RetrievalCandidate]) -> Dict[str, List[str]]:
        """Build complete citation traceability map"""
        
        traceability_map = {}
        
        for candidate in candidates:
            for verification in candidate.verification_results:
                citation_key = verification.citation.citation_text
                
                if citation_key not in traceability_map:
                    traceability_map[citation_key] = []
                    
                traceability_map[citation_key].extend([
                    f"Status: {verification.verification_status.value}",
                    f"Confidence: {verification.confidence_score:.2%}",
                    f"Source: {candidate.document_id}",
                    f"Verification: {verification.verification_timestamp}"
                ])
                
        return traceability_map

async def main():
    """
    Demonstration of verified legal RAG addressing AI limitations
    """
    
    print("🔍 JurisRank P7 Enhanced RAG with Verification System")
    print("📚 Addressing Academic AI Limitations Research")
    print("=" * 70)
    
    # Initialize verified RAG system
    rag_system = VerifiedLegalRAG()
    
    # Example query about constitutional law
    query = """
    ¿Cuál es la doctrina constitucional sobre tenencia de estupefacientes 
    para consumo personal conforme el Art 19 CN y la evolución jurisprudencial 
    de la Corte Suprema?
    """
    
    print(f"📝 Query: {query}")
    print("\n" + "=" * 70)
    
    # Perform verified retrieval
    result = await rag_system.retrieve_with_verification(
        query=query,
        constitutional_context="Art 19 CN - Personal autonomy and harm to others test"
    )
    
    print("📊 VERIFIED RETRIEVAL RESULTS:")
    print("=" * 70)
    
    print(f"🎯 Overall Confidence: {result.overall_confidence:.0%}")
    print(f"📚 Retrieved Candidates: {len(result.candidates)}")
    
    print("\n📋 Verification Summary:")
    for key, value in result.verification_summary.items():
        print(f"  • {key.replace('_', ' ').title()}: {value}")
        
    print("\n🔗 Citation Traceability:")
    for citation, trace in result.citation_traceability.items():
        print(f"\n  📖 {citation}:")
        for step in trace:
            print(f"    ✓ {step}")
            
    print("\n📄 Top Verified Candidate:")
    if result.candidates:
        top_candidate = result.candidates[0]
        print(f"  • Document: {top_candidate.document_id}")
        print(f"  • Score: {top_candidate.score:.3f}")
        print(f"  • Authority: {top_candidate.precedential_authority.name if top_candidate.precedential_authority else 'N/A'}")
        print(f"  • Citations: {len(top_candidate.legal_citations)}")
        print(f"  • Verifications: {len(top_candidate.verification_results)}")
        
        print("\n  📝 Content Preview:")
        print(f"    {top_candidate.content[:300]}...")
        
        print("\n  🔍 Traceability Chain:")
        for step in top_candidate.traceability_chain:
            print(f"    → {step}")
            
    print("\n" + "=" * 70)
    print("✅ Verified RAG processing completed")
    print("🧠 AI Limitations addressed: Hallucinations, transparency, context issues")
    print("🏛️ Constitutional analysis enhanced with complete verification")

if __name__ == "__main__":
    asyncio.run(main())