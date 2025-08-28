#!/usr/bin/env python3
"""
JurisRank Bibliography Manager
Sistema de gestión de referencias académicas para análisis jurisprudencial
Desarrollado para integración con la plataforma JurisRank
"""

import re
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import sqlite3
from pathlib import Path


@dataclass
class AcademicReference:
    """Clase para representar una referencia académica completa"""
    authors: List[str]
    title: str
    year: int
    publication: str
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    citation_format: str = "APA"
    reference_type: str = "journal"  # journal, book, conference, report
    keywords: List[str] = None
    abstract: Optional[str] = None
    citation_count: int = 0
    relevance_score: float = 0.0
    jurisprudential_relevance: float = 0.0
    created_at: datetime = None
    updated_at: datetime = None
    reference_id: Optional[str] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.reference_id is None:
            self.reference_id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Genera un ID único para la referencia"""
        content = f"{self.authors}{self.title}{self.year}{self.publication}"
        return hashlib.md5(content.encode()).hexdigest()[:12]


class BibliographyParser:
    """Parser avanzado para diferentes formatos de citas académicas"""
    
    def __init__(self):
        self.patterns = {
            'apa_journal': r'([^(]+)\((\d{4})\)[^"]*"([^"]+)"[^,]*,\s*([^,]+),\s*(\d+)\s*\((\d+)\),\s*([0-9\-]+)',
            'apa_book': r'([^(]+)\((\d{4})\)[^"]*"([^"]+)"[^:]*:\s*([^.]+)\.',
            'harvard': r'([^,]+),\s*([^(]+)\((\d{4})\)[^"]*"([^"]+)"',
            'chicago': r'([^.]+)\.\s*"([^"]+)"\.\s*([^,]+),?\s*(?:vol\.\s*(\d+),?\s*)?(?:no\.\s*(\d+)\s*)?\(([^)]+)\):\s*([0-9\-]+)',
        }
        
        # Patrones específicos para identificar tipos de publicación
        self.publication_types = {
            'journal': ['Journal', 'Review', 'Quarterly', 'Annual', 'Research', 'Studies'],
            'conference': ['Proceedings', 'Conference', 'Symposium', 'Workshop', 'Congress'],
            'report': ['Report', 'Working Paper', 'Technical Report', 'Policy Brief'],
            'book': ['Press', 'Publishers', 'Publishing', 'Books', 'University Press']
        }
    
    def parse_reference(self, reference_text: str) -> Optional[AcademicReference]:
        """
        Parsea una referencia académica desde texto libre
        Reconoce múltiples formatos de citación
        """
        reference_text = reference_text.strip()
        
        # Intentar diferentes patrones de parsing
        for format_name, pattern in self.patterns.items():
            match = re.search(pattern, reference_text, re.IGNORECASE)
            if match:
                return self._extract_reference_data(match, format_name, reference_text)
        
        # Si no coincide con patrones específicos, intentar parsing genérico
        return self._generic_parse(reference_text)
    
    def _extract_reference_data(self, match, format_name: str, original_text: str) -> AcademicReference:
        """Extrae datos de la referencia según el formato identificado"""
        
        if format_name == 'apa_journal':
            authors_str, year, title, journal, volume, issue, pages = match.groups()
            authors = self._parse_authors(authors_str)
            
            return AcademicReference(
                authors=authors,
                title=title.strip(),
                year=int(year),
                publication=journal.strip(),
                volume=volume,
                issue=issue,
                pages=pages,
                citation_format="APA",
                reference_type="journal"
            )
            
        elif format_name == 'apa_book':
            authors_str, year, title, publisher = match.groups()
            authors = self._parse_authors(authors_str)
            
            return AcademicReference(
                authors=authors,
                title=title.strip(),
                year=int(year),
                publication=publisher.strip(),
                citation_format="APA",
                reference_type="book"
            )
        
        # Más formatos pueden ser añadidos aquí
        return self._generic_parse(original_text)
    
    def _parse_authors(self, authors_str: str) -> List[str]:
        """Parsea string de autores en lista individual"""
        authors_str = authors_str.strip().rstrip(',')
        
        # Patrones comunes de separación de autores
        if ' and ' in authors_str:
            authors = authors_str.split(' and ')
        elif ', and ' in authors_str:
            authors = authors_str.split(', and ')
        elif ',' in authors_str:
            authors = authors_str.split(',')
        else:
            authors = [authors_str]
        
        # Limpiar y formatear nombres
        cleaned_authors = []
        for author in authors:
            author = author.strip()
            if author:
                cleaned_authors.append(author)
        
        return cleaned_authors
    
    def _generic_parse(self, reference_text: str) -> Optional[AcademicReference]:
        """Parsing genérico para referencias que no coinciden con patrones específicos"""
        
        # Buscar año entre paréntesis
        year_match = re.search(r'\((\d{4})\)', reference_text)
        year = int(year_match.group(1)) if year_match else datetime.now().year
        
        # Buscar título entre comillas
        title_match = re.search(r'"([^"]+)"', reference_text)
        title = title_match.group(1) if title_match else "Unknown Title"
        
        # Buscar URL
        url_match = re.search(r'https?://[^\s]+', reference_text)
        url = url_match.group(0) if url_match else None
        
        # Determinar tipo de publicación
        ref_type = self._determine_reference_type(reference_text)
        
        # Extraer autores (primera parte antes del año)
        if year_match:
            authors_part = reference_text[:year_match.start()].strip()
            authors = self._parse_authors(authors_part)
        else:
            authors = ["Unknown Author"]
        
        # Extraer publicación (después del título)
        if title_match:
            pub_part = reference_text[title_match.end():].strip()
            publication = pub_part.split(',')[0].strip() if ',' in pub_part else pub_part[:50]
        else:
            publication = "Unknown Publication"
        
        return AcademicReference(
            authors=authors,
            title=title,
            year=year,
            publication=publication,
            url=url,
            reference_type=ref_type,
            citation_format="Generic"
        )
    
    def _determine_reference_type(self, text: str) -> str:
        """Determina el tipo de publicación basándose en palabras clave"""
        text_lower = text.lower()
        
        for ref_type, keywords in self.publication_types.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    return ref_type
        
        return "journal"  # Default
    
    def parse_multiple_references(self, text: str) -> List[AcademicReference]:
        """Parsea múltiples referencias de un texto"""
        
        # Dividir por líneas y filtrar vacías
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        references = []
        current_ref = ""
        
        for line in lines:
            # Si la línea parece ser el inicio de una nueva referencia
            if self._is_new_reference(line, current_ref):
                if current_ref:
                    ref = self.parse_reference(current_ref)
                    if ref:
                        references.append(ref)
                current_ref = line
            else:
                # Continúa la referencia anterior
                current_ref += " " + line
        
        # Procesar la última referencia
        if current_ref:
            ref = self.parse_reference(current_ref)
            if ref:
                references.append(ref)
        
        return references
    
    def _is_new_reference(self, line: str, current_ref: str) -> bool:
        """Determina si una línea inicia una nueva referencia"""
        
        # Si no hay referencia actual, es nueva
        if not current_ref:
            return True
        
        # Si la línea contiene un año entre paréntesis, probablemente es nueva
        if re.search(r'\(\d{4}\)', line):
            return True
        
        # Si la línea empieza con autor (formato Apellido, Nombre)
        if re.match(r'^[A-Z][a-z]+,\s*[A-Z]', line):
            return True
        
        return False


class BibliographyDatabase:
    """Gestor de base de datos para referencias bibliográficas"""
    
    def __init__(self, db_path: str = "bibliography.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS bibliography_references (
            reference_id TEXT PRIMARY KEY,
            authors TEXT NOT NULL,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            publication TEXT NOT NULL,
            volume TEXT,
            issue TEXT,
            pages TEXT,
            doi TEXT,
            url TEXT,
            citation_format TEXT,
            reference_type TEXT,
            keywords TEXT,
            abstract TEXT,
            citation_count INTEGER DEFAULT 0,
            relevance_score REAL DEFAULT 0.0,
            jurisprudential_relevance REAL DEFAULT 0.0,
            created_at TEXT,
            updated_at TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference_id TEXT,
            topic TEXT,
            confidence REAL,
            FOREIGN KEY (reference_id) REFERENCES bibliography_references (reference_id)
        )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_year ON bibliography_references(year)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON bibliography_references(reference_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_relevance ON bibliography_references(jurisprudential_relevance)')
        
        conn.commit()
        conn.close()
    
    def save_reference(self, reference: AcademicReference) -> bool:
        """Guarda una referencia en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT OR REPLACE INTO bibliography_references (
                reference_id, authors, title, year, publication, volume, issue,
                pages, doi, url, citation_format, reference_type, keywords,
                abstract, citation_count, relevance_score, jurisprudential_relevance,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                reference.reference_id,
                json.dumps(reference.authors),
                reference.title,
                reference.year,
                reference.publication,
                reference.volume,
                reference.issue,
                reference.pages,
                reference.doi,
                reference.url,
                reference.citation_format,
                reference.reference_type,
                json.dumps(reference.keywords),
                reference.abstract,
                reference.citation_count,
                reference.relevance_score,
                reference.jurisprudential_relevance,
                reference.created_at.isoformat(),
                reference.updated_at.isoformat()
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error saving reference: {e}")
            return False
    
    def get_reference(self, reference_id: str) -> Optional[AcademicReference]:
        """Obtiene una referencia por su ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM bibliography_references WHERE reference_id = ?', (reference_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_reference(row)
        return None
    
    def search_references(self, query: str = None, year_range: Tuple[int, int] = None, 
                         ref_type: str = None, min_relevance: float = None) -> List[AcademicReference]:
        """Busca referencias con filtros opcionales"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sql = "SELECT * FROM bibliography_references WHERE 1=1"
        params = []
        
        if query:
            sql += " AND (title LIKE ? OR authors LIKE ? OR publication LIKE ?)"
            query_param = f"%{query}%"
            params.extend([query_param, query_param, query_param])
        
        if year_range:
            sql += " AND year BETWEEN ? AND ?"
            params.extend(year_range)
        
        if ref_type:
            sql += " AND reference_type = ?"
            params.append(ref_type)
        
        if min_relevance:
            sql += " AND jurisprudential_relevance >= ?"
            params.append(min_relevance)
        
        sql += " ORDER BY jurisprudential_relevance DESC, year DESC"
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_reference(row) for row in rows]
    
    def _row_to_reference(self, row) -> AcademicReference:
        """Convierte una fila de base de datos a AcademicReference"""
        return AcademicReference(
            reference_id=row[0],
            authors=json.loads(row[1]),
            title=row[2],
            year=row[3],
            publication=row[4],
            volume=row[5],
            issue=row[6],
            pages=row[7],
            doi=row[8],
            url=row[9],
            citation_format=row[10],
            reference_type=row[11],
            keywords=json.loads(row[12]) if row[12] else [],
            abstract=row[13],
            citation_count=row[14],
            relevance_score=row[15],
            jurisprudential_relevance=row[16],
            created_at=datetime.fromisoformat(row[17]),
            updated_at=datetime.fromisoformat(row[18])
        )


