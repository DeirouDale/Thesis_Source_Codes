CREATE DATABASE gaitdata;
CREATE TABLE IF NOT EXISTS patient_details(
            client_id VARCHAR(250) PRIMARY KEY,
            name VARCHAR(255) NOT NULL
)
CREATE TABLE IF NOT EXISTS assessment (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            client_id VARCHAR(250) NOT NULL FOREIGN KEY References patient_details(client_id),
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

INSERT INTO assessments (client_id, side, assessment_num, phase, image, frame, hips, knees, ankle, insole)
VALUES
  (2400001, 'Left', 1, 2, 'image1.jpg', 1, 'normal', 'normal', 'normal', '101'),
  (2400002, 'Right', 1, 2, 'image2.jpg', 1, 'normal', 'normal', 'normal', '111');

INSERT INTO patient_details(client_id,name) 
VALUES
  (2400001,'Sha Boo'),
  (2400002,'Hakk Dog');
