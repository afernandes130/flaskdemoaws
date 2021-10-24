from io import StringIO
import json
from ntpath import join
from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
import requests
import re
import tempfile

import boto3
from boto3.s3.transfer import TransferConfig
import os
import threading
import sys
import pathlib


app = Flask(__name__)

localpath = 'C:\\Users\\Public\\Downloads'
fileDonwload_name = 'teste.pdf'
bucket_name = 'teste-python-adri'
queue_url = 'https://sqs.us-west-2.amazonaws.com/744929230126/testePython'
session = boto3.Session('accessKey', 'secretKey')



myurlAPI = 'https://jph3r2ps9e.execute-api.sa-east-1.amazonaws.com/Prod'



# REGIAO API
@app.route("/upload", methods=['POST'])
def teste_upload():
    arquivo = request.files['arquivo']
    upload_file(arquivo)
    return "upload feito"

@app.route("/download", methods=['GET'])
def download():
    receive_MessageSqs()
    return "Download feito"

@app.route("/upload-file-presignedurl", methods=['GET'])
def upload_file_presignedurl():
    result = GetFilePresignedUrl()
    if (UploadFileS3(result['presigned_url'])):
        SendRequestOCr(result['filename_after_upload'])
   
    return "Envio de Imagem para OCR Concluido"

def upload_file(arquivo):
    s3_client = session.client("s3")
    try:
        print("Uploading file: {}".format(arquivo.filename))
        # TransferConfig(multipart_threshold=1024 * 25, max_concurrency=10, multipart_chunksize=1024 * 25, use_threads=True)
        tc = boto3.s3.transfer.TransferConfig()
        t = boto3.s3.transfer.S3Transfer(client=s3_client, config=tc)
        pathfile = os.path.join(localpath, arquivo.filename)
        arquivo.save(pathfile)
        t.upload_file(pathfile, bucket_name , arquivo.filename)
        s3Uri = 's3://' + bucket_name + '/' + arquivo.filename
        print("S3 URI file: {}".format(s3Uri))
        send_MessageSqs(s3Uri)
    except Exception as e:
        print("Error uploading: {}".format(e))

def download_file(s3uri):
    s3_client = session.client("s3")
    splitedUri = s3uri.split('/')
    try:
        # TransferConfig(multipart_threshold=1024 * 25, max_concurrency=10, multipart_chunksize=1024 * 25, use_threads=True)
        tc = boto3.s3.transfer.TransferConfig()
        t = boto3.s3.transfer.S3Transfer(client=s3_client, config=tc)
        pathfile = os.path.join(localpath, 'S3Download_'+ splitedUri[-1])
        t.download_file(splitedUri[-2], splitedUri[-1], pathfile)
    except Exception as e:
        print("Error download: {}".format(e))

def send_MessageSqs(s3Uri):
  sqs = boto3.client('sqs')
  response = sqs.send_message(
      QueueUrl=queue_url,
      DelaySeconds=10,
      MessageAttributes={
          'FileS3': {
              'DataType': 'String',
              'StringValue': s3Uri
          },
      },
      MessageBody=(
          'Corpo atual da mensagem'
      )
  )
  print(response['MessageId'])

def receive_MessageSqs():
  sqs = boto3.client('sqs')
  
  # Mensagem recebida SQS
  response = sqs.receive_message(
      QueueUrl=queue_url,
      AttributeNames=[
          'SentTimestamp'
      ],
      MaxNumberOfMessages=1,
      MessageAttributeNames=[
          'All'
      ],
      VisibilityTimeout=0,
      WaitTimeSeconds=0
  )

  message = response['Messages'][0]
  receipt_handle = message['ReceiptHandle']
  s3uri = message['MessageAttributes'].get('FileS3').get('StringValue')
  download_file(s3uri)

  # Apaga mensagem recebida do SQS
  sqs.delete_message(
      QueueUrl=queue_url,
      ReceiptHandle=receipt_handle
  )
  print('Received and deleted message: %s' % message)

def GetFilePresignedUrl():
    myurl = myurlAPI
    resultData = requests.get(myurl)
    if resultData.status_code == 200:
        resultJson = json.loads(resultData.text)
        print(resultJson['presigned_url'])
        return resultJson
    else:
        print('Erro ao fazer requisição')

def UploadFileS3(url):
    payload = open("C:\\Users\\afern\\Downloads\\dadosCadastrais.pdf", 'rb')
    headers = {'Content-Type': 'application/pdf'}
    response = requests.request("PUT", url, headers=headers, data=payload)
    if response.status_code == 200:
        print('Upload feito com sucesso')
        return True
    else:
        print('Erro ao fazer upload')
        return False

def SendRequestOCr(payload):
    payload = { "urlS3": payload}
    response = requests.post(myurlAPI, json=payload)
    if response.status_code == 200:
        print(response.text)
        print('Solicitação para OCR feita com sucesso')
        return True
    else:
        print('Erro ao fazer solicitação para OCR')
        return False
