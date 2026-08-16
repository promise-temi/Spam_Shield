-- DROP SCHEMA public CASCADE;
-- Script pour créer les tables nécessaires à l'application Spam Shield
CREATE SCHEMA IF NOT EXISTS public;


CREATE TABLE IF NOT EXISTS periods (
    id SERIAL PRIMARY KEY,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL
);


CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    preprocessed_text TEXT NOT NULL,
    crypted_text TEXT NOT NULL,
    metadata TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    model_label BOOLEAN DEFAULT FALSE,
    model_confidence FLOAT DEFAULT 0.0,
    business_rules_label BOOLEAN DEFAULT FALSE,
    final_label BOOLEAN DEFAULT FALSE,
    is_corected BOOLEAN DEFAULT FALSE,
    is_overridden BOOLEAN DEFAULT FALSE,
    edition_counter INT DEFAULT 0,
    banned_patterns_found TEXT[],
    period_id INT REFERENCES periods(id) ON DELETE SET NULL,
    receaved BOOLEAN DEFAULT FALSE,
    consulted BOOLEAN DEFAULT FALSE
);




CREATE TABLE IF NOT EXISTS Regexes (
    id SERIAL PRIMARY KEY,
    pattern TEXT NOT NULL
);   




CREATE TABLE IF NOT EXISTS Prospects_mails (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE, -- comme j'encrypte unique est inutile, je vais ajouter un garde fou dans le code pour vérifier que l'email n'existe pas déjà avant de l'insérer
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);




CREATE TABLE IF NOT EXISTS auth_sessions (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    code_hash TEXT,
    code_expires_at TIMESTAMP,
    session_token_hash TEXT,
    session_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);