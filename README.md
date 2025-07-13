<!-- Encabezado centrado con badges visuales -->
<p align="center">
  <img src="https://img.shields.io/badge/Flask-2.3-blue?logo=flask" />
  <img src="https://img.shields.io/badge/PostgreSQL-17.4-blue?logo=postgresql" />
  <img src="https://img.shields.io/badge/Docker-ready-blue?logo=docker" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
</p>

<h1 align="center">🍔 Delicias Order · <code>restaurant_db</code></h1>

<p align="center">
Sistema de gestión para restaurantes desarrollado con Flask, PostgreSQL y Docker.
</p>

---

## 🍽️ Descripción del Proyecto
> Proyecto web que digitaliza la administración de un restaurante: gestión de stock, pedidos, productos, usuarios y reportes diarios. Pensado para PyMEs gastronómicas, con un entorno portable, escalable y profesional.

---

## 📁 Estructura del Proyecto
```bash
proyectoRestaurant_db/
├── app.py                  # Punto de entrada de la app Flask
├── alembic/                # Configuración de migraciones
├── migrations/             # Archivos generados por Alembic
├── static/                 # Archivos estáticos (CSS, JS)
├── templates/              # Plantillas HTML (Jinja2)
├── env.py                  # Configuración Alembic
├── .env                    # Variables de entorno
├── Dockerfile              # Imagen Docker
├── docker-compose.yml      # Servicios Flask + PostgreSQL
├── requirements.txt        # Dependencias Python
├── backup.sql              # Dump de la base de datos
└── README.md               # Este archivo
---

## ⚙️ Tecnologías Usadas

| 🔧 Tecnología | 💡 Descripción                          |
| ------------- | --------------------------------------- |
| 🐍 Flask      | Framework backend ligero en Python      |
| 🐘 PostgreSQL | Base de datos relacional                |
| 🐳 Docker     | Contenedores y despliegue reproducible  |
| ⚗️ Alembic    | Migraciones de base de datos SQLAlchemy |
| 🌐 Bootstrap  | Interfaz responsiva y moderna           |
| 🧪 Jinja2     | Motor de plantillas para HTML dinámico  |

---

## 🚀 Cómo levantar el proyecto con Docker

### 🧱 1. Clonar el repositorio

```bash
git clone https://github.com/brunorios21/proyectoRestaurant_db.git
cd proyectoRestaurant_db
```

### 🛠️ 2. Configurar archivo `.env`

Crear un archivo `.env` con el siguiente contenido:

```env
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:postgres@db:5432/restaurant_db
SECRET_KEY=clave_super_secreta
```

### 🐳 3. Levantar con Docker Compose

```bash
docker-compose up --build
```

✔️ Construye la imagen Flask
✔️ Levanta la app y la base de datos PostgreSQL
✔️ Inicia servicios desde `docker-compose.yml`

---

## ⚗️ Migraciones de Base de Datos (Alembic)

Crear una nueva migración:

```bash
alembic revision -m "nombre_migracion"
```

Aplicar migraciones:

```bash
alembic upgrade head
```

---

## ✅ Funcionalidades Implementadas

* ✅ ABM de productos
* ✅ Registro y estado de pedidos
* ✅ Control y movimientos de stock
* ✅ Gestión de usuarios
* ✅ Backups manuales (`backup.sql`)
* ✅ Migraciones con Alembic

---

## 📋 Requisitos

* Python 3.11+
* PostgreSQL 17.4+
* Docker + Docker Compose
* Navegador moderno (Chrome, Firefox, etc.)

---

## 🔐 Seguridad

🔑 Variables sensibles en `.env`
🔐 Contraseñas hasheadas (`werkzeug.security`)
🛡️ Rutas protegidas por login y roles

---

## 🧪 Pruebas

> ⚠️ *En desarrollo* — Próximamente tests unitarios con `pytest`.

---

## 🧑‍💻 Autor

**Bruno Ríos**
📫 [brunorioscorp4@gmail.com](mailto:brunorioscorp4@gmail.com)
💼 [LinkedIn](https://www.linkedin.com/in/bruno-rios-576016328/)
🌐 Proyecto asociado: **Delicias Order**

---

## 🪪 Licencia

Distribuido bajo la licencia MIT.
Consultá el archivo [`LICENSE`](./LICENSE) para más detalles.

```
---
