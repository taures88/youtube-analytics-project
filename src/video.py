from googleapiclient.discovery import build

api_key: str = 'AIzaSyB3JSCvV10iguNkmZwoe-Uornw8YwIzMvQ'


class Video:

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        video_response = Video.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                           id=video_id
                                                           ).execute()

        self.video_title = str(video_response['items'][0]['snippet']['title'])
        self.url_video = f'https://www.youtube.com/watch?v={video_id}'
        self.view_count = int(video_response['items'][0]['statistics']['viewCount'])
        self.like_count = int(video_response['items'][0]['statistics']['likeCount'])

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
