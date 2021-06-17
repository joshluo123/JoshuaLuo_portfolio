-- Andrew Eppinger and Joshua Luo
-- Project Group 37
-- CS 340 Winter 2021

CREATE TABLE `VideoGameTitles` (
	titleID int auto_increment NOT NULL,
    titleName varchar(255) UNIQUE NOT NULL,
	titleESRB char DEFAULT NULL,
	titleGenre varchar(255) DEFAULT NULL,
	titleRelease date NOT NULL,
	titleDeveloperID int NOT NULL,
	titleFranchiseID int,
	PRIMARY KEY (titleID)
);

CREATE TABLE `DevelopmentStudios` (
	developerID int auto_increment NOT NULL,
    developerName varchar(255) UNIQUE NOT NULL,
   	developerCountry varchar(255) NOT NULL,
    developerFounded date NOT NULL,
   	PRIMARY KEY (developerID)
);

CREATE TABLE `Platforms` (
   	 platformID int auto_increment NOT NULL,
   	 platformName varchar(255) UNIQUE NOT NULL,
  	 platformRelease date NOT NULL,
  	 platformDeveloper varchar(255) NOT NULL,
  	 platformInProduction tinyint(1) NOT NULL,
 	 PRIMARY KEY(platformID)
);

CREATE TABLE `Franchises` (
	franchiseID int auto_increment NOT NULL,
    franchiseName varchar(255) UNIQUE NOT NULL,
   	franchiseDeveloper varchar(255) NOT NULL,
	PRIMARY KEY (franchiseID)
);

