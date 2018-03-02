from base64 import b64encode

import aiohttp

from errors import APIPageStatusError
from errors import NoSearchResultsFound


# API Used for getting all TV Show screencaps
class CompuGlobalAPI:
    def __init__(self, url, title):
        self.URL = url
        self.title = title

        # Gets random screencap with caption info
        self.random_url = self.URL + 'api/random'

        # Gets caption using episode and timestamp (e = episode, t = timestamp)
        self.caption_url = self.URL + 'api/caption?e={}&t={}'

        # Searches for screencap (q = search query)
        self.search_url = self.URL + 'api/search?q='

        # Gets frames before & after timestamp (episode/timestamp/before/after)
        self.frames_url = self.URL + 'api/frames/{}/{}/{}/{}'

        # Gets all frames nearby (e = episode, t = timestamp)
        self.nearby_url = self.URL + 'api/nearby?e={}&t={}'

        # Gets episode info and subtitles from start to end (episode/start/end)
        self.episode_url = self.URL + 'api/episode/{}/{}/{}'

    # Gets a TV Show screencap using episode and timestamp
    async def get_screencap(self, episode, timestamp):
        caption_url = self.caption_url.format(episode, timestamp)
        async with aiohttp.ClientSession() as session:
            async with session.get(caption_url) as screencap:
                if screencap.status == 200:
                    return Screencap(self, await screencap.json())

                else:
                    raise APIPageStatusError(screencap.status, self.URL)

    # Gets a random TV Show screencap (episode and timestamp)
    async def get_random_screencap(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.random_url) as screencap:

                if screencap.status == 200:
                    return Screencap(self, await screencap.json())

                else:
                    raise APIPageStatusError(screencap.status, self.URL)

    # Gets the first search result for a TV Show screencap using search_text
    async def search_for_screencap(self, search_text):
        search_url = self.search_url + search_text.replace(' ', '+')

        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as search:
                if search.status == 200:
                    search_results = await search.json()

                    if len(search_results) > 0:
                        result = search_results[0]
                        return await self.get_screencap(result['Episode'],
                                                        result['Timestamp'])

                    else:
                        raise NoSearchResultsFound()

                else:
                    raise APIPageStatusError(search.status, self.URL)

    # Gets all valid frames before and after timestamp for the episode
    async def get_frames(self, episode, timestamp, before, after):
        frames_url = self.frames_url.format(episode, timestamp, before, after)
        async with aiohttp.ClientSession() as session:
            async with session.get(frames_url) as frames:
                if frames.status == 200:
                    return await frames.json()

                else:
                    raise APIPageStatusError(frames.status, self.URL)

    # Loop through all words of the subtitles, add them to the caption and then
    # return the caption encoded in base64 for use in the url
    def encode_caption(self, caption):
        char_count = 0
        line_count = 0
        formatted_caption = ''

        for word in caption.split():
            char_count += len(word) + 1

            if char_count < 24 and line_count < 4:
                formatted_caption += ' ' + word

            elif line_count < 4:
                char_count = len(word) + 1
                line_count += 1
                if line_count < 4:
                    formatted_caption += '\n' + ' ' + word

        caption = self.shorten_caption(formatted_caption)
        encoded = b64encode(str.encode(caption, 'utf-8'), altchars=b'__')

        return encoded.decode('utf-8')

    # Favours ending the caption at the latest sentence ending (., !, ?)
    @staticmethod
    def shorten_caption(caption):
        for i in range(len(caption) - 1, 0, -1):
            if caption[i] == '.' or caption[i] == '!' or caption[i] == '?':
                return caption[:i + 1]

        return caption

    # Take caption json file and convert it to the caption for encoding
    @staticmethod
    def json_to_caption(cartoon_json):
        caption = ''
        for quote in cartoon_json['Subtitles']:
            caption += quote['Content'] + ' '

        return caption

    # Generate the gif and get the direct url for embedding
    async def generate_gif(self, gif_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(gif_url) as gif_generator:
                if gif_generator.status == 200:
                    return gif_generator.url

                else:
                    raise APIPageStatusError(gif_generator.status, self.URL)


# Simpsons Meme/GIF generator API
class Frinkiac(CompuGlobalAPI):
    def __init__(self):
        super().__init__('https://frinkiac.com/', 'The Simpsons')


# Futurama Meme/GIF generator API
class Morbotron(CompuGlobalAPI):
    def __init__(self):
        super().__init__('https://morbotron.com/', 'Futurama')


# Rick and Morty Meme/GIF generator API
class MasterOfAllScience(CompuGlobalAPI):
    def __init__(self):
        super().__init__('https://masterofallscience.com/', 'Rick and Morty')


# 30 Rock Meme/GIF generator API
class GoodGodLemon(CompuGlobalAPI):
    def __init__(self):
        super().__init__('https://goodgodlemon.com/', '30 Rock')


# West Wing Meme/GIF generator API
class CapitalBeatUs(CompuGlobalAPI):
    def __init__(self):
        super().__init__('https://capitalbeat.us/', 'West Wing')


# Steamed Hams Meme/GIF generator API
class FrinkiHams(CompuGlobalAPI):
    def __init__(self):
        super().__init__('https://frinkihams.com/', 'Steamed Hams')


# A screencap of a TV Show (episode and timestamp) generated using
# CompuGlobalAPI
class Screencap:
    def __init__(self, api: CompuGlobalAPI, json: dict):
        self.api = api
        self.json = json

        # Inititalise Episode Information, setting title, director, writer
        # and wiki url to None if they are empty
        self.key = self.json['Episode']['Key']
        self.episode = self.json['Episode']['EpisodeNumber']
        self.season = self.json['Episode']['Season']
        self.title = self.get_value(self.json['Episode']['Title'])
        self.director = self.get_value(self.json['Episode']['Director'])
        self.writer = self.get_value(self.json['Episode']['Writer'])
        self.air_date = self.json['Episode']['OriginalAirDate']
        self.wiki_url = self.get_value(self.json['Episode']['WikiLink'])
        self.timestamp = self.json['Frame']['Timestamp']

        # Initalise caption and urls
        self.caption = self.api.json_to_caption(self.json)
        self.image_url = self.api.URL + 'img/{}/{}.jpg'
        self.meme_url = self.api.URL + 'meme/{}/{}.jpg?b64lines={}'
        self.gif_url = self.api.URL + 'gif/{}/{}/{}.gif?b64lines={}'
        self.mp4_url = self.api.URL + 'mp4/{}/{}/{}.mp4?b64lines={}'

    # Returns none if empty string
    @staticmethod
    def get_value(value):
        if value == '':
            return None

        else:
            return value.replace('\n', '')

    # Gets a readable timestamp for the screencap in format (mm:ss)
    def get_real_timestamp(self):
        seconds = int(self.timestamp / 1000)
        minutes = int(seconds / 60)
        seconds -= int(minutes * 60)
        return '{}:{:02d}'.format(minutes, seconds)

    # Gets the direct image url for the screencap without any caption
    def get_image_url(self):
        return self.image_url.format(self.key, self.timestamp)

    # Gets the meme url for the screencap captioned with subtitles
    def get_meme_url(self, caption=None):
        if caption is None:
            caption = self.caption

        b64_caption = self.api.encode_caption(caption)
        return self.meme_url.format(self.key, self.timestamp, b64_caption)

    # Gets the gif url for the screencap captioned with subtitles, defaults gif
    # length to < ~7000ms, before + after must not exceed 10,000ms (10 sec.)
    async def get_gif_url(self, caption=None, before=3000, after=4000):
        if caption is None:
            caption = self.caption

        b64_caption = self.api.encode_caption(caption)

        # Get start and end frame numbers for gif
        frames = await self.api.get_frames(self.key, self.timestamp,
                                           int(before), int(after))
        start = frames[0]['Timestamp']
        end = frames[-1]['Timestamp']
        return self.gif_url.format(self.key, start, end, b64_caption)
