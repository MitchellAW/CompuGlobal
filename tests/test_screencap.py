import json
import unittest

import compuglobal

FRINKIAC = compuglobal.Frinkiac()
MORBOTRON = compuglobal.Morbotron()
MASTEROFALLSCIENCE = compuglobal.MasterOfAllScience()


class ScreencapTestCase(unittest.TestCase):
    """Tests for `screencap.py`."""
    def test_screencap_attributes(self):
        """Check attributes of Screencap"""
        with open('frinkiac.json') as frinkiac:
            test_data = json.load(frinkiac)

        data = test_data['test_1']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.id, 571)
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
                         '( yells) STUPID, SEXY FLANDERS! OW, MY LEGS! THIS IS THE WORST PAIN EVER... ')
        self.assertEqual(screen.image_url, 'https://frinkiac.com/img/{}/{}.jpg')
        self.assertEqual(screen.meme_url,
                         'https://frinkiac.com/meme/{}/{}.jpg?b64lines={}')
        self.assertEqual(screen.gif_url,
                         'https://frinkiac.com/gif/{}/{}/{}.gif?b64lines={}')
        self.assertEqual(screen.mp4_url,
                         'https://frinkiac.com/mp4/{}/{}/{}.mp4?b64lines={}')

    def test_simpsons_image_url(self):
        """Tests frinkiac image url"""
        with open('frinkiac.json') as frinkiac:
            test_data = json.load(frinkiac)

        data = test_data['test_1']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.get_image_url(),
                         'https://frinkiac.com/img/S11E10/339960.jpg')

        data = test_data['test_2']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.get_image_url(),
                         'https://frinkiac.com/img/S17E20/1082039.jpg')

        data = test_data['test_3']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.get_image_url(),
                         'https://frinkiac.com/img/S07E06/530579.jpg')

    def test_simpsons_meme_url(self):
        """Tests frinkiac meme url"""
        with open('frinkiac.json') as frinkiac:
            test_data = json.load(frinkiac)

        data = test_data['test_1']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.get_meme_url(),
                         'https://frinkiac.com/meme/S11E10/339960.jpg'
                         '?b64lines=ICggeWVsbHMpIFNUVVBJRCwgU0VYWQogRkxBTkRFUlMhIE9XLCBNWSBMRUdTIQogVEhJUyBJUyBUSEUgV09SU1QgUEFJTgogRVZFUi4uLg==')

        data = test_data['test_2']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.get_meme_url('stupid sexy flanders'),
                         'https://frinkiac.com/meme/S17E20/1082039.jpg'
                         '?b64lines=IHN0dXBpZCBzZXh5IGZsYW5kZXJz')

        data = test_data['test_3']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.get_meme_url(),
                         'https://frinkiac.com/meme/S07E06/530579.jpg'
                         '?b64lines=IE1vcmlzOnlvdSBkaWUu')

    def test_simpsons_get_gif_url(self):
        """Tests frinkiac gif urls"""
        with open('frinkiac.json') as frinkiac:
            test_data = json.load(frinkiac)

        data = test_data['test_1']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.get_gif_url(),
                         'https://frinkiac.com/gif/S11E10/336960/343960.gif'
                         '?b64lines=ICggeWVsbHMpIFNUVVBJRCwgU0VYWQogRkxBTkRFUlMhIE9XLCBNWSBMRUdTIQogVEhJUyBJUyBUSEUgV09SU1QgUEFJTgogRVZFUi4uLg==')
        self.assertEqual(screen.get_gif_url(caption='Stupid Sexy Flanders'),
                         'https://frinkiac.com/gif/S11E10/336960/343960.gif'
                         '?b64lines=IFN0dXBpZCBTZXh5IEZsYW5kZXJz')
        self.assertEqual(screen.get_gif_url(before=1000, after=1000),
                         'https://frinkiac.com/gif/S11E10/338960/340960.gif'
                         '?b64lines=ICggeWVsbHMpIFNUVVBJRCwgU0VYWQogRkxBTkRFUlMhIE9XLCBNWSBMRUdTIQogVEhJUyBJUyBUSEUgV09SU1QgUEFJTgogRVZFUi4uLg==')

    def test_simpsons_get_mp4_url(self):
        """Tests frinkiac mp4 urls"""
        with open('frinkiac.json') as frinkiac:
            test_data = json.load(frinkiac)

        data = test_data['test_1']
        screen = compuglobal.Screencap(FRINKIAC, data)
        self.assertEqual(screen.get_mp4_url(),
                         'https://frinkiac.com/mp4/S11E10/336960/343960.mp4'
                         '?b64lines=ICggeWVsbHMpIFNUVVBJRCwgU0VYWQogRkxBTkRFUlMhIE9XLCBNWSBMRUdTIQogVEhJUyBJUyBUSEUgV09SU1QgUEFJTgogRVZFUi4uLg==')
        self.assertEqual(screen.get_mp4_url(caption='Stupid Sexy Flanders'),
                         'https://frinkiac.com/mp4/S11E10/336960/343960.mp4'
                         '?b64lines=IFN0dXBpZCBTZXh5IEZsYW5kZXJz')
        self.assertEqual(screen.get_mp4_url(before=2500, after=500),
                         'https://frinkiac.com/mp4/S11E10/337560/340360.mp4?b64lines=ICggeWVsbHMpIFNUVVBJRCwgU0VYWQogRkxBTkRFUlMhIE9XLCBNWSBMRUdTIQogVEhJUyBJUyBUSEUgV09SU1QgUEFJTgogRVZFUi4uLg==')

    def test_futurama_meme_url(self):
        """Tests morbotron meme url"""
        with open('morbotron.json') as morbo:
            test_data = json.load(morbo)

        data = test_data['test_1']
        screen = compuglobal.Screencap(MORBOTRON, data)
        self.assertEqual(screen.get_meme_url(),
                         'https://morbotron.com/meme/S07E03/343676.jpg?b64lines=IGFuZCB0aGUgcmVjZXB0aW9uCiBpc24ndCB2ZXJ5Li4uIFNodXQgdXAKIGFuZCB0YWtlIG15IG1vbmV5IQ==')

        data = test_data['test_2']
        screen = compuglobal.Screencap(MORBOTRON, data)
        self.assertEqual(screen.get_meme_url('stupid sexy flanders'),
                         'https://morbotron.com/meme/S05E09/1283064.jpg?b64lines=IHN0dXBpZCBzZXh5IGZsYW5kZXJz')

        data = test_data['test_3']
        screen = compuglobal.Screencap(MORBOTRON, data)
        self.assertEqual(screen.get_meme_url(),
                         'https://morbotron.com/meme/S04E08/696528.jpg?b64lines=IFRyZW1ibGUgaW4gZmVhciBhdCBvdXIKIHRocmVlIGRpZmZlcmVudCBraW5kcwogb2Ygc2hpcHMuIEFsbCByaWdodC4KIEl0J3MgU2F0dXJkYXkgbmlnaHQu')

    def test_futurama_get_gif_url(self):
        """Tests morbotron gif urls"""
        with open('morbotron.json') as morbo:
            test_data = json.load(morbo)

        data = test_data['test_1']

        screen = compuglobal.Screencap(MORBOTRON, data)

        self.assertEqual(screen.get_gif_url(), 'https://morbotron.com/gif/S07E03/340757/347639.gif?b64lines=IGFuZCB0aGUgcmVjZXB0aW9uCiBpc24ndCB2ZXJ5Li4uIFNodXQgdXAKIGFuZCB0YWtlIG15IG1vbmV5IQ==')
        self.assertEqual(screen.get_gif_url(caption='Stupid Sexy Flanders'),
                         'https://morbotron.com/gif/S07E03/340757/347639.gif?b64lines=IFN0dXBpZCBTZXh5IEZsYW5kZXJz')
        self.assertEqual(screen.get_gif_url(), 'https://morbotron.com/gif/S07E03/340757/347639.gif?b64lines=IGFuZCB0aGUgcmVjZXB0aW9uCiBpc24ndCB2ZXJ5Li4uIFNodXQgdXAKIGFuZCB0YWtlIG15IG1vbmV5IQ==')

    def test_futurama_get_mp4_url(self):
        """Tests morbotron mp4 urls"""
        with open('morbotron.json') as morbo:
            test_data = json.load(morbo)

        data = test_data['test_1']
        screen = compuglobal.Screencap(MORBOTRON, data)
        self.assertEqual(screen.get_mp4_url(),
                         'https://morbotron.com/mp4/S07E03/340757/347639.mp4?b64lines=IGFuZCB0aGUgcmVjZXB0aW9uCiBpc24ndCB2ZXJ5Li4uIFNodXQgdXAKIGFuZCB0YWtlIG15IG1vbmV5IQ==')
        self.assertEqual(screen.get_mp4_url(caption='Stupid Sexy Flanders'),
                         'https://morbotron.com/mp4/S07E03/340757/347639.mp4?b64lines=IFN0dXBpZCBTZXh5IEZsYW5kZXJz')
        self.assertEqual(screen.get_mp4_url(before=2500, after=500),
                         'https://morbotron.com/mp4/S07E03/341382/344093.mp4?b64lines=IGFuZCB0aGUgcmVjZXB0aW9uCiBpc24ndCB2ZXJ5Li4uIFNodXQgdXAKIGFuZCB0YWtlIG15IG1vbmV5IQ==')

    def test_ram_meme_url(self):
        """Tests master of all science meme url"""
        with open('masterofall.json') as master:
            test_data = json.load(master)

        data = test_data['test_1']
        screen = compuglobal.Screencap(MASTEROFALLSCIENCE, data)
        self.assertEqual(screen.get_meme_url(),
                         'https://masterofallscience.com/meme/S01E02/616991.jpg?b64lines=IFdoZXJlIGFyZSBteQogdGVzdGljbGVzLCBTdW1tZXI_CiBUaGV5IHdlcmUgcmVtb3ZlZC4KIFdoZXJlIGhhdmUgdGhleSBnb25lPw==')

        data = test_data['test_2']
        screen = compuglobal.Screencap(MASTEROFALLSCIENCE, data)
        self.assertEqual(screen.get_meme_url('stupid sexy flanders'),
                         'https://masterofallscience.com/meme/S02E09/1183599.jpg?b64lines=IHN0dXBpZCBzZXh5IGZsYW5kZXJz')

        data = test_data['test_3']
        screen = compuglobal.Screencap(MASTEROFALLSCIENCE, data)
        self.assertEqual(screen.get_meme_url(),
                         'https://masterofallscience.com/meme/S03E01/384050.jpg?b64lines=IFsgU3F1ZWFscyBdIFdoYXQ_')

    def test_ram_get_gif_url(self):
        """Tests master of all science gif urls"""
        with open('masterofall.json') as master:
            test_data = json.load(master)

        data = test_data['test_1']
        screen = compuglobal.Screencap(MASTEROFALLSCIENCE, data)
        self.assertEqual(screen.get_gif_url(),
                         'https://masterofallscience.com/gif/S01E02/614280/620954.gif?b64lines=IFdoZXJlIGFyZSBteQogdGVzdGljbGVzLCBTdW1tZXI_CiBUaGV5IHdlcmUgcmVtb3ZlZC4KIFdoZXJlIGhhdmUgdGhleSBnb25lPw==')
        self.assertEqual(screen.get_gif_url(caption='Stupid Sexy Flanders'),
                         'https://masterofallscience.com/gif/S01E02/614280/620954.gif?b64lines=IFN0dXBpZCBTZXh5IEZsYW5kZXJz')
        self.assertEqual(screen.get_gif_url(before=1000, after=1000),
                         'https://masterofallscience.com/gif/S01E02/616157/617826.gif?b64lines=IFdoZXJlIGFyZSBteQogdGVzdGljbGVzLCBTdW1tZXI_CiBUaGV5IHdlcmUgcmVtb3ZlZC4KIFdoZXJlIGhhdmUgdGhleSBnb25lPw==')

    def test_ram_get_mp4_url(self):
        """Tests master of all science mp4 urls"""
        with open('masterofall.json') as master:
            test_data = json.load(master)

        data = test_data['test_1']
        screen = compuglobal.Screencap(MASTEROFALLSCIENCE, data)
        self.assertEqual(screen.get_mp4_url(),
                         'https://masterofallscience.com/mp4/S01E02/614280/620954.mp4?b64lines=IFdoZXJlIGFyZSBteQogdGVzdGljbGVzLCBTdW1tZXI_CiBUaGV5IHdlcmUgcmVtb3ZlZC4KIFdoZXJlIGhhdmUgdGhleSBnb25lPw==')
        self.assertEqual(screen.get_mp4_url(caption='Stupid Sexy Flanders'),
                         'https://masterofallscience.com/mp4/S01E02/614280/620954.mp4?b64lines=IFN0dXBpZCBTZXh5IEZsYW5kZXJz')
        self.assertEqual(screen.get_mp4_url(before=2500, after=500),
                         'https://masterofallscience.com/mp4/S01E02/614697/617408.mp4?b64lines=IFdoZXJlIGFyZSBteQogdGVzdGljbGVzLCBTdW1tZXI_CiBUaGV5IHdlcmUgcmVtb3ZlZC4KIFdoZXJlIGhhdmUgdGhleSBnb25lPw==')


if __name__ == '__main__':
    unittest.main()
