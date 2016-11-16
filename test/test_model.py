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


if __name__ == '__main__':
    
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(ModelTestCase))
