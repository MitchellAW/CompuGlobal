import json
import unittest

import compuglobal

FRINKIAC = compuglobal.Frinkiac()
MORBOTRON = compuglobal.Morbotron()
MASTEROFALLSCIENCE = compuglobal.MasterOfAllScience()


class CompuGlobalAPITestCase(unittest.TestCase):
    def test_json_to_caption(self):
        """Tests json converting to caption"""
        with open('frinkiac.json') as frinkiac:
            test_data = json.load(frinkiac)
        data = test_data['test_1']
        self.assertEqual(FRINKIAC.json_to_caption(data), '( yells) STUPID, SEXY FLANDERS! OW, MY LEGS! THIS IS THE WORST PAIN EVER... ')
        data = test_data['test_2']
        self.assertEqual(FRINKIAC.json_to_caption(data), 'Marge? Homer, I don\'t want to alarm you, ')
        data = test_data['test_3']
        self.assertEqual(FRINKIAC.json_to_caption(data), 'Moris:you die. ( screams) ')

        with open('morbotron.json') as morbo:
            test_data = json.load(morbo)
        data = test_data['test_1']
        self.assertEqual(FRINKIAC.json_to_caption(data), 'and the reception isn\'t very... Shut up and take my money! The new eyePhone is wonderful. ')
        data = test_data['test_2']
        self.assertEqual(FRINKIAC.json_to_caption(data), 'Sweet three-toed sloth of ice planet Hoth! She\'s awake! ( all cheering ) ')
        data = test_data['test_3']
        self.assertEqual(FRINKIAC.json_to_caption(data), 'Tremble in fear at our three different kinds of ships. All right. It\'s Saturday night. I have no date, a two-liter bottle of Shasta and my all-Rush mix tape. ')

        with open('masterofall.json') as master:
            test_data = json.load(master)
        data = test_data['test_1']
        self.assertEqual(FRINKIAC.json_to_caption(data), 'Where are my testicles, Summer? They were removed. Where have they gone? ')
        data = test_data['test_2']
        self.assertEqual(FRINKIAC.json_to_caption(data), 'I\'ll take care of your kids, if I get some extra food for it. ')
        data = test_data['test_3']
        self.assertEqual(FRINKIAC.json_to_caption(data), '[ Squeals ] What? ')

    def test_view_episode(self):
        """Tests ``api/episode/{episode}/{start}/{end}`` endpoint"""
        episode = {'Episode': {'Id': 571, 'Key': 'S11E10', 'Season': 11, 'EpisodeNumber': 10, 'Title': 'Little Big Mom', 'Director': 'Mark Kirkland', 'Writer': 'Carolyn Omine', 'OriginalAirDate': '9-Jan-00', 'WikiLink': 'https://en.wikipedia.org/wiki/Little_Big_Mom'}, 'Subtitles': []}
        self.assertEqual(FRINKIAC.view_episode('S11E10', 339960, 0), episode)
        episode = {'Episode': {'Id': 335, 'Key': 'S07E03', 'Season': 7, 'EpisodeNumber': 3, 'Title': 'Attack of the Killer App', 'Director': 'Stephen Sandoval', 'Writer': 'Patric M. Verrone', 'OriginalAirDate': '1-Jul-10', 'WikiLink': 'https://en.wikipedia.org/wiki/Attack_of_the_Killer_App'}, 'Subtitles': [{'Id': 171400, 'RepresentativeTimestamp': 345345, 'Episode': 'S07E03', 'StartTimestamp': 344094, 'EndTimestamp': 346429, 'Content': 'The new eyePhone is wonderful.', 'Language': 'en'}, {'Id': 171401, 'RepresentativeTimestamp': 348056, 'Episode': 'S07E03', 'StartTimestamp': 346513, 'EndTimestamp': 349849, 'Content': 'I use it to check recipes and send threatening e-mails', 'Language': 'en'}]}
        self.assertEqual(MORBOTRON.view_episode('S07E03', 343676, 350000), episode)
        episode = {'Episode': {'Id': 0, 'Key': '', 'Season': 0, 'EpisodeNumber': 0, 'Title': '', 'Director': '', 'Writer': '', 'OriginalAirDate': '', 'WikiLink': ''}, 'Subtitles': []}
        self.assertEqual(FRINKIAC.view_episode('Invalid', 0, 0), episode)

    def test_get_frames(self):
        """Tests ``api/frames/{episode}/{timestamp}/{before}/{after}``
        endpoint"""
        frames = [{'Id': 91796, 'Episode': 'S02E01', 'Timestamp': 228134}, {'Id': 91793, 'Episode': 'S02E01', 'Timestamp': 228301}, {'Id': 91794, 'Episode': 'S02E01', 'Timestamp': 228468}, {'Id': 91795, 'Episode': 'S02E01', 'Timestamp': 228635}, {'Id': 91798, 'Episode': 'S02E01', 'Timestamp': 228802}, {'Id': 91797, 'Episode': 'S02E01', 'Timestamp': 228969}, {'Id': 91799, 'Episode': 'S02E01', 'Timestamp': 229135}, {'Id': 91800, 'Episode': 'S02E01', 'Timestamp': 229302}, {'Id': 91804, 'Episode': 'S02E01', 'Timestamp': 229469}, {'Id': 91801, 'Episode': 'S02E01', 'Timestamp': 229636}, {'Id': 91802, 'Episode': 'S02E01', 'Timestamp': 229803}, {'Id': 91803, 'Episode': 'S02E01', 'Timestamp': 229970}, {'Id': 91809, 'Episode': 'S02E01', 'Timestamp': 230136}, {'Id': 91806, 'Episode': 'S02E01', 'Timestamp': 230303}, {'Id': 91805, 'Episode': 'S02E01', 'Timestamp': 230470}, {'Id': 91807, 'Episode': 'S02E01', 'Timestamp': 230637}, {'Id': 91808, 'Episode': 'S02E01', 'Timestamp': 230971}, {'Id': 91810, 'Episode': 'S02E01', 'Timestamp': 231137}, {'Id': 91814, 'Episode': 'S02E01', 'Timestamp': 231304}, {'Id': 91811, 'Episode': 'S02E01', 'Timestamp': 231471}, {'Id': 91812, 'Episode': 'S02E01', 'Timestamp': 231638}, {'Id': 91813, 'Episode': 'S02E01', 'Timestamp': 231805}, {'Id': 91818, 'Episode': 'S02E01', 'Timestamp': 231972}, {'Id': 91819, 'Episode': 'S02E01', 'Timestamp': 232138}, {'Id': 91815, 'Episode': 'S02E01', 'Timestamp': 232305}, {'Id': 91816, 'Episode': 'S02E01', 'Timestamp': 232472}, {'Id': 91817, 'Episode': 'S02E01', 'Timestamp': 232639}, {'Id': 91820, 'Episode': 'S02E01', 'Timestamp': 232806}, {'Id': 91824, 'Episode': 'S02E01', 'Timestamp': 232973}, {'Id': 91821, 'Episode': 'S02E01', 'Timestamp': 233139}, {'Id': 91826, 'Episode': 'S02E01', 'Timestamp': 233306}, {'Id': 91822, 'Episode': 'S02E01', 'Timestamp': 233473}, {'Id': 91823, 'Episode': 'S02E01', 'Timestamp': 233640}, {'Id': 91825, 'Episode': 'S02E01', 'Timestamp': 233807}, {'Id': 91830, 'Episode': 'S02E01', 'Timestamp': 233974}, {'Id': 91828, 'Episode': 'S02E01', 'Timestamp': 234140}, {'Id': 91827, 'Episode': 'S02E01', 'Timestamp': 234307}, {'Id': 91829, 'Episode': 'S02E01', 'Timestamp': 234641}, {'Id': 91832, 'Episode': 'S02E01', 'Timestamp': 234824}, {'Id': 91831, 'Episode': 'S02E01', 'Timestamp': 235008}, {'Id': 91835, 'Episode': 'S02E01', 'Timestamp': 235208}, {'Id': 91838, 'Episode': 'S02E01', 'Timestamp': 235392}, {'Id': 91833, 'Episode': 'S02E01', 'Timestamp': 235575}, {'Id': 91834, 'Episode': 'S02E01', 'Timestamp': 235775}, {'Id': 91836, 'Episode': 'S02E01', 'Timestamp': 235942}, {'Id': 91837, 'Episode': 'S02E01', 'Timestamp': 236109}, {'Id': 91840, 'Episode': 'S02E01', 'Timestamp': 236276}, {'Id': 91842, 'Episode': 'S02E01', 'Timestamp': 236443}, {'Id': 91839, 'Episode': 'S02E01', 'Timestamp': 236610}, {'Id': 91844, 'Episode': 'S02E01', 'Timestamp': 236776}, {'Id': 91841, 'Episode': 'S02E01', 'Timestamp': 236943}, {'Id': 91843, 'Episode': 'S02E01', 'Timestamp': 237110}, {'Id': 91845, 'Episode': 'S02E01', 'Timestamp': 237277}, {'Id': 91846, 'Episode': 'S02E01', 'Timestamp': 237444}, {'Id': 91848, 'Episode': 'S02E01', 'Timestamp': 237611}, {'Id': 91847, 'Episode': 'S02E01', 'Timestamp': 237777}, {'Id': 91849, 'Episode': 'S02E01', 'Timestamp': 237944}]
        self.assertEqual(FRINKIAC.get_frames("S02E01", 232973, 5000, 5000), frames)
        frames = [{'Id': 2503545, 'Episode': 'S10E08', 'Timestamp': 1042833}, {'Id': 2503546, 'Episode': 'S10E08', 'Timestamp': 1043042}, {'Id': 2503547, 'Episode': 'S10E08', 'Timestamp': 1043251}, {'Id': 2503548, 'Episode': 'S10E08', 'Timestamp': 1043459}, {'Id': 2503549, 'Episode': 'S10E08', 'Timestamp': 1043668}, {'Id': 2503551, 'Episode': 'S10E08', 'Timestamp': 1043876}, {'Id': 2503550, 'Episode': 'S10E08', 'Timestamp': 1044085}, {'Id': 2503552, 'Episode': 'S10E08', 'Timestamp': 1044293}, {'Id': 2503555, 'Episode': 'S10E08', 'Timestamp': 1044502}]
        self.assertEqual(MORBOTRON.get_frames('S10E08', 1043668, 1000, 1000), frames)
        self.assertEqual(MORBOTRON.get_frames('S10E08', 1043668, 0, 0), [{'Episode': 'S10E08', 'Id': 2503549, 'Timestamp': 1043668}])
        self.assertEqual(FRINKIAC.get_frames('Invalid', 0, 0, 0), [])

    def test_get_nearby_frames(self):
        """Tests the ``api/nearby?e={}&t={}`` endpoint"""
        nearby = [{'Id': 884971, 'Episode': 'S07E10', 'Timestamp': 498180}, {'Id': 884969, 'Episode': 'S07E10', 'Timestamp': 498380}, {'Id': 884970, 'Episode': 'S07E10', 'Timestamp': 498597}, {'Id': 884973, 'Episode': 'S07E10', 'Timestamp': 498797}, {'Id': 884978, 'Episode': 'S07E10', 'Timestamp': 498997}, {'Id': 884974, 'Episode': 'S07E10', 'Timestamp': 499214}, {'Id': 884975, 'Episode': 'S07E10', 'Timestamp': 499414}]
        self.assertEqual(FRINKIAC.get_nearby_frames('S07E10', 498797), nearby)
        nearby = [{'Id': 1962042, 'Episode': 'S04E05', 'Timestamp': 1115964}, {'Id': 1962043, 'Episode': 'S04E05', 'Timestamp': 1116164}, {'Id': 1962047, 'Episode': 'S04E05', 'Timestamp': 1116381}, {'Id': 1962046, 'Episode': 'S04E05', 'Timestamp': 1116581}, {'Id': 1962048, 'Episode': 'S04E05', 'Timestamp': 1116798}, {'Id': 1962050, 'Episode': 'S04E05', 'Timestamp': 1116998}, {'Id': 1962049, 'Episode': 'S04E05', 'Timestamp': 1117215}]
        self.assertEqual(MORBOTRON.get_nearby_frames('S04E05', 1116581), nearby)

        with self.assertRaises(compuglobal.APIPageStatusError):
            MORBOTRON.get_nearby_frames('Invalid', 0)

    def test_search(self):
        """Tests the ``api/search?q=`` endpoint"""
        search = [{'Id': 1503125, 'Episode': 'S11E10', 'Timestamp': 339960}, {'Id': 1503122, 'Episode': 'S11E10', 'Timestamp': 339760}, {'Id': 1801788, 'Episode': 'S13E17', 'Timestamp': 680013}, {'Id': 1801782, 'Episode': 'S13E17', 'Timestamp': 679179}, {'Id': 1801790, 'Episode': 'S13E17', 'Timestamp': 680430}, {'Id': 1801783, 'Episode': 'S13E17', 'Timestamp': 678970}, {'Id': 1503116, 'Episode': 'S11E10', 'Timestamp': 338560}, {'Id': 1503117, 'Episode': 'S11E10', 'Timestamp': 338960}, {'Id': 1801787, 'Episode': 'S13E17', 'Timestamp': 679804}, {'Id': 1503121, 'Episode': 'S11E10', 'Timestamp': 339360}, {'Id': 1801794, 'Episode': 'S13E17', 'Timestamp': 680638}, {'Id': 1801789, 'Episode': 'S13E17', 'Timestamp': 679596}, {'Id': 1503118, 'Episode': 'S11E10', 'Timestamp': 339160}, {'Id': 1801791, 'Episode': 'S13E17', 'Timestamp': 680221}, {'Id': 1503119, 'Episode': 'S11E10', 'Timestamp': 338760}, {'Id': 1503115, 'Episode': 'S11E10', 'Timestamp': 338360}, {'Id': 1503120, 'Episode': 'S11E10', 'Timestamp': 339560}, {'Id': 1801786, 'Episode': 'S13E17', 'Timestamp': 679387}, {'Id': 2200632, 'Episode': 'S16E20', 'Timestamp': 552761}, {'Id': 2212851, 'Episode': 'S17E02', 'Timestamp': 80414}, {'Id': 1923737, 'Episode': 'S14E17', 'Timestamp': 598264}, {'Id': 1923736, 'Episode': 'S14E17', 'Timestamp': 598056}, {'Id': 2261606, 'Episode': 'S17E16', 'Timestamp': 334626}, {'Id': 2200737, 'Episode': 'S16E20', 'Timestamp': 580080}, {'Id': 2212849, 'Episode': 'S17E02', 'Timestamp': 79997}, {'Id': 1719660, 'Episode': 'S13E03', 'Timestamp': 1044752}, {'Id': 1923726, 'Episode': 'S14E17', 'Timestamp': 596387}, {'Id': 1719663, 'Episode': 'S13E03', 'Timestamp': 1045378}, {'Id': 2200711, 'Episode': 'S16E20', 'Timestamp': 574241}, {'Id': 2260421, 'Episode': 'S17E16', 'Timestamp': 189898}, {'Id': 1874476, 'Episode': 'S14E08', 'Timestamp': 293794}, {'Id': 2261605, 'Episode': 'S17E16', 'Timestamp': 334835}, {'Id': 2200744, 'Episode': 'S16E20', 'Timestamp': 581123}, {'Id': 2261603, 'Episode': 'S17E16', 'Timestamp': 334417}, {'Id': 2200637, 'Episode': 'S16E20', 'Timestamp': 553804}, {'Id': 2261611, 'Episode': 'S17E16', 'Timestamp': 335460}]
        self.assertEqual(FRINKIAC.search('stupid sexy flanders'), search)
        search = [{'Id': 2220152, 'Episode': 'S07E03', 'Timestamp': 343676}, {'Id': 2220143, 'Episode': 'S07E03', 'Timestamp': 342634}, {'Id': 2220150, 'Episode': 'S07E03', 'Timestamp': 343259}, {'Id': 2220149, 'Episode': 'S07E03', 'Timestamp': 343051}, {'Id': 2220142, 'Episode': 'S07E03', 'Timestamp': 342842}, {'Id': 2220154, 'Episode': 'S07E03', 'Timestamp': 343468}, {'Id': 2220156, 'Episode': 'S07E03', 'Timestamp': 343885}, {'Id': 2059712, 'Episode': 'S05E06', 'Timestamp': 227009}, {'Id': 2243274, 'Episode': 'S07E05', 'Timestamp': 122205}, {'Id': 2243279, 'Episode': 'S07E05', 'Timestamp': 122622}, {'Id': 2243295, 'Episode': 'S07E05', 'Timestamp': 124499}, {'Id': 2059701, 'Episode': 'S05E06', 'Timestamp': 224924}, {'Id': 2059711, 'Episode': 'S05E06', 'Timestamp': 226809}, {'Id': 1794227, 'Episode': 'S03E08', 'Timestamp': 294944}, {'Id': 2243309, 'Episode': 'S07E05', 'Timestamp': 126584}, {'Id': 1820159, 'Episode': 'S02E06', 'Timestamp': 482754}, {'Id': 2243272, 'Episode': 'S07E05', 'Timestamp': 122414}, {'Id': 2410778, 'Episode': 'S08E06', 'Timestamp': 413663}, {'Id': 2393845, 'Episode': 'S09E12', 'Timestamp': 361111}, {'Id': 1820177, 'Episode': 'S02E06', 'Timestamp': 484205}, {'Id': 2243267, 'Episode': 'S07E05', 'Timestamp': 121996}, {'Id': 1991437, 'Episode': 'S02E20', 'Timestamp': 512698}, {'Id': 2243315, 'Episode': 'S07E05', 'Timestamp': 127210}, {'Id': 1820162, 'Episode': 'S02E06', 'Timestamp': 483171}, {'Id': 1820156, 'Episode': 'S02E06', 'Timestamp': 482120}, {'Id': 1991429, 'Episode': 'S02E20', 'Timestamp': 511229}, {'Id': 1794236, 'Episode': 'S03E08', 'Timestamp': 295144}, {'Id': 1991443, 'Episode': 'S02E20', 'Timestamp': 513115}, {'Id': 2059708, 'Episode': 'S05E06', 'Timestamp': 226592}, {'Id': 1910966, 'Episode': 'S02E14', 'Timestamp': 363495}, {'Id': 1820169, 'Episode': 'S02E06', 'Timestamp': 483788}, {'Id': 1816747, 'Episode': 'S03E09', 'Timestamp': 1222403}, {'Id': 2059713, 'Episode': 'S05E06', 'Timestamp': 227426}, {'Id': 1820152, 'Episode': 'S02E06', 'Timestamp': 481703}, {'Id': 2243283, 'Episode': 'S07E05', 'Timestamp': 123248}, {'Id': 1816757, 'Episode': 'S03E09', 'Timestamp': 1224489}]
        self.assertEqual(MORBOTRON.search('shutup and take my money'), search)
        with self.assertRaises(compuglobal.NoSearchResultsFound):
            FRINKIAC.search('')

    def test_search_for_screencap(self):
        """Tests the ``api/search?q=`` endpoint and checks it has the correct
        json data"""
        with open('frinkiac.json') as frinkiac:
            test_data = json.load(frinkiac)
        data = test_data['test_1']
        self.assertEqual(FRINKIAC.search_for_screencap('stupid sexy flanders').json, data)
        with open('morbotron.json') as frinkiac:
            test_data = json.load(frinkiac)
        data = test_data['test_1']
        self.assertEqual(MORBOTRON.search_for_screencap('shutup and take my money').json, data)
        with self.assertRaises(compuglobal.NoSearchResultsFound):
            FRINKIAC.search_for_screencap('')


if __name__ == '__main__':
    unittest.main()
