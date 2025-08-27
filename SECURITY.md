# Política de Seguridad JurisRank 🔐

### Divulgación Responsable de Vulnerabilidades

---

## 🇪🇸 ESPAÑOL

### 🎯 **Nuestra Política**

JurisRank se compromete a mantener los más altos estándares de seguridad para proteger los datos y la privacidad de nuestra comunidad global. Valoramos enormemente la colaboración de investigadores de seguridad y la comunidad técnica en la identificación y resolución de vulnerabilidades.

### ⚖️ **Consideraciones de Propiedad Intelectual**
- 🏛️ **Patente SOLICITADA** ante INPI Argentina
- 🏷️ **Marca JurisRank SOLICITADA** ante INPI Argentina
- 📄 **Copyright DEPOSITADO** en DNDA como software original

### 🔍 **Alcance de la Política**

#### **Sistemas Incluidos**
- API pública JurisRank (`api.jurisrank.com`)
- Sitio web principal (`jurisrank.com`)
- Repositorio público GitHub
- SDKs y librerías oficiales
- Documentación y herramientas comunitarias

#### **Sistemas Excluidos**
- Sistemas de desarrollo interno
- Infraestructura de investigación propietaria
- Sistemas de terceros integrados
- Redes corporativas internas

### 🚨 **Tipos de Vulnerabilidades**

#### **Alta Prioridad**
- Ejecución remota de código (RCE)
- Inyección SQL en APIs públicas
- Exposición de datos personales
- Bypass de autenticación/autorización
- Vulnerabilidades de escalación de privilegios

#### **Prioridad Media**
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Exposición de información sensible
- Vulnerabilidades de denegación de servicio
- Problemas de configuración de seguridad

#### **Prioridad Baja**
- Problemas de información de versión
- Vulnerabilidades que requieren acceso físico
- Issues de phishing social engineering
- Problemas de fuerza bruta sin impacto directo

### 📞 **Cómo Reportar**

#### **Canal Preferido**
```
📧 Email: security@jurisrank.com
🔒 Encryp: Usar PGP key (disponible bajo request)
⚡ Response: 24-48 horas iniciales
```

#### **Información Requerida**
- Descripción clara y detallada de la vulnerabilidad
- Pasos para reproducir el issue
- Prueba de concepto (PoC) si es posible
- Impacto potencial estimado
- Información del investigador (opcional para créditos)

#### **Template de Reporte**
```markdown
## Resumen Ejecutivo
[Descripción breve del problema]

## Detalles Técnicos
- **URL/Endpoint**: 
- **Método**: GET/POST/PUT/DELETE
- **Parámetros afectados**: 
- **Tipo de vulnerabilidad**: 

## Pasos para Reproducir
1. [Paso uno]
2. [Paso dos]
3. [Paso tres]

## Prueba de Concepto
[Código o screenshots si aplicable]

## Impacto
[Descripción del impacto potencial]

## Recomendaciones
[Sugerencias de mitigación si las tienes]
```

### ⏱️ **Timeline de Respuesta**

#### **Confirmación Inicial**
- **24-48 horas**: Acknowledgment del reporte
- **72 horas**: Evaluación inicial y triaging
- **1 semana**: Análisis detallado y plan de acción

#### **Resolución**
- **Crítica**: 24-48 horas
- **Alta**: 1-2 semanas  
- **Media**: 2-4 semanas
- **Baja**: 1-3 meses

#### **Divulgación**
- **Coordinada**: 90 días después del fix
- **Acelerada**: En caso de exploit activo
- **Extendida**: Si se requiere más tiempo para patch

### 🏆 **Reconocimientos**

#### **Hall of Fame**
Los investigadores que reporten vulnerabilidades válidas serán incluidos en nuestro Security Hall of Fame (con su permiso):
- Nombre del investigador
- Organización (opcional)
- Tipo de vulnerabilidad encontrada
- Fecha de resolución

#### **Agradecimientos**
- Mención en release notes
- LinkedIn recommendation (si se solicita)
- Referencia profesional
- Invitación a beta testing de nuevas features

### 🚫 **Condiciones de Participación**

#### **Actividades Permitidas**
- Testing automatizado responsable
- Análisis de código fuente público
- Fuzzing con rate limiting apropiado
- Social engineering limitado a emails de prueba

