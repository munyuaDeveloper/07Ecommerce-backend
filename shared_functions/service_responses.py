from django.conf import settings
import requests


class ServiceResponseManager:
    def __init__(self):
        self.service_urls = settings.SERVICE_URLS
        self.shared_service = self.service_urls['shared_service']

    def get_image_urls(self, payload):
        url = self.shared_service + 'fileupload/list-image'
        try:
            image_params = {
                "image": payload
            }
            response = requests.get(url, params=image_params)
            if response.status_code == 200:
                data = response.json()
                return data['results']
        except Exception as e:
            print(e)
            return []