from django.shortcuts import render
import requests
from datetime import datetime

# Create your views here.

#Collecting Data
def data():
    # The GraphQL query

    query = """
    {
      pairs(first: 100  , orderBy: createdAtTimestamp, orderDirection: desc) {
        id
        token0 {
          id
          symbol
          name
        }
        token1 {
          id
          symbol
          name
        }
        token0Price
        token1Price
        createdAtTimestamp
    }
    }
      """
    result = run_query(query)  # Execute the query
    print('Result - {}'.format(result))
    return result


#Requesting the API
def run_query(query):  # A simple function to use requests.post to make the API call.
    #headers = {'X-API-KEY': 'YOUR API KEY'}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2',
                            json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed and return code is {}.    {}'.format(request.status_code,
                        query))


#Converting TimeStamt to date-time
def date_converter(result):
    for coin in result['data']['pairs']:

        coin['date'] = datetime.fromtimestamp(int(coin['createdAtTimestamp']))
    return result


#Redirecting collected data to hem page
def home(request):
    result = data()
    output = date_converter(result)
    return render(request,'home.html',{'output':output['data']['pairs']})