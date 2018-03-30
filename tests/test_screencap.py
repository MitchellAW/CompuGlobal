import json
import unittest

import compuglobal

FRINKIAC = compuglobal.Frinkiac()

with open('frinkiac.json') as frinkiac:
    frinkiac_data = json.load(frinkiac)


class ScreencapTestCase(unittest.TestCase):
    """Tests for `screencap.py`."""
    def test_screencap_attributes(self):
        """Check attributes of Screencap"""

        data = frinkiac_data['test_1']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.frame.id, 1503125)
        self.assertEqual(screen.key, 'S11E10')
        self.assertEqual(screen.episode, 10)
        self.assertEqual(screen.season, 11)
        self.assertEqual(screen.title, 'Little Big Mom')
        self.assertEqual(screen.director, 'Mark Kirkland')
        self.assertEqual(screen.writer, 'Carolyn Omine')
        self.assertEqual(screen.air_date, '9-Jan-00')
        self.assertEqual(screen.wiki_url,
                         'https://en.wikipedia.org/wiki/Little_Big_Mom')
        self.assertEqual(screen.timestamp, 339960)
        self.assertEqual(screen.caption,
                         '( yells) STUPID, SEXY FLANDERS! OW, MY LEGS! THIS '
                         'IS THE WORST PAIN EVER... ')
        self.assertEqual(screen.frame.image_url,
                         'https://frinkiac.com/img/S11E10/339960.jpg')
        self.assertEqual(screen.gif_url,
                         'https://frinkiac.com/gif/{}/{}/{}.gif?b64lines={}')
        self.assertEqual(screen.mp4_url,
                         'https://frinkiac.com/mp4/{}/{}/{}.mp4?b64lines={}')

    def test_simpsons_image_url(self):
        """Tests frinkiac image url"""

        data = frinkiac_data['test_1']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.get_image_url(),
                         'https://frinkiac.com/img/S11E10/339960.jpg')

        data = frinkiac_data['test_2']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.get_image_url(),
                         'https://frinkiac.com/img/S17E20/1082039.jpg')

        data = frinkiac_data['test_3']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.get_image_url(),
                         'https://frinkiac.com/img/S07E06/530579.jpg')

    def test_simpsons_meme_url(self):
        """Tests frinkiac meme url"""

        data = frinkiac_data['test_1']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.get_meme_url(),
                         'https://frinkiac.com/meme/S11E10/339960.jpg'
                         '?b64lines=ICggeWVsbHMpIFNUVVBJRCwgU0VYWQogRkxBTkRFUl'
                         'MhIE9XLCBNWSBMRUdTIQogVEhJUyBJUyBUSEUgV09SU1QgUEFJTg'
                         'ogRVZFUi4uLg==')

        data = frinkiac_data['test_2']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.get_meme_url('stupid sexy flanders'),
                         'https://frinkiac.com/meme/S17E20/1082039.jpg'
                         '?b64lines=IHN0dXBpZCBzZXh5IGZsYW5kZXJz')

        data = frinkiac_data['test_3']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.get_meme_url(),
                         'https://frinkiac.com/meme/S07E06/530579.jpg'
                         '?b64lines=IE1vcmlzOnlvdSBkaWUu')

    def test_simpsons_get_gif_url(self):
        """Tests frinkiac gif urls"""

        data = frinkiac_data['test_1']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.get_gif_url(),
                         'https://frinkiac.com/gif/S11E10/336960/343960.gif'
                         '?b64lines=ICggeWVsbHMpIFNUVVBJRCwgU0VYWQogRkxBTkRFUl'
                         'MhIE9XLCBNWSBMRUdTIQogVEhJUyBJUyBUSEUgV09SU1QgUEFJTg'
                         'ogRVZFUi4uLg==')
        self.assertEqual(screen.get_gif_url(caption='Stupid Sexy Flanders'),
                         'https://frinkiac.com/gif/S11E10/336960/343960.gif'
                         '?b64lines=IFN0dXBpZCBTZXh5IEZsYW5kZXJz')
        self.assertEqual(screen.get_gif_url(before=1000, after=1000),
                         'https://frinkiac.com/gif/S11E10/338960/340960.gif'
                         '?b64lines=ICggeWVsbHMpIFNUVVBJRCwgU0VYWQogRkxBTkRFUl'
                         'MhIE9XLCBNWSBMRUdTIQogVEhJUyBJUyBUSEUgV09SU1QgUEFJTg'
                         'ogRVZFUi4uLg==')

    def test_simpsons_get_mp4_url(self):
        """Tests frinkiac mp4 urls"""

        data = frinkiac_data['test_1']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.get_mp4_url(),
                         'https://frinkiac.com/mp4/S11E10/336960/343960.mp4'
                         '?b64lines=ICggeWVsbHMpIFNUVVBJRCwgU0VYWQogRkxBTkRFUlM'
                         'hIE9XLCBNWSBMRUdTIQogVEhJUyBJUyBUSEUgV09SU1QgUEFJTgog'
                         'RVZFUi4uLg==')
        self.assertEqual(screen.get_mp4_url(caption='Stupid Sexy Flanders'),
                         'https://frinkiac.com/mp4/S11E10/336960/343960.mp4'
                         '?b64lines=IFN0dXBpZCBTZXh5IEZsYW5kZXJz')
        self.assertEqual(screen.get_mp4_url(before=2500, after=500),
                         'https://frinkiac.com/mp4/S11E10/337560/340360.mp4'
                         '?b64lines=ICggeWVsbHMpIFNUVVBJRCwgU0VYWQogRkxBTkRFUlM'
                         'hIE9XLCBNWSBMRUdTIQogVEhJUyBJUyBUSEUgV09SU1QgUEFJTgog'
                         'RVZFUi4uLg==')


if __name__ == '__main__':
    unittest.main()
