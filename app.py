import warnings
from flask import Flask, render_template, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
from book_rec import rec



app = Flask(__name__)
api = Api(app)

warnings.filterwarnings('ignore')
#%matplotlib inline

#import tensorflow.keras as tf

# load ratings
ratings = pd.read_csv('BX-Book-Ratings.csv', encoding='cp1251', sep=';')
ratings = ratings[ratings['Book-Rating']!=0]
# load books
books = pd.read_csv('BX-Books.csv',  encoding='cp1251', sep=';',error_bad_lines=False)

#users_ratigs = pd.merge(ratings, users, on=['User-ID'])
dataset = pd.merge(ratings, books, on=['ISBN'])
dataset_lowercase=dataset.apply(lambda x: x.str.lower() if(x.dtype == 'object') else x)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['GET'])
def get():
    if 'book_title' in request.args:
        book_title = request.args['book_title']

    rslt = rec(dataset,dataset_lowercase,book_title)
    return render_template('result.html', data = rslt)

@app.route('/recommend_api', methods=['GET'])
def recommend_api():
    if 'book_title' in request.args:
        book_title = request.args['book_title']

    rslt = rec(dataset, dataset_lowercase,book_title)
    return {'data': rslt}, 200

if __name__ == '__main__':
    app.run()  # run our Flask app