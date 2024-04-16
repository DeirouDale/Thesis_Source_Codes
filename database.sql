CREATE DATABASE gaitdata;
CREATE TABLE IF NOT EXISTS assessment (
            id INTEGER PRIMARY KEY,
            client_id INTEGER NOT NULL,
            name VARCHAR(255) NOT NULL,
            side VARCHAR(250) NOT NULL,
            assessment_num INTEGER,
            phase INTEGER,
            image VARCHAR(255),
            frame INTEGER,
            hips VARCHAR(250),
            knees VARCHAR(250),
            ankle VARCHAR(250),
            insole VARCHAR(250)
        )
