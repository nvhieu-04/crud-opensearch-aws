import boto3
import json
import json
import boto3
import base64
import botocore
from botocore.errorfactory import ClientError
from decimal import Decimal
import uuid
import urllib3
def lambda_handler(event, context):
    print(event)
    id = event.get('id', '')
    if id == '':
        return {
            'statusCode': 400,
            'body': json.dumps('Id is required')
        }
    filename = event.get('filename', '')
    base64data = event.get('base64data', '')
    if filename == '' or base64data == '':
        return {
            'statusCode': 400,
            'body': json.dumps('Filename and base64data are required')
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
    
    file = filename + str(uuid.uuid4())
    s3 = boto3.client('s3')
    try:
        s3.head_object(Bucket='testbucketexists',
                        Key= 'userId'+ id + '/' + file + '.jpg')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            s3 = boto3.resource('s3')
            s3.Object('testbucketexists', 'userId'+ id + '/' + file + '.jpg').put(Body=base64.b64decode(base64data))
            endpoint_url = f'https://search-userdata-qgqel3s3yvu4avjuxbmgvhtcvi.ap-southeast-1.es.amazonaws.com/user/_update/' + id
            update_data = {
                "doc": {
                    "image": file + '.jpg'
                }
            }
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
                    'body': json.dumps('Upload image successfully')
                }
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps('User update failed')
                }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps('Error')
            }
    return {
        'statusCode': 500,
        'body': json.dumps('File Exist')
    }