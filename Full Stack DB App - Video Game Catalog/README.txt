Video Game Catalog
Full Stack Relational Database Application
by Joshua Luo

A Video Game Catalog for a user to create and maintain a catlog of video game titles.

Video game information is maintained in a relational database. The database contains four main entities: Video Game Titles, Development Studios, Platforms, and Franchises. See 'design_documentatin.pdf' for more information on the relationships between the entities and their respective attributes.

A user can search, create, edit, and delete video game entries with attributes for title, platforms, release date, genre, franchise, developer, and ESRB rating.

On the 'Catalog' page, the user begins with a display of the entire catalog. The user can then input or select various options for the attributes to filter the catalog accordingly.

On the 'Add Something' page, the user can create a new entry for any of the four entities, as well as create relationships between them. For creating a new Video Game Title, a desired platform, franchise, or developer must first be created before they can appear in the list to relate to the title.

On the 'Delete Something' page, the user can delete entries for any of the four entities. Relationships involving the entry will update to remove the relationship. Upon selecting an entity to delete, the page will display all entries for that entity. Then the user can utilize a search bar to further filter the displayed entries.

On the 'Update/Edit Something' page, the user can change attributes for any of the entities. The user can edit the attributes in place and click the entry's action button to save the new values. Upon selecting an entity to edit, the page will display all entries for that entity. Then the user can utilize a search bar to further filter the displayed entries.

Because the displayed information is dynamically generated, any changes to the entities will immediately be present on any subsequent display of entries.

File Descriptions:

app.py: Flask server to run the web application and to make the SQL queries to the database
data_definition_queries.sql: SQL queries for creating each entity table. Followed by some sample data
data_manipulation_queries.sql: SQL qury outlines for the various queries that that are sent to the databse
db_connector.py: API for connecting to the database with credentials
db_credentials.py: user credential information for making a connection to the database
static: CSS and JavaScript files for the front-end web application
templates: Jinja web page templates for rendering each route
wsgi.py: for executing app.py in Flask