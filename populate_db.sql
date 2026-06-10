-- =============================================================
-- Eco-Distribuidora S.A. – Script de Población de Base de Datos
-- 50 registros planos (25 productos + 25 ventas)
-- Nota de Auditoría: Los datos son intencionalmente "sucios":
--   - fechas como TEXT (no DATE)
--   - clientes duplicados con variantes ortográficas
--   - stock no actualizado tras ventas registradas
-- =============================================================

-- Crear tablas (idempotente)
CREATE TABLE IF NOT EXISTS productos (
    id_producto      INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre           TEXT    NOT NULL,
    descripcion      TEXT,
    precio_unitario  REAL    NOT NULL DEFAULT 0,
    stock_actual     INTEGER NOT NULL DEFAULT 0,
    categoria        TEXT,
    fecha_ingreso    TEXT
);

CREATE TABLE IF NOT EXISTS ventas (
    id_venta        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto     INTEGER,
    nombre_cliente  TEXT,
    cantidad        INTEGER NOT NULL DEFAULT 1,
    total_venta     REAL,
    fecha_venta     TEXT,
    vendedor        TEXT
);

-- Limpiar datos previos
DELETE FROM productos;
DELETE FROM ventas;

-- =============================================================
-- 25 PRODUCTOS
-- =============================================================
INSERT INTO productos (nombre, descripcion, precio_unitario, stock_actual, categoria, fecha_ingreso) VALUES
('Arroz largo fino 5kg',       'Arroz blanco extra largo',          35.50,  120, 'Alimentos',    '2024-01-10'),
('Aceite de soya 1L',          'Aceite vegetal refinado',           28.00,   85, 'Alimentos',    '2024-01-12'),
('Azúcar blanca 2kg',          'Azúcar refinada estándar',          22.00,   60, 'Alimentos',    '2024-01-15'),
('Harina de trigo 1kg',        'Harina todo uso',                   12.50,  200, 'Alimentos',    '2024-01-18'),
('Leche entera 1L',            'Leche pasteurizada entera',         10.00,  150, 'Alimentos',    '2024-02-01'),
('Fideos spaghetti 500g',      'Pasta de trigo duro',                8.50,   90, 'Alimentos',    '2024-02-03'),
('Sal yodada 1kg',             'Sal de mesa con yodo',               4.00,  300, 'Alimentos',    '2024-02-05'),
('Café molido 250g',           'Mezcla arábica y robusta',          45.00,   40, 'Alimentos',    '2024-02-10'),
('Refresco cola 2L',           'Bebida gaseosa cola',               15.00,  200, 'Bebidas',      '2024-02-12'),
('Agua mineral 600ml',         'Agua purificada sin gas',            5.00,  500, 'Bebidas',      '2024-02-14'),
('Jugo naranja 1L',            'Jugo natural pasteurizado',         18.00,   70, 'Bebidas',      '2024-02-20'),
('Cerveza lata 350ml',         'Cerveza rubia nacional',            12.00,  180, 'Bebidas',      '2024-03-01'),
('Detergente líquido 1L',      'Limpieza ropa a mano y máquina',    32.00,   55, 'Limpieza',     '2024-03-05'),
('Cloro desinfectante 1L',     'Blanqueador multiusos',             15.00,   80, 'Limpieza',     '2024-03-07'),
('Jabón de lavar 250g',        'Jabón en barra para ropa',           6.50,  120, 'Limpieza',     '2024-03-10'),
('Desengrasante cocina 750ml', 'Limpiador grasa superficies',       28.00,   35, 'Limpieza',     '2024-03-12'),
('Shampoo cabello 400ml',      'Shampoo hidratante normal',         38.00,   60, 'Higiene',      '2024-03-15'),
('Jabón de tocador 3-pack',    'Jabón antibacterial 3 unidades',    18.00,   90, 'Higiene',      '2024-03-18'),
('Pasta dental 100g',          'Pasta dental con flúor',            14.00,  110, 'Higiene',      '2024-03-20'),
('Papel higiénico 12u',        '12 rollos doble hoja',              55.00,   45, 'Higiene',      '2024-03-22'),
('Cuaderno universitario 100h','Cuaderno espiral 100 hojas',        18.00,   75, 'Otros',        '2024-04-01'),
('Bolígrafos x10',             'Pack 10 bolígrafos azules',         15.00,  100, 'Otros',        '2024-04-03'),
('Pila AA x4',                 'Pilas alcalinas 4 unidades',        22.00,   50, 'Electrónica',  '2024-04-05'),
('Foco LED 9W',                'Foco ahorro energía base E27',      35.00,   30, 'Electrónica',  '2024-04-08'),
('Cinta adhesiva 18mm',        'Rollo cinta transparente',           8.00,  150, 'Otros',        '2024-04-10');

