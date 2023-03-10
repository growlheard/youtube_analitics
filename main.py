import os
import json
from abc import abstractmethod
import datetime
import isodate

from googleapiclient.discovery import build


class MixinSupport:
    def __init__(self):
        self.api_key: str = os.environ.get('API_KEY')  # Получаем ключ API из переменной окружения

    @staticmethod
    def get_service():
        """
        возвращает объект для работы с API ютуба
        """
        api_key: str = os.environ.get('API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    @abstractmethod
    def __repr__(self):
        pass


class Youtube(MixinSupport):
    """
   Работа с API Youtube
    """

    def __init__(self, channel_id):
        super().__init__()
        self._channel_id = channel_id
        youtube = Youtube.get_service()  # сервис youtube
        self.channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()  # инфо о канале
        self._channel_id = self.channel['items'][0]['id']  # id канала
        self.channel_title = self.channel['items'][0]['snippet']['title']  # название канала
        self.channel_description = self.channel['items'][0]['snippet']['description']  # описание канала
        self.channel_url = f'https://www.youtube.com/channel/{self.channel_id}' # ссыдка на канал
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


class Video(MixinSupport):
    def __init__(self, video_id):
        super().__init__()
        self._video_id = video_id
        youtube_service = Video.get_service()
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


class Playlist(MixinSupport):
    def __init__(self, id_playlist):
        super().__init__()
        self.id_playlist = id_playlist
        self.playlist_data = self.get_service().playlists().list(id=self.id_playlist, part='snippet, contentDetails',
                                                                 maxResults=50).execute()
        self.playlist_info = json.dumps(self.playlist_data, indent=4)
        self._playlist_title = self.playlist_data['items'][0]['snippet']['title']
        self._playlist_url = f"https://www.youtube.com/playlist?list={self.id_playlist}"
        self._playlist_videos = self.get_service().playlistItems().list(playlistId=self.id_playlist,
                                                                        part='contentDetails').execute()
        self.playlist_video_info = json.dumps(self._playlist_videos, indent=4)
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self._playlist_videos['items']]
        self.video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                               id=','.join(self.video_ids)).execute()

    def __repr__(self):
        return f"PlayList({self.id_playlist})"

    @property
    def playlist_title(self) -> str:
        """
        Название плэйлиста
        """
        return self._playlist_title

    @property
    def playlist_url(self) -> str:
        """
         URL плэйлиста
        """
        return self._playlist_url

    def print_info_playlist_videos(self) -> json:
        """
         Информация о видео в плэйлисте
        """
        print(json.dumps(self._playlist_videos, indent=2, ensure_ascii=False))

    @property
    def total_duration(self):
        """
        Суммарноя длительность плейлиста
        """
        duration = datetime.timedelta(0)

        for video in self.video_response['items']:
            iso_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_duration)

        return duration

    def show_best_video(self):
        """
        Самое поулярное видео(максимум лайков)
        """
        videos = {}
        for i in range(len(self.video_ids)):
            videos[int(self.video_response['items'][i]['statistics']['likeCount'])] = self.video_ids[i]

        return f"https://www.youtube.com/watch?v={videos[max(videos)]}"
