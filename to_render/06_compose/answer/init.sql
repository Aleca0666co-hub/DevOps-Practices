CREATE TABLE IF NOT EXISTS productos (
  id SERIAL PRIMARY KEY,
  nombre TEXT,
  precio INT
);

INSERT INTO productos (nombre, precio) VALUES
('Laptop', 1200),
('Mouse', 25),
('Teclado', 45);
