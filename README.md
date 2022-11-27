# major-project-backend

### Deployed Link
- https://stockvisualizer-api.herokuapp.com/

### For Local
- http://127.0.0.1:5000 

### Local Setup

```bash
# Clone this repository
$ git clone https://github.com/J0SAL/major-project-backend.git
# Go into the repository
$ cd major-project-backend
# Create & Activate Environment (optional & recommended) here's a sample code
$ python -m venv project_env
$ project_env\Scripts\activate.bat
# Install dependencies
pip -r requirements.txt
# Run the app
python app.py
# The server will start at <http://localhost:5000>
```



The APIs are as follows - 

1) Insert one News API - 

**URL - http://127.0.0.1/insertNews**

Note  - Date needs to be in String with "DDMMYYYY" format

Method = POST

Request Object = 
>{
       "date" : "06102018",
       "news" : "Cautious on pharma , time to get into IT",
       "stock" : "Sun Pharma"
}

Response Object - 

> {
	"message": "News Inserted",
	"id": "637a380845b803c9f502449e"
}


2) Get All News API - 

**URL- http://127.0.0.1/getNews**

Request Object 
Note  - 
1) stock field needs to be empy as shown 
2) from_str and end_str needs to be given as date in "dd-mm-yyyy" format 
```
{
       "from_str" : "2015-01-01",
       "end_str": "2019-11-06",
       "stock": ""
}
```
Response Object - 
```
{
	"message": "News Received",
	"data": [
		{
			"_id": "637dc1ab47dc0637807389bf",
			"date": "2017-01-05",
			"news": "Cautious on pharma , time to get into IT",
			"stock": "Sun Pharma",
			"status": "negative",
			"confidence": -0.975
		},
		{
			"_id": "637dc7ad373924030b760f0e",
			"date": "2018-10-06",
			"news": "Cautious on pharma , time to get into IT",
			"stock": "Sun Pharma",
			"status": "negative",
			"confidence": -0.975
		}
	]
}
```

3)  Get Stock Specific news

**URL - http://127.0.0.1/getNews**

Request Object - 

```
{
	"from_str" : "2015-01-01",
	"end_str": "2019-11-06",
	"stock": "Sun Pharma"
}
```


4) Get Sentiment for a duration

**URL - http://127.0.0.1/findSentiment**

Request Object - 

```
{
	"from_str" : "2015-01-01",
	"end_str": "2019-11-06",
	"stock": "Sun Pharma"
}
```

Response Object - 

```

{
	"message": "Success",
	"averageSentiment": -0.975,
	"totalNews": 4,
	"totalConfidence": -3.9,
	"positiveNewsCount": 1
}
```
