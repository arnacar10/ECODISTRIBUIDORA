# Informe de Auditoría Técnica
## "Del Dato a la Decisión" — Eco-Distribuidora S.A.

> **Actividad 01 · Auditoría de Sistemas Legacy**
> Marco teórico: Teoría General de Sistemas (TGS) · Ludwig von Bertalanffy
> Conexión ODS: Objetivo de Desarrollo Sostenible 8 – Trabajo Decente y Crecimiento Económico

---

## 1. Contexto y objetivo

Eco-Distribuidora S.A. posee un sistema informático funcional que registra ventas y mantiene un inventario de productos. Sin embargo, la gerencia es incapaz de responder preguntas estratégicas básicas:

- *¿Qué productos se quedarán sin stock en 15 días?*
- *¿Qué clientes están disminuyendo su frecuencia de compra?*

**Objetivo de esta auditoría:** identificar, desde la Teoría General de Sistemas, por qué un sistema CRUD tradicional es insuficiente para la toma de decisiones estratégicas, y proponer el camino hacia un DSS (Sistema de Soporte a la Decisión).

---

## 2. Diagrama de la base de datos actual (Reverse Engineering)

El sistema presenta únicamente dos tablas planas. La relación entre ellas es **lógica pero no declarada formalmente** (sin restricción `FOREIGN KEY`), lo que permite inconsistencias de datos.

```
┌───────────────────────┐          ┌───────────────────────┐
│       PRODUCTOS       │          │        VENTAS         │
├───────────────────────┤          ├───────────────────────┤
│ PK  id_producto       │◄── * ────│ FK* id_producto       │
│     nombre      TEXT  │          │ PK  id_venta          │
│     descripcion TEXT  │          │     nombre_cliente TEXT│
│     precio_unit REAL  │          │     cantidad     INT  │
│     stock_actual INT  │          │     total_venta  REAL │
│     categoria   TEXT  │          │     fecha_venta  TEXT │← TEXT, no DATE
│     fecha_ingr  TEXT  │          │     vendedor     TEXT │
└───────────────────────┘          └───────────────────────┘

FK* = Sin restricción FOREIGN KEY declarada en el esquema SQL
```

### Esquema SQL representativo

```sql
CREATE TABLE productos (
    id_producto      INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre           TEXT    NOT NULL,
    precio_unitario  REAL    NOT NULL DEFAULT 0,
    stock_actual     INTEGER NOT NULL DEFAULT 0,
    categoria        TEXT
    -- SIN: costo, stock_minimo, proveedor_id, fecha tipada
);

CREATE TABLE ventas (
    id_venta        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto     INTEGER,            -- sin FOREIGN KEY
    nombre_cliente  TEXT,               -- texto libre, sin entidad Cliente
    cantidad        INTEGER,
    total_venta     REAL,
    fecha_venta     TEXT                -- guardado como TEXT, no DATE
    -- SIN: descuento, estado, canal_venta, sucursal
);
```

---

## 3. Cuadro comparativo: CRUD Actual vs. DSS Necesario

| Dimensión | ❌ CRUD Actual | ✅ DSS Necesario |
|---|---|---|
| **Propósito** | Registrar y persistir datos sin análisis posterior | Transformar datos en información estratégica para decisiones gerenciales |
| **Modelo de datos** | 2 tablas planas, sin relaciones formales | Esquema estrella con dimensiones de tiempo, cliente, producto y geografía |
| **Capacidad analítica** | Solo consultas SELECT básicas | Reportes agregados, tendencias, proyecciones y alertas automáticas |
| **Visibilidad del stock** | Muestra número actual sin proyección | Alerta cuando un producto agotará stock en menos de X días |
| **Gestión de clientes** | Campo de texto libre en cada venta | Entidad Cliente con historial, segmentación RFM y alertas de inactividad |
| **Interfaz y UX** | Tablas interminables, sobrecarga cognitiva | Dashboard ejecutivo con KPIs, gráficos y drill-down bajo demanda |
| **Auditoría** | Sin registro de cambios | Log de auditoría y trazabilidad completa |
| **Exportación** | No contemplada | Reportes PDF/Excel y API para integración con BI externo |

---

## 4. Análisis de principios de TGS afectados

### 4.1 Entropía del sistema — Desorden creciente de la información

La entropía, en sistemas de información, es la tendencia al desorden cuando no existen mecanismos reguladores. Este sistema presenta **cinco focos de entropía críticos:**

