import datetime
from functools import reduce

import isodate
from googleapiclient.discovery import build

api_key: str = 'AIzaSyB3JSCvV10iguNkmZwoe-Uornw8YwIzMvQ'


class PlayList:
    def __init__(self, playlist_id: str) -> None:
        self.playlist_id = playlist_id

        self.playlist_video = PlayList.get_service().playlistItems().list(playlistId=playlist_id,
                                                                          part='contentDetails, snippet',
                                                                          maxResults=50
                                                                          ).execute()

        self.title = str(self.playlist_video['items'][0]['snippet']['title'])
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_video['items']]
        self.video_response = PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                              id=','.join(self.video_ids)
                                                              ).execute()



    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @property
    def total_duration(self):
        my_sum = datetime.timedelta()
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            my_sum += duration
        return my_sum


    def show_best_video(self):
        #ls = []
        for video_id in self.video_ids:
            a = PlayList.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                     id=video_id
                                                     ).execute()
            like_count = a['items'][0]['statistics']['likeCount']
            #ls.append(like_count)

            if int(like_count) > 130000:
                return f'https://youtu.be/{video_id}'



#pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
#print(pl.title)
#print(pl.total_duration)
#print(pl.show_best_video())
#print(pl.video_ids)

