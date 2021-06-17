from flask import Flask, render_template, request, jsonify
from db_connector import connect_to_database, execute_query
import os

# Configuration

app = Flask(__name__)

# Routes

@app.route('/', methods=['GET', 'POST'])
def root():
	db_connection = connect_to_database()
	if request.method == 'GET':

		# initially show table of all Video Game Titles by querying with empty inputs
		query_params = build_query_searchTitle({"titleName": "", 
												"titlePlatID": "",
												"titleFromDate": "",
												"titleToDate": "",
												"titleGenre": "",
												"titleFranchiseID": "",
												"titleDevID": "",
												"titleESRB": ""})
		table = execute_query(db_connection, query_params[0], query_params[1]).fetchall()

		# add the list of platforms for each title
		new_table = add_plats_to_titles(db_connection, table)

		# dynamically populate drop down menu platforms/franchises/devs with corresponding table values
		plat_query = "SELECT platformID, platformName FROM `Platforms` ORDER BY platformName;"
		plat = execute_query(db_connection, plat_query).fetchall()
		
		franchise_query = "SELECT franchiseID, franchiseName FROM `Franchises` ORDER BY franchiseName;"
		franchise = execute_query(db_connection, franchise_query).fetchall()
		
		dev_query =  "SELECT developerID, developerName FROM `DevelopmentStudios` ORDER BY developerName;"
		dev = execute_query(db_connection, dev_query).fetchall()

		return render_template("main.j2", titles=new_table, platforms=plat, franchises=franchise, devs=dev)
	else:
		# get request payload from POST request
		query_vals = request.get_json()

		# build query and search DB
		query_params = build_query_searchTitle(query_vals)
		result = execute_query(db_connection, query_params[0], query_params[1]).fetchall()

		new_result = add_plats_to_titles(db_connection, result)
		
		# return DB tables back to webpage
		return jsonify(new_result)

@app.route('/add', methods=['GET', 'POST'])
def add():
	db_connection = connect_to_database()
	if request.method == 'GET':
		# get platforms/franchises/devs with corresponding table values to dynamically populate drop down menu
		plat_query =  "SELECT platformID, platformName FROM `Platforms`;"
		plat = execute_query(db_connection, plat_query).fetchall()
		
		franchise_query =  "SELECT franchiseID, franchiseName FROM `Franchises`;"
		franchise = execute_query(db_connection, franchise_query).fetchall()
		
		dev_query =  "SELECT developerID, developerName FROM `DevelopmentStudios`;"
		dev = execute_query(db_connection, dev_query).fetchall()

		return render_template("add_element.j2", platforms=plat, franchises=franchise, devs=dev)
	
	# POST request
	else:
		# get request payload from POST request
		query_vals = request.get_json()

		# depending on action, INSERT into appropriate table
		if query_vals["action"] == "addTitle":
			result = execute_addTitle(db_connection, query_vals)
		elif query_vals["action"] == "addDev":
			result = execute_addDev(db_connection, query_vals)
		elif query_vals["action"] == "addPlat":
			result = execute_addPlat(db_connection, query_vals)
		elif query_vals["action"] == "addFranchise":
			result = execute_addFranchise(db_connection, query_vals)

		return jsonify(result)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
	db_connection = connect_to_database()
	if request.method == 'GET':
		# get platforms/franchises/devs/platformDevs/franchiseDevs with corresponding table values to dynamically populate drop down menu
		plat_query =  "SELECT platformID, platformName FROM `Platforms`"
		plat = execute_query(db_connection, plat_query).fetchall()
		
		franchise_query =  "SELECT franchiseID, franchiseName FROM `Franchises`"
		franchise = execute_query(db_connection, franchise_query).fetchall()
		
		dev_query =  "SELECT developerID, developerName FROM `DevelopmentStudios`"
		dev = execute_query(db_connection, dev_query).fetchall()
		
		platDev_query = "SELECT platformDeveloper FROM `Platforms` GROUP BY platformDeveloper"
		platDev = execute_query(db_connection, platDev_query).fetchall()
		
		franchiseDev_query = "SELECT franchiseDeveloper FROM `Franchises` GROUP BY franchiseDeveloper"
		franchiseDev = execute_query(db_connection, franchiseDev_query).fetchall()

		return render_template("del_element.j2", platforms=plat, franchises=franchise, devs=dev, platDev=platDev, franchiseDev=franchiseDev)
	else:
		# get request payload from POST request
		query_vals = request.get_json()
		# deleting an element
		if query_vals["action"] == "deleteTitle":
			result = execute_delTitle(db_connection,query_vals)
		elif query_vals["action"] == "deleteDev":
			result = execute_delDevStudio(db_connection,query_vals)
		elif query_vals["action"] == "deletePlat":
			result = execute_delPlat(db_connection,query_vals)
		elif query_vals["action"] == "deleteFranchise":
			result = execute_delFranchise(db_connection,query_vals)
		
		# depending on table, build query and search DB
		elif query_vals["action"] == "searchTitle":
			query_params = build_query_searchTitle(query_vals)
			result = execute_query(db_connection, query_params[0], query_params[1]).fetchall()
			result = add_plats_to_titles(db_connection, result)

		elif query_vals["action"] == "searchDev":
			query_params = build_query_searchDev(query_vals)
			result = execute_query(db_connection, query_params[0], query_params[1]).fetchall()

		elif query_vals["action"] == "searchPlat":
			query_params = build_query_searchPlat(query_vals)
			result = execute_query(db_connection, query_params[0], query_params[1]).fetchall()

		elif query_vals["action"] == "searchFranchise":
			query_params = build_query_searchFranchise(query_vals)
			result = execute_query(db_connection, query_params[0], query_params[1]).fetchall()

		return jsonify(result)

