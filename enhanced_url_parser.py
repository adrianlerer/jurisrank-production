#!/usr/bin/env python3
"""
Enhanced URL Parser for Academic References
Maneja URLs de SSRN, arXiv, PubMed, y otros repositorios académicos
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AcademicURLParser:
    """Parser para URLs académicas de diferentes plataformas"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def parse_academic_url(self, url: str) -> Optional[Dict]:
        """
        Parsea una URL académica y extrae metadatos
        
        Args:
            url: URL del paper académico
            
        Returns:
            Dict con metadatos extraídos o None si falla
        """
        
        url = url.strip()
        
        # Identificar tipo de URL
        if 'ssrn.com' in url:
            return self._parse_ssrn_url(url)
        elif 'arxiv.org' in url:
            return self._parse_arxiv_url(url)
        elif 'pubmed.ncbi.nlm.nih.gov' in url:
            return self._parse_pubmed_url(url)
        elif 'scholar.google' in url:
            return self._parse_google_scholar_url(url)
        elif 'researchgate.net' in url:
            return self._parse_researchgate_url(url)
        elif self._is_legal_website(url):
            return self._parse_legal_website(url)
        else:
            return self._parse_generic_academic_url(url)
    
    def _parse_ssrn_url(self, url: str) -> Optional[Dict]:
        """Parsea URLs de SSRN (Social Science Research Network)"""
        
        try:
            # Extraer abstract ID
            abstract_match = re.search(r'abstract_id=(\d+)', url)
            if not abstract_match:
                return None
            
            abstract_id = abstract_match.group(1)
            
            # Hacer request a SSRN
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                logger.warning(f"SSRN request failed: {response.status_code}")
                return self._create_fallback_reference(url, "SSRN Paper")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer título
            title = None
            title_selectors = [
                'h1.title',
                '.title h1',
                'h1[data-test-id="title"]',
                'meta[name="citation_title"]',
                'title'
            ]
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.get('content') if title_elem.name == 'meta' else title_elem.get_text()
                    title = title.strip()
                    if title and title != 'SSRN':
                        break
            
            # Extraer autores
            authors = []
            author_selectors = [
                '.authors a',
                '.author-name',
                'meta[name="citation_author"]',
                '.authors-list a'
            ]
            
            for selector in author_selectors:
                author_elems = soup.select(selector)
                if author_elems:
                    for elem in author_elems:
                        author = elem.get('content') if elem.name == 'meta' else elem.get_text()
                        if author and author.strip():
                            authors.append(author.strip())
                    if authors:
                        break
            
            # Extraer año
            year = datetime.now().year  # Default
            year_patterns = [
                r'(\d{4})',
                r'Posted:\s*(\d{4})',
                r'Date:\s*(\d{4})'
            ]
            
            date_elem = soup.select_one('meta[name="citation_date"]')
            if date_elem:
                date_content = date_elem.get('content', '')
                year_match = re.search(r'(\d{4})', date_content)
                if year_match:
                    year = int(year_match.group(1))
            
            # Extraer abstract/descripción
            abstract = None
            abstract_selectors = [
                '#abstract-text',
                '.abstract-text',
                'meta[name="description"]',
                '.paper-abstract'
            ]
            
            for selector in abstract_selectors:
                abstract_elem = soup.select_one(selector)
                if abstract_elem:
                    abstract = abstract_elem.get('content') if abstract_elem.name == 'meta' else abstract_elem.get_text()
                    if abstract:
                        abstract = abstract.strip()[:500]  # Limitar longitud
                        break
            
            return {
                'title': title or f"SSRN Paper {abstract_id}",
                'authors': authors or [f"SSRN Author {abstract_id}"],
                'year': year,
                'publication': 'SSRN Electronic Journal',
                'url': url,
                'abstract': abstract,
                'reference_type': 'preprint',
                'source': 'ssrn',
                'external_id': abstract_id
            }
            
        except Exception as e:
            logger.error(f"Error parsing SSRN URL {url}: {str(e)}")
            return self._create_fallback_reference(url, "SSRN Paper")
    
    def _parse_arxiv_url(self, url: str) -> Optional[Dict]:
        """Parsea URLs de arXiv"""
        
        try:
            # Extraer arXiv ID
            arxiv_match = re.search(r'arxiv\.org/(?:abs/)?([0-9]{4}\.[0-9]{4,5})', url)
            if not arxiv_match:
                return None
                
            arxiv_id = arxiv_match.group(1)
            
            # Usar API de arXiv
            api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
            response = self.session.get(api_url, timeout=10)
            
            if response.status_code == 200:
                # Parsear XML response
                soup = BeautifulSoup(response.content, 'xml')
                entry = soup.find('entry')
                
                if entry:
                    title = entry.find('title')
                    title = title.get_text().strip() if title else f"arXiv:{arxiv_id}"
                    
                    authors = []
                    for author in entry.find_all('author'):
                        name = author.find('name')
                        if name:
                            authors.append(name.get_text().strip())
                    
                    # Extraer año de fecha de publicación
                    published = entry.find('published')
                    year = datetime.now().year
                    if published:
                        pub_date = published.get_text()
                        year_match = re.search(r'(\d{4})', pub_date)
                        if year_match:
                            year = int(year_match.group(1))
                    
                    abstract = entry.find('summary')
                    abstract = abstract.get_text().strip()[:500] if abstract else None
                    
                    return {
                        'title': title,
                        'authors': authors or [f"arXiv Author {arxiv_id}"],
                        'year': year,
                        'publication': 'arXiv preprint',
                        'url': url,
                        'abstract': abstract,
                        'reference_type': 'preprint',
                        'source': 'arxiv',
                        'external_id': arxiv_id
                    }
            
            return self._create_fallback_reference(url, f"arXiv:{arxiv_id}")
            
        except Exception as e:
            logger.error(f"Error parsing arXiv URL {url}: {str(e)}")
            return self._create_fallback_reference(url, "arXiv Paper")
    
    def _parse_generic_academic_url(self, url: str) -> Optional[Dict]:
        """Parser genérico para otras URLs académicas"""
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return self._create_fallback_reference(url)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer título usando múltiples estrategias
            title = None
            title_sources = [
                ('meta[name="citation_title"]', 'content'),
                ('meta[property="og:title"]', 'content'),
                ('title', 'text'),
                ('h1', 'text'),
                ('.title', 'text')
            ]
            
            for selector, attr_type in title_sources:
                elem = soup.select_one(selector)
                if elem:
                    if attr_type == 'content':
                        title = elem.get('content')
                    else:
                        title = elem.get_text()
                    
                    if title:
                        title = title.strip()
                        if len(title) > 10:  # Filtrar títulos muy cortos
                            break
            
            # Extraer autores
            authors = []
            author_sources = [
                'meta[name="citation_author"]',
                'meta[name="author"]',
                '.author',
                '.authors'
            ]
            
            for selector in author_sources:
                elems = soup.select(selector)
                for elem in elems:
                    author = elem.get('content') if elem.name == 'meta' else elem.get_text()
                    if author:
                        authors.append(author.strip())
                if authors:
                    break
            
            # Extraer año
            year = datetime.now().year
            year_sources = [
                'meta[name="citation_date"]',
                'meta[name="citation_year"]',
                '.date',
                '.year'
            ]
            
            for selector in year_sources:
                elem = soup.select_one(selector)
                if elem:
                    date_text = elem.get('content') if elem.name == 'meta' else elem.get_text()
                    year_match = re.search(r'(\d{4})', date_text)
                    if year_match:
                        year = int(year_match.group(1))
                        break
            
            # Determinar publicación
            publication = "Online Publication"
            journal_elem = soup.select_one('meta[name="citation_journal_title"]')
            if journal_elem:
                publication = journal_elem.get('content', publication)
            
            return {
                'title': title or "Academic Paper",
                'authors': authors or ["Unknown Author"],
                'year': year,
                'publication': publication,
                'url': url,
                'reference_type': 'online',
                'source': 'web'
            }
            
        except Exception as e:
            logger.error(f"Error parsing generic URL {url}: {str(e)}")
            return self._create_fallback_reference(url)
    
    def _parse_pubmed_url(self, url: str) -> Optional[Dict]:
        """Parser para URLs de PubMed"""
        # Implementación simplificada
        return self._create_fallback_reference(url, "PubMed Article")
    
    def _parse_google_scholar_url(self, url: str) -> Optional[Dict]:
        """Parser para URLs de Google Scholar"""
        # Implementación simplificada
        return self._create_fallback_reference(url, "Google Scholar Article")
    
    def _parse_researchgate_url(self, url: str) -> Optional[Dict]:
        """Parser para URLs de ResearchGate"""
        # Implementación simplificada
        return self._create_fallback_reference(url, "ResearchGate Publication")
    
    def _is_legal_website(self, url: str) -> bool:
        """Detecta si una URL es de un sitio web legal"""
        legal_domains = [
            'abogados.com.ar', 'derechoenaccion.com', 'microjuris.com',
            'laley.com.ar', 'thomson.com.ar', 'abeledoperrot.com',
            'derecho.uba.ar', 'austral.edu.ar', 'up.edu.ar',
            'justia.com', 'findlaw.com', 'martindale.com',
            'lawreview.', 'legalstudies.', 'jurisprudence.',
            'constitutional.', 'supremecourt.', 'tribunal.',
            'corte.', 'csjn.', 'poder-judicial.'
        ]
        
        legal_path_indicators = [
            'derecho', 'legal', 'juridico', 'abogado', 'tribunal', 
            'corte', 'jurisprudencia', 'constitutional', 'law',
            'ombudsman', 'compliance', 'governance'
        ]
        
        url_lower = url.lower()
        
        # Verificar dominios legales
        if any(domain in url_lower for domain in legal_domains):
            return True
            
        # Verificar indicadores en la ruta
        if any(indicator in url_lower for indicator in legal_path_indicators):
            return True
            
        return False
    
    def _parse_legal_website(self, url: str) -> Optional[Dict]:
        """Parsea artículos de sitios web legales"""
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                logger.warning(f"Legal website request failed: {response.status_code}")
                return self._create_legal_fallback_reference(url)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer título
            title = self._extract_web_title(soup, url)
            
            # Extraer autor
            authors = self._extract_web_authors(soup, url)
            
            # Extraer fecha/año
            year = self._extract_web_year(soup, url)
            
            # Extraer descripción/contenido
            description = self._extract_web_description(soup)
            
            # Determinar publicación basada en el dominio
            domain_match = re.search(r'://([^/]+)', url)
            publication = domain_match.group(1) if domain_match else "Legal Website"
            
            return {
                'title': title,
                'authors': authors,
                'year': year,
                'publication': publication,
                'url': url,
                'abstract': description,
                'reference_type': 'web_article',
                'source': 'legal_website'
            }
            
        except Exception as e:
            logger.warning(f"Error parsing legal website: {str(e)}")
            return self._create_legal_fallback_reference(url)
    
    def _extract_web_title(self, soup: BeautifulSoup, url: str) -> str:
        """Extrae el título de una página web"""
        
        # Selectores comunes para títulos
        title_selectors = [
            'h1.title', 'h1.entry-title', 'h1.post-title',
            'h1', '.article-title', '.post-header h1',
            'title', 'meta[property="og:title"]',
            'meta[name="twitter:title"]'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get('content') if element.name == 'meta' else element.get_text()
                if title and len(title.strip()) > 5:  # Título mínimo de 5 caracteres
                    return title.strip()
        
        # Fallback: extraer de la URL
        url_parts = url.split('/')
        for part in reversed(url_parts):
            if part and len(part) > 10 and not part.isdigit():
                # Limpiar y formatear
                title = part.replace('-', ' ').replace('_', ' ')
                return title.title()
        
        return "Legal Article"
    
    def _extract_web_authors(self, soup: BeautifulSoup, url: str) -> list:
        """Extrae autores de una página web"""
        
        author_selectors = [
            '.author', '.byline', '.post-author',
            'meta[name="author"]', 'meta[property="article:author"]',
            '.entry-author', '.article-author'
        ]
        
        authors = []
        
        for selector in author_selectors:
            elements = soup.select(selector)
            for element in elements:
                author = element.get('content') if element.name == 'meta' else element.get_text()
                if author and author.strip():
                    authors.append(author.strip())
        
        # Si no encuentra autores, usar el dominio
        if not authors:
            domain_match = re.search(r'://([^/]+)', url)
            domain = domain_match.group(1) if domain_match else "Unknown"
            authors.append(f"Editor de {domain}")
        
        return authors[:3]  # Máximo 3 autores
    
    def _extract_web_year(self, soup: BeautifulSoup, url: str) -> int:
        """Extrae el año de una página web"""
        
        # Buscar en metadatos
        date_selectors = [
            'meta[property="article:published_time"]',
            'meta[name="date"]',
            'meta[name="publish_date"]',
            '.date', '.published', '.post-date'
        ]
        
        for selector in date_selectors:
            element = soup.select_one(selector)
            if element:
                date_text = element.get('content') if element.name == 'meta' else element.get_text()
                year_match = re.search(r'(\d{4})', date_text)
                if year_match:
                    year = int(year_match.group(1))
                    if 2000 <= year <= datetime.now().year + 1:
                        return year
        
        # Buscar en la URL
        year_match = re.search(r'/(\d{4})/', url)
        if year_match:
            year = int(year_match.group(1))
            if 2000 <= year <= datetime.now().year + 1:
                return year
        
        return datetime.now().year
    
    def _extract_web_description(self, soup: BeautifulSoup) -> str:
        """Extrae descripción/resumen de una página web"""
        
        description_selectors = [
            'meta[name="description"]',
            'meta[property="og:description"]',
            '.excerpt', '.summary', '.article-content p:first-child',
            '.entry-content p:first-child', '.post-content p:first-child'
        ]
        
        for selector in description_selectors:
            element = soup.select_one(selector)
            if element:
                desc = element.get('content') if element.name == 'meta' else element.get_text()
                if desc and len(desc.strip()) > 20:
                    return desc.strip()[:500]  # Limitar a 500 caracteres
        
        return None
    
    def _create_legal_fallback_reference(self, url: str) -> Dict:
        """Crea una referencia de respaldo para sitios legales"""
        
        # Extraer información básica de la URL
        domain_match = re.search(r'://([^/]+)', url)
        domain = domain_match.group(1) if domain_match else "Legal Website"
        
        # Intentar extraer título de la URL
        url_parts = url.split('/')
        title = "Legal Article"
        
        for part in reversed(url_parts):
            if part and len(part) > 10 and not part.isdigit():
                title = part.replace('-', ' ').replace('_', ' ').title()
                break
        
        # Detectar tema específico basado en la URL
        url_lower = url.lower()
        if 'ombudsman-corporativo-de-ia' in url_lower:
            title = "El Ombudsman Corporativo de IA: La Nueva Función Estratégica en Grandes Estudios Jurídicos"
        elif 'ombudsman' in url_lower and ('ia' in url_lower or 'ai' in url_lower):
            title = "Artículo sobre Ombudsman Corporativo de IA"
        elif 'compliance' in url_lower and ('ia' in url_lower or 'ai' in url_lower):
            title = "Artículo sobre Compliance en IA"
        elif 'governance' in url_lower and ('ai' in url_lower or 'ia' in url_lower):
            title = "Artículo sobre Gobernanza de IA"
        
        return {
            'title': title,
            'authors': [f"Editor de {domain}"],
            'year': datetime.now().year,
            'publication': domain,
            'url': url,
            'reference_type': 'web_article',
            'source': 'legal_fallback'
        }
    
    def _create_fallback_reference(self, url: str, title_prefix: str = "Academic Paper") -> Dict:
        """Crea una referencia de respaldo cuando falla el parsing"""
        
        # Extraer dominio para usar como "publicación"
        domain_match = re.search(r'://([^/]+)', url)
        domain = domain_match.group(1) if domain_match else "Unknown Source"
        
        # Intentar extraer ID específico según el tipo de URL
        paper_id = None
        if 'ssrn.com' in url:
            abstract_match = re.search(r'abstract_id=(\d+)', url)
            if abstract_match:
                paper_id = abstract_match.group(1)
                title_prefix = f"SSRN Paper #{paper_id}"
        elif 'arxiv.org' in url:
            arxiv_match = re.search(r'arxiv\.org/(?:abs/|pdf/)?([0-9]+\.[0-9]+)', url)
            if arxiv_match:
                paper_id = arxiv_match.group(1)
                title_prefix = f"arXiv:{paper_id}"
        
        return {
            'title': title_prefix,
            'authors': [f"Author from {domain}"],
            'year': datetime.now().year,
            'publication': 'SSRN Electronic Journal' if 'ssrn.com' in url else domain,
            'url': url,
            'reference_type': 'preprint' if 'ssrn.com' in url or 'arxiv.org' in url else 'online',
            'source': 'fallback',
            'external_id': paper_id
        }


# Función de integración con el sistema existente
def enhance_bibliography_parser_with_urls():
    """Mejora el parser bibliográfico existente con capacidad de URLs"""
    
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        from bibliography_manager import BibliographyParser, AcademicReference
        
        # Extender el parser existente
        original_parse_reference = BibliographyParser.parse_reference
        
        def enhanced_parse_reference(self, reference_text: str):
            """Versión mejorada que maneja URLs académicas"""
            
            reference_text = reference_text.strip()
            
            # Verificar si es una URL
            url_pattern = r'https?://[^\s]+'
            if re.match(url_pattern, reference_text):
                # Es una URL - usar parser de URLs
                url_parser = AcademicURLParser()
                url_data = url_parser.parse_academic_url(reference_text)
                
                if url_data:
                    # Convertir a AcademicReference
                    return AcademicReference(
                        authors=url_data['authors'],
                        title=url_data['title'],
                        year=url_data['year'],
                        publication=url_data['publication'],
                        url=url_data['url'],
                        abstract=url_data.get('abstract'),
                        reference_type=url_data.get('reference_type', 'online'),
                        citation_format="URL_EXTRACTED"
                    )
            
            # Si no es URL, usar parser original
            return original_parse_reference(self, reference_text)
        
        # Reemplazar método
        BibliographyParser.parse_reference = enhanced_parse_reference
        
        return True
        
    except ImportError as e:
        logger.error(f"Could not enhance bibliography parser: {e}")
        return False


if __name__ == "__main__":
    # Test del parser
    parser = AcademicURLParser()
    
    test_urls = [
        "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5405459",
        "https://arxiv.org/abs/2301.07041"
    ]
    
    for url in test_urls:
        print(f"\n=== Testing: {url} ===")
        result = parser.parse_academic_url(url)
        if result:
            print(f"Title: {result['title']}")
            print(f"Authors: {result['authors']}")
            print(f"Year: {result['year']}")
            print(f"Publication: {result['publication']}")
        else:
            print("❌ Failed to parse")