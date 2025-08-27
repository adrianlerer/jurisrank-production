# Contribuyendo a JurisRank

¡Bienvenido! Gracias por tu interés en contribuir a JurisRank, la plataforma de inteligencia artificial jurídica que está revolucionando el análisis legal mundial.

## 🌍 Comunidad Global

JurisRank es un proyecto open source que busca democratizar el acceso a la inteligencia artificial jurídica. Damos la bienvenida a contribuciones de:

- 👩‍💻 Desarrolladores de software
- ⚖️ Profesionales del derecho
- 🔬 Investigadores académicos  
- 🌐 Especialistas en localización
- 📚 Expertos en documentación

## 🚀 Formas de Contribuir

### 1. Desarrollo de Código
- Mejoras en la API pública
- Optimizaciones de rendimiento
- Nuevas funcionalidades
- Corrección de bugs

### 2. Documentación
- Mejoras en la documentación técnica
- Tutoriales y guías de uso
- Traducciones a otros idiomas
- Ejemplos de casos de uso

### 3. Testing y QA
- Casos de prueba adicionales
- Testing de integración
- Validación en diferentes entornos
- Reporte de problemas

### 4. Localización Legal
- Adaptación a diferentes jurisdicciones
- Terminología jurídica local
- Validación de análisis legal
- Casos de estudio regionales

## 🛠️ Configuración del Entorno de Desarrollo

### Prerrequisitos
```bash
# Python 3.8 o superior
python --version

# Git para control de versiones
git --version
```

### Setup Inicial
```bash
# 1. Fork el repositorio en GitHub
# 2. Clonar tu fork
git clone https://github.com/tu-usuario/jurisrank-core.git
cd jurisrank-core

# 3. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt
pip install -e .

# 5. Instalar herramientas de desarrollo  
pip install -e .[dev]
```

### Verificar Instalación
```bash
# Ejecutar tests
python -m pytest tests/

# Ejecutar ejemplo básico
python examples/basic_usage.py

# Verificar linting
black --check src/
flake8 src/
mypy src/
```

## 📋 Proceso de Contribución

### 1. Crear Issue
Antes de comenzar a trabajar, crea un issue para:
- Reportar bugs
- Proponer nuevas funcionalidades  
- Discutir mejoras
- Solicitar aclaraciones

### 2. Branching Strategy
```bash
# Crear rama para tu contribución
git checkout -b feature/descripcion-de-tu-feature
git checkout -b bugfix/descripcion-del-bug
git checkout -b docs/mejora-documentacion
```

### 3. Desarrollo
- Sigue las convenciones de código existentes
- Escribe tests para nuevas funcionalidades
- Actualiza la documentación según sea necesario
- Asegúrate de que todos los tests pasen

### 4. Pull Request
```bash
# Commit con mensaje descriptivo
git add .
git commit -m "feat: añadir funcionalidad X para mejorar Y"

# Push a tu fork
git push origin feature/descripcion-de-tu-feature

# Crear Pull Request en GitHub
```

## 📏 Estándares de Código

### Estilo Python
- Seguir PEP 8
- Usar Black para formateo automático
- Máximo 88 caracteres por línea
- Type hints obligatorios

### Documentación
- Docstrings en formato Google/Numpy
- Comentarios claros y concisos
- Ejemplos de uso cuando sea apropiado

### Tests
- Cobertura mínima del 80%
- Tests unitarios y de integración
- Usar pytest y fixtures apropiadas

## 🔒 Consideraciones de Propiedad Intelectual

### Código Open Source
- Todo el código contribuido se licencia bajo MIT
- Los contribuidores conservan sus derechos de autor
- Las innovaciones algorítmicas principales están protegidas por patente

### Atribución
- Los contribuidores significativos serán reconocidos
- Mantener headers de copyright apropiados
- Respetar licencias de dependencias externas

## 🌟 Reconocimientos

Agradecemos especialmente a todos los contribuidores que han ayudado a hacer de JurisRank una realidad:

- Ignacio Adrián Lerer - Creador y arquitecto principal
- [Tu nombre podría estar aquí] - ¡Contribuye y únete a la lista!

## 📞 Contacto

¿Preguntas sobre contribuciones?

- 📧 Email: contributors@jurisrank.io
- 💬 Discussions: [GitHub Discussions](https://github.com/adrianlerer/jurisrank-core/discussions)  
- 🐛 Issues: [GitHub Issues](https://github.com/adrianlerer/jurisrank-core/issues)

## 📜 Código de Conducta

Este proyecto adhiere al [Código de Conducta del Contribuyente](CODE_OF_CONDUCT.md). Al participar, te comprometes a mantener un entorno acogedor y respetuoso para todos.

---

¡Gracias por contribuir a democratizar el acceso a la inteligencia artificial jurídica! 🚀⚖️
