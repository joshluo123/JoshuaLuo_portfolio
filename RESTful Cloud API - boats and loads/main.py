from google.cloud import datastore
from flask import Flask, request, jsonify, _request_ctx_stack
import requests

from functools import wraps
import json

from six.moves.urllib.request import urlopen
from flask_cors import cross_origin, CORS
from jose import jwt


import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

from flask import make_response
import constants

app = Flask(__name__, static_url_path='/public', static_folder='./public')
app.secret_key = 'SECRET_KEY'

cors = CORS(app)

client = datastore.Client()

# Update the values of the following 3 variables
CLIENT_ID = 'Kv1jyLulhO1qcYiKkeeYEovVDFu9aiIS'
CLIENT_SECRET = '3-doVWHasvrYGtXgEPnNp8GfZDf2wwVCpU9JR19vjB335dIjq4uKR_x9_B9Hwgfb'
DOMAIN = 'cs493-luojo.us.auth0.com'

ALGORITHMS = ["RS256"]

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    api_base_url="https://" + DOMAIN,
    access_token_url="https://" + DOMAIN + "/oauth/token",
    authorize_url="https://" + DOMAIN + "/authorize",
    client_kwargs={
        'scope': 'openid profile email',
    },
)

# This code is adapted from https://auth0.com/docs/quickstart/backend/python/01-authorization?_ga=2.46956069.349333901.1589042886-466012638.1589042885#create-the-jwt-validation-decorator

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# Verify the JWT in the request's Authorization header
def verify_jwt(request):
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization'].split()
        token = auth_header[1]
    else:
        raise AuthError({"code": "no auth header",
                            "description":
                                "Authorization header is missing"}, 401)
    
    jsonurl = urlopen("https://"+ DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Invalid header. "
                            "Use an RS256 signed JWT Access Token"}, 401)
    if unverified_header["alg"] == "HS256":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Invalid header. "
                            "Use an RS256 signed JWT Access Token"}, 401)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=CLIENT_ID,
                issuer="https://"+ DOMAIN+"/"
            )
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                            "description": "token is expired"}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                            "description":
                                "incorrect claims,"
                                " please check the audience and issuer"}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Unable to parse authentication"
                                " token."}, 401)

        return payload
    else:
        raise AuthError({"code": "no_rsa_key",
                            "description":
                                "No RSA key in JWKS"}, 401)


# Generate a JWT from the Auth0 domain and return it
# Request: JSON body with 2 properties with "username" and "password"
#       of a user registered with this Auth0 domain
# Response: JSON with the JWT as the value of the property id_token
@app.route('/login', methods=['POST'])
def login_api():
    content = request.get_json()
    username = content["username"]
    password = content["password"]
    body = {'grant_type':'password','username':username,
            'password':password,
            'client_id':CLIENT_ID,
            'client_secret':CLIENT_SECRET
           }
    headers = { 'content-type': 'application/json' }
    url = 'https://' + DOMAIN + '/oauth/token'
    r = requests.post(url, json=body, headers=headers)
    return r.text, 200, {'Content-Type':'application/json'}


# Login/Create New User/Logout pages:
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/login')
    return f(*args, **kwargs)

  return decorated


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=constants.url + '/callback')


# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    session['id_token'] = auth0.authorize_access_token()['id_token']
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    # look for the user in Datastore
    query = client.query(kind=constants.users)
    query.add_filter("user_id", "=", userinfo["sub"])
    results = list(query.fetch())
    if not results:
        # new user, add their user_id
        new_user = datastore.entity.Entity(key=client.key(constants.users))
        new_user.update({"email": userinfo["email"], "user_id": userinfo["sub"]})
        client.put(new_user)
    
    return redirect('/dashboard')


@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4),
                           jwt=session['id_token'],
                           user_id=session['profile']['user_id'])


@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


# API Route Endpoints
@app.route('/users', methods=['GET'])
def post_get_users():
    # request must have header Accept: application/json
    if request.headers.get('Accept') != 'application/json':
        return bad_accept_header()  # 406

    if request.method == 'GET':
        # display all users
        query = client.query(kind=constants.users)
        results = list(query.fetch())
        return jsonify(results)

    else:
       # invalid request method type
        return bad_request_method() # 405


