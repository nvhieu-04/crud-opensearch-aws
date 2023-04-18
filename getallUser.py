import json
import urllib3

def lambda_handler(event, context):
    # Define the endpoint URL
    endpoint_url = 'https://search-userdata-qgqel3s3yvu4avjuxbmgvhtcvi.ap-southeast-1.es.amazonaws.com/user/_search'
    
    # Define the query data
    query_data = {
        "query": {
            "match_all": {}
        }
    }
    
    # Convert the query data to JSON format
    query_json = json.dumps(query_data)
    
    # Define the headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46QWRtaW4yMDIzQA=='
    }
    
    # Send a POST request with the query data to the OpenSearch endpoint
    http = urllib3.PoolManager()
    response = http.request('POST', endpoint_url, body=query_json, headers=headers)
    
    # Parse the response data to extract the documents
    response_data = json.loads(response.data.decode('utf-8'))
    documents = response_data['hits']['hits']

    return {
        'statusCode': 200,
        'body': documents
    }