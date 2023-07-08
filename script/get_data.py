from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import yaml


def scrape_channel_id(channel):
    """Gets the channel ID for a given YouTube channel name."""

    url = f"https://www.youtube.com/@{channel}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    channel_id = soup.find("meta", property="og:url")["content"].split("/")[4]
    return channel_id


def get_channel_ids(channels):
    """Gets the channel IDs for a list of YouTube channels."""
    channel_ids = []
    for channel in channels:
        channel_id = scrape_channel_id(channel)
        channel_ids.append(channel_id)
    return channel_ids


def get_channel_stats(youtube, channel_ids):
    """Gets the channel statistics for a list of YouTube channels."""
    final_data = []

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=",".join(channel_ids))

    response = request.execute()

    for item in response['items']:
        data = {'channel_name': item['snippet']['title'],
                'subscribers': item['statistics']['subscriberCount'],
                'views': item['statistics']['viewCount'],
                'total_videos': item['statistics']['videoCount'],
                'playlist_id': item['contentDetails']['relatedPlaylists']['uploads'],
                # 'country': item['snippet']['country']

                }
        final_data.append(data)
    return pd.DataFrame(final_data)


def get_video_ids(youtube, playlist_id):
    """Gets the video IDs for a YouTube playlist."""
    request = youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=playlist_id, maxResults=50
    )
    response = request.execute()

    video_ids = []
    for item in response['items']:

        video_ids.append(item['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')

    while next_page_token is not None:
        request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id, maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response['items']:

            video_ids.append(item['contentDetails']['videoId'])
        next_page_token = response.get('nextPageToken')
    return video_ids


def get_video_details(youtube, video_ids):
    """Gets the video details for a list of YouTube video IDs."""

    all_video_info = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()

        for video in response['items']:

            stats = {'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                     'statistics': ['viewCount', 'likeCount', 'favouriteCount', 'commentCount'],
                     'contentDetails': ['duration', 'definition', 'caption']
                     }
            video_info = {}
            video_info['video_id'] = video['id']

            for k in stats.keys():
                for v in stats[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            all_video_info.append(video_info)

    return pd.DataFrame(all_video_info)


def build_dataset(youtube, channel_df):
    """ This function builds a dataset of videos information from a list of channel ids."""

    data = pd.DataFrame()
    for i in channel_df.index:
        playlist_id = channel_df.loc[i, 'playlist_id']

        video_ids = get_video_ids(youtube, playlist_id)
        video_data = get_video_details(youtube, video_ids)

        data = pd.concat([data, video_data], ignore_index=True, axis=0)

    return pd.DataFrame(data)


def save_data(df,yaml_data):
    """This function saves the data as csv file"""
    data_folder = yaml_data['data_folder']
    file_name = yaml_data['file_name']
    os.makedirs('data', exist_ok=True)
    df.to_csv(os.path.join(data_folder,file_name), index=False)

def read_yaml(file_name):
    """
    This function reads a YAML file and returns the contents as a Python dictionary.

    """

    with open(file_name, 'r') as file:
        yaml_data = yaml.safe_load(file)

    return yaml_data

def config_youtube_api(yaml_data):

    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    api_service_name = "youtube"
    api_version = "v3"
    api_key = yaml_data['api_key']
    youtube = build(api_service_name, api_version, developerKey=api_key)
    return youtube

def run():

    file_name = 'config.yaml'
    yaml_data = read_yaml(file_name)

    youtube = config_youtube_api(yaml_data)
    print('Fetching Channel IDs ..................')
    channels = ["krishnaik06", 'sentdex', 'andreaskayy', 'DataProfessor', 'statquest', 'dataschool',
                'RVideoTutorials', 'DataScienceAcademy', 'KenJee_ds', 'GregHogg', 'Thuvu5', 'emma_ding', 'SundasKhalid']
    channel_ids = get_channel_ids(channels)
    print('Channel IDs fetched successfully...................')
    print('Fetching Channel stats ................')
    df = get_channel_stats(youtube=youtube, channel_ids=channel_ids)
    print('Channels stats fetched successfully .....')
    print('Fetching data and Building dataset .............')
    video_df = build_dataset(youtube, df)

    save_data(video_df,yaml_data)
    print('Dataset saved')


if __name__ == "__main__":

    run()
