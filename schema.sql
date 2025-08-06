DROP TABLE IF EXISTS bpm_logs;
DROP TABLE IF EXISTS sessions;

CREATE TABLE sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATETIME NOT NULL,
    bassin_longueur FLOAT NOT NULL,
    longueurs INT NOT NULL,
    mouvements_bras INT NOT NULL,
    temps_total FLOAT NOT NULL,
    bpm_instantane FLOAT NOT NULL
);

CREATE TABLE bpm_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT,
    timestamp DATETIME,
    bpm FLOAT,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL
);