-- =============================================================
-- 25 VENTAS
-- Nota: Los clientes tienen variantes de nombre (entropía)
--       El stock no refleja estas ventas (falta de sinergia)
-- =============================================================
INSERT INTO ventas (id_producto, nombre_cliente, cantidad, total_venta, fecha_venta, vendedor) VALUES
(1,  'Maria Fernandez',       3,  106.50, '2024-03-01', 'Carlos López'),
(2,  'Juan García',           2,   56.00, '2024-03-02', 'Ana Mamani'),
(5,  'Rosa Torres',           5,   50.00, '2024-03-03', 'Carlos López'),
(9,  'Pedro Quispe',          4,   60.00, '2024-03-04', 'Ana Mamani'),
(13, 'María Fernandez',       1,   32.00, '2024-03-05', 'Carlos López'),  -- variante: "María"
(3,  'Lucía Vargas',          2,   44.00, '2024-03-06', 'Pedro Salinas'),
(8,  'Juan Garcia',           1,   45.00, '2024-03-07', 'Ana Mamani'),     -- variante: sin tilde
(17, 'Elena Morales',         2,   76.00, '2024-03-08', 'Carlos López'),
(10, 'Carlos Mamani',        10,   50.00, '2024-03-09', 'Pedro Salinas'),
(20, 'Rosa Torres',           1,   55.00, '2024-03-10', 'Ana Mamani'),
(6,  'Pedro Quispe',          3,   25.50, '2024-03-11', 'Carlos López'),
(14, 'Lucia Vargas',          2,   30.00, '2024-03-12', 'Pedro Salinas'),  -- variante: sin tilde
(4,  'Ana Condori',           5,   62.50, '2024-03-13', 'Ana Mamani'),
(24, 'Roberto Flores',        2,   70.00, '2024-03-14', 'Carlos López'),
(11, 'Maria Fernandez',       3,   54.00, '2024-03-15', 'Pedro Salinas'), -- variante: sin acento
(7,  'Carlos Mamani',        20,   80.00, '2024-03-16', 'Ana Mamani'),
(19, 'Elena Morales',         3,   42.00, '2024-03-17', 'Carlos López'),
(2,  'Juan García',           1,   28.00, '2024-03-18', 'Pedro Salinas'),
(15, 'Sofía Ríos',            4,   26.00, '2024-03-19', 'Ana Mamani'),
(22, 'Ana Condori',           3,   45.00, '2024-03-20', 'Carlos López'),
(1,  'Roberto Flores',        2,   71.00, '2024-03-21', 'Pedro Salinas'),
(12, 'Sofia Rios',            6,   72.00, '2024-03-22', 'Ana Mamani'),    -- variante: sin tilde
(18, 'Lucía Vargas',          2,   36.00, '2024-03-23', 'Carlos López'),
(23, 'Pedro Quispe',          3,   66.00, '2024-03-24', 'Pedro Salinas'),
(16, 'MARIA FERNANDEZ',       1,   28.00, '2024-03-25', 'Ana Mamani');   -- variante: mayúsculas