class BibliographyAnalyzer:
    """Analizador avanzado de referencias bibliográficas"""
    
    def __init__(self):
        self.legal_keywords = [
            'jurisprudence', 'legal', 'court', 'law', 'justice', 'precedent',
            'constitutional', 'statute', 'regulation', 'litigation', 'judicial'
        ]
        
        self.psychological_keywords = [
            'psychology', 'behavior', 'cognitive', 'emotional', 'personality',
            'trait', 'assessment', 'scale', 'measurement', 'validation'
        ]
        
        self.tech_keywords = [
            'artificial intelligence', 'machine learning', 'algorithm', 'automation',
            'technology', 'digital', 'computational', 'data', 'AI'
        ]
    
    def calculate_jurisprudential_relevance(self, reference: AcademicReference) -> float:
        """Calcula la relevancia jurisprudencial de una referencia"""
        score = 0.0
        
        # Análisis del título
        title_lower = reference.title.lower()
        for keyword in self.legal_keywords:
            if keyword in title_lower:
                score += 0.3
        
        # Análisis de la publicación
        pub_lower = reference.publication.lower()
        if any(word in pub_lower for word in ['law', 'legal', 'jurisprudence', 'court']):
            score += 0.5
        
        # Análisis de palabras clave
        if reference.keywords:
            keyword_text = ' '.join(reference.keywords).lower()
            for keyword in self.legal_keywords:
                if keyword in keyword_text:
                    score += 0.2
        
        # Bonificación por citaciones
        if reference.citation_count > 0:
            score += min(reference.citation_count / 100, 1.0)
        
        # Bonificación por antigüedad (referencias más recientes)
        current_year = datetime.now().year
        year_factor = max(0, 1 - (current_year - reference.year) / 20)
        score *= (1 + year_factor * 0.5)
        
        return min(score, 10.0)  # Máximo 10.0
    
    def analyze_topics(self, reference: AcademicReference) -> Dict[str, float]:
        """Analiza los temas principales de una referencia"""
        topics = {}
        
        # Combinar texto relevante
        text_to_analyze = f"{reference.title} {reference.publication} {' '.join(reference.keywords or [])}"
        if reference.abstract:
            text_to_analyze += f" {reference.abstract}"
        
        text_lower = text_to_analyze.lower()
        
        # Analizar temas legales
        legal_score = sum(1 for keyword in self.legal_keywords if keyword in text_lower)
        if legal_score > 0:
            topics['Legal Studies'] = min(legal_score / len(self.legal_keywords), 1.0)
        
        # Analizar temas psicológicos
        psych_score = sum(1 for keyword in self.psychological_keywords if keyword in text_lower)
        if psych_score > 0:
            topics['Psychology'] = min(psych_score / len(self.psychological_keywords), 1.0)
        
        # Analizar temas tecnológicos
        tech_score = sum(1 for keyword in self.tech_keywords if keyword in text_lower)
        if tech_score > 0:
            topics['Technology'] = min(tech_score / len(self.tech_keywords), 1.0)
        
        return topics
    
    def generate_citation_network(self, references: List[AcademicReference]) -> Dict:
        """Genera una red de citaciones entre referencias"""
        network = {
            'nodes': [],
            'edges': []
        }
        
        for ref in references:
            network['nodes'].append({
                'id': ref.reference_id,
                'label': ref.title[:50] + "...",
                'year': ref.year,
                'authors': ref.authors,
                'relevance': ref.jurisprudential_relevance,
                'citation_count': ref.citation_count
            })
        
        # Encontrar conexiones basadas en autores comunes, temas, etc.
        for i, ref1 in enumerate(references):
            for j, ref2 in enumerate(references[i+1:], i+1):
                connection_strength = self._calculate_connection_strength(ref1, ref2)
                if connection_strength > 0.3:
                    network['edges'].append({
                        'source': ref1.reference_id,
                        'target': ref2.reference_id,
                        'strength': connection_strength
                    })
        
        return network
    
    def _calculate_connection_strength(self, ref1: AcademicReference, ref2: AcademicReference) -> float:
        """Calcula la fuerza de conexión entre dos referencias"""
        strength = 0.0
        
        # Autores comunes
        common_authors = set(ref1.authors) & set(ref2.authors)
        if common_authors:
            strength += len(common_authors) * 0.5
        
        # Palabras clave comunes
        if ref1.keywords and ref2.keywords:
            common_keywords = set(ref1.keywords) & set(ref2.keywords)
            strength += len(common_keywords) * 0.2
        
        # Proximidad temporal
        year_diff = abs(ref1.year - ref2.year)
        if year_diff <= 5:
            strength += (5 - year_diff) * 0.1
        
        return min(strength, 1.0)


