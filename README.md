# JurisRank 🏛️⚖️

### Plataforma de Análisis Jurisprudencial Evolutivo

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![API Contract](https://img.shields.io/badge/API%20Contract-92.9%25-brightgreen)](https://github.com/adrianlerer/jurisrank-core)
[![Security Headers](https://img.shields.io/badge/Security%20Headers-5%2F6-green)](https://github.com/adrianlerer/jurisrank-core/blob/main/SECURITY_CHECKLIST.md)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0.1-blue)](https://5000-i09td971cyg7b4ytmaaxl.e2b.dev/docs)
[![Release](https://img.shields.io/badge/Release-v0.9.0--open-success)](https://github.com/adrianlerer/jurisrank-core/releases)
[![External Validation](https://img.shields.io/badge/External%20Validation-✅%20Verified-brightgreen)](https://github.com/adrianlerer/jurisrank-core/blob/main/EXTERNAL_ACCESS_VERIFICATION_REPORT.md)

---

## 🇪🇸 ESPAÑOL

### 🎉 **API COMPLETAMENTE GRATUITA - FREE FOREVER**
**Sin límites • Sin restricciones • Sin costos ocultos**

JurisRank es una plataforma revolucionaria de análisis jurisprudencial que aplica metodologías evolutivas para medir la autoridad y influencia legal en sistemas jurídicos diversos. Desarrollada con tecnología de vanguardia, ofrece una **API pública completamente gratuita** para democratizar el acceso al análisis legal avanzado.

### ⚖️ **Protección de Propiedad Intelectual**
- **🏛️ Patente SOLICITADA** ante INPI Argentina
- **🏷️ Marca JurisRank SOLICITADA** ante INPI Argentina  
- **📄 Copyright DEPOSITADO** en DNDA como software original
- **📚 Papers Académicos** publicados en SSRN estableciendo prioridad intelectual

### 🚀 **Características Principales**

#### **Análisis Jurisprudencial Evolutivo**
- Medición dinámica de autoridad legal
- Análisis de influencia recíproca entre fallos
- Integración metodológica Common Law ↔ Civil Law
- Scoring evolutivo de precedentes jurisprudenciales

#### **API Pública Gratuita**
- **Acceso ilimitado** sin restricciones de uso
- **Documentación completa** bilingüe
- **Soporte técnico** de la comunidad
- **Licencia MIT** para máxima adopción

#### **Casos de Uso**
- 🎓 **Investigación Académica**: Análisis comparativo de sistemas legales
- 💼 **Desarrollo Comercial**: Integración en aplicaciones legal tech
- ⚖️ **Práctica Legal**: Herramientas de investigación jurisprudencial
- 🌐 **Community Building**: Plataforma colaborativa global

### 📚 **Fundamento Académico**
- **"The Legislator as Extended Phenotype"** - SSRN Research Paper
- **"JurisRank: Measuring Legal Phenotypic Fitness"** - SSRN Research Paper
- Metodología científica validada academicamente
- Base teórica en evolución legal y sistemas complejos

### 🌟 **Estrategia "Intel Inside"**
JurisRank implementa una estrategia de penetración de mercado inspirada en el modelo "Intel Inside", ofreciendo la API núcleo completamente gratuita para construir un ecosistema masivo de adopción en el mercado global de legal tech (valorado en $47B).

### 🔍 **Validación Externa Independiente**
**✅ Verificado por terceros independientes:**
- **API Contract**: 92.9% success rate (13/14 tests passed)
- **External Access**: Confirmed accessible from multiple networks
- **Security**: 5/6 production security headers implemented
- **Performance**: <15ms average response time
- **Documentation**: 100% OpenAPI 3.0.1 coverage

**🧪 Test Yourself:**
```bash
# Run external validation
bash <(curl -fsSL https://raw.githubusercontent.com/adrianlerer/jurisrank-core/main/examples/jurisrank_agent_test.sh)
```

### 🤝 **Únete a la Comunidad**
- **Desarrolladores**: Integra JurisRank en tus aplicaciones
- **Investigadores**: Accede a herramientas de análisis avanzado  
- **Legal Professionals**: Potencia tu práctica con IA evolutiva
- **Académicos**: Contribuye al desarrollo científico del derecho

---

## 🇺🇸 ENGLISH

### 🎉 **COMPLETELY FREE API - FREE FOREVER**
**No limits • No restrictions • No hidden costs**

JurisRank is a revolutionary jurisprudential analysis platform that applies evolutionary methodologies to measure legal authority and influence across diverse legal systems. Built with cutting-edge technology, it offers a **completely free public API** to democratize access to advanced legal analysis.

### ⚖️ **Intellectual Property Protection**
- **🏛️ PATENT FILED** with INPI Argentina
- **🏷️ JurisRank TRADEMARK FILED** with INPI Argentina
- **📄 COPYRIGHT DEPOSITED** at DNDA as original software
- **📚 Academic Papers** published on SSRN establishing intellectual priority

### 🚀 **Key Features**

#### **Evolutionary Jurisprudential Analysis**
- Dynamic measurement of legal authority
- Analysis of reciprocal influence between rulings
- Methodological integration Common Law ↔ Civil Law
- Evolutionary scoring of jurisprudential precedents

#### **Free Public API**
- **Unlimited access** without usage restrictions
- **Complete bilingual documentation**
- **Community technical support**
- **MIT License** for maximum adoption

#### **Use Cases**
- 🎓 **Academic Research**: Comparative analysis of legal systems
- 💼 **Commercial Development**: Integration in legal tech applications
- ⚖️ **Legal Practice**: Jurisprudential research tools
- 🌐 **Community Building**: Global collaborative platform

### 📚 **Academic Foundation**
- **"The Legislator as Extended Phenotype"** - SSRN Research Paper
- **"JurisRank: Measuring Legal Phenotypic Fitness"** - SSRN Research Paper
- Academically validated scientific methodology
- Theoretical foundation in legal evolution and complex systems

### 🌟 **"Intel Inside" Strategy**
JurisRank implements a market penetration strategy inspired by the "Intel Inside" model, offering the core API completely free to build a massive adoption ecosystem in the global legal tech market (valued at $47B).

### 🤝 **Join the Community**
- **Developers**: Integrate JurisRank into your applications
- **Researchers**: Access advanced analysis tools
- **Legal Professionals**: Power your practice with evolutionary AI
- **Academics**: Contribute to the scientific development of law

---

## 🚀 **Quick Start**

### Installation

#### Option 1: From Source (Recommended for now)
```bash
git clone https://github.com/adrianlerer/jurisrank-core.git
cd jurisrank-core
pip install -e .
```

#### Option 2: Direct API Usage (No Installation)
```bash
# No installation needed - use direct HTTP calls
curl -X POST https://api.jurisrank.com/v1/auth/register
```

> **Note**: PyPI package `jurisrank-sdk` coming soon. Currently install from source.

### Basic Usage
```python
import jurisrank

# Initialize free API client
client = jurisrank.Client(api_key="your_free_api_key")

# Analyze jurisprudential authority
authority_score = client.analyze_authority(case_id="example_case")
print(f"Authority Score: {authority_score}")

# Search relevant precedents
precedents = client.search_precedents(query="constitutional law", limit=10)
for precedent in precedents:
    print(f"Case: {precedent.name}, Score: {precedent.authority_score}")
```

## 📖 **Documentation**
- **[API Documentation](API_DOCUMENTATION.md)** - Complete API reference
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- **[Code of Conduct](CODE_OF_CONDUCT.md)** - Community guidelines

## 📄 **License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 **Links**
- **Repository**: [https://github.com/adrianlerer/jurisrank-core](https://github.com/adrianlerer/jurisrank-core)
- **SSRN Papers**: Research publications establishing intellectual priority
- **API Access**: Completely free, no registration required for basic usage

## 📞 **Contact**
**Ignacio Adrian Lerer**  
Senior Corporate Lawyer | JurisRank Inventor  
📧 Contact: See SECURITY.md for reporting  
⚖️ Intellectual Property: Fully protected under Argentine law

---

*JurisRank - Revolutionizing jurisprudential analysis with evolutionary technology*  
*Copyright (c) 2025 Ignacio Adrian Lerer. All rights reserved.*