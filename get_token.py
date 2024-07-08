import base64
from requests import post, get
import json

def getToken():
    # gabungkan client_id dan client_secret
    auth_string = client_id + ':' + client_secret

    # encode ke base64
    auth_b64 = base64.b64encode(auth_string.encode('utf-8'))

    # url untuk mengambil token
    url = 'https://accounts.spotify.com/api/token'

    # header untuk mengambil token - sesuai dengan guide dari spotify
    headers = {
        'Authorization': 'Basic ' + auth_b64.decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # data untuk mengambil token - sesuai dengan guide dari spotify
    data = {'grant_type': 'client_credentials'}

    # kirim request POST ke spotify
    result = post(url, headers=headers, data=data)

    # parse response ke json
    json_result = json.loads(result.content)
    token = json_result['access_token']

    # ambil token untuk akses API
    return token

## panggil fungsi getToken() dibawah ini