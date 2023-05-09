import os
from googleapiclient.discovery import build
import json

api_key: str = 'AIzaSyB3JSCvV10iguNkmZwoe-Uornw8YwIzMvQ'


class Channel:
    """Класс для ютуб-канала"""

    """ выводим название_канала  ссылку_на_канал"""

    def __str__(self):
        return f"{self.title} ({self.url})"

    """метод сложения"""

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    """метод вычитания"""

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    """метод сравнения меньше"""

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    """метод сравнения меньше или равно"""

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    """метод сравнения больше"""

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    """метод сравнения больше или равно"""

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.service = Channel.get_service()
        self.channel = self.service.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.url = f'https://www.youtube.com/channel/{channel_id}'
        self.title = self.channel['items'][0]['snippet']['title']
        self.subscriber_count = int(self.channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(self.channel['items'][0]['statistics']['videoCount'])
        self.view_count = int(self.channel['items'][0]['statistics']['viewCount'])

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, name_json: str):
        with open(name_json, 'w') as file:
            json.dump(self.channel, file, indent=4)
