from flask import Flask
from flask_restful import Api, Resource
from flask import request
from flask_cors import CORS
from flask_pymongo import PyMongo

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
CORS(app)

# app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
# mongo = PyMongo(app)



# ---------------DB models : start-------------
# ---------------DB models : end---------------

# ---------------helpers : start-------------
# ---------------helpers : end---------------


# ---------------API views : start-------------



class Class1(Resource):
  def get(self):
    return {'data': 'This is get'}
  def post(self):
    return {'data': 'This is post'}

# ---------------API views : end---------------

api = Api(app)
api.add_resource(Class1, '/')


if __name__ == '__main__':
  app.run(debug="True")