"""

Test tc_tracks_forecast module.
"""

import unittest
import numpy as np
import pandas as pd

from pinar import CONFIG
from pinar_petals.hazard.tc_tracks_forecast import TCForecast

DATA_DIR = CONFIG.hazard.test_data.dir()
TEST_BUFR_FILES = [
    DATA_DIR.joinpath(tbf) for tbf in [
        'tracks_22S_HEROLD_2020031912.det.bufr4',
        'tracks_22S_HEROLD_2020031912.eps.bufr4',
    ]
]
TEST_BUFR_FILE_MULTIMESSAGE = DATA_DIR.joinpath('test202204181200.bufr')
"""TC tracks in four BUFR formats as provided by ECMWF. Sourced from
https://confluence.ecmwf.int/display/FCST/New+Tropical+Cyclone+Wind+Radii+product
"""

TEST_CXML_FILE = DATA_DIR.joinpath("cxml_sample_track.xml")
"""A sample CXML file holding forecast data, subset from the ECMWF archive at
https://confluence.ecmwf.int/display/TIGGE/Tools#Tools-ECMWFTropicalCycloneTrackData(XMLformat)
"""

TEST_XSL_FILE = DATA_DIR.joinpath("cxml_sample_transf_w_60h_72h_filter.xsl")
"""A sample non-standard xsl file to only extract specific forecast ranges
"""


class TestECMWF(unittest.TestCase):
    """Test reading of BUFR TC track forecasts"""

    def test_fetch_ecmwf(self):
        """Test ECMWF reader with static files"""
        forecast = TCForecast()
        forecast.fetch_ecmwf(files=TEST_BUFR_FILES)

        self.assertEqual(forecast.data[0].time.size, 3)
        self.assertEqual(forecast.data[1].lat[2], -27.)
        self.assertEqual(forecast.data[0].lon[2], 73.5)
        self.assertEqual(forecast.data[1].time_step[2], 6)
        self.assertEqual(forecast.data[1].max_sustained_wind[2], 14.9)
        self.assertEqual(forecast.data[0].central_pressure[1], 1000.)
        self.assertEqual(forecast.data[0]['time.year'][1], 2020)
        self.assertEqual(forecast.data[16]['time.month'][7], 3)
        self.assertEqual(forecast.data[16]['time.day'][7], 21)
        self.assertEqual(forecast.data[0].max_sustained_wind_unit, 'm/s')
        self.assertEqual(forecast.data[0].central_pressure_unit, 'mb')
        self.assertEqual(forecast.data[1].sid, '22S')
        self.assertEqual(forecast.data[1].name, 'HEROLD')
        np.testing.assert_array_equal(forecast.data[0].basin, 'S')
        self.assertEqual(forecast.data[0].category, 'Tropical Depression')
        self.assertEqual(forecast.data[0].run_datetime,
                         np.datetime64('2020-03-19T12:00:00.000000'))
        self.assertEqual(forecast.data[1].is_ensemble, True)


    def test_ecmwf_multimessage(self):
        """Test ECMWF reader in multimessage format"""
        forecast = TCForecast()
        forecast.fetch_ecmwf(files=TEST_BUFR_FILE_MULTIMESSAGE)

        self.assertEqual(forecast.size, 122)
        self.assertEqual(forecast.data[121].lat[2], 9.6)
        self.assertEqual(forecast.data[121].lon[2], -126.8)
        np.testing.assert_array_equal(
            np.unique(
                [forecast.data[ind_i].name
                 for ind_i in np.arange(122)]
                ),
            np.array(['70E', '70W', '71E', '71W', '72W'], dtype='<U3')
            )


    def test_equal_timestep(self):
        """Test equal timestep"""
        forecast = TCForecast()
        forecast.fetch_ecmwf(files=TEST_BUFR_FILES)
        forecast.equal_timestep(1)

        self.assertEqual(forecast.data[1].time.size, 13)
        self.assertEqual(forecast.data[1].lat.size, 13)
        self.assertEqual(forecast.data[1].lon.size, 13)
        self.assertEqual(forecast.data[1].max_sustained_wind.size, 13)
        self.assertEqual(forecast.data[1].central_pressure.size, 13)
        self.assertEqual(forecast.data[1].radius_max_wind.size, 13)
        self.assertEqual(forecast.data[1].environmental_pressure.size, 13)
        self.assertEqual(forecast.data[1].time_step[2], 1.)

    def test_hdf5_io(self):
        """Test writting and reading hdf5 TCTracks instances"""
        tc_track = TCForecast()
        tc_track.fetch_ecmwf(files=TEST_BUFR_FILES)
        path = DATA_DIR.joinpath("tc_tracks_forecast.h5")
        tc_track.write_hdf5(path)
        tc_read = TCForecast.from_hdf5(path)
        path.unlink()

        self.assertEqual(len(tc_track.data), len(tc_read.data))
        for tr, tr_read in zip(tc_track.data, tc_read.data):
            self.assertEqual(set(tr.attrs.keys()), set(tr_read.attrs.keys()))
            self.assertEqual(set(tr.variables), set(tr_read.variables))
            self.assertEqual(set(tr.coords), set(tr_read.coords))
            for key in tr.attrs.keys():
                self.assertEqual(tr.attrs[key], tr_read.attrs[key])
            for v in tr.variables:
                self.assertEqual(tr[v].dtype, tr_read[v].dtype)
                np.testing.assert_array_equal(tr[v].values, tr_read[v].values)
            self.assertEqual(tr.sid, tr_read.sid)