@app.route('/update', methods=['GET', 'POST'])
def update():
	db_connection = connect_to_database()
	if request.method == 'GET':
		# get platforms/franchises/devs/platformDevs/franchiseDevs with corresponding table values to dynamically populate drop down menu
		plat_query =  "SELECT platformID, platformName FROM `Platforms`"
		plat = execute_query(db_connection, plat_query).fetchall()
		
		franchise_query =  "SELECT franchiseID, franchiseName FROM `Franchises`"
		franchise = execute_query(db_connection, franchise_query).fetchall()
		
		dev_query =  "SELECT developerID, developerName FROM `DevelopmentStudios`"
		dev = execute_query(db_connection, dev_query).fetchall()
		
		platDev_query = "SELECT platformDeveloper FROM `Platforms` GROUP BY platformDeveloper"
		platDev = execute_query(db_connection, platDev_query).fetchall()
		
		franchiseDev_query = "SELECT franchiseDeveloper FROM `Franchises` GROUP BY franchiseDeveloper"
		franchiseDev = execute_query(db_connection, franchiseDev_query).fetchall()

		return render_template("update_element.j2", platforms=plat, franchises=franchise, devs=dev, platDev=platDev, franchiseDev=franchiseDev)
	else:
		# get request payload from POST request
		query_vals = request.get_json()

		# depending on the table, build query and search DB
		if query_vals["action"] == "searchTitle":
			query_params = build_query_searchTitle(query_vals)
			result = execute_query(db_connection, query_params[0], query_params[1]).fetchall()
			result = add_plats_to_titles(db_connection, result)
		elif query_vals["action"] == "searchDev":
			query_params = build_query_searchDev(query_vals)
			result = execute_query(db_connection, query_params[0], query_params[1]).fetchall()
		elif query_vals["action"] == "searchPlat":
			query_params = build_query_searchPlat(query_vals)
			result = execute_query(db_connection, query_params[0], query_params[1]).fetchall()
		elif query_vals["action"] == "searchFranchise":
			query_params = build_query_searchFranchise(query_vals)
			result = execute_query(db_connection, query_params[0], query_params[1]).fetchall()
		
		# populating drop down menu elements for updating titles
		elif query_vals["action"] == "updateTitleElements":
			# query for list of all platforms
			query = "SELECT platformID, platformName FROM `Platforms` ORDER BY platformName"
			plat_result = execute_query(db_connection, query).fetchall();

			# query for list of all franchises
			query = "SELECT franchiseID, franchiseName FROM `Franchises` ORDER BY franchiseName"
			franchise_result = execute_query(db_connection, query).fetchall();

			# query for list of all developers
			query = "SELECT developerID, developerName FROM `DevelopmentStudios` ORDER BY developerName"
			dev_result = execute_query(db_connection, query).fetchall();

			return {"Plats": plat_result,
					"Franchises": franchise_result,
					"Devs": dev_result};
		
		# populating drop down menu elements for updating franchises
		elif query_vals["action"] == "updateFranchiseElements":
			# query for list of all developers
			query = "SELECT developerName FROM `DevelopmentStudios` ORDER BY developerName"
			dev_result = execute_query(db_connection, query).fetchall();

			return {"Devs": dev_result};

		# updating an element
		elif query_vals["action"] == "updateTitle":
			return execute_update_title(db_connection, query_vals)
		elif  query_vals["action"] == "updateDev":
			return execute_update_dev(db_connection, query_vals)
		elif  query_vals["action"] == "updatePlat":			
			return execute_update_plat(db_connection, query_vals)
		elif  query_vals["action"] == "updateFranchise":
			return execute_update_franchise(db_connection, query_vals)

		return jsonify(result)

