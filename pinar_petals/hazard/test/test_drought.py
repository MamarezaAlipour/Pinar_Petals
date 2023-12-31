"""

Tests on Drought Hazard"""


import unittest

from pinar_petals.hazard.drought import Drought


class TestReader(unittest.TestCase):
    """Test loading functions from the Drought class"""
    def test(self):

        drought = Drought()
        drought.set_area(44.5, 5, 50, 12)

        hazard_set = drought.setup()

        self.assertEqual(hazard_set.tag.haz_type, 'DR')
        self.assertEqual(hazard_set.size, 114)
        self.assertEqual(hazard_set.centroids.size, 130)
        self.assertEqual(hazard_set.intensity[112, 111], -1.6286273002624512)

# Execute Tests
if __name__ == "__main__":
    TESTS = unittest.TestLoader().loadTestsFromTestCase(TestReader)
    unittest.TextTestRunner(verbosity=2).run(TESTS)
