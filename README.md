# ☁️ Sistema de Gestión Tributaria Automatizada

![Architecture](https://img.shields.io/badge/Architecture-Cloud%20Microservices-blue)
![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20Django%20%7C%20AWS%20S3%20%7C%20Redis%20%7C%20PostgreSQL-success)
![Security](https://img.shields.io/badge/Security-MFA%20%7C%20RBAC%20%7C%20JWT-orange)

## 📌 Contexto del Proyecto
Plataforma Cloud desarrollada para centralizar, validar y homologar lotes masivos de certificados tributarios con integración directa al **Servicio de Impuestos Internos (SII)**. El sistema soluciona los cuellos de botella derivados de la carga manual dispersa, garantizando escalabilidad horizontal y altos estándares de auditoría.

## 🏛️ Arquitectura de Sistemas
El ecosistema está desacoplado en componentes especializados para evitar bloqueos por concurrencia:
* **Frontend (SPA / CDN):** Interfaz de usuario reactiva alojada en CDN con balanceador de carga.
* **API Gateway & Auth:** Enrutamiento centralizado y seguridad basada en tokens **JWT**, **MFA obligatorio** y Control de Acceso Basado en Roles (**RBAC**).
* **Async Workers & Cache (Redis):** Procesamiento en segundo plano de documentos masivos mediante colas de mensajes.
* **Persistencia Híbrida:** Metadatos transaccionales almacenados en **PostgreSQL**, y documentos físicos (PDF/ZIP) descargados de manera segura en objetos **AWS S3**.

## ⚙️ Decisiones de Diseño y Post-Mortem
1. **Desacoplamiento con AWS S3:** Evita saturar la base de datos relacional con archivos pesados, utilizando un modelo híbrido mediante `storage_key`.
2. **Patrón Adaptador para el SII:** Encapsula la comunicación con la API externa del SII, protegiendo la lógica de negocio interna ante posibles cambios en los contratos del proveedor.
3. **Seguridad por Capas (MFA y RBAC):** Restringe las operaciones financieras y administrativas según el perfil del usuario (Corredor, Auditor o Administrador).

## 📁 Estructura del Repositorio
```text
/
├── async_cert_worker.py    # Worker asíncrono (Celery/Boto3/S3)
├── database.sql            # Script DDL de PostgreSQL
└── README.md               # Documentación de arquitectura