# Listener
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 9112))
	#                                 ^^^^
    #              You can replace this number with any valid port
	app.run(port=port, debug=True)


def execute_addTitle(db_connection, query_vals):
	# query_vals = {"titleName", "titlePlatIDs", "titleRelease", "titleGenre", "titleFranchiseID", "titleDevID", "titleESRB"}
	
	# build query and parameters
	params = (query_vals["titleName"], query_vals["titleRelease"], query_vals["titleDevID"])
	query = "INSERT INTO `VideoGameTitles` (titleName, titleRelease, titleDeveloperID"
	values = " VALUES (%s, %s, %s"
	if query_vals["titleESRB"] != "" :
		params += (query_vals["titleESRB"],)
		query += ", titleESRB"
		values += ", %s"

	if query_vals["titleGenre"] != "" :
		params += (query_vals["titleGenre"],)
		query += ", titleGenre"
		values += ", %s"

	if query_vals["titleFranchiseID"] != "" :
		params += (query_vals["titleFranchiseID"],)
		query += ", titleFranchiseID"
		values += ", %s"
	values += ");"
	query += ")" + values

	try:
		execute_query(db_connection, query, params)
	except:
		return {"result": 0}
	else:
		for platformID in query_vals["titlePlatIDs"]:
			params = (query_vals["titleName"], platformID)
			query = "INSERT INTO `TitlesPlatforms` (titleID, platformID)"
			query += " VALUES ((SELECT t.titleID FROM VideoGameTitles AS t WHERE t.titleName = %s), %s);"
			execute_query(db_connection, query, params)
	
	return {"result": 1}

def execute_addDev(db_connection, query_vals):
	# query_vals = { "devName", "devCountry", "devDate"}

	# build query
	params = (query_vals["devName"], query_vals["devCountry"], query_vals ["devDate"])
	query = "INSERT INTO `DevelopmentStudios` (developerName, developerCountry, developerFounded) VALUES (%s, %s, %s);"
	
	try:
		result = execute_query(db_connection, query, params)
	except:
		return {"result": 0}
	else:
		return {"result": 1}

def execute_addPlat(db_connection, query_vals):
	# query_vals = {"platName", "platDate", "platDev", "platInProd"}

	# build query
	params = (query_vals["platName"], query_vals["platDate"], query_vals["platDev"], str(query_vals["platInProd"]))
	query = "INSERT INTO `Platforms` (platformName, platformRelease, platformDeveloper, platformInProduction) VALUES (%s, %s, %s, %s);"
	
	try:
		result = execute_query(db_connection, query, params)
	except:
		return {"result": 0}
	else:
		return {"result": 1}

def execute_addFranchise(db_connection, query_vals):
	# query_vals = {"franchiseName", "franchiseDev"}

	# build query
	params = (query_vals["franchiseName"], query_vals["franchiseDev"])
	query = "INSERT INTO `Franchises` (franchiseName, franchiseDeveloper) VALUES (%s, (SELECT developerName FROM `DevelopmentStudios` WHERE developerID = %s));"
	
	try:
		result = execute_query(db_connection, query, params)
	except:
		return {"result": 0}
	else:
		return {"result": 1}

