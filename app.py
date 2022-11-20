from flask import Flask, Response, request
from flask_restful import Api, Resource
from flask import request
from flask_cors import CORS
from flask_pymongo import pymongo
import json
# from dotenv import load_dotenv
# load_dotenv()


app = Flask(__name__)
CORS(app)

# app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
# mongo = PyMongo(app)



# ---------------DB models : start-------------

try:
  connection_string = "mongodb+srv://kushal:kushal@stock-sentiment.qcwkphz.mongodb.net/?retryWrites=true&w=majority"
  mongo = pymongo.MongoClient(
    connection_string
  )
  db = mongo.get_database('Stock-Sentiment')
  print("Connection Established")
  mongo.server_info() #trigger exception if server cannot connect to db
  
except Exception as ex:
  print("Issue with Database connection")
  print(ex)
# ---------------DB models : end---------------

# ---------------helpers : start-------------
# ---------------helpers : end---------------


# ---------------API views : start-------------



class Class1(Resource):
  def get(self):
    return {'data': 'This is get'}
  def post(self):
    return {'data': 'This is post'}

@app.route("/insertNews",methods = ["POST"])
def insert_news():
  try:
    # newsexample={
    #   "date" : "05/01/17",
    #   "news" : "Eliminating shadow economy to have positive impact on GDP : Arun Jaitley",
    #   "stock" : "HDFC Bank",
    #   "status" : "positive",
    #   "confidence" : 0.99
    #   }

    print("request --", json.loads(request.data))
    data = json.loads(request.data)
    newsexample={
      "date" : data["date"],
      "news" : data["news"],
      "stock" : data["stock"],
      "status" : data["status"],
      "confidence" : data["confidence"]
      }
    print("news --", newsexample)
    dbresponse=db.news.insert_one(newsexample)
    return Response(
      response=json.dumps({
        "message":"News Inserted",
        "id":f"{dbresponse.inserted_id}"
      }),
      status = 200,
      mimetype="application/json"
    )
  except Exception as ex:
    print(" Exception --- ", ex)



# ---------------API views : end---------------

api = Api(app)
api.add_resource(Class1, '/')


if __name__ == '__main__':
  print("Port running succesfully")
  app.run(port=80,debug="True")
  