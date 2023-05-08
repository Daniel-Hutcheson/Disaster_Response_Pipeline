# Disaster Response Pipeline Project

### Project Summary:
This project aims to be a helpful tool for first responders during a disastrous events. In case of such an event, where a large number of people and/or a big area is involved, first responders often are confronted with wast amounts of data and information through social networks and other sources. On the other hand during such events first responders have the least amount of time to filter all this data to obtain relevant and actual helpful insights to help people in the most effective way. 

This project tries to tackle this problem by processing social media messages into a form of data that can be used further for deeper analysis and also filters it regarding the actual relevance. Furthermore, after cleaning and prepping the data, a machine learning model is trained, which can be used to predict the relevance of a message regarding different categories, such as medical or infrastructure related topics.

This functionality is given through a web app, which also shows some plots regarding the currently given database.

### File Description:
This repository has three main folders that each contain a script to handle a specific part of the overall workflow:
- data/:

    This folder contains two CSV files, one with all messages we want to process and one that with all categories we want to use. Furthermore there is a python script (`process_data.py`) that processes the csv files into a cleaned SQL database, which is also saved in the same folder.

- models/:

    This folder contains a python script (`train_classifier.py`) that reads in the database, sets up a data pipeline to further optimize the data for training the ML model, actually builds and trains the model and saves it into a pickle file in the same directory.

- app/:

    This folder directory contains also a python script (`run.py`) which sets up a local web app that uses the build ML model to categorize given Messages and also displays some plots regarding the currently used database.
  
    
    
Overall project structure:

app  
| - template  
| |- master.html # main page of web app  
| |- go.html # classification result page of web app  
|- run.py # Flask file that runs app  
data  
|- disaster_categories.csv # data to process  
|- disaster_messages.csv # data to process  
|- process_data.py  
|- InsertDatabaseName.db # database to save clean data to  
models  
|- train_classifier.py  
|- classifier.pkl # saved model  
README.md  


### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Go to `app` directory: `cd app`

3. Run your web app: `python run.py`

4. Click the `PREVIEW` button to open the homepage