def execute_delTitle(db_connection, query_vals):
	#query_vals = {"ButtonVal"}

	#Build query

	params = (query_vals["ButtonVal"])
	query = "DELETE FROM VideoGameTitles WHERE titleID = %s"
	try:
		result = execute_query(db_connection, query, params)
	except:
		return {"result": 0}
	else:
		return {"result": 1}

def execute_delDevStudio(db_connection, query_vals):
	#query_vals = {"ButtonVal"}

	#Build query

	params = (query_vals["ButtonVal"])
	query = "DELETE FROM DevelopmentStudios WHERE developerID = %s"
	try:
		result = execute_query(db_connection, query, params)
	except:
		return {"result": 0}
	else:
		return {"result": 1}

def execute_delPlat(db_connection, query_vals):
	#query_vals = {"ButtonVal"}

	#Build query

	params = (query_vals["ButtonVal"])
	query = "DELETE FROM Platforms WHERE platformID = %s"
	try:
		result = execute_query(db_connection, query, params)
	except:
		return {"result": 0}
	else:
		return {"result": 1}

def execute_delFranchise(db_connection, query_vals):
	#query_vals = {"ButtonVal"}

	#Build query

	params = (query_vals["ButtonVal"])
	query = "DELETE FROM Franchises WHERE franchiseID = %s"
	try:
		result = execute_query(db_connection, query, params)
	except:
		return {"result": 0}
	else:
		return {"result": 1}

def build_query_searchTitle(query_vals):
	# query_vals = {"titleName", "titlePlatID", "titleFromDate", "titleToDate" "titleGenre", "titleFranchiseID", "titleDevID", "titleESRB"}
	query = "SELECT DISTINCT t.titleID, t.titleName, DATE_FORMAT(t.titleRelease, '%%Y-%%m-%%d') AS titleRelease, t.titleGenre, f.franchiseName, d.developerName, t.titleESRB FROM `VideoGameTitles` AS t "
	query += "LEFT JOIN TitlesPlatforms AS tpl ON t.titleID = tpl.titleID "
	query += "LEFT JOIN `DevelopmentStudios` AS d ON t.titleDeveloperID = d.developerID "
	query += "LEFT JOIN `Franchises` AS f ON t.titlefranchiseID = f.franchiseID"
	need_where = 1
	params = ()
	if query_vals["titleName"] != "":
		query += " WHERE t.titleName LIKE %s"
		params += ("%" + query_vals["titleName"] + "%",)
		need_where = 0
	if 	query_vals["titlePlatID"] != "":
		if need_where:
			query += " WHERE "
			need_where = 0
		else:
			query += " AND "
		query += "tpl.platformID = %s"
		params += (query_vals["titlePlatID"],)
	if query_vals["titleFromDate"] != "":
		if need_where:
			query += " WHERE "
			need_where = 0
		else:
			query += " AND "
		query += "t.titleRelease >= %s"
		params += (query_vals["titleFromDate"],)
	if query_vals["titleToDate"] != "":
		if need_where:
			query += " WHERE "
			need_where = 0
		else:
			query += " AND "
		query += "t.titleRelease <= %s"
		params += (query_vals["titleToDate"],)
	if query_vals["titleGenre"] != "":
		if need_where:
			query += " WHERE "
			need_where = 0
		else:
			query += " AND "
		query += "t.titleGenre = %s"
		params += (query_vals["titleGenre"],)
	if query_vals["titleFranchiseID"] != "":
		if need_where:
			query += " WHERE "
			need_where = 0
		else:
			query += " AND "
		query += "f.franchiseID = %s"
		params += (query_vals["titleFranchiseID"],)
	if query_vals["titleDevID"] != "":
		if need_where:
			query += " WHERE "
			need_where = 0
		else:
			query += " AND "
		query += "d.developerID = %s"
		params += (query_vals["titleDevID"],)
	if query_vals["titleESRB"] != "":
		if need_where:
			query += " WHERE "
			need_where = 0
		else:
			query += " AND "
		query += "t.titleESRB = %s"
		params += (query_vals["titleESRB"],)
	query += " ORDER BY t.titleName;"

	return (query, params)