1. **Fechas como texto libre:** `fecha_venta` se almacena como `TEXT` en lugar de tipo `DATE`. Esto impide ordenar cronológicamente, calcular intervalos de tiempo o agrupar por mes/trimestre.

2. **Clientes duplicados por variantes ortográficas:** El campo `nombre_cliente` acepta "Juan García", "Juan Garcia", "JUAN GARCIA" como entidades diferentes. A medida que crecen los datos, es imposible conocer el historial real de un cliente. *Evidencia en el script SQL: el mismo cliente aparece con 3 variantes.*

3. **Registros obsoletos sin depuración:** No existe mecanismo para desactivar productos descontinuados. Permanecen activos, contaminando reportes con datos irrelevantes.

4. **Sin transacciones ACID:** Una venta puede registrarse sin que el stock se descuente. El stock `actual` pierde representatividad con el tiempo y se convierte en un dato obsoleto.

5. **Saturación de interfaz:** Sin paginación ni filtros, a mayor volumen de datos mayor es el ruido visual. El sistema se vuelve progresivamente inutilizable con el crecimiento natural del negocio.

### 4.2 Falta de Sinergia — La suma de partes no genera valor superior

La sinergia sistémica implica que el conjunto produce más valor que sus partes aisladas. En este CRUD, **las partes coexisten sin comunicarse:**

1. **Sin feedback entre ventas y stock:** Una venta registrada no dispara ningún mecanismo de actualización del inventario. El sistema es estático y no retroalimenta.

2. **Sin cruce analítico entre tablas:** Aunque existen datos de productos y ventas, el sistema no calcula rotación por categoría, productos más vendidos ni margen por línea.

3. **Ausencia de la entidad Cliente:** Sin una tabla Clientes, es imposible correlacionar el comportamiento del comprador con el movimiento del inventario o detectar patrones de abandono.

4. **Solo OLTP, sin OLAP:** El sistema es puramente transaccional (OLTP). No existe ninguna capa analítica (OLAP) que procese los datos acumulados para producir inteligencia de negocio.

5. **Sin outputs proactivos:** El sistema nunca genera alertas, recomendaciones ni proyecciones. Solo responde a consultas manuales del operador.

### 4.3 Neguentropía necesaria

Para revertir la entropía, el sistema requiere:

- **Validación en ingreso:** constraints de BD (`CHECK`, `FOREIGN KEY`, tipos `DATE`), formularios con tipado estricto.
- **Procesos ETL periódicos** que normalicen registros duplicados de clientes.
- **Arquitectura de eventos** que dispare acciones al cruzar umbrales críticos (stock mínimo, inactividad de cliente).

---

## 5. Decisiones críticas de negocio que el sistema NO puede soportar

### Decisión 1: ¿Cuándo y cuánto reabastecer cada producto?

Sin calcular la **tasa de consumo promedio diario** por producto ni cruzarla con el stock actual, es imposible definir un punto de reorden óptimo. El gerente solo puede revisar el número de stock visualmente, sin proyección alguna.

**Consecuencia:** sobrestock (capital inmovilizado) o quiebre de inventario (venta perdida y cliente insatisfecho).

### Decisión 2: ¿Qué clientes están en riesgo de abandono?

Al no existir la entidad Cliente, es imposible calcular la frecuencia de compra individual, detectar caídas en la recurrencia o segmentar por valor de vida del cliente (LTV).

**Consecuencia:** la empresa no puede ejecutar acciones preventivas de retención porque el sistema no genera ninguna señal de alerta temprana de inactividad.

### Decisión 3: ¿Qué línea de productos es más rentable y debe priorizarse?

Sin calcular el **margen bruto por categoría**, sin conocer la rotación ni la estacionalidad, la gerencia no puede decidir qué productos ampliar, descontinuar o promocionar.

**Consecuencia:** todas las categorías se ven idénticas en una tabla de registros planos; las decisiones de compra y marketing se basan en intuición, no en datos.

---

## 6. KPIs propuestos para el DSS

| # | KPI | Fórmula | Umbral de alerta |
|---|---|---|---|
| 1 | **Días de Stock Proyectados (DSP)** | `stock_actual ÷ ventas_prom_diarias` | Alerta si < 15 días |
| 2 | **Tasa de Retención de Clientes (TRC)** | `clientes_activos_período / clientes_prev × 100` | Alerta si < 70% |
| 3 | **Margen Bruto por Categoría (MBC)** | `(precio - costo) × unidades / ingresos × 100` | Monitoreo mensual |
| 4 | **Velocidad de Rotación (VR)** | `unidades_vendidas / stock_promedio` | Baja rotación = riesgo sobrestock |
| 5 | **Ticket Promedio (TP)** | `ingresos_totales ÷ número_transacciones` | Tendencia para campañas |

