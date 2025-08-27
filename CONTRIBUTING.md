# Contribuir a JurisRank 🤝

¡Gracias por tu interés en contribuir al proyecto JurisRank! Tu participación es fundamental para construir la plataforma de análisis jurisprudencial más avanzada del mundo.

---

## 🇪🇸 ESPAÑOL

### 🌟 **Bienvenida a Contribuyentes**

JurisRank es un proyecto de código abierto que busca revolucionar el análisis legal a través de metodologías evolutivas. Valoramos enormemente las contribuciones de desarrolladores, investigadores, profesionales legales y académicos de todo el mundo.

### ⚖️ **Consideraciones de Propiedad Intelectual**

**IMPORTANTE**: JurisRank cuenta con protección de propiedad intelectual:
- 🏛️ **Patente SOLICITADA** ante INPI Argentina
- 🏷️ **Marca JurisRank SOLICITADA** ante INPI Argentina
- 📄 **Copyright DEPOSITADO** en DNDA

Al contribuir, aceptas que tu contribución:
- Se licencia bajo MIT License para el componente público
- Respeta los derechos de propiedad intelectual existentes
- No infringe patentes o marcas de terceros

### 🚀 **Tipos de Contribuciones**

#### **📝 Documentación**
- Mejoras en documentación API
- Traducciones a nuevos idiomas
- Ejemplos de uso y tutoriales
- Corrección de errores tipográficos

#### **🔧 Desarrollo de Software**
- Implementación de nuevas funcionalidades públicas
- Optimización de rendimiento
- Corrección de bugs
- SDKs para diferentes lenguajes

#### **🔬 Investigación y Testing**
- Casos de prueba para metodologías
- Validación de algoritmos públicos
- Análisis de casos jurisprudenciales
- Benchmarking y métricas

#### **🌐 Community Building**
- Organización de eventos
- Creación de contenido educativo
- Soporte a nuevos usuarios
- Advocacy en conferencias

### 📋 **Proceso de Contribución**

#### **1. Setup Inicial**
```bash
# Fork el repositorio
git clone https://github.com/tu-usuario/jurisrank-production.git
cd jurisrank-production

# Crear rama para tu feature
git checkout -b feature/nueva-funcionalidad

# Instalar dependencias de desarrollo
pip install -r requirements.txt
python -m pytest tests/ -v  # Verificar tests existentes
```

#### **2. Desarrollo**
- Sigue las convenciones de código establecidas
- Documenta tu código apropiadamente
- Incluye tests cuando sea aplicable
- Verifica que tu código pase las pruebas existentes

#### **3. ⚡ API Contract Testing (OBLIGATORIO)**
Antes de enviar tu PR, **DEBES** correr las pruebas de contrato de API:

```bash
# Ejecutar suite completa de validación
python test_api_contract_validation.py

# Resultado esperado: Success Rate > 90%
# ✅ DNS/TLS Connectivity
# ✅ Security Headers (5/6)  
# ✅ API Contract Compliance
# ✅ Error Handling
# ✅ Performance (<100ms)
# ✅ Content Type Validation
```

#### **4. 🔧 Tests de Desarrollo Obligatorios**
```bash
# Tests unitarios básicos
python -m pytest tests/test_basic.py -v

# Tests de integración
python test_integration.py

# Tests de rendimiento
python test_performance.py

# Validación de documentación
python test_documentation.py

# Tests avanzados (Patent P7)
python test_advanced_ingestion.py
python test_scraping_simulation.py
```

