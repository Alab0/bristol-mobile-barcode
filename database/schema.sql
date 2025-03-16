CREATE TABLE country_and_manufacturer(
	id INT PRIMARY KEY,
	country VARCHAR(255) NOT NULL,
	manufacturer VARCHAR(255) NOT NULL
);

INSERT INTO country_and_manufacturer (id, country, manufacturer) VALUES
	(9002490, 'Австрия', 'RED BULL');

CREATE TABLE product(
	barcode BIGINT PRIMARY KEY,
	id INT NOT NULL,
	name VARCHAR(255) NOT NULL
);