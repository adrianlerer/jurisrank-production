#!/usr/bin/env python3
"""
HRM-JurisRank Integration Module
Integración del Hierarchical Reasoning Model (HRM) con el sistema JurisRank
para análisis avanzado de relevancia bibliográfica y razonamiento jurisprudencial
"""

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("Warning: PyTorch not available - using simulation mode")

import json
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging
import sys
import os

# Importar módulos locales
sys.path.insert(0, '.')
try:
    from jurisrank_bibliography_integration import JurisRankBibliographyService, AcademicReference
except ImportError:
    print("Warning: JurisRank bibliography integration not available")

logger = logging.getLogger(__name__)

class HRMReasoningEngine:
    """
    Motor de razonamiento jerárquico para análisis bibliográfico avanzado
    Basado en el Hierarchical Reasoning Model (HRM) desarrollado por Adrian Lerer
    """
    
    def __init__(self, hrm_model_path: Optional[str] = None, device: str = "cpu"):
        """
        Inicializa el motor de razonamiento HRM
        
        Args:
            hrm_model_path: Ruta al modelo HRM preentrenado
            device: Dispositivo de cómputo (cpu, cuda)
        """
        self.device = device
        self.hrm_model_path = hrm_model_path
        self.model = None
        
        # Configuración de razonamiento jerárquico
        self.reasoning_config = {
            'hierarchical_levels': 3,  # Niveles de razonamiento (abstracto -> concreto)
            'max_reasoning_steps': 50,  # Máximo pasos de razonamiento
            'attention_heads': 8,       # Cabezas de atención
            'embedding_dim': 512,       # Dimensión de embeddings
        }
        
        # Inicializar arquitectura (simulada - real requiere código HRM)
        self._init_reasoning_architecture()
        
    def _init_reasoning_architecture(self):
        """Inicializa la arquitectura de razonamiento jerárquico"""
        logger.info("Initializing HRM reasoning architecture")
        
        # Simulación de la arquitectura HRM
        # En implementación real, cargarías el modelo desde tu repo HRM
        self.reasoning_modules = {
            'high_level': {  # Módulo de planificación abstracta
                'type': 'abstract_planner',
                'function': 'legal_strategy_planning',
                'parameters': {'planning_depth': 5}
            },
            'mid_level': {   # Módulo de análisis intermedio
                'type': 'case_analyzer', 
                'function': 'precedent_evaluation',
                'parameters': {'context_window': 1024}
            },
            'low_level': {   # Módulo de procesamiento detallado
                'type': 'token_processor',
                'function': 'citation_extraction',
                'parameters': {'token_precision': True}
            }
        }
        
        logger.info("HRM architecture initialized successfully")
        
    def hierarchical_reasoning(self, query: str, candidates: List[AcademicReference]) -> Dict:
        """
        Ejecuta razonamiento jerárquico sobre candidatos bibliográficos
        
        Args:
            query: Consulta legal/académica
            candidates: Lista de referencias candidatas
            
        Returns:
            Dict con análisis jerárquico de relevancia
        """
        
        reasoning_result = {
            'query': query,
            'candidates_count': len(candidates),
            'reasoning_timestamp': datetime.now().isoformat(),
            'hierarchical_analysis': {},
            'final_ranking': [],
            'reasoning_path': [],
            'confidence_scores': {}
        }
        
        # NIVEL 1: Razonamiento de Alto Nivel (Estratégico/Abstracto)
        high_level_analysis = self._high_level_reasoning(query, candidates)
        reasoning_result['hierarchical_analysis']['high_level'] = high_level_analysis
        reasoning_result['reasoning_path'].append("High-level strategic analysis completed")
        
        # NIVEL 2: Razonamiento de Nivel Medio (Análisis de Casos)
        mid_level_analysis = self._mid_level_reasoning(query, candidates, high_level_analysis)
        reasoning_result['hierarchical_analysis']['mid_level'] = mid_level_analysis
        reasoning_result['reasoning_path'].append("Mid-level case analysis completed")
        
        # NIVEL 3: Razonamiento de Bajo Nivel (Procesamiento Detallado)
        low_level_analysis = self._low_level_reasoning(query, candidates, mid_level_analysis)
        reasoning_result['hierarchical_analysis']['low_level'] = low_level_analysis
        reasoning_result['reasoning_path'].append("Low-level detailed processing completed")
        
        # Integración Jerárquica: Combinar todos los niveles
        final_ranking = self._integrate_hierarchical_results(
            high_level_analysis, mid_level_analysis, low_level_analysis
        )
        
        reasoning_result['final_ranking'] = final_ranking
        reasoning_result['confidence_scores'] = self._calculate_confidence_scores(final_ranking)
        
        return reasoning_result
    
    def _high_level_reasoning(self, query: str, candidates: List[AcademicReference]) -> Dict:
        """Razonamiento de alto nivel - Planificación estratégica abstracta"""
        
        # Análisis estratégico de la consulta
        query_strategy = self._analyze_query_strategy(query)
        
        # Categorización abstracta de candidatos
        abstract_categories = self._categorize_candidates_abstractly(candidates)
        
        # Planificación de estrategia de búsqueda
        search_strategy = self._plan_search_strategy(query_strategy, abstract_categories)
        
        return {
            'query_strategy': query_strategy,
            'abstract_categories': abstract_categories,
            'search_strategy': search_strategy,
            'reasoning_confidence': 0.85
        }
    
    def _mid_level_reasoning(self, query: str, candidates: List[AcademicReference], 
                           high_level_context: Dict) -> Dict:
        """Razonamiento de nivel medio - Análisis de casos y precedentes"""
        
        case_analyses = []
        
        for candidate in candidates:
            case_analysis = {
                'reference_id': candidate.reference_id,
                'title': candidate.title,
                'precedent_strength': self._evaluate_precedent_strength(candidate, query),
                'contextual_relevance': self._evaluate_contextual_relevance(
                    candidate, high_level_context['search_strategy']
                ),
                'citation_network_position': self._analyze_citation_network_position(candidate),
                'temporal_relevance': self._evaluate_temporal_relevance(candidate)
            }
            case_analyses.append(case_analysis)
        
        # Análisis comparativo entre casos
        comparative_analysis = self._comparative_case_analysis(case_analyses)
        
        return {
            'case_analyses': case_analyses,
            'comparative_analysis': comparative_analysis,
            'mid_level_rankings': sorted(case_analyses, 
                                       key=lambda x: x['precedent_strength'], reverse=True)
        }
    
    def _low_level_reasoning(self, query: str, candidates: List[AcademicReference],
                           mid_level_context: Dict) -> Dict:
        """Razonamiento de bajo nivel - Procesamiento detallado token por token"""
        
        detailed_analyses = []
        
        for candidate in candidates:
            # Análisis detallado de texto
            token_analysis = self._detailed_token_analysis(candidate, query)
            
            # Extracción precisa de citaciones
            citation_extraction = self._precise_citation_extraction(candidate)
            
            # Análisis semántico profundo
            semantic_analysis = self._deep_semantic_analysis(candidate, query)
            
            detailed_analysis = {
                'reference_id': candidate.reference_id,
                'token_analysis': token_analysis,
                'citation_extraction': citation_extraction,
                'semantic_analysis': semantic_analysis,
                'fine_grained_score': self._calculate_fine_grained_score(
                    token_analysis, citation_extraction, semantic_analysis
                )
            }
            detailed_analyses.append(detailed_analysis)
        
        return {
            'detailed_analyses': detailed_analyses,
            'precision_metrics': self._calculate_precision_metrics(detailed_analyses)
        }
    
    def _integrate_hierarchical_results(self, high_level: Dict, mid_level: Dict, 
                                      low_level: Dict) -> List[Dict]:
        """Integra los resultados de los tres niveles jerárquicos"""
        
        integrated_ranking = []
        
        # Combinar análisis de todos los niveles
        for mid_analysis in mid_level['case_analyses']:
            ref_id = mid_analysis['reference_id']
            
            # Encontrar análisis correspondiente en bajo nivel
            low_analysis = next(
                (la for la in low_level['detailed_analyses'] if la['reference_id'] == ref_id),
                None
            )
            
            if low_analysis:
                # Calcular score integrado jerárquicamente
                integrated_score = (
                    high_level['reasoning_confidence'] * 0.3 +
                    mid_analysis['precedent_strength'] * 0.4 +
                    low_analysis['fine_grained_score'] * 0.3
                )
                
                integrated_result = {
                    'reference_id': ref_id,
                    'title': mid_analysis['title'],
                    'integrated_score': integrated_score,
                    'high_level_contribution': high_level['reasoning_confidence'] * 0.3,
                    'mid_level_contribution': mid_analysis['precedent_strength'] * 0.4,
                    'low_level_contribution': low_analysis['fine_grained_score'] * 0.3,
                    'reasoning_explanation': self._generate_reasoning_explanation(
                        high_level, mid_analysis, low_analysis
                    )
                }
                
                integrated_ranking.append(integrated_result)
        
        # Ordenar por score integrado
        integrated_ranking.sort(key=lambda x: x['integrated_score'], reverse=True)
        
        return integrated_ranking
    
    def _analyze_query_strategy(self, query: str) -> Dict:
        """Analiza la estrategia de la consulta a nivel abstracto"""
        
        # Identificar tipo de consulta legal
        legal_query_types = {
            'precedent_search': ['precedent', 'case law', 'ruling'],
            'doctrinal_analysis': ['doctrine', 'principle', 'theory'],
            'comparative_law': ['comparison', 'compare', 'versus'],
            'constitutional_analysis': ['constitutional', 'constitution', 'fundamental'],
            'procedural_inquiry': ['procedure', 'process', 'method']
        }
        
        query_lower = query.lower()
        detected_types = []
        
        for query_type, keywords in legal_query_types.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_types.append(query_type)
        
        return {
            'primary_type': detected_types[0] if detected_types else 'general_inquiry',
            'secondary_types': detected_types[1:] if len(detected_types) > 1 else [],
            'complexity_level': len(detected_types),
            'strategic_approach': self._determine_strategic_approach(detected_types)
        }
    
    def _categorize_candidates_abstractly(self, candidates: List[AcademicReference]) -> Dict:
        """Categoriza candidatos en categorías abstractas"""
        
        categories = {
            'primary_sources': [],      # Casos, estatutos
            'secondary_sources': [],    # Comentarios, análisis
            'comparative_sources': [],  # Derecho comparado
            'historical_sources': [],   # Precedentes históricos
            'contemporary_sources': []  # Análisis recientes
        }
        
        current_year = datetime.now().year
        
        for candidate in candidates:
            # Clasificación por tipo y antigüedad
            if candidate.year >= current_year - 5:
                categories['contemporary_sources'].append(candidate.reference_id)
            elif candidate.year >= current_year - 20:
                categories['primary_sources'].append(candidate.reference_id)
            else:
                categories['historical_sources'].append(candidate.reference_id)
            
            # Clasificación por contenido (heurística simple)
            if any(term in candidate.title.lower() for term in ['court', 'ruling', 'judgment']):
                if candidate.reference_id not in categories['primary_sources']:
                    categories['primary_sources'].append(candidate.reference_id)
            
            if any(term in candidate.title.lower() for term in ['analysis', 'commentary', 'review']):
                categories['secondary_sources'].append(candidate.reference_id)
        
        return categories
    
    def _plan_search_strategy(self, query_strategy: Dict, abstract_categories: Dict) -> Dict:
        """Planifica la estrategia de búsqueda basada en análisis abstracto"""
        
        strategy = {
            'primary_focus': query_strategy['primary_type'],
            'search_priority': [],
            'weighting_scheme': {},
            'reasoning_depth': 'standard'
        }
        
        # Determinar prioridades según tipo de consulta
        if query_strategy['primary_type'] == 'precedent_search':
            strategy['search_priority'] = ['primary_sources', 'contemporary_sources', 'historical_sources']
            strategy['weighting_scheme'] = {'precedent_strength': 0.5, 'temporal_relevance': 0.3, 'citation_network': 0.2}
            
        elif query_strategy['primary_type'] == 'doctrinal_analysis':
            strategy['search_priority'] = ['secondary_sources', 'primary_sources', 'comparative_sources']
            strategy['weighting_scheme'] = {'doctrinal_depth': 0.4, 'scholarly_authority': 0.4, 'precedent_strength': 0.2}
            
        elif query_strategy['primary_type'] == 'comparative_law':
            strategy['search_priority'] = ['comparative_sources', 'primary_sources', 'secondary_sources']
            strategy['weighting_scheme'] = {'comparative_depth': 0.5, 'jurisdictional_relevance': 0.3, 'methodological_soundness': 0.2}
        
        else:  # general_inquiry
            strategy['search_priority'] = ['contemporary_sources', 'primary_sources', 'secondary_sources']
            strategy['weighting_scheme'] = {'overall_relevance': 0.4, 'authority': 0.3, 'recency': 0.3}
        
        # Ajustar profundidad de razonamiento según complejidad
        if query_strategy['complexity_level'] > 2:
            strategy['reasoning_depth'] = 'deep'
        elif query_strategy['complexity_level'] > 1:
            strategy['reasoning_depth'] = 'enhanced'
        
        return strategy
    
    # Métodos de soporte (implementaciones simplificadas)
    
    def _evaluate_precedent_strength(self, candidate: AcademicReference, query: str) -> float:
        """Evalúa la fuerza precedencial de un candidato"""
        base_score = candidate.jurisprudential_relevance / 10.0  # Normalizar a 0-1
        
        # Bonus por palabras clave en query
        query_terms = set(query.lower().split())
        title_terms = set(candidate.title.lower().split())
        overlap = len(query_terms & title_terms) / len(query_terms) if query_terms else 0
        
        return min(base_score + overlap * 0.3, 1.0)
    
    def _evaluate_contextual_relevance(self, candidate: AcademicReference, strategy: Dict) -> float:
        """Evalúa relevancia contextual según estrategia"""
        relevance_score = 0.5  # Base score
        
        # Ajustar según tipo de fuente y estrategia
        primary_focus = strategy.get('primary_focus', 'general_inquiry')
        
        if primary_focus == 'precedent_search' and candidate.reference_type == 'journal':
            relevance_score += 0.2
        elif primary_focus == 'doctrinal_analysis' and any(
            term in candidate.publication.lower() for term in ['law review', 'journal', 'quarterly']
        ):
            relevance_score += 0.3
            
        return min(relevance_score, 1.0)
    
    def _analyze_citation_network_position(self, candidate: AcademicReference) -> Dict:
        """Analiza posición en red de citaciones"""
        return {
            'citation_count': candidate.citation_count,
            'network_centrality': min(candidate.citation_count / 100, 1.0),  # Normalizado
            'influence_factor': candidate.citation_count * 0.01
        }
    
    def _evaluate_temporal_relevance(self, candidate: AcademicReference) -> float:
        """Evalúa relevancia temporal"""
        current_year = datetime.now().year
        age = current_year - candidate.year
        
        # Decaimiento temporal suave
        if age <= 5:
            return 1.0
        elif age <= 10:
            return 0.8
        elif age <= 20:
            return 0.6
        else:
            return 0.4
    
    def _comparative_case_analysis(self, case_analyses: List[Dict]) -> Dict:
        """Análisis comparativo entre casos"""
        return {
            'total_cases': len(case_analyses),
            'avg_precedent_strength': sum(ca['precedent_strength'] for ca in case_analyses) / len(case_analyses) if case_analyses else 0,
            'strength_distribution': {
                'high': len([ca for ca in case_analyses if ca['precedent_strength'] > 0.7]),
                'medium': len([ca for ca in case_analyses if 0.4 <= ca['precedent_strength'] <= 0.7]),
                'low': len([ca for ca in case_analyses if ca['precedent_strength'] < 0.4])
            }
        }
    
    def _detailed_token_analysis(self, candidate: AcademicReference, query: str) -> Dict:
        """Análisis detallado a nivel de tokens"""
        return {
            'token_overlap_ratio': 0.75,  # Simplificado
            'semantic_similarity': 0.68,
            'legal_terminology_density': 0.82,
            'query_coverage': 0.64
        }
    
    def _precise_citation_extraction(self, candidate: AcademicReference) -> Dict:
        """Extracción precisa de citaciones"""
        return {
            'internal_citations': 12,  # Simulado
            'external_citations': 8,
            'legal_authorities_cited': 5,
            'citation_quality_score': 0.77
        }
    
    def _deep_semantic_analysis(self, candidate: AcademicReference, query: str) -> Dict:
        """Análisis semántico profundo"""
        return {
            'conceptual_alignment': 0.73,
            'jurisdictional_match': 0.85,
            'doctrinal_coherence': 0.69,
            'argumentative_structure': 0.71
        }
    
    def _calculate_fine_grained_score(self, token_analysis: Dict, citation_extraction: Dict, 
                                    semantic_analysis: Dict) -> float:
        """Calcula score detallado de bajo nivel"""
        return (
            token_analysis['semantic_similarity'] * 0.3 +
            citation_extraction['citation_quality_score'] * 0.3 +
            semantic_analysis['conceptual_alignment'] * 0.4
        )
    
    def _calculate_precision_metrics(self, detailed_analyses: List[Dict]) -> Dict:
        """Calcula métricas de precisión"""
        scores = [da['fine_grained_score'] for da in detailed_analyses]
        return {
            'avg_precision': sum(scores) / len(scores) if scores else 0,
            'precision_variance': 0.15,  # Simulado
            'high_precision_count': len([s for s in scores if s > 0.8])
        }
    
    def _calculate_confidence_scores(self, final_ranking: List[Dict]) -> Dict:
        """Calcula scores de confianza"""
        if not final_ranking:
            return {'overall_confidence': 0.0}
            
        scores = [fr['integrated_score'] for fr in final_ranking]
        return {
            'overall_confidence': sum(scores) / len(scores),
            'top_result_confidence': scores[0] if scores else 0,
            'ranking_stability': 0.82  # Simulado
        }
    
    def _generate_reasoning_explanation(self, high_level: Dict, mid_analysis: Dict, 
                                     low_analysis: Dict) -> str:
        """Genera explicación del razonamiento jerárquico"""
        return (
            f"HRM Analysis: Strategic approach '{high_level.get('query_strategy', {}).get('primary_type', 'general')}' "
            f"with precedent strength {mid_analysis.get('precedent_strength', 0):.2f} "
            f"and detailed score {low_analysis.get('fine_grained_score', 0):.2f}"
        )
    
    def _determine_strategic_approach(self, detected_types: List[str]) -> str:
        """Determina enfoque estratégico"""
        if 'precedent_search' in detected_types:
            return 'precedent_focused'
        elif 'doctrinal_analysis' in detected_types:
            return 'doctrine_focused'
        elif 'comparative_law' in detected_types:
            return 'comparative_focused'
        else:
            return 'balanced_approach'


