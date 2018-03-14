import asyncio
from base64 import b64encode

import aiohttp

from .errors import *
from .screencap import Screencap


__title__ = 'compuglobal'
__author__ = 'MitchellAW'
__license__ = 'MIT'
__version__ = '1.1.0'


# API Used for getting all TV Show screencaps
class CompuGlobalAPI:
    def __init__(self, url, title, timeout):
        self.URL = url
        self.title = title
        # Time to wait on timeouts for each request
        self.timeout = timeout

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
        async with aiohttp.ClientSession() as cs:
            async with cs.get(caption_url, timeout=self.timeout) as screen:
                if screen.status == 200:
                    return Screencap(self, await screen.json())

                else:
                    raise APIPageStatusError(screen.status, self.URL)

    # Gets a random TV Show screencap (episode and timestamp)
    async def get_random_screencap(self):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(self.random_url, timeout=self.timeout) as screen:
                if screen.status == 200:
                    return Screencap(self, await screen.json())

                else:
                    raise APIPageStatusError(screen.status, self.URL)

    # Gets the first search result for a TV Show screencap using search_text
    # Raises NoSearchResultsFound exception if no search results are found
    async def search_for_screencap(self, search_text):
        search_url = self.search_url + search_text.replace(' ', '+')

        async with aiohttp.ClientSession() as cs:
            async with cs.get(search_url, timeout=self.timeout) as search:
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
        async with aiohttp.ClientSession() as cs:
            async with cs.get(frames_url, timeout=self.timeout) as frames:
                if frames.status == 200:
                    return await frames.json()

                else:
                    raise APIPageStatusError(frames.status, self.URL)

    # Loop through all words of the subtitles, add them to the caption and then
    # return the caption encoded in base64 for use in the url
    def encode_caption(self, caption, max_lines=4, max_chars=24, shorten=True):
        char_count = 0
        line_count = 0
        formatted_caption = ''

        # Loop through and format to suit max_lines and max_chars per line
        for word in caption.split():
            char_count += len(word) + 1

            if char_count < max_chars and line_count < max_lines:
                formatted_caption += ' ' + word

            elif line_count < max_lines:
                char_count = len(word) + 1
                line_count += 1
                if line_count < max_lines:
                    formatted_caption += '\n' + ' ' + word

        # Shorten caption at end of sentences if set to True
        caption = formatted_caption
        if shorten:
            caption = self.shorten_caption(formatted_caption)
        encoded = b64encode(str.encode(caption, 'utf-8'), altchars=b'__')

        return encoded.decode('utf-8')

    # Favours ending the caption at the latest sentence ending (., !, ?)
    @staticmethod
    def shorten_caption(caption):
        for i in range(len(caption) - 1, 0, -1):
            if caption[i] == '.' or caption[i] == '!' or caption[i] == '?':
                return caption[:i + 1]

            elif caption[i] == '♪':
                return caption[:i]

        return caption

    # Take caption json file and convert it to the caption for encoding
    @staticmethod
    def json_to_caption(cartoon_json):
        caption = ''
        for quote in cartoon_json['Subtitles']:
            caption += quote['Content'] + ' '

        return caption

    # Generate the gif and get the direct url for embedding, returns original
    #  gif_url if it times out
    async def generate_gif(self, gif_url):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(gif_url, timeout=self.timeout) as gif_loader:
                    if gif_loader.status == 200:
                        return gif_loader.url

                    else:
                        raise APIPageStatusError(gif_loader.status, self.URL)

        except asyncio.TimeoutError:
            return gif_url


# West Wing Meme/GIF generator API
class CapitalBeatUs(CompuGlobalAPI):
    def __init__(self, timeout=15):
        super().__init__('https://capitalbeat.us/', 'West Wing', timeout)


# Simpsons Meme/GIF generator API
class Frinkiac(CompuGlobalAPI):
    def __init__(self, timeout=15):
        super().__init__('https://frinkiac.com/', 'The Simpsons', timeout)


# Steamed Hams Meme/GIF generator API
class FrinkiHams(CompuGlobalAPI):
    def __init__(self, timeout=15):
        super().__init__('https://frinkihams.com/', 'Steamed Hams', timeout)


# 30 Rock Meme/GIF generator API
class GoodGodLemon(CompuGlobalAPI):
    def __init__(self, timeout=15):
        super().__init__('https://goodgodlemon.com/', '30 Rock', timeout)


# Rick and Morty Meme/GIF generator API
class MasterOfAllScience(CompuGlobalAPI):
    def __init__(self, timeout=15):
        super().__init__('https://masterofallscience.com/', 'Rick and Morty',
                         timeout)


# Futurama Meme/GIF generator API
class Morbotron(CompuGlobalAPI):
    def __init__(self, timeout=15):
        super().__init__('https://morbotron.com/', 'Futurama', timeout)
