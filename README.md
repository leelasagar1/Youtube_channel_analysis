# Project Title: YouTube Channel Data Analysis

This project is designed to get data from famous Data Science YouTube channels and perform exploratory data analysis on the collected information. The script utilizes the YouTube Data API to fetch channel statistics, video details, and playlist information.

## Description

This project allows users to gather data from multiple YouTube channels and analyze it for further insights. The script provides functions to scrape channel IDs, retrieve channel statistics, fetch video IDs from playlists, and obtain video details such as views, likes, and comments.

## Installation

To use the YouTube Channel Data Scraper, follow the steps below:

1. Clone the GitHub repository to your local machine.
2. Ensure that you have Python 3.x installed.
3. Install the required Python packages by running the following command:

```shell
pip install -r requirements.txt
```

4. Obtain a YouTube Data API key by following the official documentation: [YouTube Data API](https://developers.google.com/youtube/v3/getting-started).
5. Add your API key to the `config.yaml` file under the `api_key` field.

## Usage

To run the YouTube Channel Data Scraper , execute the following command:

```shell
python script/get_data.py
```

The script will perform the following steps:

1. Read the configuration from the `config.yaml` file.
2. Configure the YouTube Data API using the provided API key.
3. Fetch the channel IDs for the specified YouTube channels.
4. Retrieve the channel statistics (such as subscribers, views, and total videos) for the identified channels.
5. Fetch video IDs from the playlists of the channels.
6. Obtain video details (including views, likes, and comments) for the collected video IDs.
7. Build a dataset with the scraped information.
8. Save the dataset as a CSV file in the specified data folder.

## Exploratory Data Analysis

The second part of the project involves performing exploratory data analysis (EDA) on the collected YouTube channel and video data. This phase allows you to gain insights into the channels' performance and understand the engagement of the audience.

EDA includes following analyses and visualizations:

- Distribution of subscribers, views, and likes across channels.
- Correlation between subscribers, views,likes and comments.
- Trend analysis of views and likes over time.
- Most popular video topics based on tags and categories.

