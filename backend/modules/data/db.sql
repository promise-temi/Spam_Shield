-- DROP SCHEMA public CASCADE;
-- Script pour créer les tables nécessaires à l'application Spam Shield
CREATE SCHEMA IF NOT EXISTS public;


CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    preprocessed_text TEXT NOT NULL,
    crypted_text TEXT NOT NULL,
    metadata TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    model_label BOOLEAN DEFAULT FALSE,
    business_rules_label BOOLEAN DEFAULT FALSE,
    final_label BOOLEAN DEFAULT FALSE,
    is_edited BOOLEAN DEFAULT FALSE,
    edition_counter INT DEFAULT 0,
    banned_patterns_found TEXT[]

    
);

CREATE TABLE IF NOT EXISTS periods (
    id SERIAL PRIMARY KEY,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL
);

Create TABLE IF NOT EXISTS period_frequency (
    id SERIAL PRIMARY KEY,
    frequency INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Regexes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    pattern TEXT NOT NULL
);   

CREATE TABLE IF NOT EXISTS Messages_Regexes (
    id SERIAL PRIMARY KEY,
    message_id INT NOT NULL,
    regex_id INT NOT NULL,
    FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE,
    FOREIGN KEY (regex_id) REFERENCES Regexes(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Prospects_mails (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE, -- comme j'encrypte unique est inutile, je vais ajouter un garde fou dans le code pour vérifier que l'email n'existe pas déjà avant de l'insérer
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS metadata_options (
    id SERIAL PRIMARY KEY,
    option_name VARCHAR(255) NOT NULL UNIQUE,
    is_mandatory BOOLEAN DEFAULT FALSE
);

INSERT INTO metadata_options (option_name, is_mandatory) 
VALUES 
    ('name', TRUE), 
    ('surname', TRUE), 
    ('email', TRUE), 
    ('phone', TRUE), 
    ('subject', TRUE),
    ('gibberish', TRUE);