@app.route('/boats', methods=['POST', 'GET'])
def post_get_boats():
    # request must have header Accept: application/json
    if request.headers.get('Accept') != 'application/json':
        return bad_accept_header()  # 406

    # validate user is authorized
    user = verify_jwt(request)

    if request.method == 'POST':
        # create a new boat owned by the authorized user
        content = request.get_json()

        # validate all required attributes are present
        if content is None or "name" not in content or "type" not in content or "length" not in content:
            result = {"Error": "The request object is missing at least one of the required attributes"}
            return (result, 400)

        # create a boat in Datastore
        new_boat = datastore.entity.Entity(key=client.key(constants.boats))
        new_boat.update({"name": content["name"], "type": content["type"], "length": content["length"], "owner": user["sub"], "loads": []})
        client.put(new_boat)
        result = {
            "id": new_boat.key.id,
            "name": new_boat["name"],
            "type": new_boat["type"],
            "length": new_boat["length"],
            "owner": new_boat["owner"],
            "loads": new_boat["loads"],
            "self": constants.url + "/boats/" + str(new_boat.key.id)
        }
        return (result, 201)

    elif request.method == 'GET':
        # list all boats owned by the authorized user

        # function for getting a page of results based on a given cursor
        def get_page_boats(cursor=None):
            query = client.query(kind=constants.boats)
            query.add_filter("owner", "=", user["sub"])
            query_iter = query.fetch(start_cursor=cursor, limit=5)
            page = next(query_iter.pages)
            results = list(page)
            for e in results:
                load_self = []
                for load_id in e["loads"]:
                    load_self.append({"id": load_id, "self": constants.url + "/loads/" + str(load_id)})
                e["id"] = e.key.id
                e["loads"] = load_self
                e["self"] = constants.url + "/boats/" + str(e.key.id)
            next_cursor = query_iter.next_page_token

            return results, next_cursor

        # no cursor received, start a query with a new cursor
        if request.args.get("cursor") is None:
            boats, next_cursor = get_page_boats()
        
        # received a cursor, make a query with this cursor
        else:
            boats, next_cursor = get_page_boats(request.args.get("cursor").encode('ascii'))

        result_page = {"boats": boats}

        # if there is a next page, include a next url with a query parameter of the cursor
        if next_cursor is not None:
            result_page["next"] = constants.url + "/boats?cursor=" + next_cursor.decode('ascii')

        # include a count of the total number of entries owned by the authorized user
        query = client.query(kind=constants.boats)
        query.add_filter("owner", "=", user["sub"])
        total_entries = len(list(query.fetch()))
        result_page["total"] = total_entries

        return jsonify(result_page)

    else:
        # invalid request method type
        return bad_request_method() # 405


