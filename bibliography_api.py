#!/usr/bin/env python3
"""
JurisRank Bibliography API
API REST para gestión de referencias académicas y análisis bibliográfico
Integrado con la plataforma JurisRank
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
from datetime import datetime
import logging
import os
from typing import Dict, List
import sys

# Agregar el directorio src al path para importar el módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from bibliography_manager import JurisRankBibliographyManager, AcademicReference
except ImportError as e:
    print(f"Error importing bibliography_manager: {e}")
    print("Make sure the bibliography_manager.py file exists in the src/ directory")
    sys.exit(1)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Inicializar el gestor de bibliografía
bibliography_manager = JurisRankBibliographyManager("jurisrank_bibliography.db")

# Template HTML para la interfaz web
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JurisRank Bibliography Manager</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            padding: 40px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .header h1 {
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .header p {
            color: #7f8c8d;
            font-size: 1.1em;
        }
        
        .section {
            margin-bottom: 40px;
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }
        
        .section h2 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #34495e;
        }
        
        textarea, input, select {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        textarea {
            height: 200px;
            resize: vertical;
            font-family: 'Courier New', monospace;
        }
        
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            margin-right: 10px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: linear-gradient(45deg, #95a5a6, #7f8c8d);
        }
        
        .results {
            margin-top: 30px;
            padding: 25px;
            background: white;
            border-radius: 15px;
            border: 2px solid #e0e0e0;
            max-height: 500px;
            overflow-y: auto;
        }
        
        .reference-item {
            background: #f8f9fa;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        
        .reference-title {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 8px;
            font-size: 1.1em;
        }
        
        .reference-authors {
            color: #7f8c8d;
            margin-bottom: 5px;
        }
        
        .reference-meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.9em;
            color: #95a5a6;
        }
        
        .relevance-score {
            background: linear-gradient(45deg, #27ae60, #2ecc71);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: bold;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #7f8c8d;
        }
        
        .error {
            background: #e74c3c;
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
        }
        
        .success {
            background: #27ae60;
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 2px solid #e0e0e0;
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            color: #7f8c8d;
            margin-top: 5px;
        }
        
        .search-filters {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 JurisRank Bibliography Manager</h1>
            <p>Sistema Avanzado de Gestión de Referencias Académicas</p>
        </div>
        
        <!-- Sección de Importación -->
        <div class="section">
            <h2>📥 Importar Referencias</h2>
            <div class="form-group">
                <label for="references-text">Pegar referencias académicas (formato libre):</label>
                <textarea id="references-text" placeholder="Ejemplo:&#10;Autor, A. (2024). Título del artículo. Revista Académica, 10(2), 123-145.&#10;&#10;Autor, B., & Autor, C. (2023). Otro título..."></textarea>
            </div>
            <button class="btn" onclick="importReferences()">🔄 Importar y Analizar</button>
            <button class="btn btn-secondary" onclick="clearText()">🗑️ Limpiar</button>
            <div id="import-results"></div>
        </div>
        
        <!-- Sección de Búsqueda -->
        <div class="section">
            <h2>🔍 Buscar Referencias</h2>
            <div class="search-filters">
                <div class="form-group">
                    <label for="search-query">Consulta de búsqueda:</label>
                    <input type="text" id="search-query" placeholder="artificial intelligence, derecho, psicología...">
                </div>
                <div class="form-group">
                    <label for="year-from">Año desde:</label>
                    <input type="number" id="year-from" placeholder="2000" min="1900" max="2024">
                </div>
                <div class="form-group">
                    <label for="year-to">Año hasta:</label>
                    <input type="number" id="year-to" placeholder="2024" min="1900" max="2024">
                </div>
                <div class="form-group">
                    <label for="reference-type">Tipo de referencia:</label>
                    <select id="reference-type">
                        <option value="">Todos los tipos</option>
                        <option value="journal">Artículo de revista</option>
                        <option value="book">Libro</option>
                        <option value="conference">Conferencia</option>
                        <option value="report">Reporte</option>
                    </select>
                </div>
            </div>
            <button class="btn" onclick="searchReferences()">🔍 Buscar</button>
            <button class="btn btn-secondary" onclick="clearSearch()">🗑️ Limpiar Búsqueda</button>
            <div id="search-results"></div>
        </div>
        
        <!-- Sección de Estadísticas -->
        <div class="section">
            <h2>📊 Estadísticas de la Biblioteca</h2>
            <button class="btn" onclick="generateReport()">📈 Generar Reporte</button>
            <button class="btn" onclick="exportBibliography('json')">📄 Exportar JSON</button>
            <button class="btn" onclick="exportBibliography('apa')">📝 Exportar APA</button>
            <button class="btn" onclick="exportBibliography('bibtex')">📚 Exportar BibTeX</button>
            <div id="statistics-results"></div>
        </div>
    </div>

    <script>
        const API_BASE = '';
        
        async function apiCall(endpoint, method = 'GET', data = null) {
            const config = {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                }
            };
            
            if (data) {
                config.body = JSON.stringify(data);
            }
            
            try {
                const response = await fetch(API_BASE + endpoint, config);
                const result = await response.json();
                
                if (!response.ok) {
                    throw new Error(result.error || 'Error en la solicitud');
                }
                
                return result;
            } catch (error) {
                console.error('API Error:', error);
                throw error;
            }
        }
        
        function showLoading(elementId) {
            document.getElementById(elementId).innerHTML = '<div class="loading">⏳ Procesando...</div>';
        }
        
        function showError(elementId, message) {
            document.getElementById(elementId).innerHTML = `<div class="error">❌ Error: ${message}</div>`;
        }
        
        function showSuccess(elementId, message) {
            document.getElementById(elementId).innerHTML = `<div class="success">✅ ${message}</div>`;
        }
        
        async function importReferences() {
            const text = document.getElementById('references-text').value.trim();
            
            if (!text) {
                showError('import-results', 'Por favor ingrese al menos una referencia.');
                return;
            }
            
            showLoading('import-results');
            
            try {
                const result = await apiCall('/api/v1/bibliography/import', 'POST', { text: text });
                
                let html = `<div class="success">✅ Referencias importadas exitosamente</div>`;
                html += `<div class="stats-grid">`;
                html += `<div class="stat-card"><div class="stat-number">${result.imported}</div><div class="stat-label">Importadas</div></div>`;
                html += `<div class="stat-card"><div class="stat-number">${result.failed}</div><div class="stat-label">Fallidas</div></div>`;
                
                if (result.analysis) {
                    html += `<div class="stat-card"><div class="stat-number">${result.analysis.average_relevance.toFixed(2)}</div><div class="stat-label">Relevancia Promedio</div></div>`;
                    html += `<div class="stat-card"><div class="stat-number">${result.analysis.year_range[0]}-${result.analysis.year_range[1]}</div><div class="stat-label">Rango de Años</div></div>`;
                }
                
                html += `</div>`;
                
                if (result.references && result.references.length > 0) {
                    html += '<h3 style="margin-top: 20px; color: #2c3e50;">Referencias Procesadas:</h3>';
                    html += '<div class="results">';
                    
                    result.references.forEach(ref => {
                        html += `<div class="reference-item">`;
                        html += `<div class="reference-title">${ref.title}</div>`;
                        html += `<div class="reference-authors">${ref.authors.join(', ')} (${ref.year})</div>`;
                        html += `<div class="reference-meta">`;
                        html += `<span>Temas: ${Object.keys(ref.topics).join(', ')}</span>`;
                        html += `<span class="relevance-score">Relevancia: ${ref.relevance.toFixed(2)}</span>`;
                        html += `</div></div>`;
                    });
                    
                    html += '</div>';
                }
                
                document.getElementById('import-results').innerHTML = html;
                
            } catch (error) {
                showError('import-results', error.message);
            }
        }
        
        async function searchReferences() {
            const query = document.getElementById('search-query').value.trim();
            const yearFrom = document.getElementById('year-from').value;
            const yearTo = document.getElementById('year-to').value;
            const refType = document.getElementById('reference-type').value;
            
            showLoading('search-results');
            
            try {
                const params = new URLSearchParams();
                
                if (query) params.append('query', query);
                if (yearFrom) params.append('year_from', yearFrom);
                if (yearTo) params.append('year_to', yearTo);
                if (refType) params.append('reference_type', refType);
                
                const result = await apiCall(`/api/v1/bibliography/search?${params.toString()}`);
                
                if (result.references.length === 0) {
                    document.getElementById('search-results').innerHTML = '<div class="results">No se encontraron referencias que coincidan con los criterios de búsqueda.</div>';
                    return;
                }
                
                let html = `<div class="success">✅ Encontradas ${result.references.length} referencias</div>`;
                html += '<div class="results">';
                
                result.references.forEach(ref => {
                    html += `<div class="reference-item">`;
                    html += `<div class="reference-title">${ref.title}</div>`;
                    html += `<div class="reference-authors">${ref.authors.join(', ')} (${ref.year})</div>`;
                    html += `<div class="reference-meta">`;
                    html += `<span>${ref.publication}</span>`;
                    html += `<span class="relevance-score">Relevancia: ${ref.jurisprudential_relevance.toFixed(2)}</span>`;
                    html += `</div>`;
                    if (ref.url) {
                        html += `<div style="margin-top: 10px;"><a href="${ref.url}" target="_blank" style="color: #667eea;">🔗 Ver enlace</a></div>`;
                    }
                    html += `</div>`;
                });
                
                html += '</div>';
                document.getElementById('search-results').innerHTML = html;
                
            } catch (error) {
                showError('search-results', error.message);
            }
        }
        
        async function generateReport() {
            showLoading('statistics-results');
            
            try {
                const result = await apiCall('/api/v1/bibliography/report');
                
                let html = '<div class="success">✅ Reporte generado exitosamente</div>';
                
                // Estadísticas generales
                html += '<div class="stats-grid">';
                html += `<div class="stat-card"><div class="stat-number">${result.statistics.total_references}</div><div class="stat-label">Total Referencias</div></div>`;
                html += `<div class="stat-card"><div class="stat-number">${result.statistics.average_jurisprudential_relevance}</div><div class="stat-label">Relevancia Promedio</div></div>`;
                html += `<div class="stat-card"><div class="stat-number">${result.statistics.year_range[0]}-${result.statistics.year_range[1]}</div><div class="stat-label">Rango de Años</div></div>`;
                html += `<div class="stat-card"><div class="stat-number">${result.statistics.most_productive_year[0]} (${result.statistics.most_productive_year[1]})</div><div class="stat-label">Año Más Productivo</div></div>`;
                html += '</div>';
                
                // Referencias más relevantes
                if (result.most_relevant_references) {
                    html += '<h3 style="margin-top: 30px; color: #2c3e50;">🏆 Referencias Más Relevantes:</h3>';
                    html += '<div class="results">';
                    
                    result.most_relevant_references.slice(0, 5).forEach((ref, index) => {
                        html += `<div class="reference-item">`;
                        html += `<div class="reference-title">#${index + 1} ${ref.title}</div>`;
                        html += `<div class="reference-authors">${ref.authors.join(', ')} (${ref.year})</div>`;
                        html += `<div class="reference-meta">`;
                        html += `<span class="relevance-score">Relevancia: ${ref.relevance}</span>`;
                        html += `</div></div>`;
                    });
                    
                    html += '</div>';
                }
                
                document.getElementById('statistics-results').innerHTML = html;
                
            } catch (error) {
                showError('statistics-results', error.message);
            }
        }
        
        async function exportBibliography(format) {
            try {
                const result = await apiCall(`/api/v1/bibliography/export?format=${format}`);
                
                // Crear un blob con el contenido
                const blob = new Blob([result.content], { type: 'text/plain;charset=utf-8' });
                
                // Crear enlace de descarga
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = `bibliography.${format}`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                
                showSuccess('statistics-results', `Bibliografía exportada en formato ${format.toUpperCase()}`);
                
            } catch (error) {
                showError('statistics-results', error.message);
            }
        }
        
        function clearText() {
            document.getElementById('references-text').value = '';
            document.getElementById('import-results').innerHTML = '';
        }
        
        function clearSearch() {
            document.getElementById('search-query').value = '';
            document.getElementById('year-from').value = '';
            document.getElementById('year-to').value = '';
            document.getElementById('reference-type').value = '';
            document.getElementById('search-results').innerHTML = '';
        }
        
        // Cargar estadísticas al iniciar
        window.onload = function() {
            generateReport();
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Página principal con interfaz web"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    """Endpoint de salud"""
    return jsonify({
        'status': 'healthy',
        'service': 'JurisRank Bibliography API',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/v1/bibliography/import', methods=['POST'])
def import_references():
    """
    Importa referencias desde texto libre
    
    Body: {"text": "texto con referencias académicas"}
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text field is required'}), 400
        
        text = data['text']
        if not text.strip():
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        logger.info(f"Importing references from text ({len(text)} characters)")
        
        # Procesar las referencias
        results = bibliography_manager.import_references_from_text(text)
        
        logger.info(f"Import completed: {results['imported']} imported, {results['failed']} failed")
        
        return jsonify({
            'success': True,
            'imported': results['imported'],
            'failed': results['failed'],
            'references': results['references'],
            'analysis': results['analysis']
        })
        
    except Exception as e:
        logger.error(f"Error importing references: {str(e)}")
        return jsonify({'error': f'Import failed: {str(e)}'}), 500

