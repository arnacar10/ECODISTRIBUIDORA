# 📦 Eco-Distribuidora S.A. — Sistema CRUD Legacy

> **Actividad 01: Auditoría de Sistemas Legacy — "Del Dato a la Decisión"**
> Sistema de gestión de inventario básico desarrollado en Python (Flask) + SQLite.

---

## ⚠ Nota de Auditoría

Este sistema es **intencionalmente deficiente** para la toma de decisiones estratégicas.
Fue generado como objeto de análisis para la actividad académica. Consultar el
[Informe de Auditoría Técnica](docs/INFORME_AUDITORIA.md) para el diagnóstico completo
basado en la Teoría General de Sistemas.

---

## 📁 Estructura del repositorio

```
eco-distribuidora/
│
├── app.py                      # Aplicación Flask principal (CRUD)
├── init_db.py                  # Script de inicialización de BD
├── populate_db.sql             # 50 registros SQL (25 productos + 25 ventas)
├── requirements.txt            # Dependencias Python
│
├── templates/                  # Plantillas HTML (Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── productos.html
│   ├── producto_form.html
│   ├── ventas.html
│   └── venta_form.html
│
├── static/
│   └── css/
│       └── style.css           # Estilos del sistema
│
└── docs/
    └── INFORME_AUDITORIA.md    # Informe técnico completo (TGS + DSS)
```

---

## 🚀 Instrucciones de ejecución

### Requisitos previos

- Python 3.9 o superior
- pip

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/eco-distribuidora.git
cd eco-distribuidora
```

### 2. Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Inicializar y poblar la base de datos

```bash
python init_db.py
```

Salida esperada:
```
[OK] Base de datos creada: eco_distribuidora.db
     Productos insertados: 25
     Ventas insertadas:    25

[!] Notas de auditoría:
     - Los clientes tienen variantes de nombre (entropía)
     - El stock NO fue descontado tras las ventas (falta de sinergia)
     - Las fechas están como TEXT, no como tipo DATE
```

### 5. Ejecutar la aplicación

```bash
python app.py
```

### 6. Abrir en el navegador

```
http://localhost:5000
```

---

## 🔍 Funcionalidades del sistema (CRUD)

| Módulo | Operaciones disponibles |
|---|---|
| **Productos** | Listar todos · Crear · Editar · Eliminar |
| **Ventas** | Listar todas · Registrar nueva · Eliminar |

### Lo que el sistema NO puede hacer (fallas auditadas)

| Pregunta de negocio | Disponible |
|---|---|
| ¿Qué productos agotarán stock en 15 días? | ❌ |
| ¿Qué clientes están dejando de comprar? | ❌ |
| ¿Qué categoría genera mayor margen? | ❌ |
| ¿Cuánto vendí este mes vs. el anterior? | ❌ |
| ¿Cuál es el ticket promedio por vendedor? | ❌ |

---

## 📊 Informe de Auditoría

Ver el análisis completo en [`docs/INFORME_AUDITORIA.md`](docs/INFORME_AUDITORIA.md), que incluye:

- Diagrama de base de datos (reverse engineering)
- Cuadro comparativo CRUD vs. DSS
- Análisis de Entropía y Sinergia (TGS)
- 3 decisiones críticas que el sistema no puede soportar
- 5 KPIs propuestos
- Propuesta de evolución hacia un DSS
- Conclusión ética — ODS 8

---

## 👥 Equipo (Squad)

| Miembro | Rol en la actividad |
|---|---|
| [Nombre 1] | Exploración del sistema · Análisis de entropía |
| [Nombre 2] | Diagrama de BD · Cuadro comparativo CRUD/DSS |
| [Nombre 3] | Propuesta de evolución DSS · KPIs |
| [Nombre 4] | Conclusión ética ODS 8 · Revisión final |

---

## 📚 Referencias

- Von Bertalanffy, L. (1968). *General System Theory*. George Braziller.
- Turban, E., Sharda, R., & Delen, D. (2011). *Decision Support and Business Intelligence Systems*. Pearson.
- ONU. (2015). *Objetivos de Desarrollo Sostenible — ODS 8*. Naciones Unidas.
