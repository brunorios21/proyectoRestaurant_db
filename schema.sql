-- Creación de la base de datos (si es necesario en PostgreSQL)
CREATE DATABASE restaurant_db;

-- Seleccionar la base de datos (para PostgreSQL, en SQLite esto no es necesario)
-- \c restaurant_db; -- Este comando es específico de PostgreSQL y no es SQL estándar.

-- Tabla de Usuarios
CREATE TABLE Usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol VARCHAR(50) CHECK (rol IN ('admin', 'mesero', 'cocinero')) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Productos
CREATE TABLE Productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock_actual INT DEFAULT 0,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Pedidos
CREATE TABLE Pedidos (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES Usuarios(id),
    cliente VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    metodo_pago VARCHAR(50) NOT NULL,
    total_precio DECIMAL(10,2) NOT NULL, -- Cambiado de "total" a "total_precio"
    estado VARCHAR(50) CHECK (estado IN ('pendiente', 'preparando', 'entregado')) DEFAULT 'pendiente',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de DetallePedidos
CREATE TABLE DetallePedidos (
    id SERIAL PRIMARY KEY,
    pedido_id INT REFERENCES Pedidos(id) ON DELETE CASCADE,
    producto_id INT REFERENCES Productos(id),
    cantidad INT NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL
);

-- Tabla de Stock (ingredientes)
CREATE TABLE Stock (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cantidad INT NOT NULL DEFAULT 0,
    unidad VARCHAR(50) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Movimientos de Stock (registro de entrada/salida)
CREATE TABLE MovimientosStock (
    id SERIAL PRIMARY KEY,
    stock_id INT REFERENCES Stock(id),
    tipo_movimiento VARCHAR(50) CHECK (tipo_movimiento IN ('entrada', 'salida')) NOT NULL,
    cantidad INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Envíos (si el restaurante maneja delivery)
CREATE TABLE Envios (
    id SERIAL PRIMARY KEY,
    pedido_id INT REFERENCES Pedidos(id) ON DELETE CASCADE,
    direccion VARCHAR(255) NOT NULL,
    estado VARCHAR(50) CHECK (estado IN ('pendiente', 'en camino', 'entregado')) DEFAULT 'pendiente',
    repartidor VARCHAR(100),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Consultas de Selección
SELECT * FROM Usuarios;
SELECT * FROM Productos WHERE stock_actual < 5;
SELECT * FROM Pedidos WHERE estado = 'pendiente';

-- Inserciones
INSERT INTO Productos (nombre, descripcion, precio, stock_actual) VALUES ('Ensalada César', 'Ensalada con aderezo César y crutones', 7.50, 20);

-- Actualizaciones
UPDATE Productos SET precio = 9.90 WHERE nombre = 'Hamburguesa';
UPDATE Pedidos SET estado = 'preparando' WHERE id = 1;

-- Eliminaciones
DELETE FROM Productos WHERE id = 3;
DELETE FROM Usuarios WHERE id = 2;

-- Consultas con JOIN
SELECT dp.*, p.nombre 
FROM DetallePedidos dp 
JOIN Productos p ON dp.producto_id = p.id 
WHERE dp.pedido_id = 1;