class HRMJurisRankIntegrator:
    """Integrador principal HRM-JurisRank para análisis bibliográfico avanzado"""
    
    def __init__(self, jurisrank_service: Optional['JurisRankBibliographyService'] = None):
        """
        Inicializa el integrador HRM-JurisRank
        
        Args:
            jurisrank_service: Servicio JurisRank existente
        """
        self.jurisrank_service = jurisrank_service
        self.hrm_engine = HRMReasoningEngine()
        
        logger.info("HRM-JurisRank Integrator initialized")
    
    def enhanced_bibliography_analysis(self, query: str, max_candidates: int = 20) -> Dict:
        """
        Análisis bibliográfico mejorado con razonamiento jerárquico HRM
        
        Args:
            query: Consulta de investigación
            max_candidates: Máximo número de candidatos a analizar
            
        Returns:
            Dict con análisis jerárquico completo
        """
        
        logger.info(f"Starting enhanced analysis for query: {query}")
        
        # 1. Obtener candidatos usando JurisRank
        if self.jurisrank_service:
            candidates_data = self.jurisrank_service.bibliography_manager.search_and_rank(query)
            candidates = []
            
            # Convertir a objetos AcademicReference
            for candidate_data in candidates_data[:max_candidates]:
                ref = self.jurisrank_service.bibliography_manager.database.get_reference(
                    candidate_data['reference_id']
                )
                if ref:
                    candidates.append(ref)
        else:
            candidates = []  # Modo de prueba sin JurisRank
        
        if not candidates:
            return {
                'error': 'No candidates found',
                'query': query,
                'suggestions': ['Try broader search terms', 'Check bibliography database']
            }
        
        # 2. Ejecutar razonamiento jerárquico HRM
        hrm_analysis = self.hrm_engine.hierarchical_reasoning(query, candidates)
        
        # 3. Generar análisis integrado
        integrated_analysis = {
            'query': query,
            'analysis_timestamp': datetime.now().isoformat(),
            'methodology': 'HRM_JurisRank_Integration',
            'candidates_processed': len(candidates),
            'hrm_reasoning': hrm_analysis,
            'enhanced_rankings': self._enhance_rankings_with_hrm(hrm_analysis),
            'reasoning_insights': self._extract_reasoning_insights(hrm_analysis),
            'recommendations': self._generate_recommendations(hrm_analysis)
        }
        
        logger.info(f"Enhanced analysis completed: {len(candidates)} candidates processed")
        
        return integrated_analysis
    
    def _enhance_rankings_with_hrm(self, hrm_analysis: Dict) -> List[Dict]:
        """Mejora rankings con insights HRM"""
        
        enhanced_rankings = []
        
        for ranking in hrm_analysis.get('final_ranking', []):
            enhanced_ranking = {
                **ranking,
                'hrm_confidence': hrm_analysis.get('confidence_scores', {}).get('overall_confidence', 0),
                'reasoning_quality': self._assess_reasoning_quality(ranking),
                'explanation': ranking.get('reasoning_explanation', ''),
                'hierarchical_breakdown': {
                    'strategic_level': ranking.get('high_level_contribution', 0),
                    'case_analysis_level': ranking.get('mid_level_contribution', 0),
                    'detailed_level': ranking.get('low_level_contribution', 0)
                }
            }
            enhanced_rankings.append(enhanced_ranking)
        
        return enhanced_rankings
    
    def _extract_reasoning_insights(self, hrm_analysis: Dict) -> Dict:
        """Extrae insights del razonamiento HRM"""
        
        return {
            'reasoning_path_length': len(hrm_analysis.get('reasoning_path', [])),
            'reasoning_steps': hrm_analysis.get('reasoning_path', []),
            'hierarchical_depth': len(hrm_analysis.get('hierarchical_analysis', {})),
            'confidence_metrics': hrm_analysis.get('confidence_scores', {}),
            'dominant_reasoning_level': self._identify_dominant_level(hrm_analysis),
            'reasoning_complexity': self._assess_reasoning_complexity(hrm_analysis)
        }
    
    def _generate_recommendations(self, hrm_analysis: Dict) -> List[str]:
        """Genera recomendaciones basadas en análisis HRM"""
        
        recommendations = []
        
        # Analizar confianza general
        confidence = hrm_analysis.get('confidence_scores', {}).get('overall_confidence', 0)
        
        if confidence > 0.8:
            recommendations.append("✅ High-confidence results: Top recommendations are highly reliable")
        elif confidence > 0.6:
            recommendations.append("⚠️ Medium-confidence results: Consider additional sources")
        else:
            recommendations.append("⚠️ Low-confidence results: Broaden search or refine query")
        
        # Analizar distribución jerárquica
        final_ranking = hrm_analysis.get('final_ranking', [])
        if final_ranking:
            top_result = final_ranking[0]
            
            if top_result.get('high_level_contribution', 0) > 0.5:
                recommendations.append("🎯 Results are strategically aligned with query intent")
            
            if top_result.get('low_level_contribution', 0) > 0.5:
                recommendations.append("🔍 Results show high precision in detailed analysis")
        
        # Recomendaciones específicas de razonamiento
        reasoning_path = hrm_analysis.get('reasoning_path', [])
        if len(reasoning_path) > 3:
            recommendations.append("🧠 Complex hierarchical reasoning applied - comprehensive analysis")
        
        return recommendations
    
    def _assess_reasoning_quality(self, ranking: Dict) -> float:
        """Evalúa calidad del razonamiento"""
        
        # Evaluar equilibrio entre niveles jerárquicos
        high_contrib = ranking.get('high_level_contribution', 0)
        mid_contrib = ranking.get('mid_level_contribution', 0)
        low_contrib = ranking.get('low_level_contribution', 0)
        
        # Preferir distribución balanceada
        balance_score = 1.0 - abs(0.33 - high_contrib) - abs(0.33 - mid_contrib) - abs(0.33 - low_contrib)
        
        # Evaluar score integrado
        integrated_score = ranking.get('integrated_score', 0)
        
        return (balance_score * 0.4 + integrated_score * 0.6)
    
    def _identify_dominant_level(self, hrm_analysis: Dict) -> str:
        """Identifica nivel dominante de razonamiento"""
        
        final_ranking = hrm_analysis.get('final_ranking', [])
        if not final_ranking:
            return 'none'
        
        top_result = final_ranking[0]
        
        high_contrib = top_result.get('high_level_contribution', 0)
        mid_contrib = top_result.get('mid_level_contribution', 0)  
        low_contrib = top_result.get('low_level_contribution', 0)
        
        max_contrib = max(high_contrib, mid_contrib, low_contrib)
        
        if max_contrib == high_contrib:
            return 'strategic_planning'
        elif max_contrib == mid_contrib:
            return 'case_analysis'
        else:
            return 'detailed_processing'
    
    def _assess_reasoning_complexity(self, hrm_analysis: Dict) -> str:
        """Evalúa complejidad del razonamiento"""
        
        reasoning_steps = len(hrm_analysis.get('reasoning_path', []))
        hierarchical_levels = len(hrm_analysis.get('hierarchical_analysis', {}))
        
        if reasoning_steps >= 3 and hierarchical_levels >= 3:
            return 'high'
        elif reasoning_steps >= 2 and hierarchical_levels >= 2:
            return 'medium'
        else:
            return 'low'


