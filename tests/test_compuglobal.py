import json
import unittest

import compuglobal


FRINKIAC = compuglobal.Frinkiac()

with open('frinkiac.json') as frinkiac:
    frinkiac_data = json.load(frinkiac)


class CompuGlobalAPITestCase(unittest.TestCase):
    def test_json_to_caption_1(self):
        """Tests json converting to caption"""
        self.assertEqual(FRINKIAC.json_to_caption(frinkiac_data['test_1']), '( yells) STUPID, SEXY FLANDERS! OW, MY LEGS! THIS IS THE WORST PAIN EVER... ')
        self.assertEqual(FRINKIAC.json_to_caption(frinkiac_data['test_2']), 'Marge? Homer, I don\'t want to alarm you, ')
        self.assertEqual(FRINKIAC.json_to_caption(frinkiac_data['test_3']), 'Moris:you die. ( screams) ')

    def test_view_episode_1(self):
        """Tests ``api/episode/{episode}/{start}/{end}`` endpoint"""
        self.assertEqual(FRINKIAC.view_episode('S11E10', 339960, 0), frinkiac_data['episode_test_1'])
        self.assertEqual(FRINKIAC.view_episode('S11E10', 339960, 349960), frinkiac_data['episode_test_2'])

    def test_view_episode_2(self):
        """Tests ``api/episode/{episode}/{start}/{end}`` endpoint with
        invalid parameters"""
        self.assertEqual(FRINKIAC.view_episode('Invalid', 0, 0), frinkiac_data['episode_test_3'])

    def test_get_frames_1(self):
        """Tests ``api/frames/{episode}/{timestamp}/{before}/{after}``
        endpoint"""
        self.assertEqual(FRINKIAC.get_frames('S02E01', 232973, 5000, 5000), frinkiac_data['frames_test_1'])
        self.assertEqual(FRINKIAC.get_frames('S07E07', 225507, 3000, 3000), frinkiac_data['frames_test_2'])

    def test_get_frames_2(self):
        """Tests ``api/frames/{episode}/{timestamp}/{before}/{after}``
        endpoint with invalid parameters"""
        self.assertEqual(FRINKIAC.get_frames('Invalid', 0, 0, 0), [])

    def test_get_nearby_frames_1(self):
        """Tests the ``api/nearby?e={}&t={}`` endpoint"""
        self.assertEqual(FRINKIAC.get_nearby_frames('S07E10', 498797), frinkiac_data['nearby_frames_test_1'])
        self.assertEqual(FRINKIAC.get_nearby_frames('S03E17', 1314891), frinkiac_data['nearby_frames_test_2'])

    def test_get_nearby_frames_2(self):
        """Tests the ``api/nearby?e={}&t={}`` endpoint with invalid
        parameters"""
        with self.assertRaises(compuglobal.APIPageStatusError):
            FRINKIAC.get_nearby_frames('Invalid', 0)

    def test_search_1(self):
        """Tests the ``api/search?q=`` endpoint"""
        self.assertEqual(FRINKIAC.search('stupid sexy flanders'), frinkiac_data['search_test_1'])
        self.assertEqual(FRINKIAC.search('i sleep in a racing car'), frinkiac_data['search_test_2'])

    def test_search_2(self):
        """Tests the ``api/search?q=`` endpoint with search query that
        returns no search results"""
        with self.assertRaises(compuglobal.NoSearchResultsFound):
            FRINKIAC.search('')

    def test_search_for_screencap_1(self):
        """Tests the ``api/search?q=`` endpoint and checks it has the correct
        json data"""
        self.assertEqual(FRINKIAC.search_for_screencap('stupid sexy flanders').json, frinkiac_data['test_1'])
        self.assertEqual(FRINKIAC.search_for_screencap('i sleep in a racing car').json, frinkiac_data['search_test_3'])

    def test_search_for_screencap_2(self):
        """Tests the ``api/search?q=`` endpoint with search query that
        returns no search results"""
        with self.assertRaises(compuglobal.NoSearchResultsFound):
            FRINKIAC.search_for_screencap('')


if __name__ == '__main__':
    unittest.main()
