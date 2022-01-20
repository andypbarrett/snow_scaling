'''Paths and utilities to get file lists'''

from pathlib import Path

SNOW_SCALING_PATH = Path(
    "/",
    "media",
    "apbarret",
    "andypbarrett_work",
    "Data",
    "Snow_Scaling"
    )

RAW_DATA_PATH = SNOW_SCALING_PATH / "NSIDC_ASO_DATA"

TUOLOME_TIFFS = RAW_DATA_PATH.glob('*.tif')