CREATE TABLE `TitlesPlatforms` (
	titleID int not NULL,
    platformID int not NULL,
	FOREIGN KEY (titleID) REFERENCES VideoGameTitles(titleID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (platformID) REFERENCES Platforms(platformID) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (titleID, platformID)
);

ALTER TABLE `VideoGameTitles`
ADD FOREIGN KEY (titleDeveloperID) REFERENCES DevelopmentStudios(developerID) ON DELETE CASCADE ON UPDATE CASCADE,
ADD FOREIGN KEY (titleFranchiseID) REFERENCES Franchises(franchiseID) ON DELETE SET NULL ON UPDATE CASCADE;

-- sample data
INSERT INTO `Platforms` (platformName, platformRelease, platformDeveloper, platformInProduction)
VALUES 
	('Windows', '1962-01-01', 'Microsoft', 1),
	('Nintendo Switch', '2017-03-03', 'Nintendo', 1),
	('Xbox One', '2013-11-22', 'Microsoft', 0),
	('PlayStation 4', '2013-11-15', 'Sony', 0),
	('PlayStation 5', '2020-11-12', 'Sony', 1),
	('Xbox Series X/S', '2020-11-10', 'Microsoft', 1);

INSERT INTO `DevelopmentStudios` (developerName, developerCountry, developerFounded)
VALUES 
	('Treyarch', 'USA', '1996-1-1'),
	('343 Industries', 'USA', '2007-1-1'),
	('Riot Games', 'USA', '2006-9-1'),
	('Nintendo', 'Japan', '2015-9-16'),
	('CD Projekt Red', 'Poland', '1994-1-1');

INSERT INTO `Franchises` (franchiseName, franchiseDeveloper)
VALUES 
	('Call of Duty', 'Treyarch'),
	('Halo', '343 Industries'),
	('Animal Crossing', 'Nintendo'),
	('The Witcher', 'CD Projekt Red'),
	('FIFA', 'Electronic Arts');

INSERT INTO `VideoGameTitles` (titleName, titleESRB, titleGenre, titleRelease, titleDeveloperID, titleFranchiseID)
VALUES
	('The Witcher 3: Wild Hunt', 'M', 'Role-Playing Games', '2015-05-19',
		(SELECT developerID FROM DevelopmentStudios WHERE developerName = 'CD Projekt Red'),
		(SELECT franchiseID FROM Franchises WHERE franchiseName = 'The Witcher')),
	('Animal Crossing: New Horizons', 'E', 'Simulation', '2020-03-20',
		(SELECT developerID FROM DevelopmentStudios WHERE developerName = 'Nintendo'),
		(SELECT franchiseID FROM Franchises WHERE franchiseName = 'Animal Crossing')),
	('League of Legends', 'T', 'Multiplayer Online Battle Arena', '2009-10-27',
		(SELECT developerID FROM DevelopmentStudios WHERE developerName = 'Riot Games'),
		NULL),
	('Halo Infinite', 'T', 'First-Person Shooter', '2021-12-31',
		(SELECT developerID FROM DevelopmentStudios WHERE developerName = '343 Industries'),
		(SELECT franchiseID FROM Franchises WHERE franchiseName = 'Halo')),
	('Call of Duty: Black Ops Cold War', 'M', 'First-Person Shooter', '2020-11-12',
		(SELECT developerID FROM DevelopmentStudios WHERE developerName = 'Treyarch'),
		(SELECT franchiseID FROM Franchises WHERE franchiseName = 'Call of Duty'));

INSERT INTO `TitlesPlatforms` (titleID, platformID)
VALUES
	((SELECT titleID FROM VideoGameTitles WHERE titleName = 'Call of Duty: Black Ops Cold War'),
		(SELECT platformID FROM Platforms WHERE platformName = 'PlayStation 4')),
	((SELECT titleID FROM VideoGameTitles WHERE titleName = 'Call of Duty: Black Ops Cold War'),
		(SELECT platformID FROM Platforms WHERE platformName = 'PlayStation 5')),
	((SELECT titleID FROM VideoGameTitles WHERE titleName = 'Call of Duty: Black Ops Cold War'),
		(SELECT platformID FROM Platforms WHERE platformName = 'Windows')),
	((SELECT titleID FROM VideoGameTitles WHERE titleName = 'Call of Duty: Black Ops Cold War'),
		(SELECT platformID FROM Platforms WHERE platformName = 'Xbox One')),
	((SELECT titleID FROM VideoGameTitles WHERE titleName = 'Call of Duty: Black Ops Cold War'),
		(SELECT platformID FROM Platforms WHERE platformName = 'Xbox Series X/S')),
	((SELECT titleID FROM VideoGameTitles WHERE titleName = 'Halo Infinite'),
		(SELECT platformID FROM Platforms WHERE platformName = 'Xbox One')),
	((SELECT titleID FROM VideoGameTitles WHERE titleName = 'Halo Infinite'),
		(SELECT platformID FROM Platforms WHERE platformName = 'Xbox Series X/S')),
	((SELECT titleID FROM VideoGameTitles WHERE titleName = 'League of Legends'),
		(SELECT platformID FROM Platforms WHERE platformName = 'Windows')),
	((SELECT titleID FROM VideoGameTitles WHERE titleName = 'Animal Crossing: New Horizons'),
		(SELECT platformID FROM Platforms WHERE platformName = 'Nintendo Switch')),
	((SELECT titleID FROM VideoGameTitles WHERE titleName = 'The Witcher 3: Wild Hunt'),
		(SELECT platformID FROM Platforms WHERE platformName = 'PlayStation 4')),
	((SELECT titleID FROM VideoGameTitles WHERE titleName = 'The Witcher 3: Wild Hunt'),
		(SELECT platformID FROM Platforms WHERE platformName = 'PlayStation 5')),
	((SELECT titleID FROM VideoGameTitles WHERE titleName = 'The Witcher 3: Wild Hunt'),
		(SELECT platformID FROM Platforms WHERE platformName = 'Xbox One')),
	((SELECT titleID FROM VideoGameTitles WHERE titleName = 'The Witcher 3: Wild Hunt'),
		(SELECT platformID FROM Platforms WHERE platformName = 'Xbox Series X/S')),
	((SELECT titleID FROM VideoGameTitles WHERE titleName = 'The Witcher 3: Wild Hunt'),
		(SELECT platformID FROM Platforms WHERE platformName = 'Windows')),
	((SELECT titleID FROM VideoGameTitles WHERE titleName = 'The Witcher 3: Wild Hunt'),
		(SELECT platformID FROM Platforms WHERE platformName = 'Nintendo Switch'));
	