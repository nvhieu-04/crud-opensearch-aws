import json
import urllib3
import boto3
import base64
import botocore
from botocore.errorfactory import ClientError

def lambda_handler(event, context):
    user_id = event.get('id', '')
    if user_id == '':
        return {
            'statusCode': 400,
            'body': json.dumps('Id is required')
        }
    endpoint_url = f'https://search-userdata-qgqel3s3yvu4avjuxbmgvhtcvi.ap-southeast-1.es.amazonaws.com/user/_doc/' + user_id
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
    s3 = boto3.client('s3')
    filename = document.get('image', '')
    print(filename)
    if filename == '':
        return {
            'statusCode': 404,
            'body': json.dumps('File not found')
        }
    #Check file exist()
    try:
        s3.head_object(Bucket='testbucketexists', Key='userId'+ user_id + '/' + filename )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return {
                'statusCode': 404,
                'body': json.dumps('File not found')
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps('Error')
            }
    # url = s3.generate_presigned_url(
    #     ClientMethod='get_object',
    #     Params={
    #         'Bucket': 'myawsbucket-1244',
    #         'Key': filename + '.jpg',
    #     }
    # )
    # print(url)
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps(url)
    # }
    url = s3.get_object(
        Bucket='testbucketexists', 
        Key='userId'+ user_id + '/' + filename,
        )
    print(url)
    convertBase64 = base64.b64encode(url['Body'].read())
    value = {
        'filename': filename + '.jpg',
        'base64data': convertBase64.decode('utf-8'),
    }
    return {
        'statusCode': 200,
        'body': json.dumps(value)
    }