class JurisRankBibliographyManager:
    """Sistema completo de gestión bibliográfica para JurisRank"""
    
    def __init__(self, db_path: str = "jurisrank_bibliography.db"):
        self.parser = BibliographyParser()
        self.database = BibliographyDatabase(db_path)
        self.analyzer = BibliographyAnalyzer()
    
    def import_references_from_text(self, text: str) -> Dict:
        """Importa referencias desde texto y las analiza completamente"""
        references = self.parser.parse_multiple_references(text)
        
        results = {
            'imported': 0,
            'failed': 0,
            'references': [],
            'analysis': {}
        }
        
        for ref in references:
            # Calcular relevancia jurisprudencial
            ref.jurisprudential_relevance = self.analyzer.calculate_jurisprudential_relevance(ref)
            
            # Analizar temas
            topics = self.analyzer.analyze_topics(ref)
            ref.keywords.extend(topics.keys())
            
            # Guardar en base de datos
            if self.database.save_reference(ref):
                results['imported'] += 1
                results['references'].append({
                    'id': ref.reference_id,
                    'title': ref.title,
                    'authors': ref.authors,
                    'year': ref.year,
                    'relevance': ref.jurisprudential_relevance,
                    'topics': topics
                })
            else:
                results['failed'] += 1
        
        # Generar análisis general
        if results['references']:
            results['analysis'] = {
                'total_references': results['imported'],
                'average_relevance': sum(r['relevance'] for r in results['references']) / len(results['references']),
                'year_range': [
                    min(r['year'] for r in results['references']),
                    max(r['year'] for r in results['references'])
                ],
                'most_relevant': max(results['references'], key=lambda x: x['relevance'])
            }
        
        return results
    
    def search_and_rank(self, query: str, filters: Dict = None) -> List[Dict]:
        """Busca y rankea referencias según relevancia jurisprudencial"""
        
        if filters is None:
            filters = {}
        
        references = self.database.search_references(
            query=query,
            year_range=filters.get('year_range'),
            ref_type=filters.get('reference_type'),
            min_relevance=filters.get('min_relevance')
        )
        
        # Formatear resultados con información adicional
        results = []
        for ref in references:
            topics = self.analyzer.analyze_topics(ref)
            results.append({
                'reference_id': ref.reference_id,
                'title': ref.title,
                'authors': ref.authors,
                'year': ref.year,
                'publication': ref.publication,
                'jurisprudential_relevance': ref.jurisprudential_relevance,
                'topics': topics,
                'citation_format': ref.citation_format,
                'url': ref.url
            })
        
        return results
    
    def generate_bibliography_report(self) -> Dict:
        """Genera un reporte completo de la biblioteca"""
        
        all_references = self.database.search_references()
        
        if not all_references:
            return {'error': 'No references found in database'}
        
        # Estadísticas generales
        total_refs = len(all_references)
        avg_relevance = sum(ref.jurisprudential_relevance for ref in all_references) / total_refs
        
        # Distribución por años
        year_distribution = {}
        for ref in all_references:
            year_distribution[ref.year] = year_distribution.get(ref.year, 0) + 1
        
        # Top autores
        author_count = {}
        for ref in all_references:
            for author in ref.authors:
                author_count[author] = author_count.get(author, 0) + 1
        
        top_authors = sorted(author_count.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Distribución por tipo
        type_distribution = {}
        for ref in all_references:
            type_distribution[ref.reference_type] = type_distribution.get(ref.reference_type, 0) + 1
        
        # Referencias más relevantes
        top_references = sorted(all_references, 
                              key=lambda x: x.jurisprudential_relevance, 
                              reverse=True)[:10]
        
        return {
            'statistics': {
                'total_references': total_refs,
                'average_jurisprudential_relevance': round(avg_relevance, 2),
                'year_range': [min(year_distribution.keys()), max(year_distribution.keys())],
                'most_productive_year': max(year_distribution.items(), key=lambda x: x[1])
            },
            'distributions': {
                'by_year': year_distribution,
                'by_type': type_distribution,
                'by_relevance': {
                    'high (>5.0)': len([r for r in all_references if r.jurisprudential_relevance > 5.0]),
                    'medium (2.0-5.0)': len([r for r in all_references if 2.0 <= r.jurisprudential_relevance <= 5.0]),
                    'low (<2.0)': len([r for r in all_references if r.jurisprudential_relevance < 2.0])
                }
            },
            'top_authors': top_authors,
            'most_relevant_references': [
                {
                    'title': ref.title[:100] + "..." if len(ref.title) > 100 else ref.title,
                    'authors': ref.authors[:3],  # Solo primeros 3 autores
                    'year': ref.year,
                    'relevance': round(ref.jurisprudential_relevance, 2)
                }
                for ref in top_references
            ]
        }
    
    def export_bibliography(self, format: str = "json", filters: Dict = None) -> str:
        """Exporta la bibliografía en diferentes formatos"""
        
        references = self.database.search_references(
            query=filters.get('query') if filters else None,
            year_range=filters.get('year_range') if filters else None,
            ref_type=filters.get('reference_type') if filters else None
        )
        
        if format.lower() == "json":
            return json.dumps([asdict(ref) for ref in references], 
                            default=str, indent=2, ensure_ascii=False)
        
        elif format.lower() == "bibtex":
            return self._export_bibtex(references)
        
        elif format.lower() == "apa":
            return self._export_apa(references)
        
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_bibtex(self, references: List[AcademicReference]) -> str:
        """Exporta referencias en formato BibTeX"""
        bibtex_entries = []
        
        for ref in references:
            authors_str = " and ".join(ref.authors)
            entry_type = "article" if ref.reference_type == "journal" else ref.reference_type
            
            entry = f"@{entry_type}{{{ref.reference_id},\n"
            entry += f"  author = {{{authors_str}}},\n"
            entry += f"  title = {{{ref.title}}},\n"
            entry += f"  year = {{{ref.year}}},\n"
            entry += f"  journal = {{{ref.publication}}},\n"
            
            if ref.volume:
                entry += f"  volume = {{{ref.volume}}},\n"
            if ref.issue:
                entry += f"  number = {{{ref.issue}}},\n"
            if ref.pages:
                entry += f"  pages = {{{ref.pages}}},\n"
            if ref.doi:
                entry += f"  doi = {{{ref.doi}}},\n"
            if ref.url:
                entry += f"  url = {{{ref.url}}},\n"
            
            entry += "}\n\n"
            bibtex_entries.append(entry)
        
        return "".join(bibtex_entries)
    
    def _export_apa(self, references: List[AcademicReference]) -> str:
        """Exporta referencias en formato APA"""
        apa_entries = []
        
        for ref in references:
            # Formatear autores
            if len(ref.authors) == 1:
                authors_str = ref.authors[0]
            elif len(ref.authors) == 2:
                authors_str = f"{ref.authors[0]} & {ref.authors[1]}"
            else:
                authors_str = f"{', '.join(ref.authors[:-1])}, & {ref.authors[-1]}"
            
            # Construir cita APA
            entry = f"{authors_str} ({ref.year}). {ref.title}. "
            
            if ref.reference_type == "journal":
                entry += f"{ref.publication}"
                if ref.volume:
                    entry += f", {ref.volume}"
                if ref.issue:
                    entry += f"({ref.issue})"
                if ref.pages:
                    entry += f", {ref.pages}"
            else:
                entry += f"{ref.publication}"
            
            if ref.url:
                entry += f" Retrieved from {ref.url}"
            
            entry += ".\n\n"
            apa_entries.append(entry)
        
        return "".join(apa_entries)


if __name__ == "__main__":
    # Ejemplo de uso del sistema
    manager = JurisRankBibliographyManager()
    
    # Texto de ejemplo con las referencias de la imagen
    sample_references = """
    Spielberger, Charles D, Gerald Jacobs, Sheryl Russell, and Rosario S Crane (2013). "Assessment of Anger: The State-Trait Anger Scale," in Advances in Personality Assessment: Routledge, 161-89.

    Staff (2022). "Bringing Dark Patterns to Light." https://www.ftc.gov/system/files/ftc_gov/pdf/P214800%20Dark%20Patterns%20Report%209.14.2022%20-%20FINAL.pdf.

    Teeny, Jacob D, Joseph J Siev, Pablo Briñol, and Richard E Petty (2021). "A Review and Conceptual Framework for Understanding Personalized Matching Effects in Persuasion," Journal of Consumer Psychology, 31 (2), 382-414.

    Valenzuela, Ana, Stefano Puntoni, Donna Hoffman, Noah Castelo, Julian De Freitas, Berkeley Dietvorst, Christian Hildebrand, Young Eun Huh, Robert Meyer, and Miriam E Sweeney (2024). "How Artificial Intelligence Constrains the Human Experience," Journal of the Association for Consumer Research, 9 (3), 000-00.

    Venkatesh, Viswanath (2000). "Determinants of Perceived Ease of Use: Integrating Control, Intrinsic Motivation, and Emotion into the Technology Acceptance Model," Information Systems Research, 11 (4), 342-65.

    Waytz, Adam, Joy Heafner, and Nicholas Epley (2014). "The Mind in the Machine: Anthropomorphism Increases Trust in an Autonomous Vehicle," Journal of Experimental Social Psychology, 52, 113-17.
    """
    
    print("=== JurisRank Bibliography Manager - Demo ===\n")
    
    # Importar referencias
    print("1. Importing references from text...")
    results = manager.import_references_from_text(sample_references)
    
    print(f"✅ Successfully imported: {results['imported']} references")
    print(f"❌ Failed to import: {results['failed']} references")
    
    if results['analysis']:
        print(f"\n📊 Analysis Summary:")
        print(f"   Average Jurisprudential Relevance: {results['analysis']['average_relevance']:.2f}")
        print(f"   Year Range: {results['analysis']['year_range'][0]}-{results['analysis']['year_range'][1]}")
        print(f"   Most Relevant: {results['analysis']['most_relevant']['title'][:50]}...")
    
    print("\n" + "="*60)
    
    # Generar reporte
    print("2. Generating bibliography report...")
    report = manager.generate_bibliography_report()
    
    print(f"\n📈 Bibliography Statistics:")
    print(f"   Total References: {report['statistics']['total_references']}")
    print(f"   Average Relevance: {report['statistics']['average_jurisprudential_relevance']}")
    print(f"   Most Productive Year: {report['statistics']['most_productive_year'][0]} ({report['statistics']['most_productive_year'][1]} refs)")
    
    print(f"\n🏆 Top 3 Most Relevant References:")
    for i, ref in enumerate(report['most_relevant_references'][:3], 1):
        print(f"   {i}. {ref['title']} ({ref['year']}) - Relevance: {ref['relevance']}")
    
    print("\n" + "="*60)
    
    # Búsqueda y ranking
    print("3. Searching for 'artificial intelligence' related references...")
    search_results = manager.search_and_rank("artificial intelligence")
    
    print(f"\n🔍 Found {len(search_results)} relevant references:")
    for i, result in enumerate(search_results[:3], 1):
        print(f"   {i}. {result['title'][:50]}...")
        print(f"      Relevance: {result['jurisprudential_relevance']:.2f}")
        print(f"      Topics: {list(result['topics'].keys())}")
        print()