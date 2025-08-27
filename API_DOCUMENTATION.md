# JurisRank API Documentation

## 🚀 Free Forever API - Documentación Completa

JurisRank ofrece acceso **completamente gratuito e ilimitado** a su plataforma de inteligencia artificial jurídica a través de una API RESTful robusta y fácil de usar.

---

## 📋 Índice

1. [Inicio Rápido](#inicio-rápido)
2. [Autenticación](#autenticación)
3. [Endpoints](#endpoints)
4. [Modelos de Datos](#modelos-de-datos)
5. [Códigos de Error](#códigos-de-error)
6. [Límites y Cuotas](#límites-y-cuotas)
7. [SDKs](#sdks)
8. [Ejemplos](#ejemplos)

---

## 🚀 Inicio Rápido

### 1. Obtener API Key
```bash
# Regístrate para obtener tu API key gratuita
curl -X POST https://api.jurisrank.io/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "tu-email@example.com", "name": "Tu Nombre"}'
```

### 2. Primera Consulta
```bash
# Analizar documento jurídico
curl -X POST https://api.jurisrank.io/v1/analyze \
  -H "Authorization: Bearer TU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"document_url": "https://example.com/documento.pdf"}'
```

### 3. Python SDK
```python
from jurisrank import JurisRankAPI

# Inicializar cliente
client = JurisRankAPI(api_key="tu_api_key_aqui")

# Analizar documento
result = client.analyze_document("documento_legal.pdf")
print(f"Authority Score: {result.authority_score}")
```

---

## 🔐 Autenticación

### API Key Authentication

Todas las solicitudes requieren un API key enviado en el header `Authorization`:

```http
Authorization: Bearer TU_API_KEY_AQUI
```

### Obtener API Key

```bash
POST https://api.jurisrank.io/auth/register
Content-Type: application/json

{
  "email": "tu-email@example.com",
  "name": "Tu Nombre",
  "organization": "Tu Organización (opcional)"
}
```

**Respuesta:**
```json
{
  "api_key": "jrank_1a2b3c4d5e6f...",
  "user_id": "user_123",
  "tier": "free_forever",
  "created_at": "2025-08-27T10:00:00Z"
}
```

---

## 📞 Soporte y Contacto

### Canales de Soporte
- 📧 **Email**: api-support@jurisrank.io
- 💬 **Community**: [GitHub Discussions](https://github.com/adrianlerer/jurisrank-core/discussions)
- 📚 **Documentación**: https://docs.jurisrank.net
- 🚨 **Status**: https://status.jurisrank.io

---

**¿Listo para revolucionar tu análisis jurídico?** 
[🚀 Obtén tu API key gratuita ahora](https://api.jurisrank.io/register)