#### **Actividades Prohibidas**
- Acceso a datos de usuarios reales
- Disrupción de servicios en producción
- Modificación o eliminación de datos
- Distribución de vulnerabilidades sin coordinación
- Testing en infraestructura de terceros

### 🛡️ **Compromisos de JurisRank**

#### **Safe Harbor**
- No tomaremos acciones legales contra investigadores que actúen de buena fe
- Protegeremos la identidad de reporters si así lo solicitan
- Trabajaremos colaborativamente en la resolución

#### **Transparencia**
- Publicaremos advisories de seguridad para issues resueltos
- Mantendremos un registro público de mejoras de seguridad
- Comunicaremos timeline actualizado para resoluciones complejas

---

## 🇺🇸 ENGLISH

### 🎯 **Our Policy**

JurisRank is committed to maintaining the highest security standards to protect the data and privacy of our global community. We greatly value the collaboration of security researchers and the technical community in identifying and resolving vulnerabilities.

### ⚖️ **Intellectual Property Considerations**
- 🏛️ **PATENT FILED** with INPI Argentina
- 🏷️ **JurisRank TRADEMARK FILED** with INPI Argentina
- 📄 **COPYRIGHT DEPOSITED** at DNDA as original software

### 🔍 **Policy Scope**

#### **Included Systems**
- JurisRank public API (`api.jurisrank.com`)
- Main website (`jurisrank.com`)
- Public GitHub repository
- Official SDKs and libraries
- Documentation and community tools

#### **Excluded Systems**
- Internal development systems
- Proprietary research infrastructure
- Third-party integrated systems
- Internal corporate networks

### 📞 **How to Report**

#### **Preferred Channel**
```
📧 Email: security@jurisrank.com
🔒 Encryption: Use PGP key (available upon request)
⚡ Response: 24-48 hours initial
```

### ⏱️ **Response Timeline**

#### **Initial Confirmation**
- **24-48 hours**: Report acknowledgment
- **72 hours**: Initial evaluation and triaging
- **1 week**: Detailed analysis and action plan

#### **Resolution**
- **Critical**: 24-48 hours
- **High**: 1-2 weeks
- **Medium**: 2-4 weeks
- **Low**: 1-3 months

### 🏆 **Recognition**

#### **Security Hall of Fame**
Researchers who report valid vulnerabilities will be included in our Security Hall of Fame (with permission):
- Researcher name
- Organization (optional)
- Type of vulnerability found
- Resolution date

---

## 🔗 **Recursos Adicionales / Additional Resources**

### **Documentación de Seguridad**
- **Security Best Practices**: `docs/security/`
- **API Security Guide**: `API_DOCUMENTATION.md#security`
- **Privacy Policy**: `PRIVACY.md`

### **Herramientas Recomendadas**
- **OWASP ZAP**: Para testing automatizado
- **Burp Suite**: Para análisis manual
- **Nuclei**: Para vulnerability scanning
- **GitLeaks**: Para secrets scanning

### **Estándares y Compliance**
- **OWASP Top 10**: Seguimiento completo
- **ISO 27001**: Alignment en procesos
- **GDPR**: Compliance en manejo de datos
- **Argentina Data Protection**: Ley de Protección de Datos Personales

---

## 📞 **Contactos de Emergencia**

### **Security Team**
- **Primary**: security@jurisrank.com
- **Emergency**: +54 [REDACTED] (solo para incidentes críticos)
- **PGP Key**: Disponible bajo request

### **Legal Contact**
**Ignacio Adrian Lerer**  
Senior Corporate Lawyer | JurisRank Inventor  
⚖️ Legal matters: Ver CONTRIBUTING.md para contact info  
📧 IP concerns: Contactar via security team  

---

## 📋 **Actualizaciones de Política**

Esta política será revisada y actualizada regularmente. Las versiones históricas están disponibles en el historial de commits del repositorio.

**Última actualización**: 2025-08-26  
**Próxima revisión**: 2025-11-26  
**Versión**: 1.0  

---

*Seguridad a través de transparencia y colaboración*  
*Security through transparency and collaboration*

*Copyright (c) 2025 Ignacio Adrian Lerer. All rights reserved.*