def add_plats_to_titles(db_connection, titles_result):
	new_title_res = ()
	# for each title going in the table
	for title_info in titles_result:
		# get all the platforms for a given titleID
		titlesPlats_query = "SELECT p.platformName as Platform FROM `TitlesPlatforms` as tp "
		titlesPlats_query += "JOIN `VideoGameTitles` as t ON tp.titleID = t.titleID "
		titlesPlats_query += "JOIN `Platforms` as p ON tp.platformID = p.platformID "
		titlesPlats_query += "WHERE t.titleID = %s "
		titlesPlats_query += "ORDER BY p.platformName"
		titlesPlats_params = (title_info[0])
		titles_Plats = execute_query(db_connection, titlesPlats_query, titlesPlats_params).fetchall()

		# form a tuple of all the platforms for a given title
		plat_tuple = ()
		for plat in titles_Plats:
			plat_tuple += (plat[0],)

		# add tuple of platforms into the new title_info tuple
		new_title = title_info + (plat_tuple,)
		new_title_res += (new_title,)

	return new_title_res

def build_query_searchDev(query_vals):
	# query_vals = {"devName", "devCountry", "devFromDate", "devToDate"}
	query = "SELECT developerID, developerName, developerCountry, DATE_FORMAT(developerFounded, '%%Y-%%m-%%d') FROM `DevelopmentStudios`"
	need_where = 1
	params = ()
	if query_vals["devName"] != "":
		query += " WHERE developerName LIKE %s"
		params += ("%" + query_vals["devName"] + "%",)
		need_where = 0
	if query_vals["devCountry"] != "":
		if need_where:
			query += " WHERE "
			need_where = 0
		else:
			query += " AND "
		query += "developerCountry = %s"
		params += (query_vals["devCountry"],)
	if query_vals["devFromDate"] != "":
		if need_where:
			query += " WHERE "
			need_where = 0
		else:
			query += " AND "
		query += "developerFounded >= %s"
		params += (query_vals["devFromDate"],)
	if query_vals["devToDate"] != "":
		if need_where:
			query += " WHERE "
			need_where = 0
		else:
			query += " AND "
		query += "developerFounded <= %s"
		params += (query_vals["devToDate"],)
	query += " ORDER BY developerName;"

	return (query, params)

def build_query_searchPlat(query_vals):
	# query_vals = {"platName", "platFromDate", "platToDate", "platDev", "platInProd"}
	query = "SELECT platformID, platformName, DATE_FORMAT(platformRelease, '%%Y-%%m-%%d'), platformDeveloper, platformInProduction FROM `Platforms`"
	need_where = 1
	params = ()
	if query_vals["platName"] != "":
		query += " WHERE platformName LIKE %s"
		params += ("%" + query_vals["platName"] + "%",)
		need_where = 0
	if query_vals["platFromDate"] != "":
		if need_where:
			query += " WHERE "
			need_where = 0
		else:
			query += " AND "
		query += "platformRelease >= %s"
		params += (query_vals["platFromDate"],)
	if query_vals["platToDate"] != "":
		if need_where:
			query += " WHERE "
			need_where = 0
		else:
			query += " AND "
		query += "platformRelease >= %s"
		params += (query_vals["platToDate"],)
	if query_vals["platDev"] != "":
		if need_where:
			query += " WHERE "
			need_where = 0
		else:
			query += " AND "
		query += " platformDeveloper = %s"
		params += (query_vals["platDev"],)
	if query_vals["platInProd"] != "":
		if need_where:
			query += " WHERE "
			need_where = 0
		else:
			query += " AND "
		query += "platformInProduction = %s"
		params += (query_vals["platInProd"],)
	query += " ORDER BY platformName;"

	return (query, params)

