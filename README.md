<p align="center">
 <a href="http://dataframe-playground.test.fedcloud.eu/"><img width="70%" src="docs/resources/header_logo.svg" /></a>
</p>

<h2 align="center"><a href="http://dataframe-playground.test.fedcloud.eu/">Dataframe Playground Web App</a></h2>
Simple data mining without any coding in your browser. Chained filters, interactive data visualizations, and many special features for bioinformatics. Shareable URLs for presenting your data in an interactive environment.

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
