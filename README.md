<p align="center">
 <a href="http://micromix.systems/"><img width="50%" src="docs/resources/header_logo.svg" /></a>
</p>

<h2 align="center"><a href="http://micromix.systems">Open Web App (Alpha)</a></h2>

<h4 align="center"><a href="http://micromix.systems/?config=5feb57e749815081f54e381a">Or start with sample session</a></h4>
Simple data mining without any coding in your browser. Chained filters, interactive data visualizations, and many special features for bioinformatics. Shareable URLs for presenting your data in an interactive environment. Interactive 3D & 2D Web.gl enabled heatmap build on Uber's Deck.gl included.
<p align="center"><img width="70%" src="docs/resources/screenshot_01.png" /></p>

## 🧮 Features

### 🔬 Basic
* Conditionally filter values (> Greater, < Smaller than, = Equal to, != Not)
* Chain conditions (Multiple filters)
* Quickly visualize results with expandable list of external plugins (Plotly, Clustergrammer, High-Performance Heatmap)
* Conditionally change values (Change cells with values=x to y)
* Calculate Fold-Changes
* Convert to Log (Custom bases)
* Merge datasets
* Download results as Excel, CSV

### 🧬 Bioinformatics
* Search for locus tags
* Filter for KEGG Pathways, GO Names, COG categories
* Filter for members of pathogenicity islands (Salmonella, B. Theta)
* Calculate transcript lengths
* Calculate TPM (Transcripts Per Million)

### 🔗 Sharing
* Sessions can be locked and the URL shared
* Data in a locked session can be interactively explored by receipients

![dfp_overview](https://user-images.githubusercontent.com/26855197/108297122-a6d0f800-714f-11eb-8464-781e4ea4d1bc.png)

<hr>

## 🛠️ Local installation
> This web-app consists of a Vue.js frontend communicating with a Python backend over flask. Sessions are stored in a MongoDB. ℹ️ The application always requires a running backend `flask run` and frontend `npm run serve`.

### Environment variables
> ℹ️ Make sure to have the environment variable `mongocredential` set to your MongoDB access token (e.g. `mongodb+srv://user:1234567abcde@cluster.abc.def.mongodb.net/abd?retryWrites=true&w=majority`) and accessible to the python virtual environment of the backend.

### Install backend
Clone repo and go to backend directory
```
git clone https://github.com/chinapwn/Dataframe-Playground.git
cd Dataframe-Playground
cd backend
```
Create and switch to Python virtual environment (Optional)
```
python3 -m venv venv
source venv/bin/activate
```
Install Python dependencies
```
pip install -r requirements.txt
````
Launch flask server
```
flask run
```
### Install frontend
Go to frontend directory (from repo's root folder)
```
cd frontend
```
Install vue-cli with Node Package Manager (npm)
```
npm install -g @vue/cli
```
Install node dependencies
```
npm install
```
Launch frontend
```
npm run serve
```
> Open the address shown in the terminal where you executed the line above with your web browser.
### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
