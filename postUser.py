import json
import urllib3

def lambda_handler(event, context):
    print(event)
    # Define the endpoint URL
    
    name = event.get('name', '')
    phone = event.get('phone', '')
    id = event.get('id', '')
    if id == '':
        return {
            'statusCode': 400,
            'body': json.dumps('Id is required')
        }
    if name == '' or phone == '':
        return {
            'statusCode': 400,
            'body': json.dumps('Name and phone number are required')
        }
    if len(name) < 6:
        return {
            'statusCode': 400,
            'body': json.dumps('Length of username must be greater than 6')
        }
    if name[0].isnumeric():
        return {
            'statusCode': 400,
            'body': json.dumps('Name must not start with a number')
        }
    if name[0].islower():
        return {
            'statusCode': 400,
            'body': json.dumps('Name must not start with a lowercase letter')
        }
    if len(phone) != 10:
            return {
                'statusCode': 400,
                'body': json.dumps('Phone number must be 10 digits')
            }
    if phone[0] != '0':
        return {
            'statusCode': 400,
            'body': json.dumps('Phone number must start with 0')
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
    print('result:'+response_data)
    checkdata = response_data.get('found', '')
    if checkdata == True:
        return {
            'statusCode': 400,
            'body': json.dumps('User already exists')
        }

    # Define the document data
    doc_data = {"name": name, "id": id, "phone": phone}
    endpoint_url = 'https://search-userdata-qgqel3s3yvu4avjuxbmgvhtcvi.ap-southeast-1.es.amazonaws.com/user/_doc/' + id
    # Convert the document data to JSON format
    doc_json = json.dumps(doc_data)
    
    # Define the headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46QWRtaW4yMDIzQA=='
    }
    
    # Send a POST request with the document data to the OpenSearch endpoint
    http = urllib3.PoolManager()
    response = http.request('POST', endpoint_url, body=doc_json, headers=headers)
    
    # Check the response status code
    if response.status == 201:
        return {
            'statusCode': 200,
            'body': json.dumps('Document created successfully')
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Document creation failed')
        }