#!/usr/bin/env python3
"""
JurisRank Bibliography Integration Module
Integración avanzada del sistema de gestión bibliográfica con JurisRank API
Permite análisis cruzado entre referencias académicas y datos jurisprudenciales
"""

import requests
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging
from dataclasses import asdict
import sys
import os

# Importar los módulos locales
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from bibliography_manager import JurisRankBibliographyManager, AcademicReference
except ImportError as e:
    print(f"Error importing bibliography_manager: {e}")
    sys.exit(1)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JurisRankAPIClient:
    """Cliente para interactuar con la API principal de JurisRank"""
    
    def __init__(self, base_url: str = "https://api.jurisrank.com", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        # Configurar headers por defecto
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'JurisRank-Bibliography-Manager/1.0.0'
        })
        
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}'
            })
    
    def analyze_authority(self, case_text: str, reference_context: Optional[Dict] = None) -> Dict:
        """
        Analiza la autoridad jurisprudencial de un caso usando JurisRank
        
        Args:
            case_text: Texto del caso o referencia legal
            reference_context: Contexto adicional de la referencia académica
            
        Returns:
            Dict con el análisis de autoridad
        """
        try:
            payload = {
                'text': case_text,
                'analysis_type': 'authority_scoring',
                'metadata': reference_context or {}
            }
            
            response = self.session.post(f"{self.base_url}/v1/analyze/authority", json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"JurisRank API returned status {response.status_code}")
                return {'error': f'API request failed: {response.status_code}', 'authority_score': 0.0}
                
        except Exception as e:
            logger.error(f"Error calling JurisRank API: {str(e)}")
            return {'error': str(e), 'authority_score': 0.0}
    
    def search_precedents(self, query: str, legal_system: str = "mixed") -> List[Dict]:
        """
        Busca precedentes legales relacionados con la consulta
        
        Args:
            query: Consulta de búsqueda
            legal_system: Sistema legal (common_law, civil_law, mixed)
            
        Returns:
            Lista de precedentes encontrados
        """
        try:
            params = {
                'query': query,
                'legal_system': legal_system,
                'limit': 20
            }
            
            response = self.session.get(f"{self.base_url}/v1/precedents/search", params=params)
            
            if response.status_code == 200:
                return response.json().get('precedents', [])
            else:
                logger.warning(f"Precedents search returned status {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error searching precedents: {str(e)}")
            return []
    
    def get_citation_network(self, case_id: str) -> Dict:
        """
        Obtiene la red de citaciones para un caso específico
        
        Args:
            case_id: ID del caso
            
        Returns:
            Dict con la red de citaciones
        """
        try:
            response = self.session.get(f"{self.base_url}/v1/cases/{case_id}/citations")
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Citation network request returned status {response.status_code}")
                return {'nodes': [], 'edges': []}
                
        except Exception as e:
            logger.error(f"Error getting citation network: {str(e)}")
            return {'nodes': [], 'edges': []}


