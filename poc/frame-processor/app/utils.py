import requests


def get_image_embedding(data: bytes, api_url: str, api_key: str):
    resp = requests.post(
        api_url,
        headers={'Authorization': f'Bearer {api_key}'},
        files={'image': ('frame.jpg', data, 'image/jpeg')}
    )
    resp.raise_for_status()
    return resp.json().get('embedding', [])
