# Documentación API JurisRank 📚⚖️

### API Gratuita para Análisis Jurisprudencial Evolutivo

**🎉 FREE FOREVER API - Sin límites, completamente gratuita**

---

## 🇪🇸 ESPAÑOL

### 🌟 **Introducción**

La API pública de JurisRank ofrece acceso gratuito e ilimitado a capacidades avanzadas de análisis jurisprudencial evolutivo. Diseñada para investigadores, desarrolladores y profesionales legales, democratiza el acceso a herramientas de análisis legal de vanguardia.

### ⚖️ **Protección de Propiedad Intelectual**
- 🏛️ **Patente SOLICITADA** ante INPI Argentina
- 🏷️ **Marca JurisRank SOLICITADA** ante INPI Argentina
- 📄 **Copyright DEPOSITADO** en DNDA como software original

### 🚀 **Características de la API**

#### **Acceso Completamente Gratuito**
- ✅ Sin límites de requests por minuto/día/mes
- ✅ Sin restricciones de uso comercial o académico
- ✅ Sin costos ocultos ni upgrades pagos
- ✅ Soporte comunitario incluido

#### **Capacidades de Análisis**
- **Scoring de Autoridad Legal**: Medición evolutiva de influencia jurisprudencial
- **Análisis de Precedentes**: Identificación de casos relacionados y su peso legal
- **Detección de Tendencias**: Evolución temporal de doctrinas jurídicas
- **Comparación Sistemática**: Análisis entre sistemas Common Law y Civil Law

### 📋 **Endpoints Principales**

#### **Autenticación**
```http
GET /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "organization": "Universidad/Empresa",
  "use_case": "research/commercial/academic"
}

Response:
{
  "api_key": "jr_free_[your-api-key]",
  "status": "active",
  "tier": "free_forever"
}
```

#### **Análisis de Autoridad Legal**
```http
POST /api/v1/jurisprudence/authority
Authorization: Bearer jr_free_[your-api-key]
Content-Type: application/json

{
  "case_identifier": "string",
  "jurisdiction": "argentina|mexico|colombia|chile|spain",
  "legal_area": "constitutional|civil|commercial|criminal|administrative"
}

Response:
{
  "authority_score": 0.85,
  "influence_rank": 15,
  "citation_count": 142,
  "temporal_trend": "increasing",
  "confidence_interval": [0.78, 0.92]
}
```

#### **Búsqueda de Precedentes**
```http
GET /api/v1/precedents/search
Authorization: Bearer jr_free_[your-api-key]
Parameters:
- query: "derechos humanos constitución"
- jurisdiction: "argentina"
- limit: 20
- sort_by: "authority_score|date|relevance"

Response:
{
  "results": [
    {
      "case_id": "unique_identifier",
      "title": "Caso Ejemplo vs Estado",
      "court": "Corte Suprema de Justicia",
      "date": "2023-05-15",
      "authority_score": 0.92,
      "relevance_score": 0.88,
      "summary": "Resumen automático del fallo...",
      "key_concepts": ["due process", "constitutional rights"]
    }
  ],
  "total_results": 156,
  "query_time_ms": 245
}
```

#### **Análisis Comparativo**
```http
POST /api/v1/compare/systems
Authorization: Bearer jr_free_[your-api-key]
Content-Type: application/json

{
  "concept": "contract_formation",
  "jurisdictions": ["argentina", "usa_common", "spain"],
  "time_period": "2020-2025"
}

Response:
{
  "comparative_analysis": {
    "argentina": {
      "approach": "civil_law",
      "key_principles": ["written_form", "causa_licita"],
      "authority_cases": [...]
    },
    "usa_common": {
      "approach": "common_law", 
      "key_principles": ["consideration", "offer_acceptance"],
      "authority_cases": [...]
    }
  },
  "convergence_score": 0.67
}
```

### 🔧 **SDKs y Librerías**

#### **Python SDK**
```bash
pip install jurisrank-sdk
```

```python
import jurisrank

# Configuración
client = jurisrank.Client(api_key="jr_free_your_api_key")

# Análisis de autoridad
authority = client.analyze_authority(
    case_id="example_case_2023", 
    jurisdiction="argentina"
)
print(f"Autoridad Legal: {authority.score}")

# Búsqueda de precedentes
precedents = client.search_precedents(
    query="derecho al trabajo",
    jurisdiction="argentina",
    limit=10
)
for case in precedents:
    print(f"{case.title}: {case.authority_score}")
```

#### **JavaScript SDK**
```bash
npm install @jurisrank/sdk
```