@app.route('/boats/<boat_id>', methods=['GET', 'PATCH', 'PUT', 'DELETE'])
def get_patch_put_delete_boat_id(boat_id):
    # validate user is authorized
    user = verify_jwt(request)

    # validate boat_id matches an existing boat
    boat_key = client.key(constants.boats, int(boat_id))
    boat = client.get(key=boat_key)
    if boat is None:
        result = {"Error": "No boat with this boat_id exists"}
        return (result, 404)

    # validate boat belongs to the authorized user
    if boat["owner"] != user["sub"]:
        result = {"Error": "User is not the owner of the boat"}
        return (result, 403)

    if request.method == 'GET':
        # view a boat owned by the authorized user
        
        # request must have header Accept: application/json
        if request.headers.get('Accept') != 'application/json':
            return bad_accept_header()  # 406

        load_self = []
        for load_id in boat["loads"]:
            load_self.append({"id": load_id, "self": constants.url + "/loads/" + str(load_id)})

        result = {
            "id": boat.key.id,
            "name": boat["name"],
            "type": boat["type"],
            "length": boat["length"],
            "owner": boat["owner"],
            "loads": load_self,
            "self": constants.url + "/boats/" + str(boat.key.id)
        }

        return jsonify(result)

    elif request.method == 'PATCH':
        # edit some atttributes of a boat owned by the authorized user
        content = request.get_json()

        # request must have header Accept: application/json
        if request.headers.get('Accept') != 'application/json':
            return bad_accept_header()  # 406

        # validate that the request includes at least one required attribute
        if content is None or not ("name" in content or "type" in content or "length" in content):
            result = {"Error": "The request object does not have at least one of the required attributes"}
            return (result, 400)

        # validate that the request is not attempting to edit the 'id'
        if "id" in content:
            result = {"Error": "The id property cannot be changed"}
            return (result, 403)

        # edit designated boat attributes
        if "name" in content:
            update_name = content["name"]
        else:
            update_name = boat["name"]

        if "type" in content:
            update_type = content["type"]
        else:
            update_type = boat["type"]

        if "length" in content:
            update_length = content["length"]
        else:
            update_length = boat["length"]

        boat.update({"name": update_name, "type": update_type, "length": update_length, "owner": boat["owner"], "loads": boat["loads"]})
        client.put(boat)

        load_self = []
        for load_id in boat["loads"]:
            load_self.append({"id": load_id, "self": constants.url + "/loads/" + str(load_id)})

        result = {
            "id": boat.key.id,
            "name": boat["name"],
            "type": boat["type"],
            "length": boat["length"],
            "owner": boat["owner"],
            "loads": load_self,
            "self": constants.url + "/boats/" + str(boat.key.id)
        }

        return jsonify(result)

    elif request.method == 'PUT':
        # edit all attributes of a boat owned by the authorized user
        content = request.get_json()

        # request must have header Accept: application/json
        if request.headers.get('Accept') != 'application/json':
            return bad_accept_header()  # 406

        # validate that the request includes all three required attributes
        if content is None or "name" not in content or "type" not in content or "length" not in content:
            result = {"Error": "The request object is missing at least one of the required attributes"}
            return (result, 400)

        # validate that the request is not attempting to edit the 'id'
        if "id" in content:
            result = {"Error": "The id property cannot be changed"}
            return (result, 403)

        boat.update({"name": content["name"], "type": content["type"], "length": content["length"], "owner": boat["owner"], "loads": boat["loads"]})
        client.put(boat)

        load_self = []
        for load_id in boat["loads"]:
            load_self.append({"id": load_id, "self": constants.url + "/loads/" + str(load_id)})

        result = {
            "id": boat.key.id,
            "name": boat["name"],
            "type": boat["type"],
            "length": boat["length"],
            "owner": boat["owner"],
            "loads": load_self,
            "self": constants.url + "/boats/" + str(boat.key.id)
        }

        return jsonify(result)

    elif request.method == 'DELETE':
        # remove the carrier for every load
        for load in boat["loads"]:
            key = client.key(constants.loads, load["id"])
            load = client.get(key=key)

            load.update({"volume": load["volume"], "carrier": None, "content": load["content"], "creation_date": load["creation_date"]})
            client.put(load)

        # delete a boat owned by the authorized user
        client.delete(boat_key)
        return ('', 204)

    else:
        # invalid request method type
        return bad_request_method() # 405


@app.route('/loads', methods=['POST', 'GET'])
def post_get_loads():
    # request must have header Accept: application/json
    if request.headers.get('Accept') != 'application/json':
        return bad_accept_header()  # 406

    if request.method == 'POST':
        # create a new load
        content = request.get_json()

        # validate that the request includes all required attributes
        if content is None or "volume" not in content or "content" not in content or "creation_date" not in content:
            result = {"Error": "The request object is missing at least one of the required attributes"}
            return (result, 400)

        # create a load in Datastore
        new_load = datastore.entity.Entity(key=client.key(constants.loads))
        new_load.update({"volume": content["volume"], "carrier": None, "content": content["content"], "creation_date": content["creation_date"]})
        client.put(new_load)
        result = {
            "id": new_load.key.id,
            "volume": new_load["volume"],
            "carrier": new_load["carrier"],
            "content": new_load["content"],
            "creation_date": new_load["creation_date"],
            "self": constants.url + "/loads/" + str(new_load.key.id)
        }
        return (result, 201)

    elif request.method == 'GET':
        # list all loads

        # function for getting a page of results based on a given cursor
        def get_page_loads(cursor=None):
            query = client.query(kind=constants.loads)
            query_iter = query.fetch(start_cursor=cursor, limit=5)
            page = next(query_iter.pages)
            results = list(page)
            for e in results:
                e["id"] = e.key.id
                if e["carrier"]:
                    e["carrier"] = {"id": e["carrier"], "self": constants.url + "/boats/" + str(e["carrier"])}
                e["self"] = constants.url + "/loads/" + str(e.key.id)
            next_cursor = query_iter.next_page_token

            return results, next_cursor

        # no cursor received, start a query with a new cursor
        if request.args.get("cursor") is None:
            loads, next_cursor = get_page_loads()
        
        # received a cursor, make a query with this cursor
        else:
            loads, next_cursor = get_page_loads(request.args.get("cursor").encode('ascii'))

        result_page = {"loads": loads}

        # if there is a next page, include a next url with a query parameter of the cursor
        if next_cursor is not None:
            result_page["next"] = constants.url + "/loads?cursor=" + next_cursor.decode('ascii')

        # include a count of the total number of loads
        query = client.query(kind=constants.loads)
        total_entries = len(list(query.fetch()))
        result_page["total"] = total_entries

        return jsonify(result_page)

    else:
        # invalid request method type
        return bad_request_method() # 405


