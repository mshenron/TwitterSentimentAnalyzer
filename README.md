# TwitterSentiment ![](Media/AI_icon.png)
Falcon based API interface for sentiment analysis over twitter data


#### dependencies:
pip install -r requirements.txt

#### To start the App

Open utils.py file and go to line number 38 - 42 and input your api tokens there
```python
        # keys and tokens from the Twitter Dev Console
        consumer_key='#YOUR CUSTOMER KEY HERE'
        consumer_secret='#YOUR CUSTOMER SECRET HERE'
        access_token='#YOUR ACCESS TOKEN HERE'
        access_token_secret='YOUR ACCESS TOKEN SECRET HERE'
```
open terminal and start the server using
```bash
bash start.sh
```
#### API calls :
###### http://127.0.0.1:8089/api/AnalyzeTweets/
```python
import requests
url = "http://127.0.0.1:8089/api/AnalyzeTweets/"
payload = "{\"query\":\"bjp\"}"
headers = {'cache-control': "no-cache"}
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)
```
Returns a json object with <br />
{'PTP': positive tweets percentage <br />
'NTP' : negative tweets percentage<br />
'NTWP': neutral tweets percentage<br />
}

###### http://127.0.0.1:8089/api/GetSent/

```python
import requests
url = "http://35.196.64.132:8089/api/GetSent/"
payload = "{\"tweet\":\"I was happy to see her again\"}"
headers = {'cache-control': "no-cache"}
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)
```
Returns a json object with<br />
{'sentiment':sentiment of the sentence i.e Positive/Negative or Neutral<br />
'polarity': sentiment score<br />
'cleaned_text': processed text<br />
}
###### http://127.0.0.1:8089/api/SearchTwitter/

```python
import requests
url = "http://35.196.64.132:8089/api/SearchTwitter/"
payload = ""
headers = {'cache-control': "no-cache"}
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)
```
Returns a json object with <br />
{'PTP': positive tweets percentage<br />
'NTP' : negative tweets percentage<br />
'NTWP': neutral tweets percentage<br />
'ptweets': All positive tweets<br />
'ntweets' : all negative tweets<br />
}
