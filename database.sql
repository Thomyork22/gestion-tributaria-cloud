-- DDL Arquitectura Cloud & Gestión Tributaria (PostgreSQL)

CREATE TABLE IF NOT EXISTS certificados_tributarios (
    id SERIAL PRIMARY KEY,
    folio VARCHAR(100) UNIQUE NOT NULL,
    storage_key VARCHAR(255) NOT NULL,
    estado VARCHAR(50) NOT NULL DEFAULT 'PENDIENTE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS auditoria_sistema (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    accion VARCHAR(100) NOT NULL,
    entidad VARCHAR(150) NOT NULL,
    resultado VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para optimización de consultas masivas
CREATE INDEX idx_certificados_estado ON certificados_tributarios(estado);
CREATE INDEX idx_auditoria_usuario ON auditoria_sistema(usuario_id);