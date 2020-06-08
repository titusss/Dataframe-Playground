# Plugins
Plugins are just REST-API endpoints which return a link to a html visualization which is displayed in an ***iframe***.
## Structure
Plugins consist of:
 - ID
 - Name
 - An API address that:
	 - accepts POST requests with a **comma-seperated** file
	 - returns a URL to the visualization
 - Description
 - Logo
## Database and storage
Plugins are stored in the ***plugins*** collection of the MongoDB as described above.
The ***visualization*** collection stores the ID's of the plugins that are activated in this session.

Whenever a session is opened, the *config* is loaded from the *visualization* collection and the backend searches the *plugins* collection for plugins with the ID saved in said *config*.
## Adding a plugin: Frontend
Plugins can be added by any user over the website. **These plugins are not stored permantly and require an API endpoint that accepts a CSV with or without Pandas Indices**. This limits the possiblity of sharing a session with an plugin that returns a malicious website embeded in the visualization iframe. Be very careful with this!
## Adding a plugin: Backend
Some API endpoints expect the posted dataframe to be formatted in a special way and don't accept the generically structured CSV-table. To reshape the dataframe in the backend, you need a few lines of Pandas-Python-Code. Copy and paste the ***template.py*** in ***public/server/plugins***.

