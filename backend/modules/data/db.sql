-- Script pour créer les tables nécessaires à l'application Spam Shield
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    preprocessed_text TEXT NOT NULL,
    crypted_text TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    label VARCHAR(10) NOT NULL,
    force_label BOOLEAN DEFAULT FALSE,
    is_edited BOOLEAN DEFAULT FALSE,
    period_end_date TIMESTAMP,
    is_pattern_spam BOOLEAN DEFAULT FALSE,
    is_pattern_ham BOOLEAN DEFAULT FALSE,
    is_gibberish BOOLEAN DEFAULT FALSE,
    contains_odds BOOLEAN DEFAULT FALSE
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
