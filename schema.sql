-- DROP TABLE IF EXISTS bpm_logs;
DROP TABLE IF EXISTS sessions;

CREATE TABLE sessions (
    id BIGINT UNSIGNED  AUTO_INCREMENT PRIMARY KEY,
    `date` DATETIME NOT NULL,
    longueurs INT NOT NULL,
    mouvements_bras INT NOT NULL,
    temps_total FLOAT NOT NULL,
    bpm_instantane FLOAT NOT NULL
);

CREATE TABLE bassin (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    longueur DECIMAL(3,2) UNSIGNED NOT NULL,
)

-- CREATE TABLE bpm_logs (
--     id BIGINT UNSIGNED  AUTO_INCREMENT PRIMARY KEY,
--     session_id BIGINT UNSIGNED ,
--     timestamp DATETIME,
--     bpm FLOAT,
--     FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
-- );

CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL
);
