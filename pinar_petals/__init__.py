"""

pinar init
"""
from shutil import copyfile
from pathlib import Path

import pinar
import pinar_petals.util.config
from .util.constants import *

REPO_DATA = {
    'data/system': [
        SYSTEM_DIR.joinpath('GDP2Asset_converter_2.5arcmin.nc'),
    ],
    'data/demo': [
        HAZ_DEMO_FLDDPH,
        HAZ_DEMO_FLDFRC,
        DEMO_GDP2ASSET,
        DEMO_DIR.joinpath('crop_production_demo_data_yields_CHE.nc4'),
        DEMO_DIR.joinpath('crop_production_demo_data_cultivated_area_CHE.nc4'),
        DEMO_DIR.joinpath('FAOSTAT_data_producer_prices.csv'),
        DEMO_DIR.joinpath('FAOSTAT_data_production_quantity.csv'),
        DEMO_DIR.joinpath('gepic_gfdl-esm2m_ewembi_historical_2005soc_co2_yield-whe-noirr_global_DEMO_TJANJIN_annual_1861_2005.nc'),
        DEMO_DIR.joinpath('hist_mean_mai-firr_1976-2005_DE_FR.hdf5'),
        DEMO_DIR.joinpath('histsoc_landuse-15crops_annual_FR_DE_DEMO_2001_2005.nc'),
        DEMO_DIR.joinpath('lpjml_ipsl-cm5a-lr_ewembi_historical_2005soc_co2_yield-whe-noirr_annual_FR_DE_DEMO_1861_2005.nc'),
        DEMO_DIR.joinpath('pepic_miroc5_ewembi_historical_2005soc_co2_yield-whe-firr_global_annual_DEMO_TJANJIN_1861_2005.nc'),
        DEMO_DIR.joinpath('pepic_miroc5_ewembi_historical_2005soc_co2_yield-whe-noirr_global_annual_DEMO_TJANJIN_1861_2005.nc'),
        DEMO_DIR.joinpath('Portugal_firms_June_2017.csv'),
        DEMO_DIR.joinpath('Portugal_firms_2016_17_18_MODIS.csv'),
    ]
}


def copy_repo_data(reload=False):
    for src_dir, path_list in REPO_DATA.items():
        for path in path_list:
            if not path.exists() or reload:
                src = Path(__file__).parent.parent.joinpath(src_dir, path.name)
                copyfile(src, path)

copy_repo_data()
