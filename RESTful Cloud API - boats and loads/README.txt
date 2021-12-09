Boats and Loads
RESTful Cloud API
by Joshua Luo

A RESTful Cloud API for managing boats and loads. The API manages boat and loads and assigning/removing loads to/from boats.

Users are created and authenticated via Auth0.

Boats are private entities that may only be created, edited, deleted, and viewed by the owner (the user that creates the boat).

Loads may be assigned to only one boat. One boat may be assigned any number of loads.

API supports authenticating users for appropriate requests. Boats are private, and may only be accessed by their respective owners/creators (except for assigning/removing loads). Loads are public, and may be created, edited, viewed, assigned, or removed by any user, even someone who is not authenticated.

See 'api_documentation.pdf' for more information on the data model for boats and loads and the route endpoints for the API.

Originally deployed on Google Cloud Platform.

File Descriptions:

api_documentation: API specification document for describing the entity data models and API endpoints.
app.yaml: GCP required file for deployment.
constants.py: variable constants for use in main.py.
main.py: application file for providing UI for user login/creation and the RESTful API endpoints.
requirements.txt: required Python packages for running main.py.