class EnhancedBibliographyAnalyzer:
    """Analizador bibliográfico mejorado con integración JurisRank"""
    
    def __init__(self, jurisrank_client: Optional[JurisRankAPIClient] = None):
        self.bibliography_manager = JurisRankBibliographyManager()
        self.jurisrank_client = jurisrank_client or JurisRankAPIClient()
        
        # Keywords específicos para análisis jurisprudencial
        self.legal_topics = {
            'constitutional_law': ['constitutional', 'constitution', 'fundamental rights', 'bill of rights'],
            'criminal_law': ['criminal', 'crime', 'prosecution', 'defendant', 'guilty', 'sentence'],
            'civil_law': ['civil', 'tort', 'contract', 'damages', 'liability', 'negligence'],
            'administrative_law': ['administrative', 'regulation', 'agency', 'bureaucracy', 'public administration'],
            'international_law': ['international', 'treaty', 'convention', 'diplomatic', 'sovereignty'],
            'commercial_law': ['commercial', 'business', 'corporate', 'company', 'trade', 'commerce'],
            'family_law': ['family', 'marriage', 'divorce', 'custody', 'adoption', 'domestic'],
            'property_law': ['property', 'real estate', 'ownership', 'possession', 'title', 'land'],
            'labor_law': ['labor', 'employment', 'worker', 'union', 'workplace', 'wages'],
            'environmental_law': ['environmental', 'pollution', 'climate', 'sustainability', 'ecology']
        }
    
    def enhanced_relevance_analysis(self, reference: AcademicReference) -> Dict:
        """
        Análisis de relevancia mejorado que incluye JurisRank scoring
        
        Args:
            reference: Referencia académica a analizar
            
        Returns:
            Dict con análisis completo de relevancia
        """
        # Análisis básico de relevancia
        basic_relevance = self.bibliography_manager.analyzer.calculate_jurisprudential_relevance(reference)
        
        # Análisis de temas legales específicos
        legal_topics = self._analyze_legal_topics(reference)
        
        # Intentar obtener scoring de JurisRank si es aplicable
        jurisrank_score = 0.0
        precedent_connections = []
        
        if self._is_legal_reference(reference):
            try:
                # Crear contexto para JurisRank
                context = {
                    'title': reference.title,
                    'authors': reference.authors,
                    'year': reference.year,
                    'publication': reference.publication,
                    'reference_type': reference.reference_type
                }
                
                # Analizar autoridad con JurisRank
                authority_analysis = self.jurisrank_client.analyze_authority(
                    reference.title + " " + (reference.abstract or ""),
                    context
                )
                
                jurisrank_score = authority_analysis.get('authority_score', 0.0)
                
                # Buscar precedentes relacionados
                precedents = self.jurisrank_client.search_precedents(
                    reference.title + " " + " ".join(reference.keywords or [])
                )
                
                precedent_connections = precedents[:5]  # Top 5 precedentes
                
            except Exception as e:
                logger.warning(f"JurisRank integration failed for reference {reference.reference_id}: {str(e)}")
        
        # Calcular score combinado
        combined_score = self._calculate_combined_relevance(
            basic_relevance, jurisrank_score, legal_topics
        )
        
        return {
            'basic_relevance': basic_relevance,
            'jurisrank_authority_score': jurisrank_score,
            'combined_relevance': combined_score,
            'legal_topics': legal_topics,
            'precedent_connections': precedent_connections,
            'is_legal_reference': self._is_legal_reference(reference),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _analyze_legal_topics(self, reference: AcademicReference) -> Dict[str, float]:
        """Analiza temas legales específicos en la referencia"""
        
        # Combinar texto relevante
        text_to_analyze = f"{reference.title} {reference.publication} {' '.join(reference.keywords or [])}"
        if reference.abstract:
            text_to_analyze += f" {reference.abstract}"
        
        text_lower = text_to_analyze.lower()
        
        topic_scores = {}
        
        for topic, keywords in self.legal_topics.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                # Normalizar score por número de keywords del tema
                topic_scores[topic] = min(score / len(keywords), 1.0)
        
        return topic_scores
    
    def _is_legal_reference(self, reference: AcademicReference) -> bool:
        """Determina si una referencia es específicamente legal/jurisprudencial"""
        
        legal_indicators = [
            'law', 'legal', 'jurisprudence', 'court', 'judicial', 'justice',
            'legislation', 'statute', 'regulation', 'precedent', 'case law',
            'constitutional', 'criminal', 'civil rights', 'tort', 'contract'
        ]
        
        text_to_check = f"{reference.title} {reference.publication}".lower()
        
        return any(indicator in text_to_check for indicator in legal_indicators)
    
    def _calculate_combined_relevance(self, basic_score: float, jurisrank_score: float, 
                                   legal_topics: Dict[str, float]) -> float:
        """Calcula un score de relevancia combinado"""
        
        # Peso de los componentes
        basic_weight = 0.4
        jurisrank_weight = 0.4
        topics_weight = 0.2
        
        # Score de temas legales (promedio de temas detectados)
        topics_score = sum(legal_topics.values()) / len(legal_topics) if legal_topics else 0.0
        
        combined = (basic_score * basic_weight + 
                   jurisrank_score * jurisrank_weight + 
                   topics_score * 10 * topics_weight)  # Escalar topics_score
        
        return min(combined, 10.0)  # Máximo 10.0
    
    def generate_cross_platform_report(self, references: List[AcademicReference]) -> Dict:
        """
        Genera un reporte que combina análisis bibliográfico con datos de JurisRank
        
        Args:
            references: Lista de referencias a analizar
            
        Returns:
            Dict con reporte completo cross-platform
        """
        
        report = {
            'metadata': {
                'total_references': len(references),
                'analysis_timestamp': datetime.now().isoformat(),
                'jurisrank_integration': self.jurisrank_client is not None
            },
            'relevance_analysis': {
                'basic_scores': [],
                'jurisrank_scores': [],
                'combined_scores': [],
                'legal_references_count': 0
            },
            'legal_topics_distribution': {},
            'precedent_connections': [],
            'top_legal_references': [],
            'network_analysis': {
                'nodes': [],
                'edges': []
            }
        }
        
        # Analizar cada referencia
        for ref in references:
            enhanced_analysis = self.enhanced_relevance_analysis(ref)
            
            # Recopilar scores
            report['relevance_analysis']['basic_scores'].append(enhanced_analysis['basic_relevance'])
            report['relevance_analysis']['jurisrank_scores'].append(enhanced_analysis['jurisrank_authority_score'])
            report['relevance_analysis']['combined_scores'].append(enhanced_analysis['combined_relevance'])
            
            if enhanced_analysis['is_legal_reference']:
                report['relevance_analysis']['legal_references_count'] += 1
                
                # Agregar a top referencias legales
                report['top_legal_references'].append({
                    'reference_id': ref.reference_id,
                    'title': ref.title,
                    'authors': ref.authors,
                    'year': ref.year,
                    'combined_relevance': enhanced_analysis['combined_relevance'],
                    'legal_topics': enhanced_analysis['legal_topics'],
                    'precedent_connections_count': len(enhanced_analysis['precedent_connections'])
                })
            
            # Agregar temas legales a la distribución
            for topic, score in enhanced_analysis['legal_topics'].items():
                if topic not in report['legal_topics_distribution']:
                    report['legal_topics_distribution'][topic] = []
                report['legal_topics_distribution'][topic].append(score)
            
            # Recopilar conexiones de precedentes
            for precedent in enhanced_analysis['precedent_connections']:
                report['precedent_connections'].append({
                    'reference_id': ref.reference_id,
                    'precedent': precedent
                })
        
        # Calcular estadísticas resumidas
        if report['relevance_analysis']['basic_scores']:
            report['relevance_analysis']['basic_average'] = sum(report['relevance_analysis']['basic_scores']) / len(report['relevance_analysis']['basic_scores'])
            report['relevance_analysis']['jurisrank_average'] = sum(report['relevance_analysis']['jurisrank_scores']) / len(report['relevance_analysis']['jurisrank_scores'])
            report['relevance_analysis']['combined_average'] = sum(report['relevance_analysis']['combined_scores']) / len(report['relevance_analysis']['combined_scores'])
        
        # Procesar distribución de temas legales
        for topic, scores in report['legal_topics_distribution'].items():
            report['legal_topics_distribution'][topic] = {
                'count': len(scores),
                'average_score': sum(scores) / len(scores),
                'max_score': max(scores)
            }
        
        # Ordenar top referencias legales
        report['top_legal_references'].sort(key=lambda x: x['combined_relevance'], reverse=True)
        report['top_legal_references'] = report['top_legal_references'][:10]  # Top 10
        
        return report
    
    def export_enhanced_bibliography(self, format: str = "json", 
                                   include_jurisrank_data: bool = True) -> str:
        """
        Exporta bibliografía con análisis mejorado incluyendo datos de JurisRank
        
        Args:
            format: Formato de exportación (json, enhanced_apa, enhanced_bibtex)
            include_jurisrank_data: Incluir datos de JurisRank en la exportación
            
        Returns:
            String con la bibliografía exportada
        """
        
        # Obtener todas las referencias
        references = self.bibliography_manager.database.search_references()
        
        if not references:
            return json.dumps({'error': 'No references found'})
        
        enhanced_references = []
        
        # Realizar análisis mejorado para cada referencia
        for ref in references:
            enhanced_data = {
                'reference': asdict(ref),
                'enhanced_analysis': None
            }
            
            if include_jurisrank_data:
                enhanced_data['enhanced_analysis'] = self.enhanced_relevance_analysis(ref)
            
            enhanced_references.append(enhanced_data)
        
        if format.lower() == "json":
            return json.dumps(enhanced_references, default=str, indent=2, ensure_ascii=False)
        
        elif format.lower() == "enhanced_apa":
            return self._export_enhanced_apa(enhanced_references)
        
        elif format.lower() == "enhanced_bibtex":
            return self._export_enhanced_bibtex(enhanced_references)
        
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_enhanced_apa(self, enhanced_references: List[Dict]) -> str:
        """Exporta en formato APA mejorado con scores de relevancia"""
        
        apa_entries = []
        
        for item in enhanced_references:
            ref = item['reference']
            analysis = item.get('enhanced_analysis')
            
            # Formatear autores
            authors = ref['authors']
            if len(authors) == 1:
                authors_str = authors[0]
            elif len(authors) == 2:
                authors_str = f"{authors[0]} & {authors[1]}"
            else:
                authors_str = f"{', '.join(authors[:-1])}, & {authors[-1]}"
            
            # Construir cita APA básica
            entry = f"{authors_str} ({ref['year']}). {ref['title']}. "
            
            if ref['reference_type'] == "journal":
                entry += f"{ref['publication']}"
                if ref.get('volume'):
                    entry += f", {ref['volume']}"
                if ref.get('issue'):
                    entry += f"({ref['issue']})"
                if ref.get('pages'):
                    entry += f", {ref['pages']}"
            else:
                entry += f"{ref['publication']}"
            
            if ref.get('url'):
                entry += f" Retrieved from {ref['url']}"
            
            entry += "."
            
            # Agregar información de análisis mejorado
            if analysis:
                entry += f"\n    [JurisRank Combined Relevance: {analysis['combined_relevance']:.2f}"
                if analysis['legal_topics']:
                    topics = ", ".join(analysis['legal_topics'].keys())
                    entry += f" | Legal Topics: {topics}"
                entry += "]"
            
            entry += "\n\n"
            apa_entries.append(entry)
        
        return "".join(apa_entries)
    
    def _export_enhanced_bibtex(self, enhanced_references: List[Dict]) -> str:
        """Exporta en formato BibTeX mejorado con metadatos de JurisRank"""
        
        bibtex_entries = []
        
        for item in enhanced_references:
            ref = item['reference']
            analysis = item.get('enhanced_analysis')
            
            authors_str = " and ".join(ref['authors'])
            entry_type = "article" if ref['reference_type'] == "journal" else ref['reference_type']
            
            entry = f"@{entry_type}{{{ref['reference_id']},\n"
            entry += f"  author = {{{authors_str}}},\n"
            entry += f"  title = {{{ref['title']}}},\n"
            entry += f"  year = {{{ref['year']}}},\n"
            entry += f"  journal = {{{ref['publication']}}},\n"
            
            if ref.get('volume'):
                entry += f"  volume = {{{ref['volume']}}},\n"
            if ref.get('issue'):
                entry += f"  number = {{{ref['issue']}}},\n"
            if ref.get('pages'):
                entry += f"  pages = {{{ref['pages']}}},\n"
            if ref.get('doi'):
                entry += f"  doi = {{{ref['doi']}}},\n"
            if ref.get('url'):
                entry += f"  url = {{{ref['url']}}},\n"
            
            # Agregar metadatos de JurisRank
            if analysis:
                entry += f"  jurisrank_relevance = {{{analysis['combined_relevance']:.2f}}},\n"
                entry += f"  jurisrank_authority = {{{analysis['jurisrank_authority_score']:.2f}}},\n"
                if analysis['legal_topics']:
                    topics_str = ", ".join(analysis['legal_topics'].keys())
                    entry += f"  legal_topics = {{{topics_str}}},\n"
            
            entry += "}\n\n"
            bibtex_entries.append(entry)
        
        return "".join(bibtex_entries)


class JurisRankBibliographyService:
    """Servicio completo que integra gestión bibliográfica con JurisRank"""
    
    def __init__(self, jurisrank_api_key: Optional[str] = None, 
                 jurisrank_base_url: str = "https://api.jurisrank.com"):
        
        # Inicializar componentes
        self.jurisrank_client = JurisRankAPIClient(jurisrank_base_url, jurisrank_api_key)
        self.enhanced_analyzer = EnhancedBibliographyAnalyzer(self.jurisrank_client)
        self.bibliography_manager = self.enhanced_analyzer.bibliography_manager
        
        logger.info("JurisRank Bibliography Service initialized")
    
    def process_legal_document(self, document_text: str, document_metadata: Dict) -> Dict:
        """
        Procesa un documento legal completo extrayendo referencias y analizándolas
        
        Args:
            document_text: Texto completo del documento
            document_metadata: Metadatos del documento (título, autor, fecha, etc.)
            
        Returns:
            Dict con análisis completo del documento
        """
        
        logger.info(f"Processing legal document: {document_metadata.get('title', 'Unknown')}")
        
        # Extraer referencias del documento
        import_results = self.bibliography_manager.import_references_from_text(document_text)
        
        # Realizar análisis cruzado con JurisRank
        references = self.bibliography_manager.database.search_references()
        cross_platform_report = self.enhanced_analyzer.generate_cross_platform_report(references)
        
        # Analizar autoridad del documento completo con JurisRank
        document_authority = self.jurisrank_client.analyze_authority(
            document_text[:5000],  # Primeros 5000 caracteres
            document_metadata
        )
        
        return {
            'document_metadata': document_metadata,
            'import_results': import_results,
            'cross_platform_analysis': cross_platform_report,
            'document_authority_analysis': document_authority,
            'processing_timestamp': datetime.now().isoformat(),
            'recommendations': self._generate_recommendations(cross_platform_report)
        }
    
    def _generate_recommendations(self, analysis_report: Dict) -> List[str]:
        """Genera recomendaciones basadas en el análisis"""
        
        recommendations = []
        
        # Análisis de la calidad de referencias
        avg_relevance = analysis_report['relevance_analysis'].get('combined_average', 0)
        
        if avg_relevance < 3.0:
            recommendations.append(
                "📚 Consider including more high-quality legal references to strengthen the jurisprudential foundation"
            )
        
        if analysis_report['relevance_analysis']['legal_references_count'] == 0:
            recommendations.append(
                "⚖️ This document lacks direct legal references. Consider adding relevant case law or jurisprudential sources"
            )
        
        # Análisis de diversidad temática
        topics_count = len(analysis_report['legal_topics_distribution'])
        
        if topics_count < 2:
            recommendations.append(
                "🌐 Consider broadening the legal scope by including references from different legal domains"
            )
        
        # Análisis de precedentes
        precedent_count = len(analysis_report['precedent_connections'])
        
        if precedent_count > 0:
            recommendations.append(
                f"🏛️ Found {precedent_count} relevant precedent connections. Consider exploring these for deeper legal analysis"
            )
        
        # Análisis temporal
        if analysis_report.get('temporal_distribution'):
            recommendations.append(
                "📅 Consider the temporal relevance of references and include recent developments in the field"
            )
        
        return recommendations


# Ejemplo de uso y testing
if __name__ == "__main__":
    print("=== JurisRank Bibliography Integration - Demo ===\n")
    
    # Inicializar el servicio
    service = JurisRankBibliographyService()
    
    # Texto de ejemplo con referencias académicas y contenido legal
    sample_legal_document = """
    Analysis of Artificial Intelligence in Legal Decision Making
    
    This document examines the growing role of artificial intelligence in judicial processes
    and its implications for jurisprudential authority. The following references provide
    the theoretical foundation for this analysis:
    
    Spielberger, Charles D, Gerald Jacobs, Sheryl Russell, and Rosario S Crane (2013). 
    "Assessment of Anger: The State-Trait Anger Scale," in Advances in Personality Assessment: 
    Routledge, 161-89.

    Valenzuela, Ana, Stefano Puntoni, Donna Hoffman, Noah Castelo, Julian De Freitas, Berkeley
    Dietvorst, Christian Hildebrand, Young Eun Huh, Robert Meyer, and Miriam E Sweeney (2024). 
    "How Artificial Intelligence Constrains the Human Experience," Journal of the Association 
    for Consumer Research, 9 (3), 000-00.

    Waytz, Adam, Joy Heafner, and Nicholas Epley (2014). "The Mind in the Machine: 
    Anthropomorphism Increases Trust in an Autonomous Vehicle," Journal of Experimental 
    Social Psychology, 52, 113-17.
    
    The integration of AI systems in legal decision-making processes raises fundamental
    questions about the nature of judicial authority and the role of human judgment in
    legal interpretation. Recent developments in machine learning algorithms have enabled
    more sophisticated analysis of legal precedents, potentially augmenting judicial
    decision-making capabilities.
    """
    
    document_metadata = {
        'title': 'Analysis of Artificial Intelligence in Legal Decision Making',
        'author': 'Research Team',
        'document_type': 'legal_analysis',
        'jurisdiction': 'international',
        'date': '2024-08-28'
    }
    
    print("1. Processing legal document with integrated analysis...")
    
    # Procesar documento
    analysis_results = service.process_legal_document(sample_legal_document, document_metadata)
    
    print(f"✅ Document processed successfully")
    print(f"📊 References imported: {analysis_results['import_results']['imported']}")
    print(f"⚖️ Legal references detected: {analysis_results['cross_platform_analysis']['relevance_analysis']['legal_references_count']}")
    print(f"🎯 Average combined relevance: {analysis_results['cross_platform_analysis']['relevance_analysis'].get('combined_average', 0):.2f}")
    
    print(f"\n🏷️ Legal topics identified:")
    for topic, data in analysis_results['cross_platform_analysis']['legal_topics_distribution'].items():
        print(f"   - {topic.replace('_', ' ').title()}: {data['count']} references (avg score: {data['average_score']:.2f})")
    
    print(f"\n💡 Recommendations:")
    for rec in analysis_results['recommendations']:
        print(f"   {rec}")
    
    print("\n" + "="*60)
    
    # Demostración de exportación mejorada
    print("2. Generating enhanced bibliography export...")
    
    enhanced_export = service.enhanced_analyzer.export_enhanced_bibliography(
        format="enhanced_apa", 
        include_jurisrank_data=True
    )
    
    print("✅ Enhanced APA bibliography generated:")
    print(enhanced_export[:500] + "..." if len(enhanced_export) > 500 else enhanced_export)
    
    print("\n" + "="*60)
    
    print("3. Cross-platform analysis completed!")
    print("🚀 JurisRank Bibliography Integration is ready for production use.")
    print("📚 The system successfully combines academic reference management with jurisprudential analysis.")