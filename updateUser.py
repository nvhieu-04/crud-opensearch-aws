import json
import urllib3

def lambda_handler(event, context):
    print(event)
    # Define the endpoint URL and update data
    id = event.get('id', '')
    if id == '':
        return {
            'statusCode': 400,
            'body': json.dumps('Id is required')
        }
    name = event.get('name', '')
    phone = event.get('phone', '')
    if name == '' and phone == '':
        return {
            'statusCode': 400,
            'body': json.dumps('Name or phone is required')
        }
    endpoint_url = f'https://search-userdata-qgqel3s3yvu4avjuxbmgvhtcvi.ap-southeast-1.es.amazonaws.com/user/_update/' + id
    update_data = {
        "doc": {
            "name": name,
            "phone": phone
        }
    }
    
    # Convert the update data to JSON format
    update_json = json.dumps(update_data)
    
    # Define the headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46QWRtaW4yMDIzQA=='
    }
    
    # Send a POST request to the OpenSearch endpoint
    http = urllib3.PoolManager()
    response = http.request('POST', endpoint_url, body=update_json, headers=headers)
    
    # Parse the response data to check if the update was successful
    response_data = json.loads(response.data.decode('utf-8'))
    print(response_data)
    if response_data['result'] == 'updated':
        return {
            'statusCode': 200,
            'body': json.dumps('User updated successfully')
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('User update failed')
        }