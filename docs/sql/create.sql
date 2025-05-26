CREATE SCHEMA fietsverhuur;
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT, INSERT, UPDATE, DELETE, SHOW VIEW ON fietsverhuur.* TO 'user'@'localhost';

USE fietsverhuur;

CREATE TABLE klant (
	klant_id INT NOT NULL AUTO_INCREMENT,
    voornaam VARCHAR(64) NOT NULL,
    achternaam VARCHAR(64) NOT NULL,
    straat VARCHAR(64) NOT NULL,
    huisnummer INT NOT NULL,
    toevoeging VARCHAR(2) DEFAULT NULL,
    postcode VARCHAR(8) NOT NULL,
    plaats VARCHAR(64) NOT NULL,
    PRIMARY KEY (klant_id)
);

CREATE TABLE fiets_type (
	fiets_type_id INT NOT NULL AUTO_INCREMENT,
    beschrijving VARCHAR(32) NOT NULL,
    model VARCHAR(32) NOT NULL,
    electrisch BOOLEAN DEFAULT FALSE,
    dagprijs DOUBLE NOT NULL,
    PRIMARY KEY (fiets_type_id)
);

CREATE TABLE fiets (
	fiets_id INT NOT NULL AUTO_INCREMENT,
    fiets_type_id INT NOT NULL,
    merk VARCHAR(32) NOT NULL,
    aankoop_datum DATE NOT NULL,
    PRIMARY KEY (fiets_id),
    FOREIGN KEY (fiets_type_id) REFERENCES fiets_type(fiets_type_id)
);

CREATE TABLE vestiging (
	vestiging_id INT NOT NULL AUTO_INCREMENT,
	naam VARCHAR(32) NOT NULL,
    straat VARCHAR(64) NOT NULL,
    huisnummer INT NOT NULL,
    toevoeging VARCHAR(2) DEFAULT NULL,
    postcode VARCHAR(8) NOT NULL,
    plaats VARCHAR(64) NOT NULL,
    telefoonnummer VARCHAR(10) DEFAULT NULL,
    PRIMARY KEY (vestiging_id)
);

CREATE TABLE contract (
	contract_id INT NOT NULL AUTO_INCREMENT,
    klant_id INT NOT NULL,
    vestiging_id INT NOT NULL,
    start_datum DATE NOT NULL,
    eind_datum DATE NOT NULL,
    PRIMARY KEY (contract_id),
    FOREIGN KEY (klant_id) REFERENCES klant(klant_id),
    FOREIGN KEY (vestiging_id) REFERENCES vestiging(vestiging_id)
);

CREATE TABLE contract_fiets (
	contract_fiets_id INT NOT NULL AUTO_INCREMENT,
	contract_id INT NOT NULL,
    fiets_id INT NOT NULL,
    PRIMARY KEY (contract_fiets_id),
    FOREIGN KEY (contract_id) REFERENCES contract (contract_id),
    FOREIGN KEY (fiets_id) REFERENCES fiets (fiets_id),
    UNIQUE (contract_id, fiets_id)
);

CREATE INDEX klant_voornaam_idx ON klant(voornaam);
CREATE INDEX klant_achternaam_idx ON klant(achternaam);
CREATE INDEX klant_adres_idx ON klant(straat, huisnummer, toevoeging);
CREATE INDEX klant_postcode_idx ON klant(postcode);
CREATE INDEX klant_plaats_idx ON klant(plaats);
CREATE INDEX fiets_type_beschrijving ON fiets_type(beschrijving);
CREATE INDEX fiets_type_model ON fiets_type(model);
CREATE INDEX fiets_merk_idx ON fiets(merk);
CREATE INDEX vestiging_naam_idx ON vestiging(naam);