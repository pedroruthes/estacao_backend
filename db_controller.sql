CREATE DATABASE db_controller;

-- Locais
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
	lng DOUBLE PRECISION NOT NULL
);

-- Controladores (ex: Arduíno)
CREATE TABLE controllers (
    id SERIAL PRIMARY KEY,
    hw_desc TEXT NOT NULL,
    key TEXT NOT NULL,
	enabled BOOLEAN NOT NULL DEFAULT TRUE,
	version FLOAT,
	location_id INTEGER NOT NULL REFERENCES locations(id)
);

-- Estação Meteorológica da Educação
CREATE TABLE sensors_meteo_sme (
	id SERIAL PRIMARY KEY,
	temperature FLOAT,
	humidity FLOAT,
	dir_wind INTEGER,
	vel_wind FLOAT,
	pressure INTEGER,
	rain_measure FLOAT,
	time TIMESTAMP DEFAULT now(),
	controller_id INTEGER NOT NULL REFERENCES controllers(id)
);

-- Cargos (ex: Professor de Geografia)
CREATE TABLE profiles (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL
);

-- Perfis de usuários (ex: Administrador)
CREATE TABLE positions (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL
);

-- Usuários
CREATE TABLE persons (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL,
	enabled BOOLEAN NOT NULL DEFAULT TRUE,
	created_at TIMESTAMP DEFAULT now(),
	updated_at TIMESTAMP DEFAULT now(),
	profile_id INTEGER NOT NULL REFERENCES profiles(id),
    position_id INTEGER NOT NULL REFERENCES positions(id)
);

-- Relacionamento N:N entre Pessoas e Locais
CREATE TABLE persons_locations (
    location_id INTEGER NOT NULL REFERENCES locations(id),
    person_id INTEGER NOT NULL REFERENCES locations(id),
    PRIMARY KEY (person_id, location_id)
);

-- Recuperação de senha
CREATE TABLE forgot_passwords (
	id SERIAL PRIMARY KEY,
	recovery_code INTEGER NOT NULL,
	expire_in TIMESTAMP DEFAULT (now() + INTERVAL '15 minutes'),
	used BOOLEAN DEFAULT FALSE,
	person_id INTEGER NOT NULL REFERENCES persons(id)
);

-- Registro de eventos
CREATE TABLE log_events (
	id SERIAL PRIMARY KEY,
	description TEXT NOT NULL,
	time TIMESTAMP DEFAULT now(),
	person_id INTEGER NOT NULL REFERENCES persons(id)
);

-- Sensores
CREATE TABLE sensors (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	type TEXT NOT NULL
);

-- Relacionamento N:N entre Sensores e Controladores
CREATE TABLE sensors_controllers (
	sensor_id INTEGER NOT NULL REFERENCES sensors(id),
    controller_id INTEGER NOT NULL REFERENCES controllers(id),
    PRIMARY KEY (sensor_id, controller_id)
);