```javascript
import JurisRank from '@jurisrank/sdk';

const client = new JurisRank({
  apiKey: 'jr_free_your_api_key'
});

// Análisis de autoridad
const authority = await client.analyzeAuthority({
  caseId: 'example_case_2023',
  jurisdiction: 'argentina'
});
console.log(`Legal Authority: ${authority.score}`);

// Búsqueda de precedentes  
const precedents = await client.searchPrecedents({
  query: 'constitutional rights',
  jurisdiction: 'argentina',
  limit: 10
});
precedents.forEach(case => {
  console.log(`${case.title}: ${case.authorityScore}`);
});
```

### 📚 **Casos de Uso**

#### **Investigación Académica**
- Análisis comparativo de sistemas jurídicos
- Estudios de evolución doctrinal
- Medición de influencia judicial
- Investigación en sociología jurídica

#### **Práctica Legal Profesional**
- Identificación de precedentes relevantes
- Evaluación de fortaleza argumentativa
- Análisis de tendencias jurisprudenciales
- Preparación de estrategias procesales

#### **Desarrollo de Software Legal**
- Integración en plataformas de investigación legal
- Herramientas de due diligence automatizado
- Sistemas de alertas jurisprudenciales
- Aplicaciones de educación legal

---

## 🇺🇸 ENGLISH

### 🌟 **Introduction**

JurisRank's public API offers free and unlimited access to advanced evolutionary jurisprudential analysis capabilities. Designed for researchers, developers, and legal professionals, it democratizes access to cutting-edge legal analysis tools.

### ⚖️ **Intellectual Property Protection**
- 🏛️ **PATENT FILED** with INPI Argentina
- 🏷️ **JurisRank TRADEMARK FILED** with INPI Argentina  
- 📄 **COPYRIGHT DEPOSITED** at DNDA as original software

### 🚀 **API Features**

#### **Completely Free Access**
- ✅ No limits on requests per minute/day/month
- ✅ No commercial or academic use restrictions
- ✅ No hidden costs or paid upgrades
- ✅ Community support included

#### **Analysis Capabilities**
- **Legal Authority Scoring**: Evolutionary measurement of jurisprudential influence
- **Precedent Analysis**: Identification of related cases and their legal weight
- **Trend Detection**: Temporal evolution of legal doctrines
- **Systematic Comparison**: Analysis between Common Law and Civil Law systems

### 📋 **Main Endpoints**

#### **Authentication**
```http
GET /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com", 
  "organization": "University/Company",
  "use_case": "research/commercial/academic"
}

Response:
{
  "api_key": "jr_free_[your-api-key]",
  "status": "active",
  "tier": "free_forever"
}
```

#### **Legal Authority Analysis**
```http
POST /api/v1/jurisprudence/authority
Authorization: Bearer jr_free_[your-api-key]
Content-Type: application/json

{
  "case_identifier": "string",
  "jurisdiction": "argentina|mexico|colombia|chile|spain|usa|uk",
  "legal_area": "constitutional|civil|commercial|criminal|administrative"
}

Response:
{
  "authority_score": 0.85,
  "influence_rank": 15,
  "citation_count": 142,
  "temporal_trend": "increasing",
  "confidence_interval": [0.78, 0.92]
}
```

### 📚 **Use Cases**

#### **Academic Research**
- Comparative analysis of legal systems
- Studies of doctrinal evolution
- Measurement of judicial influence
- Legal sociology research

#### **Professional Legal Practice** 
- Identification of relevant precedents
- Evaluation of argumentative strength
- Analysis of jurisprudential trends
- Preparation of procedural strategies

#### **Legal Software Development**
- Integration in legal research platforms
- Automated due diligence tools
- Jurisprudential alert systems
- Legal education applications

---

## 🔗 **Enlaces y Recursos / Links and Resources**

- **Base URL**: `https://api.jurisrank.com/v1/`
- **Documentación Interactiva**: `https://docs.jurisrank.com/`
- **Status Page**: `https://status.jurisrank.com/`
- **Community Forum**: `https://community.jurisrank.com/`
- **GitHub Repository**: `https://github.com/adrianlerer/jurisrank-core`

## 🆘 **Soporte / Support**

- **Community Support**: GitHub Issues y Community Forum
- **Documentation**: Documentación completa online
- **Examples**: Ejemplos de código en múltiples lenguajes
- **Status**: Monitoreo en tiempo real de API

---

## 📞 **Contacto / Contact**

**Ignacio Adrian Lerer**  
Senior Corporate Lawyer | JurisRank Inventor  
📧 Technical Support: Ver GitHub Issues  
⚖️ Intellectual Property: Fully protected under Argentine law  

---

*API gratuita para democratizar el análisis jurisprudencial*  
*Free API to democratize jurisprudential analysis*

*Copyright (c) 2025 Ignacio Adrian Lerer. All rights reserved.*