#### **5. Pull Request**
- Crea un PR descriptivo con:
  - Título claro y conciso siguiendo [Conventional Commits](https://www.conventionalcommits.org/)
  - Descripción detallada de cambios
  - **RESULTADO DE TESTS DE CONTRATO** (obligatorio)
  - Screenshots si aplica
  - Referencias a issues relacionados

**Ejemplo de título PR:**
```
feat(api): add rate limiting for authentication endpoints

- Implement 10 rpm limit for /auth/register
- Add structured error responses for rate limit violations  
- Include Retry-After headers
- Update API contract validation tests

Contract Test Results: ✅ 13/14 passed (92.9%)
```

#### **6. Code Review**
- Responde constructivamente a feedback
- Realiza cambios solicitados
- **Re-ejecuta tests de contrato** después de cambios
- Mantén la discusión enfocada y profesional

### 🎯 **Estándares de Calidad**

#### **🔧 Código**
- Documentación completa en docstrings
- Cumplimiento con estándares de estilo (PEP 8 para Python)
- Tests unitarios con >80% cobertura
- Compatibilidad con versiones soportadas

#### **📚 Documentación**
- Lenguaje claro y profesional
- Ejemplos prácticos y funcionables
- Formato Markdown consistente
- Bilingüe (Español/Inglés) cuando sea relevante

#### **🛡️ Seguridad y API Contract**
**OBLIGATORIO para desarrolladores externos:**
- Tests de contrato API con >90% success rate
- Validación de security headers
- Structured error responses siguiendo el estándar
- Performance benchmarks <100ms para endpoints críticos
- OpenAPI schema compliance

#### **🔍 Guía de Testing para Desarrolladores**
```bash
# 1. Setup del entorno de testing
python -m venv venv_testing
source venv_testing/bin/activate  # Linux/Mac
pip install -r requirements.txt

# 2. Correr tests básicos
python -m pytest tests/ -v --cov=src --cov-report=html

# 3. Validación completa de contrato API
python test_api_contract_validation.py

# 4. Tests específicos por componente
python test_integration.py          # Integración con mock server
python test_performance.py         # Benchmarks de rendimiento  
python test_advanced_ingestion.py  # Patent P7 compliance
python test_scraping_simulation.py # Multi-jurisdictional testing

# 5. Validación de documentación
python test_documentation.py       # Docs completeness check
```

#### **📊 Métricas de Calidad Requeridas**
| Métrica | Mínimo Requerido | Objetivo |
|---------|------------------|----------|
| **Test Coverage** | >80% | >95% |
| **API Contract Success** | >90% | >95% |
| **Performance (Health)** | <200ms | <100ms |
| **Security Headers** | 4/6 | 6/6 |
| **Error Structure** | JSON structured | Full compliance |
| **Documentation** | All public APIs | Complete + examples |

### 🛡️ **Código de Conducta**

Este proyecto adhiere al [Código de Conducta](CODE_OF_CONDUCT.md). Al participar, te comprometes a mantener un ambiente respetuoso y profesional.

### 📞 **Comunicación**

- **Issues**: Para reportar bugs o solicitar features
- **Discussions**: Para preguntas generales y discusiones
- **Email**: Para temas sensibles (ver SECURITY.md)

---

## 🇺🇸 ENGLISH

### 🌟 **Welcome Contributors**

JurisRank is an open source project that aims to revolutionize legal analysis through evolutionary methodologies. We greatly value contributions from developers, researchers, legal professionals, and academics worldwide.

### ⚖️ **Intellectual Property Considerations**

**IMPORTANT**: JurisRank has intellectual property protection:
- 🏛️ **PATENT FILED** with INPI Argentina
- 🏷️ **JurisRank TRADEMARK FILED** with INPI Argentina
- 📄 **COPYRIGHT DEPOSITED** at DNDA

By contributing, you agree that your contribution:
- Is licensed under MIT License for the public component
- Respects existing intellectual property rights
- Does not infringe third-party patents or trademarks

### 🚀 **Types of Contributions**

#### **📝 Documentation**
- API documentation improvements
- Translations to new languages
- Usage examples and tutorials
- Typo and error corrections

#### **🔧 Software Development**
- Implementation of new public features
- Performance optimization
- Bug fixes
- SDKs for different languages

#### **🔬 Research and Testing**
- Test cases for methodologies
- Validation of public algorithms
- Jurisprudential case analysis
- Benchmarking and metrics

#### **🌐 Community Building**
- Event organization
- Educational content creation
- New user support
- Conference advocacy

### 📋 **Contribution Process**

#### **1. Initial Setup**
```bash
# Fork the repository
git clone https://github.com/your-username/jurisrank-production.git
cd jurisrank-production

# Create branch for your feature
git checkout -b feature/new-functionality

# Install development dependencies
pip install -r requirements.txt
python -m pytest tests/ -v  # Verify existing tests
```

#### **2. Development**
- Follow established code conventions
- Document your code appropriately
- Include tests when applicable
- Verify your code passes existing tests

#### **3. ⚡ API Contract Testing (MANDATORY)**
Before submitting your PR, you **MUST** run the API contract tests:

```bash
# Run complete validation suite
python test_api_contract_validation.py

# Expected result: Success Rate > 90%
# ✅ DNS/TLS Connectivity
# ✅ Security Headers (5/6)  
# ✅ API Contract Compliance
# ✅ Error Handling
# ✅ Performance (<100ms)
# ✅ Content Type Validation
```

#### **4. 🔧 Mandatory Development Tests**
```bash
# Basic unit tests
python -m pytest tests/test_basic.py -v

# Integration tests
python test_integration.py

# Performance tests
python test_performance.py

# Documentation validation
python test_documentation.py

# Advanced tests (Patent P7)
python test_advanced_ingestion.py
python test_scraping_simulation.py
```

#### **5. Pull Request**
- Create a descriptive PR with:
  - Clear and concise title following [Conventional Commits](https://www.conventionalcommits.org/)
  - Detailed description of changes
  - **CONTRACT TEST RESULTS** (mandatory)
  - Screenshots if applicable
  - References to related issues

**PR Title Example:**
```
feat(api): add rate limiting for authentication endpoints

- Implement 10 rpm limit for /auth/register
- Add structured error responses for rate limit violations  
- Include Retry-After headers
- Update API contract validation tests

Contract Test Results: ✅ 13/14 passed (92.9%)
```

#### **6. Code Review**
- Respond constructively to feedback
- Make requested changes
- **Re-run contract tests** after changes
- Keep discussion focused and professional

### 🎯 **Quality Standards**

#### **🔧 Code**
- Complete documentation in docstrings
- Compliance with style standards (PEP 8 for Python)
- Unit tests with >80% coverage
- Compatibility with supported versions

#### **📚 Documentation**
- Clear and professional language
- Practical and functional examples
- Consistent Markdown format
- Bilingual (Spanish/English) when relevant

#### **🛡️ Security and API Contract**
**MANDATORY for external developers:**
- API contract tests with >90% success rate
- Security headers validation
- Structured error responses following standard
- Performance benchmarks <100ms for critical endpoints
- OpenAPI schema compliance

#### **🔍 Testing Guide for Developers**
```bash
# 1. Testing environment setup
python -m venv venv_testing
source venv_testing/bin/activate  # Linux/Mac
pip install -r requirements.txt

# 2. Run basic tests
python -m pytest tests/ -v --cov=src --cov-report=html

# 3. Complete API contract validation
python test_api_contract_validation.py

# 4. Component-specific tests
python test_integration.py          # Integration with mock server
python test_performance.py         # Performance benchmarks  
python test_advanced_ingestion.py  # Patent P7 compliance
python test_scraping_simulation.py # Multi-jurisdictional testing

# 5. Documentation validation
python test_documentation.py       # Docs completeness check
```

#### **📊 Required Quality Metrics**
| Metric | Minimum Required | Target |
|--------|------------------|---------|
| **Test Coverage** | >80% | >95% |
| **API Contract Success** | >90% | >95% |
| **Performance (Health)** | <200ms | <100ms |
| **Security Headers** | 4/6 | 6/6 |
| **Error Structure** | JSON structured | Full compliance |
| **Documentation** | All public APIs | Complete + examples |

### 🛡️ **Code of Conduct**

This project adheres to the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you commit to maintaining a respectful and professional environment.

### 📞 **Communication**

- **Issues**: To report bugs or request features
- **Discussions**: For general questions and discussions
- **Email**: For sensitive matters (see SECURITY.md)

---

## 🔗 **Enlaces Útiles / Useful Links**

- **Repository**: [https://github.com/adrianlerer/jurisrank-production](https://github.com/adrianlerer/jurisrank-production)
- **API Documentation**: `API_DOCUMENTATION.md`
- **Security Policy**: `SECURITY.md`
- **Code of Conduct**: `CODE_OF_CONDUCT.md`

---

## 📞 **Contacto / Contact**

**Ignacio Adrian Lerer**  
Senior Corporate Lawyer | JurisRank Inventor  
📧 Contact: See SECURITY.md for reporting guidelines  
⚖️ Intellectual Property: Fully protected under Argentine law  

---

*¡Únete a la revolución del análisis jurisprudencial!*  
*Join the jurisprudential analysis revolution!*

*Copyright (c) 2025 Ignacio Adrian Lerer. All rights reserved.*