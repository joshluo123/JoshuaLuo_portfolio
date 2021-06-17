-- Andrew Eppinger and Joshua Luo
-- Project Group 37
-- CS 340 Winter 2021

--colon (:) character being used to denote the variables that will have data from the backend programming language

-- SELECT queries
-- search for Video Game Titles in Catalog, Delete, and Update pages
SELECT DISTINCT t.titleID, t.titleName, DATE_FORMAT(t.titleRelease, '%%Y-%%m-%%d') AS titleRelease, t.titleGenre, f.franchiseName, d.developerName, t.titleESRB FROM `VideoGameTitles` AS t
LEFT JOIN TitlesPlatforms AS tpl ON t.titleID = tpl.titleID
LEFT JOIN `DevelopmentStudios` AS d ON t.titleDeveloperID = d.developerID
LEFT JOIN `Franchises` AS f ON t.titlefranchiseID = f.franchiseID
	-- input parameters to filter Video Game Titles, included as needed
WHERE t.titleName LIKE %:titleNameInput%
AND tpl.platformID = :titlePlatIdInput
AND t.titleRelease >= :titleFromDateInput
AND t.titleRelease <= :titleToDateInput
AND t.titleGenre = :titleGenreInput
AND t.franchiseID = :titleFranchiseIdInput
AND d.developerID = :titleDevIdInput
AND t.titleESRB = :titleESRBInput
ORDER BY t.titleName;

-- additional Video Game Title search to get all platforms for each returned TitleID from above query
SELECT p.platformName as Platform FROM `TitlesPlatforms` as tp
JOIN `VideoGameTitles` as t ON tp.titleID = t.titleID
JOIN `Platforms` as p ON tp.platformID = p.platformID
WHERE tp.titleID = :titleID
ORDER BY p.platformName;

-- search for Development Studios for Delete and Update pages
SELECT developerID, developerName, developerCountry, DATE_FORMAT(developerFounded, '%%Y-%%m-%%d') FROM `DevelopmentStudios`
	-- input parameters to filter Development Studios, included as needed
WHERE developerName LIKE %:devNameInput%
AND developerCountry = :devCountryInput
AND developerFounded >= :devFromDateInput
AND developerFounded <= :devToDateInput
ORDER BY devName;

-- search for Platforms for Delete and Update pages
SELECT platformID, platformName, DATE_FORMAT(platformRelease, '%%Y-%%m-%%d'), platformDeveloper, platformInProduction FROM `Platforms`
	-- input parameters to filter Platforms, included as needed
WHERE platformName LIKE %:platNameInput%
AND platformRelease >= :platFromDateInput
AND platformRelease <= :platToDateInput
AND platformDeveloper = :platDevInput
AND platformInProduction = :platInProdInput
ORDER BY platformName;

-- search for Franchises for Delete and Update pages
SELECT * FROM `Franchises`
	-- input parameters to filter Franchises, included as needed
WHERE franchiseName LIKE %:franchiseNameInput%
AND franchiseDeveloper = :franchiseDevInput
ORDER BY franchiseName;

-- search queries for getting platforms/franchises/devs to populate drop down menu options on all webpages
SELECT platformID, platformName FROM `Platforms`;
SELECT franchiseID, franchiseName FROM `Franchises`;
SELECT developerID, developerName FROM `DevelopmentStudios`;


-- INSERT queries: front-end will validate all NOT NULL attributes are appropriately inputted
-- add to VideoGameTitles; titleName, titleRelease, titleDeveloperID are required; titleESRB, titleGenre, titleFranchiseID are optional and included as needed
INSERT INTO `VideoGameTitles` (titleName, titleRelease, titleDeveloperID, titleESRB, titleGenre, titleFranchiseID)
VALUES (:titleNameInput, :titleReleaseInput, :titleDevIdInput, :titleESRBInput, :titleGenreInput, :titleFranchiseIdInput);

-- additional VideoGameTitles add query to add each platform for each title in the M:M intersection table
INSERT INTO `TitlesPlatforms` (titleID, platformID)
VALUES ((SELECT t.titleID FROM VideoGameTitles AS t WHERE t.titleName = :titleNameInput), :platformIdInput);

-- add to DevelopmentStudios
INSERT INTO `DevelopmentStudios` (developerName, developerCountry, developerFounded)
VALUES (:devNameInput, :devCountryInput, :devFoundedInput);

-- add to Platforms
INSERT INTO `Platforms` (platformName, platformRelease, platformDeveloper, platformInProduction)
VALUES (:platNameInput, :platReleaseInput, :platDevInput, :platInProdInput);

-- add to Franchises
INSERT INTO `Franchises` (franchiseName, franchiseDeveloper)
VALUES (:franchiseNameInput, (SELECT developerName FROM `DevelopmentStudios` WHERE developerID = :franchiseDevInput));


-- DELETE queries (search result table will have a hidden ID field to easily get the ID)
-- delete VideoGameTitles
DELETE FROM `VideoGameTitles`
WHERE titleID = :titleID_from_del_form;

-- delete DevelopmentStudios
DELETE FROM `DevelopmentStudios`
WHERE developerID = :devID_from_del_form;

-- delete Platforms
DELETE FROM `Platforms`
WHERE platformID = :platID_from_del_form;

-- delete Franchises
DELETE FROM `Franchises`
WHERE franchiseID = :franchiseID_from_del_form;

-- UPDATE queries: front-end will validate NOT NULL attributes are appropriately inputted, and NULLABLE attributes are set to NULL if nothing is inputted
-- update VideoGameTitles
UPDATE `VideoGameTitles`
SET
	titleName = :titleNameInput,
	titleRelease = :titleReleaseInput,
	titleGenre = :titleGenreInput,
	titleFranchiseID = :titleFranchiseIdInput,
	titleDeveloperID = :titleDevIdInput,
	titleESRB = :titleESRBInput,
WHERE titleID = :titleID_from_update_form;

-- additional VideoGameTitles update query for updating the platforms in the M:M intersection table
-- deletes all existing associated platforms and adds newly inputted platforms
DELETE FROM `TitlesPlatforms` WHERE titleID = %s;
INSERT INTO `TitlesPlatforms` (titleID, platformID) VALUES (:titleID, :platID);	-- once per inputted platform

-- update DevelopmentStudios
UPDATE `DevelopmentStudios`
SET
	developerName = :devNameInput,
	developerCountry = :devCountryInput,
	developerFounded = :devFoundedInput,
WHERE developerID = :devID_from_update_form;

-- update Platforms
UPDATE `Platforms`
SET
	platformName = :platformNameInput,
	platformRelease = :platformReleaseInput,
	platformDeveloper = :platformDeveloperInput,
	platformInProduction = :platformInProductionInput
WHERE platformID = :platformID_from_update_form;

-- query to update Franchises
UPDATE `Franchises`
SET
	franchiseName = :franchiseNameInput,
	franchiseDeveloper = :franchiseDevInput,
WHERE franchiseID = :franchiseID_from_update_form;
