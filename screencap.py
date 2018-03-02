

# A screencap of a TV Show (episode and timestamp) generated using
# CompuGlobalAPI
class Screencap:
    def __init__(self, api, json: dict):
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
    def get_gif_url(self, caption=None, before=3000, after=4000):
        if caption is None:
            caption = self.caption

        b64_caption = self.api.encode_caption(caption)

        # Get start and end frame numbers for gif
        frames = self.api.get_frames(self.key, self.timestamp,
                                     int(before), int(after))
        start = frames[0]['Timestamp']
        end = frames[-1]['Timestamp']
        return self.gif_url.format(self.key, start, end, b64_caption)
