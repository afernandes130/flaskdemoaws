import json
import boto3
import uuid

def lambda_handler(event, context):
    #print("##EVENT##")
    #print(event)
    
    folder = "queue-ocr/"
    
    bucketName = 'testeorb-menssageria'
    key = folder + uuid.uuid4().hex

    url = boto3.client('s3').generate_presigned_url(
    ClientMethod='put_object', 
    Params={
        'Bucket': bucketName, 
        'Key': key,
        'ContentType': 'application/pdf'
    },
    ExpiresIn=3600,
    HttpMethod='PUT')


    data = {
    "bucketName":bucketName,
    "key":key,
    "filename_after_upload": "s3://" + bucketName + folder + key,
    "presigned_url": url
    } 

    
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
