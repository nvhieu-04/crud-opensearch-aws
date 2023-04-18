import json
import urllib3
import string    
import random

def gen_phone():
    first = str(random.randint(100,999))
    second = str(random.randint(1,888)).zfill(3)

    last = (str(random.randint(1,9998)).zfill(4))
    while last in ['1111','2222','3333','4444','5555','6666','7777','8888']:
        last = (str(random.randint(1,9998)).zfill(4))
        
    return '{}-{}-{}'.format(first,second, last)


def lambda_handler(event, context):
    # Define the endpoint URL
    print(event)
    for id in range(1, 100000):
        endpoint_url = f'https://search-userdata-qgqel3s3yvu4avjuxbmgvhtcvi.ap-southeast-1.es.amazonaws.com/users/_doc/' + str(id)
        #endpoint_url = f'https://search-userdata-qgqel3s3yvu4avjuxbmgvhtcvi.ap-southeast-1.es.amazonaws.com/users/_bulk/' + str(id)
        # Define the headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic YWRtaW46QWRtaW4yMDIzQA=='
        }
        S = 10  # number of characters in the string.  
        # call random.choices() string module to find the string in Uppercase + numeric data.  
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
        for _ in range(1, 10):
           phone = gen_phone()
        doc_data = {"name": str(ran), "id": id, "phone": phone}
        doc_json = json.dumps(doc_data)
        # Send a POST request to the OpenSearch endpoint
        http = urllib3.PoolManager()
        response = http.request('POST', endpoint_url,body=doc_json, headers=headers)
        print(response.data)

    return {
        'statusCode': 200,
        'body': json.dumps('Success')}    

if __name__ == '__main__':
    lambda_handler(None, None)