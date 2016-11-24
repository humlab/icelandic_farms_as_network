import unittest
import sys
import os
import datetime

root = os.path.split(__file__)[0]
sys.path = [ os.path.join(root, "../server/src") ] + sys.path

import model
import repository

class  ModelTestCase(unittest.TestCase):

    def setUp(self):
        self.registry = repository.RepositoryRegistry()

    #@unittest.skip("skipping")
    def test_can_fetch_a_specific_farm(self):
        
        farm_id = 3008
        farm_repository = self.registry.get(repository.IsleifFarmRepository)
        farm = farm_repository.get_by_id(farm_id)
        subunit = farm.subunits[0] if len(farm.subunits) > 0 else None

        self.assertIsNotNone(farm)
        self.assertIsNotNone(subunit)
        self.assertEqual(farm.isleif_farms_id, farm_id)
        self.assertEqual(subunit.jam_subunit_isleif, farm)

    def test_can_fetch_a_specific_person(self):
        
        entity_id = 235
        person = self.registry.get(repository.PeopleHistoricalRepository).get_by_id(entity_id)
        farm = person.isleif_farms 
        
        self.assertIsNotNone(person)
        self.assertIsNotNone(farm)
        self.assertEqual(person.entity_name, 'Beneficium Miklibær')
        self.assertEqual(farm.Hreppur, 'Akrahreppur')

    def test_can_fetch_full_text_for_farm_by_id(self):
        
        farm_id = 3008
        full_text_repository = self.registry.get(repository.JamFullTextRepository)
        items = full_text_repository.get_all_by_farm_id(farm_id)

        self.assertIsNotNone(items)
        self.assertTrue(len(items) > 0)

if __name__ == '__main__':
    
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(ModelTestCase))