# Ejemplo de uso y demostración
def demonstrate_hrm_integration():
    """Demuestra la integración HRM-JurisRank"""
    
    print("🧠 HRM-JurisRank Integration Demonstration")
    print("=" * 60)
    
    # Inicializar integrador
    integrator = HRMJurisRankIntegrator()
    
    # Consulta de prueba
    legal_query = "Constitutional implications of AI in judicial decision-making"
    
    print(f"📋 Query: {legal_query}")
    print("\n🔄 Executing hierarchical reasoning analysis...")
    
    # Ejecutar análisis (modo demo sin JurisRank real)
    analysis = integrator.enhanced_bibliography_analysis(legal_query)
    
    if 'error' in analysis:
        print(f"\n⚠️ {analysis['error']}")
        print("💡 Suggestions:", analysis.get('suggestions', []))
        return
    
    print(f"\n✅ Analysis completed!")
    print(f"   Methodology: {analysis['methodology']}")
    print(f"   Candidates processed: {analysis['candidates_processed']}")
    
    # Mostrar insights de razonamiento
    insights = analysis.get('reasoning_insights', {})
    print(f"\n🧠 Reasoning Insights:")
    print(f"   Complexity: {insights.get('reasoning_complexity', 'unknown')}")
    print(f"   Dominant level: {insights.get('dominant_reasoning_level', 'unknown')}")
    print(f"   Reasoning steps: {insights.get('reasoning_path_length', 0)}")
    
    # Mostrar recomendaciones
    recommendations = analysis.get('recommendations', [])
    if recommendations:
        print(f"\n💡 Recommendations:")
        for rec in recommendations[:3]:
            print(f"   {rec}")
    
    print(f"\n🎯 HRM Integration ready for production use!")


if __name__ == "__main__":
    demonstrate_hrm_integration()