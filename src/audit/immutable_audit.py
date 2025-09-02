#!/usr/bin/env python3
"""
JurisRank P7 Enhanced - Sistema de Auditoría Inmutable
Integración de mejoras Coan & Surden con investigación de limitaciones de IA

Características:
1. Logging inmutable de cada ranking constitucional
2. Trazabilidad completa de prompts y modelos usados  
3. Hash cryptográfico para prevenir manipulación
4. Integración con knowledge graph constitucional
5. Auditoría de verificación de citas

Author: Ignacio Adrian Lerer
Research Base: Coan & Surden + AI Limitations in Legal Practice
Integration: JurisRank P7 Enhanced Constitutional Engine
"""

import json
import datetime
import hashlib
import logging
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalysisType(Enum):
    """Types of constitutional analysis for audit logging"""
    CONSTITUTIONAL_RANKING = "constitutional_ranking"
    PRECEDENT_ANALYSIS = "precedent_analysis"
    CITATION_VERIFICATION = "citation_verification"
    MULTI_MODEL_ENSEMBLE = "multi_model_ensemble"
    HUMAN_REVIEW_WORKFLOW = "human_review_workflow"

class AIModel(Enum):
    """AI Models used in constitutional analysis"""
    DARWIN_ASI = "darwin_asi_384_experts"
    GPT_4O = "gpt-4o"
    CLAUDE_35_SONNET = "claude-3.5-sonnet"
    GEMINI_PRO = "gemini-pro"
    JURISRANK_SLM = "jurisrank_slm_constitutional"

@dataclass
class ConstitutionalAuditEntry:
    """Immutable audit entry for constitutional analysis"""
    timestamp: str
    case_id: str
    analysis_type: AnalysisType
    constitutional_articles: List[str]
    precedents_analyzed: List[str]
    prompt_kit_used: Optional[str]
    ai_model: AIModel
    model_version: str
    constitutional_ranking: Dict[str, Any]
    verification_results: Dict[str, float]
    human_reviewer_id: Optional[str]
    confidence_score: float
    citation_verification_status: Dict[str, str]
    knowledge_graph_path: List[str]
    user_id: str
    session_hash: str
    immutable_hash: str

