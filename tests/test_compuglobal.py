import json
import unittest

import compuglobal


FRINKIAC = compuglobal.Frinkiac()
MORBOTRON = compuglobal.Morbotron()
MASTEROFALLSCIENCE = compuglobal.MasterOfAllScience()

with open('frinkiac.json') as frinkiac:
    frinkiac_data = json.load(frinkiac)

with open('morbotron.json') as morbo:
    morbo_data = json.load(morbo)

with open('masterofall.json') as master:
    master_data = json.load(master)


class CompuGlobalAPITestCase(unittest.TestCase):
    def test_json_to_caption_frinkiac(self):
        """Tests json converting to caption"""
        self.assertEqual(FRINKIAC.json_to_caption(frinkiac_data['test_1']), '( yells) STUPID, SEXY FLANDERS! OW, MY LEGS! THIS IS THE WORST PAIN EVER... ')
        self.assertEqual(FRINKIAC.json_to_caption(frinkiac_data['test_2']), 'Marge? Homer, I don\'t want to alarm you, ')
        self.assertEqual(FRINKIAC.json_to_caption(frinkiac_data['test_3']), 'Moris:you die. ( screams) ')

    def test_json_to_caption_morbotron(self):
        self.assertEqual(MORBOTRON.json_to_caption(morbo_data['test_1']), 'and the reception isn\'t very... Shut up and take my money! The new eyePhone is wonderful. ')
        self.assertEqual(MORBOTRON.json_to_caption(morbo_data['test_2']), 'Sweet three-toed sloth of ice planet Hoth! She\'s awake! ( all cheering ) ')
        self.assertEqual(MORBOTRON.json_to_caption(morbo_data['test_3']), 'Tremble in fear at our three different kinds of ships. All right. It\'s Saturday night. I have no date, a two-liter bottle of Shasta and my all-Rush mix tape. ')

    def test_json_to_caption_master(self):
        self.assertEqual(MASTEROFALLSCIENCE.json_to_caption(master_data['test_1']), 'Where are my testicles, Summer? They were removed. Where have they gone? ')
        self.assertEqual(MASTEROFALLSCIENCE.json_to_caption(master_data['test_2']), 'I\'ll take care of your kids, if I get some extra food for it. ')
        self.assertEqual(MASTEROFALLSCIENCE.json_to_caption(master_data['test_3']), '[ Squeals ] What? ')

    def test_view_episode(self):
        """Tests ``api/episode/{episode}/{start}/{end}`` endpoint"""
        self.assertEqual(FRINKIAC.view_episode('S11E10', 339960, 0), frinkiac_data['episode_test_1'])
        self.assertEqual(MORBOTRON.view_episode('S07E03', 343676, 350000), morbo_data['episode_test_1'])
        self.assertEqual(MASTEROFALLSCIENCE.view_episode('Invalid', 0, 0), master_data['episode_test_1'])

    def test_get_frames(self):
        """Tests ``api/frames/{episode}/{timestamp}/{before}/{after}``
        endpoint"""
        self.assertEqual(FRINKIAC.get_frames("S02E01", 232973, 5000, 5000), frinkiac_data['frames_test_1'])
        self.assertEqual(MORBOTRON.get_frames('S10E08', 1043668, 1000, 1000), morbo_data['frames_test_1'])
        self.assertEqual(MORBOTRON.get_frames('S10E08', 1043668, 0, 0), morbo_data['frames_test_2'])
        self.assertEqual(FRINKIAC.get_frames('Invalid', 0, 0, 0), [])

    def test_get_nearby_frames(self):
        """Tests the ``api/nearby?e={}&t={}`` endpoint"""
        self.assertEqual(FRINKIAC.get_nearby_frames('S07E10', 498797), frinkiac_data['nearby_frames_test_1'])
        self.assertEqual(MORBOTRON.get_nearby_frames('S04E05', 1116581), morbo_data['nearby_frames_test_1'])
        with self.assertRaises(compuglobal.APIPageStatusError):
            MASTEROFALLSCIENCE.get_nearby_frames('Invalid', 0)

    def test_search(self):
        """Tests the ``api/search?q=`` endpoint"""
        self.assertEqual(FRINKIAC.search('stupid sexy flanders'), frinkiac_data['search_test_1'])
        self.assertEqual(MORBOTRON.search('shutup and take my money'), morbo_data['search_test_1'])
        with self.assertRaises(compuglobal.NoSearchResultsFound):
            MASTEROFALLSCIENCE.search('')

    def test_search_for_screencap(self):
        """Tests the ``api/search?q=`` endpoint and checks it has the correct
        json data"""
        self.assertEqual(FRINKIAC.search_for_screencap('stupid sexy flanders').json, frinkiac_data['test_1'])
        self.assertEqual(MORBOTRON.search_for_screencap('shutup and take my money').json, morbo_data['test_1'])
        with self.assertRaises(compuglobal.NoSearchResultsFound):
            FRINKIAC.search_for_screencap('')


if __name__ == '__main__':
    unittest.main()
