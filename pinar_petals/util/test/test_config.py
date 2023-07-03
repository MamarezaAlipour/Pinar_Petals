"""

Test config module.
"""
import unittest
from pathlib import Path

from pinar.util.constants import SYSTEM_DIR
from pinar.util.config import CONFIG

class TestConfig(unittest.TestCase):
    """Test Config methods"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_petals_config_supersession(self):
        """Check whether the petals configuration correctly supersedes."""
        self.assertEqual(CONFIG._comment.str(), "this is a pinar_petals configuration file meant"
            " to supersede the default configuration in pinar_petals/conf during test")
        self.assertEqual(SYSTEM_DIR, Path.home().joinpath('pinar', 'data'))


# Execute Tests
if __name__ == "__main__":
    TESTS = unittest.TestLoader().loadTestsFromTestCase(TestConfig)
    unittest.TextTestRunner(verbosity=2).run(TESTS)