@app.route('/api/v1/bibliography/search', methods=['GET'])
def search_references():
    """
    Busca referencias con filtros opcionales
    
    Query params:
    - query: texto de búsqueda
    - year_from: año inicial
    - year_to: año final  
    - reference_type: tipo de referencia
    - min_relevance: relevancia mínima
    """
    try:
        query = request.args.get('query', '').strip()
        year_from = request.args.get('year_from')
        year_to = request.args.get('year_to')
        ref_type = request.args.get('reference_type', '').strip()
        min_relevance = request.args.get('min_relevance')
        
        # Construir filtros
        filters = {}
        
        if year_from or year_to:
            year_range = []
            year_range.append(int(year_from) if year_from else 1900)
            year_range.append(int(year_to) if year_to else datetime.now().year)
            filters['year_range'] = tuple(year_range)
        
        if ref_type:
            filters['reference_type'] = ref_type
            
        if min_relevance:
            filters['min_relevance'] = float(min_relevance)
        
        logger.info(f"Searching references with query='{query}', filters={filters}")
        
        # Realizar búsqueda
        results = bibliography_manager.search_and_rank(query or None, filters)
        
        logger.info(f"Search completed: {len(results)} references found")
        
        return jsonify({
            'success': True,
            'total': len(results),
            'references': results,
            'query': query,
            'filters': filters
        })
        
    except Exception as e:
        logger.error(f"Error searching references: {str(e)}")
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@app.route('/api/v1/bibliography/report', methods=['GET'])
def generate_report():
    """Genera reporte completo de la biblioteca"""
    try:
        logger.info("Generating bibliography report")
        
        report = bibliography_manager.generate_bibliography_report()
        
        logger.info("Report generated successfully")
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            **report
        })
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return jsonify({'error': f'Report generation failed: {str(e)}'}), 500