@app.route('/loads/<load_id>', methods=['GET', 'PATCH', 'PUT', 'DELETE'])
def get_patch_put_delete_load_id(load_id):
    # validate load_id matches an existing load
    load_key = client.key(constants.loads, int(load_id))
    load = client.get(key=load_key)
    if load is None:
        result = {"Error": "No load with this load_id exists"}
        return (result, 404)

    if request.method == 'GET':
        # view a load

        # request must have header Accept: application/json
        if request.headers.get('Accept') != 'application/json':
            return bad_accept_header()  # 406

        carrier_self = load["carrier"]
        if load["carrier"]:
            carrier_self = {"id": load["carrier"], "self": constants.url + "/boats/" + str(load["carrier"])}

        result = {
            "id": load.key.id,
            "volume": load["volume"],
            "carrier": carrier_self,
            "content": load["content"],
            "creation_date": load["creation_date"],
            "self": constants.url + "/loads/" + str(load.key.id)
        }

        return jsonify(result)

    elif request.method == 'PATCH':
        # edit some atttributes of a load
        content = request.get_json()

        # request must have header Accept: application/json
        if request.headers.get('Accept') != 'application/json':
            return bad_accept_header()  # 406

        # validate that the request includes at least one required attribute
        if content is None or not ("volume" in content or "content" in content or "creation_date" in content):
            result = {"Error": "The request object does not have at least one of the required attributes"}
            return (result, 400)

        # validate that the request is not attempting to edit the 'id'
        if "id" in content:
            result = {"Error": "The id property cannot be changed"}
            return (result, 403)

        # edit designated load attributes
        if "volume" in content:
            update_volume = content["volume"]
        else:
            update_volume = load["volume"]

        if "content" in content:
            update_content = content["content"]
        else:
            update_content = load["content"]

        if "creation_date" in content:
            update_creation_date = content["creation_date"]
        else:
            update_creation_date = load["creation_date"]

        load.update({"volume": update_volume, "carrier": load["carrier"], "content": update_content, "creation_date": update_creation_date})
        client.put(load)

        carrier_self = load["carrier"]
        if load["carrier"]:
            carrier_self = {"id": load["carrier"], "self": constants.url + "/boats/" + str(load["carrier"])}

        result = {
            "id": load.key.id,
            "volume": load["volume"],
            "carrier": carrier_self,
            "content": load["content"],
            "creation_date": load["creation_date"],
            "self": constants.url + "/loads/" + str(load.key.id)
        }

        return jsonify(result)

    elif request.method == 'PUT':
        # edit all attributes of a load
        content = request.get_json()

        # request must have header Accept: application/json
        if request.headers.get('Accept') != 'application/json':
            return bad_accept_header()  # 406

        # validate that the request includes all three required attribute
        if content is None or "volume" not in content or "content" not in content or "creation_date" not in content:
            result = {"Error": "The request object is missing at least one of the required attributes"}
            return (result, 400)

        # validate that the request is not attempting to edit the 'id'
        if "id" in content:
            result = {"Error": "The id property cannot be changed"}
            return (result, 403)

        load.update({"volume": content["volume"], "carrier": load["carrier"], "content": content["content"], "creation_date": content["creation_date"]})
        client.put(load)

        carrier_self = load["carrier"]
        if load["carrier"]:
            carrier_self = {"id": load["carrier"], "self": constants.url + "/boats/" + str(load["carrier"])}

        result = {
            "id": load.key.id,
            "volume": load["volume"],
            "carrier": carrier_self,
            "content": load["content"],
            "creation_date": load["creation_date"],
            "self": constants.url + "/loads/" + str(load.key.id)
        }

        return jsonify(result)

    elif request.method == 'DELETE':
        # if the load is being carried
        if load["carrier"]:
            # remove the load from the carrier boat
            key = client.key(constants.boats, load["carrier"])
            boat = client.get(key=key)

            # remake the list of loads, except for this load being deleted
            all_loads = []
            for l in boat["loads"]:
                if l != load_id:
                    all_loads.append(l)
            
            boat.update({"name": boat["name"], "type": boat["type"], "length": boat["length"], "owner": boat["owner"], "loads": all_loads})
            client.put(boat)

        # delete a load
        client.delete(load_key)
        return ('', 204)

    else:
        # invalid request method type
        return bad_request_method() # 405


