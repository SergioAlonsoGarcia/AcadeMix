-- Crear la base de datos
CREATE DATABASE Academix_DB;
USE Academix_DB;

-- Crear la tabla usuarios
CREATE TABLE usuarios (
    Correo VARCHAR(255) PRIMARY KEY NOT NULL UNIQUE,
    Nombre VARCHAR(255) NOT NULL,
    Contraseña VARCHAR(255) NOT NULL,
    UNIQUE (Nombre)  -- Agregar un índice único en la columna Nombre
);

-- Crear la tabla clases con las claves foráneas
CREATE TABLE clases (
    ID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Nombre VARCHAR(255) NOT NULL UNIQUE,  -- Hacer que 'Nombre' sea único
    Docente VARCHAR(255) NOT NULL,
    FOREIGN KEY (Docente) REFERENCES usuarios(Nombre),
    Correo_Docente VARCHAR(255),
    FOREIGN KEY (Correo_Docente) REFERENCES usuarios(Correo)
);


CREATE TABLE estudiantes_clases (
    ID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    ID_Clase INT NOT NULL,
    Correo_Estudiante VARCHAR(255) NOT NULL,
    Nombre_Clase VARCHAR(255) NOT NULL,
    FOREIGN KEY (ID_Clase) REFERENCES clases(ID),
    FOREIGN KEY (Correo_Estudiante) REFERENCES usuarios(Correo),
    FOREIGN KEY (Nombre_Clase) REFERENCES clases(Nombre)
);

CREATE TABLE tareas_cursas (
    ID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Nombre VARCHAR(255) NOT NULL,
    Tema VARCHAR(255) NOT NULL,
    ID_Clase INT NOT NULL,
    Archivo LONGBLOB, -- Campo para almacenar el archivo PDF en formato binario
    Estado VARCHAR(50) DEFAULT 'pendiente', -- Nuevo campo para el estado de la tarea
    FOREIGN KEY (ID_Clase) REFERENCES clases(ID)
);

-- Inserciones en la tabla usuarios
INSERT INTO `academix_db`.`usuarios` (`Correo`, `Nombre`, `Contraseña`) VALUES 
('carlinjubilate@gmail.com', 'Pepin', '1234'),
('juanperez@gmail.com', 'Juan Perez', '5678'),
('mariagomez@gmail.com', 'Maria Gomez', 'abcd1234'),
('luisfernandez@gmail.com', 'Luis Fernandez', 'qwerty123'),
('andreavazquez@gmail.com', 'Andrea Vazquez', 'password2024'),
('josemaria@gmail.com', 'Jose Maria', '1234abcd'),
('lauracastillo@gmail.com', 'Laura Castillo', 'asdfgh1234'),
('pedroperez@gmail.com', 'Pedro Perez', 'securepass99'),
('soniamartinez@gmail.com', 'Sonia Martinez', 'qwerty12345'),
('alexandradiaz@gmail.com', 'Alexandra Diaz', 'mypassword01'),
('1','Khal','1');

INSERT INTO `academix_db`.`clases` (`Nombre`, `Docente`, `Correo_Docente`) 
VALUES
('Matemáticas', 'Pepin', 'carlinjubilate@gmail.com'),
('Física', 'Maria Gomez', 'mariagomez@gmail.com'),
('Química', 'Luis Fernandez', 'luisfernandez@gmail.com'),
('Historia', 'Andrea Vazquez', 'andreavazquez@gmail.com'),
('Literatura', 'Sonia Martinez', 'soniamartinez@gmail.com'),
('Biología', 'Pedro Perez', 'pedroperez@gmail.com'),
('Geografía', 'Laura Castillo', 'lauracastillo@gmail.com'),
('Inglés', 'Jose Maria', 'josemaria@gmail.com'),
('Arte', 'Alexandra Diaz', 'alexandradiaz@gmail.com'),
('Programación', 'Juan Perez', 'juanperez@gmail.com');
