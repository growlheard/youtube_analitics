import os
import json

from googleapiclient.discovery import build


class Youtube:
    """
   Работа с API Youtube
    """
    def __init__(self, channel_id):
        self._channel_id = channel_id

        api_key: str = os.environ.get('API_KEY')  # Получаем ключ API из переменной окружения
        youtube = build('youtube', 'v3', developerKey=api_key)  # сервис youtube
        self.channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()  # инфо о канале

        # Инициализация атрибутов класса
        self._channel_id = self.channel['items'][0]['id']  # id канала
        self.channel_title = self.channel['items'][0]['snippet']['title']  # название канала
        self.channel_description = self.channel['items'][0]['snippet']['description']  # описание канала
        self.subscriber_count = int(self.channel['items'][0]['statistics']['subscriberCount'])  # количество подписчиков
        self.video_count = int(self.channel['items'][0]['statistics']['videoCount'])  # количество видео
        self.view_count = int(self.channel['items'][0]['statistics']['viewCount'])  # общее количество просмотров

    def print_info(self):
        """
         Выводим информацию о канале на консоль
         """
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))


