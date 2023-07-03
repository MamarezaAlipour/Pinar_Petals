"""

Test files_handler module.
"""

from pathlib import Path
import unittest
import xmlrunner

from pinar_petals.hazard.tc_tracks_forecast import TCForecast


class TestDataAvail(unittest.TestCase):
    """Test availability of data used through APIs"""

    def test_ecmwf_tc_bufr(self):
        """Test availability ECMWF essentials TC forecast."""
        fcast = TCForecast.fetch_bufr_ftp()
        [f.close() for f in fcast]


# Execute Tests
if __name__ == '__main__':
    TESTS = unittest.TestLoader().loadTestsFromTestCase(TestDataAvail)
    xmlrunner.XMLTestRunner(output=str(Path(__file__).parent.joinpath('tests_xml'))).run(TESTS)
