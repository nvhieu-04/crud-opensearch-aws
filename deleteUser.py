import json
import urllib3

def lambda_handler(event, context):
    # Define the endpoint URL
    print(event)
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
    
    # Send a DELETE request to the OpenSearch endpoint
    http = urllib3.PoolManager()
    response = http.request('DELETE', endpoint_url, headers=headers)
    
    # Parse the response data to check if the document was deleted successfully
    response_data = json.loads(response.data.decode('utf-8'))
    if response_data['result'] == 'deleted':
        return {
            'statusCode': 200,
            'body': json.dumps('User deleted successfully')
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('User delete failed')
        }
    