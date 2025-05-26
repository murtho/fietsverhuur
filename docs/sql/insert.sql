USE fietsverhuur;

INSERT INTO klant (klant_id, voornaam, achternaam, straat, huisnummer, postcode, plaats) VALUES (121, 'Bart', 'Janssen', 'Schoolstraat', '24', '3436AB', 'Driebergen');

INSERT INTO fiets_type (fiets_type_id, beschrijving, model, electrisch, dagprijs) VALUES (1, 'Randstad Racer D', 'Dames', TRUE, 45);
INSERT INTO fiets_type (fiets_type_id, beschrijving, model, electrisch, dagprijs) VALUES (2, 'Randstad Racer H', 'Heren', TRUE, 45);
INSERT INTO fiets_type (fiets_type_id, beschrijving, model, electrisch, dagprijs) VALUES (7, 'Grachten Caddy', 'Bakfiets', FALSE, 65);

INSERT INTO fiets (fiets_id, merk, fiets_type_id, aankoop_datum) VALUES (1, 'Batavus', 1, CURDATE());
INSERT INTO fiets (fiets_id, merk, fiets_type_id, aankoop_datum) VALUES (2, 'Gazelle', 2, CURDATE());
INSERT INTO fiets (fiets_id, merk, fiets_type_id, aankoop_datum) VALUES (3, 'Gazelle', 7, CURDATE());

INSERT INTO vestiging (naam, straat, huisnummer, postcode, plaats) VALUES ('WTC', 'Strawinskylaan', 1, '1077XW', 'Amsterdam');
INSERT INTO vestiging (naam, straat, huisnummer, postcode, plaats) VALUES ('NDSM', 'NDSM-Plein', 28, '1033WB', 'Amsterdam');

INSERT INTO contract (contract_id, klant_id, vestiging_id, start_datum, eind_datum) VALUES (1202, 121, (SELECT vestiging.vestiging_id FROM vestiging WHERE vestiging.naam = 'WTC'), '2024-01-14', '2024-01-17');

INSERT INTO contract_fiets (contract_id, fiets_id) VALUES (1202, 1);
INSERT INTO contract_fiets (contract_id, fiets_id) VALUES (1202, 2);
INSERT INTO contract_fiets (contract_id, fiets_id) VALUES (1202, 3);