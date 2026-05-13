# Sistema AFE - Gestión de Facturas Electrónicas

**https://afe-platform-iota.vercel.app/login

Sistema empresarial integral para automatizar la gestión, aprobación y validación de facturas electrónicas en entornos multi-tenant.

## 🚀 Stack Tecnológico

- **Frontend:** React 19 + TypeScript + Redux + Material-UI
- **Backend:** FastAPI + Python 3.10+ + SQLAlchemy
- **Base de Datos:** MySQL 8.0+ (Normalización 3NF)
- **Invoice Extractor:** Python + Microsoft Graph API

---

## 📁 Estructura del Proyecto

```
PRIVADO_ODO/
├── afe-backend/           # API REST con FastAPI
├── afe_frontend/          # Aplicación React SPA
├── invoice_extractor/     # Módulo de extracción automática
└── README.md             # Este archivo
```

---

## ⚡ Quick Start

> **📚 Para instalación completa paso a paso, ver [INSTALACION.md](INSTALACION.md)**

### Requisitos Previos
- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Cuenta Azure AD (para OAuth - opcional)

### 1️⃣ Base de Datos

```bash
# Crear base de datos
mysql -u root -p
CREATE DATABASE afe_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'afe_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON afe_db.* TO 'afe_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2️⃣ Backend

```bash
cd afe-backend

# Entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Editar .env con credenciales

# Migraciones
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload --port 8000
```

**Documentación API:** http://localhost:8000/docs

### 3️⃣ Frontend

```bash
cd afe_frontend

# Dependencias
npm install

# Configurar .env.local
cp .env.example .env.local
# Editar VITE_API_BASE_URL=http://localhost:8000/api/v1

# Iniciar servidor
npm run dev
```

**Aplicación:** http://localhost:5173

### 4️⃣ Invoice Extractor

```bash
cd invoice_extractor

# Entorno virtual
python -m venv venv
source venv/bin/activate

# Dependencias
pip install -r requirements.txt

# Configurar .env (credenciales Microsoft Graph)
cp .env.example .env

# Ejecutar extracción manual
python -m src.main
```

---

## 🏗️ Arquitectura General

```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │ HTTPS
┌──────▼───────────┐      ┌─────────────────┐
│  Frontend React  │◄────►│  Backend FastAPI│
│  Puerto: 5173    │ REST │  Puerto: 8000   │
└──────────────────┘      └────────┬────────┘
                                   │
                          ┌────────▼────────┐
                          │  MySQL Database │
                          │  Puerto: 3306   │
                          └────────▲────────┘
                                   │
                        ┌──────────┴──────────┐
                        │ Invoice Extractor   │
                        │ (Cron/Scheduler)    │
                        └─────────────────────┘
                                   │
                          ┌────────▼─────────┐
                          │ Microsoft 365    │
                          │ Graph API        │
                          └──────────────────┘
```

---

## 📊 Módulos Principales

### Backend (FastAPI)
- ✅ **Autenticación:** JWT local + OAuth Microsoft SSO
- ✅ **Multi-tenancy:** Segregación por grupos jerárquicos
- ✅ **Workflow:** Aprobación manual y automática (IA)
- ✅ **RBAC:** 4 roles (admin, responsable, contador, viewer)
- ✅ **Notificaciones:** Emails vía Microsoft Graph
- ✅ **Dashboard:** Estadísticas en tiempo real

**Endpoints:** 80+ endpoints REST documentados en Swagger

### Frontend (React)
- ✅ **Dashboard:** Métricas visuales con gráficos (Recharts)
- ✅ **Gestión Facturas:** CRUD completo con filtros avanzados
- ✅ **Workflow:** Aprobación/rechazo con modal de detalle
- ✅ **Proveedores:** Gestión y asignación de NITs
- ✅ **Configuración:** Email extractor, grupos, usuarios
- ✅ **Tema:** Material-UI personalizado (Zentria)

### Base de Datos (MySQL)
- ✅ **15+ Tablas** normalizadas en 3NF
- ✅ **Tablas principales:**
  - `facturas` - Núcleo del sistema con estados
  - `workflow_aprobacion_facturas` - Auditoría 3NF
  - `proveedores` - Catálogo de proveedores
  - `usuarios` - Autenticación dual (local/OAuth)
  - `grupos` - Multi-tenancy jerárquico
  - `asignacion_nit_responsable` - Asignaciones automáticas

### Invoice Extractor (Python)
- ✅ **Descarga automática** de correos corporativos
- ✅ **Parsing:** XML (DIAN) y PDF
- ✅ **Extracción incremental:** Solo correos nuevos
- ✅ **Deduplicación:** Por CUFE (Código Único)
- ✅ **Configuración:** Whitelist de NITs por cuenta
- ✅ **Scheduler:** APScheduler o Cron job

---

## 🔐 Variables de Entorno

### Backend `.env`
```bash
DATABASE_URL=mysql+pymysql://usuario:password@localhost:3306/afe_db
SECRET_KEY=tu-clave-secreta-aqui
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
GRAPH_TENANT_ID=xxx
GRAPH_CLIENT_ID=xxx
GRAPH_CLIENT_SECRET=xxx
OAUTH_MICROSOFT_TENANT_ID=xxx
OAUTH_MICROSOFT_CLIENT_ID=xxx
OAUTH_MICROSOFT_CLIENT_SECRET=xxx
```

### Frontend `.env.local`
```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Invoice Extractor `.env`
```bash
DATABASE_URL=mysql+pymysql://usuario:password@localhost:3306/afe_db
TENANT_ID_CORREOS=xxx
CLIENT_ID_CORREOS=xxx
CLIENT_SECRET_CORREOS=xxx
BACKEND_API_URL=http://localhost:8000/api/v1
```

