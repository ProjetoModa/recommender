from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import Recommender
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

cors = CORS()
recommender = Recommender()

def create_app():
    app = Flask(__name__)
    
    app.config.from_pyfile('config.py')
    
    cors.init_app(app)
    
    from models import db, Product
    db.init_app(app)
    
    with app.app_context():
        try:
            data = pd.read_sql(Product.query.statement, db.engine)
            recommender.init_app(data)
        except Exception as e:
            print(e)
    
    @app.route('/')
    def index():
        return "ok"
    
    @app.route('/recomm', methods=['GET','POST'])
    def recomm():
        state = request.json.get('state')
        return jsonify({"products": recommender.recommend(state)})
    
    @app.route('/entropy', methods=['GET','POST'])
    def entropy():
        state = request.json.get('state')
        return jsonify({"entropy": recommender.entropy(state)})
        
    return app