class ImmutableConstitutionalAudit:
    """
    Sistema de auditoría inmutable para análisis constitucional JurisRank P7
    
    Integra:
    - Logging inmutable (Coan & Surden requirement)
    - Constitutional knowledge graph traceability
    - AI limitations mitigation tracking
    - Multi-model ensemble audit trail
    - Citation verification audit
    """
    
    def __init__(self, audit_dir: str = "logs"):
        self.audit_dir = Path(audit_dir)
        self.audit_dir.mkdir(exist_ok=True)
        
        # Ensure logs directory exists
        if not self.audit_dir.exists():
            self.audit_dir.mkdir(parents=True)
            
        logger.info(f"Initialized immutable audit system in {self.audit_dir}")
        
    def log_constitutional_analysis(self,
                                  case_id: str,
                                  analysis_type: AnalysisType,
                                  constitutional_articles: List[str],
                                  precedents_analyzed: List[str],
                                  prompt_kit: Optional[str],
                                  ai_model: AIModel,
                                  model_version: str,
                                  constitutional_ranking: Dict[str, Any],
                                  verification_results: Dict[str, float],
                                  knowledge_graph_path: List[str],
                                  user_id: str,
                                  human_reviewer_id: Optional[str] = None,
                                  confidence_score: float = 0.0,
                                  citation_verification: Optional[Dict[str, str]] = None) -> str:
        """
        Log constitutional analysis with immutable audit trail
        
        Returns: audit_file_path for external reference
        """
        
        timestamp = datetime.datetime.utcnow().isoformat()
        
        # Create session hash from key parameters
        session_data = f"{case_id}_{timestamp}_{ai_model.value}_{user_id}"
        session_hash = hashlib.sha256(session_data.encode()).hexdigest()[:16]
        
        # Create audit entry
        audit_entry = ConstitutionalAuditEntry(
            timestamp=timestamp,
            case_id=case_id,
            analysis_type=analysis_type,
            constitutional_articles=constitutional_articles,
            precedents_analyzed=precedents_analyzed,
            prompt_kit_used=prompt_kit,
            ai_model=ai_model,
            model_version=model_version,
            constitutional_ranking=constitutional_ranking,
            verification_results=verification_results,
            human_reviewer_id=human_reviewer_id,
            confidence_score=confidence_score,
            citation_verification_status=citation_verification or {},
            knowledge_graph_path=knowledge_graph_path,
            user_id=user_id,
            session_hash=session_hash,
            immutable_hash=""  # Will be calculated below
        )
        
        # Calculate immutable hash
        entry_dict = asdict(audit_entry)
        entry_dict.pop('immutable_hash')  # Remove hash field before calculating
        entry_json = json.dumps(entry_dict, sort_keys=True, ensure_ascii=False)
        immutable_hash = hashlib.sha256(entry_json.encode()).hexdigest()
        audit_entry.immutable_hash = immutable_hash
        
        # Generate audit filename with timestamp and hash
        timestamp_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        audit_filename = f"{case_id}_{timestamp_str}_{session_hash}.json"
        audit_filepath = self.audit_dir / audit_filename
        
        # Write immutable audit entry
        with open(audit_filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(audit_entry), f, ensure_ascii=False, indent=2)
            
        logger.info(f"Logged constitutional analysis: {audit_filepath}")
        logger.info(f"Immutable hash: {immutable_hash}")
        
        return str(audit_filepath)
        
    def log_jurisrank_p7_analysis(self,
                                 case_id: str,
                                 constitutional_question: str,
                                 bazterrica_arriola_analysis: Dict[str, Any],
                                 knowledge_graph_paths: List[str],
                                 citation_verifications: Dict[str, str],
                                 ai_model: AIModel,
                                 user_id: str,
                                 prompt_kit: str = "constitutional_art19") -> str:
        """
        Specialized logging for JurisRank P7 constitutional analysis
        Integrates with enhanced constitutional engine and verified RAG
        """
        
        # Extract constitutional ranking from Bazterrica-Arriola analysis
        constitutional_ranking = {
            "personal_autonomy_score": bazterrica_arriola_analysis.get("autonomy_score", 0.0),
            "harm_to_others_test": bazterrica_arriola_analysis.get("harm_test_result", "unknown"),
            "constitutional_morality": bazterrica_arriola_analysis.get("morality_analysis", ""),
            "precedent_evolution": bazterrica_arriola_analysis.get("evolution_chain", []),
            "article_19_application": bazterrica_arriola_analysis.get("art19_conclusion", "")
        }
        
        # Extract verification scores
        verification_results = {}
        for citation, status in citation_verifications.items():
            if status == "verified":
                verification_results[citation] = 1.0
            elif status == "partial_match":
                verification_results[citation] = 0.7
            else:
                verification_results[citation] = 0.0
                
        return self.log_constitutional_analysis(
            case_id=case_id,
            analysis_type=AnalysisType.CONSTITUTIONAL_RANKING,
            constitutional_articles=["Art 19 CN"],
            precedents_analyzed=["Bazterrica 1986", "Arriola 2009"],
            prompt_kit=prompt_kit,
            ai_model=ai_model,
            model_version="jurisrank_p7_enhanced_v1.0",
            constitutional_ranking=constitutional_ranking,
            verification_results=verification_results,
            knowledge_graph_path=knowledge_graph_paths,
            user_id=user_id,
            confidence_score=bazterrica_arriola_analysis.get("overall_confidence", 0.85)
        )
        
    def verify_audit_integrity(self, audit_file: str) -> bool:
        """
        Verify the integrity of an audit file using immutable hash
        """
        
        try:
            with open(audit_file, 'r', encoding='utf-8') as f:
                audit_data = json.load(f)
                
            # Extract stored hash
            stored_hash = audit_data.pop('immutable_hash')
            
            # Recalculate hash
            entry_json = json.dumps(audit_data, sort_keys=True, ensure_ascii=False)
            calculated_hash = hashlib.sha256(entry_json.encode()).hexdigest()
            
            # Verify integrity
            integrity_verified = (stored_hash == calculated_hash)
            
            if integrity_verified:
                logger.info(f"Audit integrity verified: {audit_file}")
            else:
                logger.error(f"Audit integrity FAILED: {audit_file}")
                logger.error(f"Stored: {stored_hash}")
                logger.error(f"Calculated: {calculated_hash}")
                
            return integrity_verified
            
        except Exception as e:
            logger.error(f"Error verifying audit integrity: {e}")
            return False
            
    def generate_constitutional_audit_report(self, 
                                           case_id: Optional[str] = None,
                                           start_date: Optional[datetime.datetime] = None,
                                           end_date: Optional[datetime.datetime] = None) -> Dict[str, Any]:
        """
        Generate comprehensive audit report for constitutional analyses
        """
        
        audit_files = list(self.audit_dir.glob("*.json"))
        
        if case_id:
            audit_files = [f for f in audit_files if case_id in f.name]
            
        report = {
            "report_generated": datetime.datetime.utcnow().isoformat(),
            "total_analyses": len(audit_files),
            "constitutional_articles_analyzed": set(),
            "precedents_referenced": set(),
            "ai_models_used": set(),
            "prompt_kits_used": set(),
            "integrity_status": {},
            "confidence_scores": [],
            "verification_rates": {},
            "human_review_percentage": 0
        }
        
        human_reviewed_count = 0
        
        for audit_file in audit_files:
            try:
                with open(audit_file, 'r', encoding='utf-8') as f:
                    audit_data = json.load(f)
                    
                # Verify integrity
                integrity_ok = self.verify_audit_integrity(str(audit_file))
                report["integrity_status"][audit_file.name] = integrity_ok
                
                # Aggregate data
                report["constitutional_articles_analyzed"].update(audit_data.get("constitutional_articles", []))
                report["precedents_referenced"].update(audit_data.get("precedents_analyzed", []))
                report["ai_models_used"].add(audit_data.get("ai_model", "unknown"))
                
                if audit_data.get("prompt_kit_used"):
                    report["prompt_kits_used"].add(audit_data["prompt_kit_used"])
                    
                if audit_data.get("confidence_score"):
                    report["confidence_scores"].append(audit_data["confidence_score"])
                    
                if audit_data.get("human_reviewer_id"):
                    human_reviewed_count += 1
                    
                # Aggregate verification results
                for citation, score in audit_data.get("verification_results", {}).items():
                    if citation not in report["verification_rates"]:
                        report["verification_rates"][citation] = []
                    report["verification_rates"][citation].append(score)
                    
            except Exception as e:
                logger.error(f"Error processing audit file {audit_file}: {e}")
                
        # Calculate percentages and averages
        if audit_files:
            report["human_review_percentage"] = (human_reviewed_count / len(audit_files)) * 100
            
        if report["confidence_scores"]:
            report["average_confidence"] = sum(report["confidence_scores"]) / len(report["confidence_scores"])
            
        # Convert sets to lists for JSON serialization
        report["constitutional_articles_analyzed"] = list(report["constitutional_articles_analyzed"])
        report["precedents_referenced"] = list(report["precedents_referenced"])
        report["ai_models_used"] = list(report["ai_models_used"])
        report["prompt_kits_used"] = list(report["prompt_kits_used"])
        
        return report

