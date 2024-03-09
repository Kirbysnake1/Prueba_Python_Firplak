CREATE DATABASE FIRPLAKSA
use FIRPLAKSA

CREATE TABLE Entregas (
    ID_Entrega INT AUTO_INCREMENT PRIMARY KEY,
    Numero_Guia_Transporte VARCHAR(50),
    Numero_Documento_Entrega VARCHAR(50),
    Fecha_Despacho DATE,
    Cliente VARCHAR(100),
    Destino VARCHAR(100),
    Fecha_Entrega DATE,
    Estado_Entrega VARCHAR(50),
    Tipo_Transportadora VARCHAR(50),
    POD_Recibido BOOLEAN,
    Observaciones TEXT,
    Fecha_Registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



select * from Entregas