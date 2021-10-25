# AWS Demo
![image](https://user-images.githubusercontent.com/19678590/138619405-2f45c29c-139d-4745-9b32-de83fb39d668.png)

Passo1 - Faz uma requisição Get no API. Como resposta será retornado as informações para upload do arquivo
Ex:
```json
{
    "bucketName": "testeorb-menssageria",
    "key": "queue-ocr/a51fa98e043642d5aec1d9dc96881e1b",
    "filename_after_upload": "s3://testeorb-menssageriaqueue-ocr/queue-ocr/a51fa98e043642d5aec1d9dc96881e1b",
    "presigned_url": "https://testeorb-menssageria.s3.amazonaws.com/queue-ocr/a51fa98e043642d5aec1d9dc96881e1b?AWSAccessKeyId=ASIASU3CHBWSA6WESJ2A&Signature=fXx84h3vFp7nYbWlmoKu4xVAOfM%3D&content-type=application%2Fpdf&x-amz-security-token=IQoJb3JpZ2luX2VjELf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXNhLWVhc3QtMSJHMEUCIHZOUYNNNNXrwEpL96A4ZhEy4TcbunsQ7rU7EbEw8c9aAiEA80PFVP3k2IZb7fj3TdVtgFsfsn8qUgsUPOq%2B4Ahs%2BjUqkAIIUBAAGgwxODIyMDUyMjIzMDgiDGjky4h5VhMD%2F5bCgCrtAcTXK9iiL7bDncLfSfheueGW1faHnkp2aD5cCaAaDH18D7JbJbMGinupWaz8dIe0SwbHy8DVRVuTPPuQUEixL7BFzkojgRVtTJypjCAL%2FV2F4Ekd%2B2zXqF6hM8XRqUvP1wu41w%2BFo0z19ognYl6Yyl5kvSXFgmQ24ICgadnu3gyV%2B57kZiZB4SnUTfbGZjzvnuUvyo9gY%2F3NQJ376%2FTEQJws%2FORzqiV%2BLnsqj8kGfy4spWwGIOUrCkb8va9VfT9mR0guKiD1zRTd%2BugXVVq6hfoPqQ%2BE917L%2FQchFozIxAUVE%2BCL1bX7zmG822ttvDCCv9eLBjqaAZzYj0NadTf4yX%2BK7UwW3bX5va32PY1L53AeVlX3R4QQgMCE4hxxrLsl4aHlSHT7dtd9reojuoJ0wzU9NH5Bf3nZ9Yqek%2FnTOyj7113YA9Ypvs18bfatlMKlxEYV2x%2FsRKGur4wKpIwCWK6mcALt9xiv%2BYd%2BghNkkX5ZMhEQ5Rd5dcO2IIdzJXQUEcWFszI3lUAVUyPGbvBBnuQ%3D&Expires=1635118482"
}

```

Passo2 - Com a URL retorna no passo, basta enviar o arquivo para no payload. Se a chamada retornar 200 significa que deu tudo certo.
```python
def UploadFileS3(url):
    payload = open("X:\\...\\nomeArquivo.pdf", 'rb')
    headers = {'Content-Type': 'application/pdf'}
    response = requests.request("PUT", url, headers=headers, data=payload)
    if response.status_code == 200:
        print('Upload feito com sucesso')
        return True
    else:
        print('Erro ao fazer upload')
        return False
```

Passo 3 - Após o envio do arquivos para o S3, basta enviar para o metodo que atualmente recebe o body o parametro "filename_after_upload" ao invés do arquivos em base64.

```python
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
 ```