---

## 7. Propuesta de evolución hacia un DSS

### 7.1 Nuevos módulos necesarios

| Módulo | Descripción |
|---|---|
| **Entidades extendidas** | Tablas `Clientes`, `Proveedores`, `Categorias`, `MovimientosInventario` con FK declaradas |
| **Capa analítica (OLAP)** | Vistas materializadas o tablas de hechos que agreguen ventas por período, cliente y categoría |
| **Motor de alertas** | Reglas configurables de umbral: stock < N días, cliente sin compra > 30 días |
| **Dashboard ejecutivo** | KPIs en tiempo real, gráficos de tendencia, drill-down. Reemplaza tablas interminables |
| **Módulo predictivo** | Regresión o media móvil sobre histórico para proyectar demanda futura |
| **Auditoría y seguridad** | Log de cambios, control de acceso por roles, backup automatizado |

### 7.2 Diagramas UML recomendados

- **Diagrama de Clases:** Entidades Cliente, Producto, Venta, Proveedor, Categoría con multiplicidades correctas.
- **Diagrama de Casos de Uso:** Actores (Gerente, Vendedor, Sistema de alertas) e interacciones, diferenciando operaciones OLTP y OLAP.
- **Diagrama de Secuencia:** Flujo: *registro de venta → actualización de stock → verificación de umbral → alerta automática al gerente.*

### 7.3 Arquitectura objetivo (DSS)

```
┌─────────────────────────────────────────────────────────┐
│                  CAPA DE PRESENTACIÓN                   │
│         Dashboard ejecutivo · Alertas · Reportes        │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                  CAPA ANALÍTICA (OLAP)                  │
│      KPIs · Tendencias · Proyecciones · Segmentación    │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                CAPA DE DATOS ENRIQUECIDA                │
│  Productos · Clientes · Ventas · Proveedores · Auditoría│
└─────────────────────────────────────────────────────────┘
```

---

## 8. Conclusión ética — Conexión ODS 8

> **ODS 8:** Promover el crecimiento económico sostenido, inclusivo y sostenible, el empleo pleno y productivo y el **trabajo decente** para todas las personas.

Un sistema que obliga al empleado a revisar tablas interminables para extraer información básica no es solamente una falla técnica: **es una carga laboral injusta.**

El trabajador dedica horas a tareas de bajo valor agregado que podrían automatizarse:

- Revisión manual de tablas para detectar stock bajo
- Elaboración de reportes en hojas de cálculo externas
- Corrección manual de registros duplicados de clientes
- Búsqueda de patrones de venta sin herramientas analíticas

Esto genera **agotamiento cognitivo, errores por fatiga y frustración**, reduciendo la calidad del trabajo y la satisfacción laboral.

Desde la perspectiva del ODS 8, promover el trabajo decente implica diseñar herramientas tecnológicas que **dignifiquen las tareas del trabajador**, eliminando la carga de información redundante y devolviendo tiempo para actividades de mayor valor estratégico.

La solución ética no es solo modernizar el software. Es comprometer a los equipos de TI y dirección en el diseño de herramientas **centradas en el usuario**, que reduzcan la fricción informacional y garanticen que ningún trabajador pierda tiempo valioso compensando las deficiencias del sistema que debería servirles.

---

## 9. Checklist de cumplimiento

- [x] El informe identifica claramente al menos **2 fallas relacionadas con la Entropía** del sistema *(Sección 4.1 — 5 fallas de entropía)*
- [x] Se proponen al menos **3 indicadores (KPIs)** que el sistema debería tener para ser un DSS *(Sección 6 — 5 KPIs con fórmula)*
- [x] El informe está redactado en **Markdown en GitHub** *(este archivo)*
- [x] Se evidencia la participación de los 4 miembros mediante el **historial de commits** *(ver commits del repositorio)*
- [x] El análisis incluye una **reflexión sobre el impacto en la productividad (ODS 8)** *(Sección 8)*

---

*Informe generado como parte de la Actividad 01 · Auditoría de Sistemas Legacy · "Del Dato a la Decisión"*
