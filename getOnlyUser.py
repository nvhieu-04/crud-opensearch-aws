import json
import urllib3

def lambda_handler(event, context):
    print(event)
    # Define the endpoint URL
    id = event.get('id', '')
    if id == '':
        return {
            'statusCode': 400,
            'body': json.dumps('Id is required')
        }
    endpoint_url = f'https://search-userdata-qgqel3s3yvu4avjuxbmgvhtcvi.ap-southeast-1.es.amazonaws.com/user/_doc/' + id
    
    # Define the headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46QWRtaW4yMDIzQA=='
    }
    
    # Send a GET request to the OpenSearch endpoint
    http = urllib3.PoolManager()
    response = http.request('GET', endpoint_url, headers=headers)
    
    # Parse the response data to extract the document
    response_data = json.loads(response.data.decode('utf-8'))
    print(response_data)
    checkdata = response_data.get('found', '')
    if checkdata == False:
        return {
            'statusCode': 400,
            'body': json.dumps('User not found')
        }
    document = response_data['_source']
    print(document)
    # Extract the desired fields from the document
    if document == None:
        return {
            'statusCode': 400,
            'body': json.dumps('User not found')
        }
    return {
        'statusCode': 200,
        'body': document
    }