class TestCXML(unittest.TestCase):
    """Test that cxml track data can be read."""

    def test_default_xsl(self):
        """ "Test with default XSL conversion"""
        forecast = TCForecast.read_cxml(TEST_CXML_FILE)

        self.assertEqual(len(forecast.data), 7)
        self.assertTrue(
            all(
                forecast.data[0].time.data
                == np.array(
                    [
                        "2022-03-02T12:00:00",
                        "2022-03-02T18:00:00",
                        "2022-03-03T00:00:00",
                        "2022-03-03T06:00:00",
                        "2022-03-03T12:00:00",
                        "2022-03-03T18:00:00",
                        "2022-03-04T00:00:00",
                        "2022-03-04T06:00:00",
                        "2022-03-04T12:00:00",
                        "2022-03-04T18:00:00",
                        "2022-03-05T00:00:00",
                        "2022-03-05T06:00:00",
                        "2022-03-05T12:00:00",
                        "2022-03-05T18:00:00",
                        "2022-03-06T00:00:00",
                        "2022-03-06T06:00:00",
                        "2022-03-06T12:00:00",
                        "2022-03-06T18:00:00",
                        "2022-03-07T00:00:00",
                        "2022-03-07T06:00:00",
                        "2022-03-07T12:00:00",
                        "2022-03-07T18:00:00",
                        "2022-03-08T12:00:00",
                    ],
                    dtype="datetime64[ns]",
                )
            )
        )
        self.assertEqual(forecast.data[0].name, "Vernon")
        self.assertTrue(all([i.ensemble_number == '24' for i in forecast.data]))
        self.assertEqual(
            forecast.data[2].run_datetime,
            pd.Timestamp('2022-03-02 12:00:00+0000', tz='UTC'),
        )
        self.assertTrue(forecast.data[4].is_ensemble)

    def test_custom_xsl(self):
        """Test with custom XSL conversion"""
        forecast = TCForecast.read_cxml(
            cxml_path=TEST_CXML_FILE, xsl_path=TEST_XSL_FILE
        )
        self.assertEqual(len(forecast.data), 6)
        self.assertEqual(forecast.data[0].time.size, 3)
        self.assertEqual([f.time.size for f in forecast.data], [3, 3, 3, 3, 2, 1])


# Execute Tests
if __name__ == "__main__":
    TESTS = unittest.TestLoader().loadTestsFromTestCase(TestECMWF)
    TESTS.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCXML))
    unittest.TextTestRunner(verbosity=2).run(TESTS)
