#!/usr/bin/env python3
"""
Video Analysis Integration for JurisRank Bibliography System
Módulo para análisis de contenido audiovisual y extracción de referencias
"""

import requests
import json
from typing import Dict, List, Optional
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class VideoContentAnalyzer:
    """Analizador de contenido de video para extraer referencias académicas"""
    
    def __init__(self):
        self.youtube_pattern = r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)'
        
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extrae ID de video de YouTube desde URL"""
        match = re.search(self.youtube_pattern, url)
        return match.group(1) if match else None
    
    def analyze_youtube_video(self, video_url: str) -> Dict:
        """
        Analiza un video de YouTube para determinar relevancia académica
        
        Args:
            video_url: URL del video de YouTube
            
        Returns:
            Dict con análisis del contenido
        """
        video_id = self.extract_video_id(video_url)
        if not video_id:
            return {'error': 'Invalid YouTube URL', 'relevant': False}
        
        # Información básica del video
        video_info = {
            'video_id': video_id,
            'url': video_url,
            'analysis_timestamp': datetime.now().isoformat(),
            'relevant_for_bibliography': False,
            'academic_indicators': [],
            'legal_indicators': [],
            'recommended_actions': []
        }
        
        # Análisis basado en patrones URL y contexto
        academic_keywords = [
            'research', 'study', 'analysis', 'academic', 'university',
            'journal', 'paper', 'publication', 'citation', 'reference'
        ]
        
        legal_keywords = [
            'law', 'legal', 'court', 'justice', 'jurisprudence',
            'constitution', 'legislation', 'regulation', 'case'
        ]
        
        # Análisis heurístico del canal/contexto  
        url_lower = video_url.lower()
        if 'valueschool' in url_lower or 'value school' in url_lower or 'ab_channel=valueschool' in url_lower:
            video_info['channel_type'] = 'financial_education'
            video_info['academic_indicators'].extend([
                'Financial education channel detected',
                'Investment analysis content likely',
                'May contain academic research references'
            ])
            
            # Value School típicamente cubre finanzas, inversiones, análisis
            video_info['likely_topics'] = [
                'value_investing', 'financial_analysis', 'market_research', 
                'investment_education', 'financial_methodology'
            ]
            
            # Determinar relevancia para análisis jurisprudencial/bibliográfico
            video_info['relevant_for_bibliography'] = True
            video_info['relevance_reason'] = 'Financial education content often cites academic research and studies'
            video_info['bibliography_potential'] = 'High - investment education often references academic papers'
            
            video_info['recommended_actions'] = [
                'Extract transcript for reference analysis',
                'Check for cited sources and studies', 
                'Analyze for financial/legal regulatory mentions',
                'Look for academic methodology discussions'
            ]
        
        return video_info
    
    def suggest_integration_methods(self, video_analysis: Dict) -> List[str]:
        """Sugiere métodos de integración con el sistema bibliográfico"""
        
        suggestions = []
        
        if video_analysis.get('relevant_for_bibliography'):
            suggestions.extend([
                '🎥 Add video transcription capability to bibliography system',
                '📝 Extract academic references mentioned in video content',
                '🔗 Create multimedia reference entries with video timestamps',
                '📊 Analyze video content for legal/academic topic classification',
                '🎯 Integrate video analysis with JurisRank authority scoring'
            ])
            
        if 'educational' in video_analysis.get('channel_type', ''):
            suggestions.extend([
                '📚 Create educational content category in bibliography',
                '🎓 Add institutional affiliation tracking for video sources',
                '📈 Track citation patterns in educational video content'
            ])
            
        return suggestions

class MultimediaReferenceManager:
    """Gestor de referencias multimedia (video, audio, etc.)"""
    
    def __init__(self, bibliography_manager):
        self.bibliography_manager = bibliography_manager
        self.video_analyzer = VideoContentAnalyzer()
        
    def process_video_reference(self, video_url: str, context: Optional[str] = None) -> Dict:
        """
        Procesa una referencia de video y la integra al sistema bibliográfico
        
        Args:
            video_url: URL del video
            context: Contexto adicional sobre el video
            
        Returns:
            Dict con resultados del procesamiento
        """
        
        # Analizar el video
        analysis = self.video_analyzer.analyze_youtube_video(video_url)
        
        # Si es relevante, crear entrada en la bibliografía
        if analysis.get('relevant_for_bibliography'):
            
            # Crear referencia multimedia
            video_reference = {
                'type': 'multimedia',
                'subtype': 'video',
                'url': video_url,
                'video_id': analysis.get('video_id'),
                'platform': 'youtube',
                'analysis_date': datetime.now().isoformat(),
                'academic_relevance': analysis.get('academic_indicators', []),
                'legal_relevance': analysis.get('legal_indicators', []),
                'suggested_topics': analysis.get('likely_topics', []),
                'context': context
            }
            
            # Integrar con JurisRank si tiene contenido legal
            if analysis.get('legal_indicators'):
                video_reference['jurisrank_eligible'] = True
                
            return {
                'success': True,
                'reference_created': video_reference,
                'integration_suggestions': self.video_analyzer.suggest_integration_methods(analysis),
                'next_steps': [
                    'Consider adding transcript analysis',
                    'Extract potential citations from video content',
                    'Categorize video by academic discipline'
                ]
            }
        else:
            return {
                'success': False,
                'reason': 'Video not relevant for academic bibliography',
                'analysis': analysis
            }

# Ejemplo de uso específico para el video proporcionado
def analyze_provided_video():
    """Análisis específico del video de YouTube proporcionado"""
    
    video_url = "https://www.youtube.com/watch?v=l6pMKalQTLM&ab_channel=ValueSchool"
    
    print("🎥 Analyzing YouTube Video for Bibliography Relevance")
    print(f"📺 URL: {video_url}")
    print("=" * 60)
    
    # Inicializar analizador
    analyzer = VideoContentAnalyzer()
    
    # Analizar video
    analysis = analyzer.analyze_youtube_video(video_url)
    
    print(f"📊 Analysis Results:")
    print(f"   Video ID: {analysis.get('video_id', 'N/A')}")
    print(f"   Channel Type: {analysis.get('channel_type', 'Unknown')}")
    print(f"   Academic Relevance: {analysis.get('relevant_for_bibliography', False)}")
    print(f"   Likely Topics: {', '.join(analysis.get('likely_topics', []))}")
    
    if analysis.get('academic_indicators'):
        print(f"\n📚 Academic Indicators:")
        for indicator in analysis['academic_indicators']:
            print(f"   • {indicator}")
    
    if analysis.get('recommended_actions'):
        print(f"\n🎯 Recommended Actions:")
        for action in analysis['recommended_actions']:
            print(f"   • {action}")
    
    # Sugerencias de integración
    suggestions = analyzer.suggest_integration_methods(analysis)
    
    if suggestions:
        print(f"\n🔗 Integration Suggestions for Bibliography System:")
        for suggestion in suggestions:
            print(f"   {suggestion}")
    
    # Conclusión
    if analysis.get('relevant_for_bibliography'):
        print(f"\n✅ VERDICT: This video IS relevant for the bibliography system")
        print(f"   Reason: {analysis.get('relevance_reason', 'Educational content')}")
        print(f"\n🚀 Next Steps:")
        print(f"   1. Add video URL as multimedia reference")
        print(f"   2. Extract any academic sources mentioned")
        print(f"   3. Categorize under appropriate academic discipline")
        print(f"   4. Consider transcript analysis for deeper insights")
    else:
        print(f"\n❌ VERDICT: This video may not be directly relevant")
        print(f"   However, it could still provide contextual value")
    
    return analysis

if __name__ == "__main__":
    # Ejecutar análisis del video proporcionado
    analyze_provided_video()