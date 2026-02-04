DROP DATABASE IF EXISTS hello_class;
CREATE DATABASE hello_class;
use hello_class;

drop table if exists student;


create table student
(
    studentID int unsigned not null,
    firstname varchar(255),
    lastname varchar(255),
    primary key (studentID)
);

insert into student (studentID, firstname, lastname)
values (1,'Maria','Vilma'),
(2, 'Kari','Guro'),
(3,'Emily','Mari');

CREATE DATABASE IF NOT EXISTS population;
use population;

#DROP DATABASE pets_db;
CREATE DATABASE IF NOT EXISTS pets_db;
USE pets_db;

CREATE TABLE PetSpecies (
    speciesID SERIAL,
    common_name nvarchar(100),
    scientific_name nvarchar(100)
);

INSERT INTO PetSpecies (speciesID,common_name , scientific_name)
VALUES (1, 'cat', 'Felis catus'),
       (2, 'dog','Canis lupus familiaris');

CREATE TABLE Owners (
    ownerID SERIAL,
    name nvarchar(100),

    PRIMARY KEY (OwnerID)
);

INSERT INTO Owners
VALUES (1,'Mrs Smith'),
       (2, 'Billy'),
       (3, 'Sally'),
       (4, 'Steven');

CREATE TABLE Pets (
    petID SERIAL,
    name nvarchar(100),
    speciesID BIGINT UNSIGNED,
    ownerID BIGINT UNSIGNED,

    PRIMARY KEY (petID),
    FOREIGN KEY (speciesID) REFERENCES PetSpecies(speciesID),
    FOREIGN KEY (ownerID) REFERENCES Owners(ownerID)
);

INSERT INTO Pets (name, speciesID, ownerID)
VALUES ('Fluffy', 1, 1),
       ('Spot', 2,2),
       ('Mr McFluffButt', 1, 3),
       ('Spot', 2, 4);


SELECT Pets.name, PS.scientific_name
FROM Pets
JOIN pets_db.PetSpecies PS on PS.speciesID = Pets.speciesID
WHERE PS.common_name = 'dog';

DROP TABLE IF EXISTS Job;
CREATE TABLE Job
(
    JobID SERIAL,
    JobTitle nvarchar(255),

    PRIMARY KEY (JobID)
);

INSERT INTO Job
VALUES (1, 'Undefined'),
       (2, 'Unemployed'),
       (100, 'Lawyer'),
       (0, 'Programmer'),
       (0, 'Lecturer');

INSERT INTO Job
VALUES (7, 'CEO');



DROP TABLE IF EXISTS Person;

CREATE TABLE Person(
	PersonID SERIAL,
	FirstName nvarchar(255),
	LastName nvarchar(255),
	Address nvarchar(255),
	City nvarchar(255),
    JobID BIGINT UNSIGNED DEFAULT (1) NOT NULL,

	PRIMARY KEY (PersonID),
    FOREIGN KEY (JobID) REFERENCES Job(JobID)
);

INSERT INTO Person (FirstName, LastName, Address, City)
VALUES
	('Craig', 'Marais', 'Ammerud', 'Oslo'),
	('Per', 'Persen', 'Storgata', 'Oslo'),
	('Kari', 'Normann', 'Frogner', 'Oslo'),
	('Nina', 'Persen', 'Majorstua', 'Oslo'),
	('Steve', 'Bobs', 'California','LA');


INSERT INTO Person (FirstName, LastName, Address, City, JobID)
VALUES ('Jill', 'Bates', 'California', 'LA', 7)