---

## 🔄 Flujo de Datos Completo

```
1. Microsoft 365 Correo
       ↓
2. Invoice Extractor (descarga + parse)
       ↓
3. INSERT en MySQL (estado: en_cuarentena)
       ↓
4. Backend clasifica (asigna grupo + responsable)
       ↓
5. Automatización (IA analiza confianza)
       ├─ Alta confianza (>88%) → APROBADA_AUTO
       └─ Baja confianza → EN_REVISION (manual)
       ↓
6. Usuario aprueba/rechaza (Frontend)
       ↓
7. Contador valida (estado: validada_contabilidad)
       ↓
8. Sistema de Pagos (⚠️ NO IMPLEMENTADO)
```

---

## 🎯 Funcionalidades Principales

### ✅ Implementado (95%)
- [x] Extracción automática de facturas desde email
- [x] Workflow de aprobación manual y automático
- [x] Multi-tenancy con grupos jerárquicos
- [x] Dashboard con estadísticas y gráficos
- [x] Autenticación OAuth Microsoft + local
- [x] Sistema de notificaciones por email
- [x] Validación contable
- [x] Exportación a Excel
- [x] Auditoría completa de cambios



---

## 📖 Documentación Técnica

### Documentos Disponibles
- **[DOCUMENTACION_TECNICA.md](DOCUMENTACION_TECNICA.md)** - Documentación técnica completa de traspaso
- **[Backend README](afe-backend/README.md)** - Guía detallada del backend
- **[Frontend README](afe_frontend/README.md)** - Guía del frontend
- **[Invoice Extractor README](invoice_extractor/README.md)** - Guía del extracto

---

## 🚀 Despliegue en Producción

### Backend
```bash
# Con Uvicorn + Systemd
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Con Gunicorn
gunicorn app.main:app --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Frontend
```bash
npm run build
# Servir dist/ con Nginx o Apache
```

### Invoice Extractor
```bash
# Cron job (cada 2 horas)
0 */2 * * * cd /opt/invoice_extractor && \
  /opt/invoice_extractor/venv/bin/python -m src.main
```

---

## 🔧 Configuración Azure AD

### Para OAuth SSO (Backend)
1. Azure Portal → App registrations → New registration
2. Redirect URI: `http://localhost:8000/api/v1/auth/microsoft-callback`
3. API permissions: `User.Read` (Delegated)
4. Copiar: Tenant ID, Client ID, Client Secret

### Para Microsoft Graph (Email)
1. Azure Portal → App registrations → New registration
2. API permissions: `Mail.Read`, `Mail.Send` (Application)
3. Grant admin consent
4. Copiar: Tenant ID, Client ID, Client Secret

---

## 🧪 Testing

```bash
# Backend
cd afe-backend
pytest

# Frontend
cd afe_frontend
npm run test
```

---

## 📊 Modelo de Datos (Resumen)

```
usuarios (RBAC)
    ↓
facturas ──→ workflow_aprobacion (auditoría 3NF)
    ↓
proveedores
    ↓
grupos (multi-tenant)
    ↓
asignacion_nit_responsable (automatización)
```

**15+ tablas** con relaciones completas. Ver diagramas en documentación técnica.

---

## 🤝 Contribución

1. Fork del proyecto
2. Crear branch: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m "Agregar nueva funcionalidad"`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

---

## 📝 Estado del Proyecto

**Estado:**  Operativo  (95% completo)
**Última actualización:** 22 de Diciembre de 2025




---