@app.route('/boats/<boat_id>/loads/<load_id>', methods=['PUT', 'DELETE'])
def assign_remove_load_boat(boat_id, load_id):
    boat_key = client.key(constants.boats, int(boat_id))
    boat = client.get(key=boat_key)

    load_key = client.key(constants.loads, int(load_id))
    load = client.get(key=load_key)

    # validate boat_id and load_id match an existing boat and load
    if boat is None or load is None:
        result = {"Error": "The specified boat and/or load does not exist"}
        return (result, 404)

    if request.method == 'PUT':
        # assign a load to a boat

        # validate that the load has no carrier
        if load["carrier"] is not None:
            result = {"Error": "The load is already assigned to a boat"}
            return (result, 403)

        # update load["carrier"] to boat_id
        load.update({"volume": load["volume"], "carrier": int(boat_id), "content": load["content"], "creation_date": load["creation_date"]})
        client.put(load)

        # update boat["loads"] to include load_id
        all_loads = []
        for l in boat["loads"]:
            all_loads.append(l)
        all_loads.append(int(load_id))
        boat.update({"name": boat["name"], "type": boat["type"], "length": boat["length"], "owner": boat["owner"], "loads": all_loads})
        client.put(boat)

        return ('', 204)

    elif request.method == 'DELETE':
        # remove a load from a boat

        # validate that the load is assigned to the boat
        if load["carrier"] != int(boat_id):
            result = {"Error": "No load with this load_id is assigned to the boat with this boat_id"}
            return (result, 404)

        # update load["carrier"] to None
        load.update({"volume": load["volume"], "carrier": None, "content": load["content"], "creation_date": load["creation_date"]})
        client.put(load)

        # update boat["loads"] to remove load_id
        all_loads = []
        for l in boat["loads"]:
            if l != int(load_id):
                all_loads.append(l)
        
        boat.update({"name": boat["name"], "type": boat["type"], "length": boat["length"], "owner": boat["owner"], "loads": all_loads})
        client.put(boat)

        return ('', 204)

    else:
        # invalid request method type
        return bad_request_method() # 405


@app.route('/clear', methods=['DELETE'])
def clear():
    if request.method == 'DELETE':
        query = client.query(kind=constants.boats)
        results = list(query.fetch())
        for b in results:
            boat_key = client.key(constants.boats, b.key.id)
            client.delete(boat_key)

        query = client.query(kind=constants.loads)
        results = list(query.fetch())
        for l in results:
            load_key = client.key(constants.loads, l.key.id)
            client.delete(load_key)

        return ('', 204)


def bad_request_method():
    # assemble the error response for a bad request method type
    res = make_response(json.dumps({"Error": "Unsupported request method"}))
    res.mimetype = 'application/json'
    res.status_code = 405
    return res


def bad_accept_header():
    # assemble the error response for a request missing 'Accept: application/json'
    res = make_response(json.dumps({"Error": "The request's Accept header is missing or unsupported"}))
    res.mimetype = 'application/json'
    res.status_code = 406
    return res

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)

