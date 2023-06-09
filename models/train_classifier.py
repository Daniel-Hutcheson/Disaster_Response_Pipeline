# import libraries
import sys

import pandas as pd
from sqlalchemy import create_engine

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV

import pickle


def load_data(database_filepath):
    '''
    Loads the data from a given SQL database.

    Args:
    database_filepath = filepath to the database to load

    returns:
    X: Input variables
    Y: Output variables
    '''

    engine = create_engine('sqlite:///{}'.format(database_filepath))

    df = pd.read_sql('data_cleaned', con=engine)
    X = df.message.copy()
    Y = df.drop(columns=['message','id','original','genre']).copy()

    category_names = Y.columns.values

    return X, Y, category_names

def tokenize(text):
    '''
    Tokenizes the given input text.

    Args:
    text: Text to tokenize

    returns:
    cleaned tokens
    '''
    
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def build_model():
    '''
    Builds a model.

    returns:
    model
    '''

    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        # ('clf', RandomForestClassifier()),
        ('multi_output', MultiOutputClassifier(AdaBoostClassifier()))
    ])

    params = pipeline.get_params()
    # print(params)

    parameters = {
        'vect__ngram_range': ((1, 1), (1, 2)),
        'multi_output__estimator__n_estimators': [50, 100, 200]
    }

    model = GridSearchCV(pipeline, param_grid=parameters)

    return model


def evaluate_model(model, X_test, Y_test, category_names):
    '''
    This function evaluates the model and prints out all relevant stats relating to the models performance.

    Args:
    model: the build model
    X_test: test set
    Y_test: test set
    category_names: the names of the columns to be predicted by the model
    '''
    Y_pred = model.predict(X_test)

    i = 0
    for category in category_names:
        print(classification_report(Y_test[category], Y_pred[:,i], zero_division=True))
        i += 1


def save_model(model, model_filepath):
    '''
    Saves a given model to a pickle file using a given filepath.
    '''

    with open(model_filepath, 'wb') as file:
        pickle.dump(model, file)


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train[:10], Y_train[:10])
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()