def main():
    """
    Demonstration of immutable audit system for constitutional analysis
    """
    
    print("📋 JurisRank P7 Enhanced - Sistema de Auditoría Inmutable")
    print("🔒 Integración Coan & Surden + AI Limitations Research")
    print("=" * 70)
    
    # Initialize audit system
    audit_system = ImmutableConstitutionalAudit()
    
    # Example: Log constitutional analysis
    case_id = "CSJN-2024-CONSTITUTIONAL-001"
    
    # Simulated Bazterrica-Arriola analysis result
    constitutional_analysis = {
        "autonomy_score": 0.92,
        "harm_test_result": "no_harm_to_others_identified", 
        "morality_analysis": "state_cannot_impose_particular_morality",
        "evolution_chain": ["Bazterrica_1986", "Arriola_2009"],
        "art19_conclusion": "constitutional_protection_applies",
        "overall_confidence": 0.89
    }
    
    # Simulated knowledge graph paths
    knowledge_paths = [
        "ART_19_CN → BAZTERRICA_1986 → personal_autonomy",
        "BAZTERRICA_1986 → ARRIOLA_2009 → constitutional_evolution",
        "ARRIOLA_2009 → constitutional_morality → dignidad_humana"
    ]
    
    # Simulated citation verifications
    citations = {
        "Bazterrica, Gustavo Mario - Fallos 308:1392 (1986)": "verified",
        "Arriola, Sebastián y otros - Fallos 332:1963 (2009)": "verified",
        "Art 19 CN": "verified"
    }
    
    # Log the analysis
    audit_file = audit_system.log_jurisrank_p7_analysis(
        case_id=case_id,
        constitutional_question="¿Protege el Art 19 CN la tenencia para consumo personal?",
        bazterrica_arriola_analysis=constitutional_analysis,
        knowledge_graph_paths=knowledge_paths,
        citation_verifications=citations,
        ai_model=AIModel.DARWIN_ASI,
        user_id="constitutional_analyst_001",
        prompt_kit="constitutional_art19_enhanced"
    )
    
    print(f"✅ Audit logged: {audit_file}")
    
    # Verify integrity
    integrity_ok = audit_system.verify_audit_integrity(audit_file)
    print(f"🔒 Audit integrity: {'✅ VERIFIED' if integrity_ok else '❌ FAILED'}")
    
    # Generate audit report
    report = audit_system.generate_constitutional_audit_report(case_id=case_id)
    
    print("\n📊 CONSTITUTIONAL AUDIT REPORT:")
    print("=" * 70)
    print(f"📄 Total Analyses: {report['total_analyses']}")
    print(f"🏛️ Constitutional Articles: {', '.join(report['constitutional_articles_analyzed'])}")
    print(f"⚖️ Precedents Referenced: {', '.join(report['precedents_referenced'])}")
    print(f"🤖 AI Models Used: {', '.join(report['ai_models_used'])}")
    print(f"📝 Prompt Kits Used: {', '.join(report['prompt_kits_used'])}")
    print(f"🎯 Average Confidence: {report.get('average_confidence', 0):.0%}")
    print(f"👥 Human Review Rate: {report['human_review_percentage']:.1f}%")
    
    print("\n" + "=" * 70)
    print("✅ Immutable audit system demonstration completed")
    print("🔒 All constitutional analyses logged with cryptographic integrity")
    print("📋 Full traceability for AI limitations mitigation compliance")

if __name__ == "__main__":
    main()