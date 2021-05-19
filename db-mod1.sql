create table appearlstore (
	id BIGSERIAL NOT NULL PRIMARY KEY,
	person_id INT NOT NULL,
    amount NUMERIC(20,2) NOT NULL,
    type_of_payment VARCHAR(20) NOT NULL 
);

create table hardwarestore (
	id BIGSERIAL NOT NULL PRIMARY KEY,
	person_id INT NOT NULL,
    amount NUMERIC(20,2) NOT NULL,
    type_of_payment VARCHAR(20) NOT NULL 
);

create table grocerystore (
	id BIGSERIAL NOT NULL PRIMARY KEY,
	person_id INT NOT NULL,
    amount NUMERIC(20,2) NOT NULL,
    type_of_payment VARCHAR(20) NOT NULL 
);