@app.route('/api/v1/bibliography/export', methods=['GET'])
def export_bibliography():
    """
    Exporta la bibliografía en diferentes formatos
    
    Query params:
    - format: json, bibtex, apa (default: json)
    - query: filtro de búsqueda opcional
    - year_from, year_to: rango de años opcional
    - reference_type: tipo de referencia opcional
    """
    try:
        export_format = request.args.get('format', 'json').lower()
        query = request.args.get('query', '').strip() or None
        year_from = request.args.get('year_from')
        year_to = request.args.get('year_to')
        ref_type = request.args.get('reference_type', '').strip() or None
        
        # Construir filtros para exportación
        filters = {}
        if query:
            filters['query'] = query
            
        if year_from or year_to:
            year_range = []
            year_range.append(int(year_from) if year_from else 1900)
            year_range.append(int(year_to) if year_to else datetime.now().year)
            filters['year_range'] = tuple(year_range)
            
        if ref_type:
            filters['reference_type'] = ref_type
        
        logger.info(f"Exporting bibliography in format '{export_format}' with filters: {filters}")
        
        # Exportar bibliografía
        content = bibliography_manager.export_bibliography(export_format, filters)
        
        logger.info(f"Export completed: {len(content)} characters")
        
        return jsonify({
            'success': True,
            'format': export_format,
            'content': content,
            'filters': filters,
            'timestamp': datetime.now().isoformat()
        })
        
    except ValueError as e:
        return jsonify({'error': f'Invalid export format: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Error exporting bibliography: {str(e)}")
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

@app.route('/api/v1/bibliography/reference/<reference_id>', methods=['GET'])
def get_reference(reference_id):
    """Obtiene una referencia específica por ID"""
    try:
        reference = bibliography_manager.database.get_reference(reference_id)
        
        if not reference:
            return jsonify({'error': 'Reference not found'}), 404
        
        # Analizar temas
        topics = bibliography_manager.analyzer.analyze_topics(reference)
        
        return jsonify({
            'success': True,
            'reference': {
                'reference_id': reference.reference_id,
                'title': reference.title,
                'authors': reference.authors,
                'year': reference.year,
                'publication': reference.publication,
                'volume': reference.volume,
                'issue': reference.issue,
                'pages': reference.pages,
                'doi': reference.doi,
                'url': reference.url,
                'citation_format': reference.citation_format,
                'reference_type': reference.reference_type,
                'keywords': reference.keywords,
                'abstract': reference.abstract,
                'citation_count': reference.citation_count,
                'relevance_score': reference.relevance_score,
                'jurisprudential_relevance': reference.jurisprudential_relevance,
                'topics': topics,
                'created_at': reference.created_at.isoformat(),
                'updated_at': reference.updated_at.isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting reference {reference_id}: {str(e)}")
        return jsonify({'error': f'Failed to get reference: {str(e)}'}), 500

@app.route('/api/v1/bibliography/statistics', methods=['GET'])
def get_statistics():
    """Obtiene estadísticas resumidas de la biblioteca"""
    try:
        report = bibliography_manager.generate_bibliography_report()
        
        # Extraer solo las estadísticas principales
        stats = {
            'total_references': report['statistics']['total_references'],
            'average_relevance': report['statistics']['average_jurisprudential_relevance'],
            'year_range': report['statistics']['year_range'],
            'most_productive_year': report['statistics']['most_productive_year'],
            'type_distribution': report['distributions']['by_type'],
            'relevance_distribution': report['distributions']['by_relevance']
        }
        
        return jsonify({
            'success': True,
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        return jsonify({'error': f'Failed to get statistics: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Verificar que el archivo de gestión existe
    if not os.path.exists('src/bibliography_manager.py'):
        print("❌ Error: bibliography_manager.py not found in src/ directory")
        print("Please ensure the file exists before running the API")
        sys.exit(1)
    
    print("🚀 Starting JurisRank Bibliography API...")
    print("📚 Bibliography Manager initialized successfully")
    print("🌐 Web interface available at: http://localhost:5001")
    print("📖 API Documentation: http://localhost:5001/health")
    
    # Ejecutar la aplicación
    app.run(host='0.0.0.0', port=5001, debug=True)