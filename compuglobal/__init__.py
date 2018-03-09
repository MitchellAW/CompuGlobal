from base64 import b64encode

import requests

from .errors import *
from .screencap import *


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
    def get_screencap(self, episode, timestamp):
        caption_url = self.caption_url.format(episode, timestamp)
        screen = requests.get(caption_url)
        if screen.status_code == 200:
            return Screencap(self, screen.json())

        else:
            raise APIPageStatusError(screen.status_code, self.URL)

    # Gets a random TV Show screencap (episode and timestamp)
    def get_random_screencap(self):
        screen = requests.get(self.random_url)
        if screen.status_code == 200:
            return Screencap(self, screen.json())

        else:
            raise APIPageStatusError(screen.status_code, self.URL)

    # Gets the first search result for a TV Show screencap using search_text
    def search_for_screencap(self, search_text):
        search_url = self.search_url + search_text.replace(' ', '+')

        search = requests.get(search_url)
        if search.status_code == 200:
            search_results = search.json()

            if len(search_results) > 0:
                result = search_results[0]
                return self.get_screencap(result['Episode'],
                                          result['Timestamp'])

            else:
                raise NoSearchResultsFound()

        else:
            raise APIPageStatusError(search.status_code, self.URL)

    # Gets all valid frames before and after timestamp for the episode
    def get_frames(self, episode, timestamp, before, after):
        frames_url = self.frames_url.format(episode, timestamp, before, after)
        frames = requests.get(frames_url)
        if frames.status_code == 200:
            return frames.json()

        else:
            raise APIPageStatusError(frames.status_code, self.URL)

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
    def generate_gif(self, gif_url):
        gif_loader = requests.get(gif_url)
        if gif_loader.status_code == 200:
            return gif_loader.url

        else:
            raise APIPageStatusError(gif_loader.status_code, self.URL)


# West Wing Meme/GIF generator API
class CapitalBeatUs(CompuGlobalAPI):
    def __init__(self):
        super().__init__('https://capitalbeat.us/', 'West Wing')


# Simpsons Meme/GIF generator API
class Frinkiac(CompuGlobalAPI):
    def __init__(self):
        super().__init__('https://frinkiac.com/', 'The Simpsons')


# Steamed Hams Meme/GIF generator API
class FrinkiHams(CompuGlobalAPI):
    def __init__(self):
        super().__init__('https://frinkihams.com/', 'Steamed Hams')


# 30 Rock Meme/GIF generator API
class GoodGodLemon(CompuGlobalAPI):
    def __init__(self):
        super().__init__('https://goodgodlemon.com/', '30 Rock')


# Rick and Morty Meme/GIF generator API
class MasterOfAllScience(CompuGlobalAPI):
    def __init__(self):
        super().__init__('https://masterofallscience.com/', 'Rick and Morty')


# Futurama Meme/GIF generator API
class Morbotron(CompuGlobalAPI):
    def __init__(self):
        super().__init__('https://morbotron.com/', 'Futurama')