def build_query_searchFranchise(query_vals):
	# query_vals = {"franchiseName", "franchiseDev"}
	query = "SELECT * FROM `Franchises`"
	need_where = 1
	params = ()
	if query_vals["franchiseName"] != "":
		query += " WHERE franchiseName LIKE %s"
		params += ("%" + query_vals["franchiseName"] + "%",)
		need_where = 0
	if query_vals["franchiseDev"] != "":
		if need_where:
			query += " WHERE "
			need_where = 0
		else:
			query += " AND "
		query += " franchiseDeveloper = %s"
		params += (query_vals["franchiseDev"],)
	query += " ORDER BY franchiseName;"

	return (query, params)

def execute_update_title(db_connection, query_vals):
	# query_vals = {"titleID", "titleName", titlePlats, "titleRelease", "titleGenre", 
	#						"titleFranchiseID", "titleDevID", "titleESRB"}
	query = "UPDATE `VideoGameTitles` SET "	
	
	query += "titleName = %s, "
	query += "titleRelease = %s"
	params = (query_vals["titleName"], query_vals["titleRelease"])

	if query_vals["titleGenre"] != "":
		query += ", titleGenre = %s"
		params += (query_vals["titleGenre"],)
	else :
		query += ", titleGenre = NULL"

	if query_vals["titleFranchiseID"] != "":
		query += ", titleFranchiseID = %s"
		params += (query_vals["titleFranchiseID"],)
	else:
		query += ", titleFranchiseID = NULL"

	query += ", titleDeveloperID = %s"
	params += (query_vals["titleDevID"],)
	
	if query_vals["titleESRB"] != "":
		query += ", titleESRB = %s"
		params += (query_vals["titleESRB"],)
	else:
		query += ", titleESRB = NULL"

	query += " WHERE titleID = %s;"
	params += (query_vals["titleID"],)

	try:
		execute_query(db_connection, query, params)
	except:
		return {"result": 0}
	else:
		# update TitlesPlatforms table with query_vals["titleID"] and list from query_vals["titlePlats"]
		# delete existing pairs
		query = "DELETE FROM `TitlesPlatforms` WHERE titleID = %s;"
		execute_query(db_connection, query, (query_vals["titleID"],))

		# add ID/PlatID pairs
		query = "INSERT INTO `TitlesPlatforms` (titleID, platformID) VALUES (%s, %s);"
		for platID in query_vals["titlePlats"]:
			execute_query(db_connection, query, (query_vals["titleID"], platID))

		return {"result": 1}

def execute_update_dev(db_connection, query_vals):
	# query_vals = {"devID", "devName", "devCountry", "devDate"}
	query = "UPDATE `DevelopmentStudios` SET "	
	query += "developerName = %s, "
	query += "developerCountry = %s, "
	query += "developerFounded = %s "
	query += "WHERE developerID = %s;"

	params = (query_vals["devName"], query_vals["devCountry"], query_vals["devDate"], query_vals["devID"])

	try:
		execute_query(db_connection, query, params)
	except:
		return {"result": 0}
	else:
		return {"result": 1}

def execute_update_plat(db_connection, query_vals):
	# query_vals = {"platID", "platName", "platDate", "platDev" "platInProd"}
	query = "UPDATE `Platforms` SET "
	query += "platformName = %s, "
	query += "platformRelease = %s, "
	query += "platformDeveloper = %s, "
	query += "platformInProduction = %s "
	query += "WHERE platformID = %s"

	params = (query_vals["platName"], query_vals["platDate"], query_vals["platDev"], query_vals["platInProd"], query_vals["platID"],)

	try:
		execute_query(db_connection, query, params)
	except:
		return {"result": 0}
	else:
		return {"result": 1}

def execute_update_franchise(db_connection, query_vals):
	# query_vals = {"franchiseID", "franchiseName", "franchiseDev"}
	query = "UPDATE `Franchises` SET "
	query += "franchiseName = %s, "
	query += "franchiseDeveloper = %s "
	query += "WHERE franchiseID = %s"

	params = (query_vals["franchiseName"], query_vals["franchiseDev"], query_vals["franchiseID"])

	try:
		execute_query(db_connection, query, params)
	except:
		return {"result": 0}
	else:
		return {"result": 1}
