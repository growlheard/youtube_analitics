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
        self.channel_url = 'https://www.youtube.com/channel/' + self.channel_id  # ссыдка на канал
        self.subscriber_count = int(self.channel['items'][0]['statistics']['subscriberCount'])  # количество подписчиков
        self.video_count = int(self.channel['items'][0]['statistics']['videoCount'])  # количество видео
        self.view_count = int(self.channel['items'][0]['statistics']['viewCount'])  # общее количество просмотров

    def print_info(self):
        """
        Выводим информацию о канале на консоль
        """
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        """
        Получение ссылки на канал
        """
        return self._channel_id

    @staticmethod
    def get_service():
        """
        возвращает объект для работы с API ютуба
        """
        api_key: str = os.environ.get('API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename):
        """
        сохраняет информацию по каналу, хранящуюся в атрибутах экземпляра класса Youtube, в json-файл
        """
        with open(filename, "w", encoding='utf-8') as file:
            json.dump({
                "channel_id": self._channel_id,
                "channel_title": self.channel_title,
                "channel_description": self.channel_description,
                "channel_link": self.channel_url,
                "subscriber_count": self.subscriber_count,
                "video_count": self.video_count,
                "view_count": self.view_count
            }, file, indent=2, ensure_ascii=False)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._channel_id}')"

    def __str__(self):
        return f'YouTube-канал: {self.channel_title}'

    def __add__(self, other):
        """
        Сложение количества подписчиков каналов
        """
        if isinstance(other, Youtube):
            return self.subscriber_count + other.subscriber_count

    def __gt__(self, other):
        """
        Сравнивает количества подписчиков каналов
        """
        if isinstance(other, Youtube):
            return self.subscriber_count > other.subscriber_count


class Video:
    def __init__(self, video_id):
        self._video_id = video_id

        youtube_service = Youtube.get_service()
        self.video = youtube_service.videos().list(id=video_id, part='snippet,statistics').execute()

        self.video_title = self.video['items'][0]['snippet']['title']
        self.video_views = int(self.video['items'][0]['statistics']['viewCount'])
        self.video_likes = int(self.video['items'][0]['statistics']['likeCount'])

    @property
    def video_id(self):
        """
        Возвращает id видео
        """
        return self.video_id

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._video_id}')"

    def __str__(self):
        return f'{self.video_title}'

    def video_info(self):
        """
        Выводим информацию о видео на консоль
        """
        print(json.dumps(self.video, indent=2, ensure_ascii=False))


class PLVideo(Video):
    def __init__(self, video_id, video_playlist):
        super().__init__(video_id)
        self.video_playlist = video_playlist

        youtube = Youtube.get_service()
        self.playlist = youtube.playlists().list(id=self.video_playlist, part='snippet').execute()
        self.playlist_title = self.playlist['items'][0]['snippet']['title']

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._video_id}', '{self.video_playlist}')"

    def __str__(self):
        return f"{super().__str__()} ({self.playlist_title})"

    def info_playlist(self):
        """
        Выводим информацию о плэйлисте в консоль
        """
        print(json.dumps(self.playlist, indent=2, ensure_ascii=False))
