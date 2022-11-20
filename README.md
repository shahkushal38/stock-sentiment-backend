# major-project-backend

The APIs are as follows - 

1) Insert one News API - 

**URL - http://127.0.0.1/insertNews**

Request Object = 
>{
       "date" : "05/01/17",
       "news" : "Cautious on pharma , time to get into IT",
       "stock" : "Sun Pharma",
       "status" : "negative",
       "confidence" : -0.975
}

Response Object - 

> {
	"message": "News Inserted",
	"id": "637a380845b803c9f502449e"
}