from flask import Flask, Response, request
from flask_restful import Api, Resource
from flask import request
from flask_cors import CORS
from flask_pymongo import pymongo
import json
import os
import datetime
from dotenv import load_dotenv
load_dotenv()

from prediction import predict_sentiment


app = Flask(__name__)
CORS(app)

# app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
# mongo = PyMongo(app)



# ---------------DB models : start-------------

try:
  connection_string = os.environ.get('MONGO_URI')
  mongo = pymongo.MongoClient(
    connection_string
  )
  db = mongo.get_database('Stock-Sentiment')
  news = db.news
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

@app.route("/findSentiment", methods = ["POST"])
def find_sentiment():
  try:
    print("request --", json.loads(request.data))
    data= json.loads(request.data)
    from_str = data["from_str"]
    end_str = data["end_str"]
    if(data["stock"]==""):
      raise Exception("Stock name is required")
    res = db.news.aggregate([
      {
        "$match":{
          "stock": data["stock"],
          "date":{
            '$gte':from_str,
            '$lte' : end_str
        }
        }
      },
      {
        "$group":{
          "_id":"$stock",
          "sentimentSum":{"$sum":"$confidence"},
          "sentimentCount":{"$sum":1}
        }
      }

    ])

    res1 = db.news.aggregate([
      {
        "$match":{
          "stock": data["stock"],
          "status":"POSITIVE",
          "date":{
            '$gte':from_str,
            '$lte' : end_str
        }
        }
      },
      {
        "$group":{
          "_id":"$stock",
          "positiveCount":{"$sum":1}
        }
      }

    ])

    lst=[]
    for x in res:
      lst.append(x)
    
    for x in res1:
      if(x):
        lst.append(x)
    print("List--")  
    print(lst)
    average = lst[0]["sentimentSum"]/lst[0]["sentimentCount"]
    return Response(
      response=json.dumps({
        "message":"Success",
        "averageSentiment":average,
        "totalNews":lst[0]["sentimentCount"],
        "totalConfidence": lst[0]["sentimentSum"],
        "positiveNewsCount":lst[1]["positiveCount"]
      }),
      status = 200,
      mimetype="application/json"
    )

  except Exception as ex:
    print(" Exception --- ", ex)


@app.route("/getNews", methods=["POST"])
def get_news():
    try:
      print("request --", json.loads(request.data))
      data= json.loads(request.data)
      from_str = data["from_str"]
      end_str = data["end_str"]
      if(data["stock"]):
        query={
          "stock": data["stock"],
          "date":{
            '$gte':from_str,
            '$lte' : end_str
          }
        }  
      else:
        query={
          "date":{
            '$gte':from_str,
            '$lte' : end_str
          }
        }
      
      res = db.news.find(query)
      lst=[]
      for x in res:
        x['_id'] = str(x['_id'])
        lst.append(x)
      
      print(lst)
      return Response(
      response=json.dumps({
        "message":"News Received",
        "data":lst
      }),
      status = 200,
      mimetype="application/json"
      )
    except Exception as ex:
      print(" Exception --- ", ex)

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
    date_str = data["date"] # The date - 29 Dec 2017
    format_str = '%d%m%Y' # The format
    datetime_obj = datetime.datetime.strptime(date_str, format_str)
    # print(datetime_obj.date())
    date_str = str(datetime_obj.date())
    newsexample={
      "date" : date_str,
      "news" : data["news"],
      "stock" : data["stock"],
      "URL": data["URL"],
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

@app.route("/insertNewsApi",methods = ["POST"])
def insert_news_api():
  try:
    print("request --", json.loads(request.data))
    data = json.loads(request.data)
    date_str = data["date"] # The date - 29 Dec 2017
    format_str = '%d%m%Y' # The format
    datetime_obj = datetime.datetime.strptime(date_str, format_str)
    # print(datetime_obj.date())
    date_str = str(datetime_obj.date())

    confidenceLst = predict_sentiment(data["news"])
    confidence = confidenceLst[0]
    status = confidenceLst[1]
    newsexample={
      "date" : date_str,
      "news" : data["news"],
      "stock" : data["stock"],
      "URL": data["URL"],
      "status" : status,
      "confidence" : confidence
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

# @app.route("/getAllNews", methods = ["GET"])
# def get_all_news():
#   try:
#     all_news = news.find()
#     res = []
#     for obj in all_news:
#       obj['_id'] = str(obj['_id'])
#       res.append(obj)
#     return {
#       'message': 'All news',
#       'data': res,
#     }, 201
#   except Exception as e:
#     return {'message': 'Server Error' + str(e)}, 500

# @app.route("/getConfidence", methods = ["POST"])
# def get_confidence():
#   try:
#     data = json.loads(request.data)
#     confidence = predict_sentiment(data["news"])
#     return {
#       "message":"Confidence Received",
#       "confidence": float(confidence)
#     }
#   except Exception as ex:
#     print(" Exception ", ex)

@app.route("/insertAllNews", methods = ["POST"])
def insert_allnews():
  try:
    print("request --", json.loads(request.data))
    data = json.loads(request.data)
    dbresponse=db.news.insert_many(data)
    if(dbresponse):
      return Response(
        response=json.dumps({
          "message":"News Inserted"
        }),
        status = 200,
        mimetype="application/json"
      )
    else:
      raise Exception("Error occurred ")
  except Exception as ex:
    print(" Exception --- ", ex)

@app.route("/insertBulkNewsSentiment", methods = ["POST"])
def insert_BulkNews():
  try:
    print("request --", json.loads(request.data))
    data = json.loads(request.data)
    print("data--", data[1])
    for x in range(0,len(data),1):
      sentimentRes = predict_sentiment(data[x]["news"])
      x["status"]=sentimentRes[1]
      x["confidence"]=sentimentRes[0]
    print("request2 -- ", data)
    # dbresponse=db.news.insert_many(data)
    if(dbresponse):
      return Response(
        response=json.dumps({
          "message":"News Inserted"
        }),
        status = 200,
        mimetype="application/json"
      )
    else:
      raise Exception("Error occurred ")
  except Exception as ex:
    print(" Exception --- ", ex)

# ---------------API views : end---------------

api = Api(app)
api.add_resource(Class1, '/')


if __name__ == '__main__':
  # print("Port running succesfully")
  app.run(debug="True")
  