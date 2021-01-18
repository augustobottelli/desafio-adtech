import os
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

import numpy as np
import ee
from keras import load_model

from exceptions import GEEException

CPU_COUNT = cpu_count()


class GEEClient:
    def __init__(self):
        self.ee = ee
        self.load_credentials()

    @staticmethod
    def load_credentials():
        try:
            account_mail = "abottelli@competencia-sadosky.iam.gserviceaccount.com"
            credentials = ee.ServiceAccountCredentials(account_mail, "private-key.json")
            ee.Initialize(credentials)
        except:
            GEEException("Failed to initialize credentials")

    @staticmethod
    def get_coord_bands(long, lat, start_date, end_date, scale=10, cloud_pixel_pct=10):
        generate_request = (
            ee.ImageCollection("COPERNICUS/S2_SR")
            .filterBounds(ee.Geometry.Point(long, lat))
            .filterDate(start_date, end_date)
            .filterMetadata("CLOUDY_PIXEL_PERCENTAGE", "less_than", cloud_pixel_pct)
            .reduce(ee.Reducer.mean())
            .reduceRegion(ee.Reducer.mean(), ee.Geometry.Point(long, lat), scale=scale)
        )
        pixel_bands = generate_request.getInfo()
        return pixel_bands


class Observation:
    def __init__(self, obs):
        self.X, self.y = self.get_features(obs)

    @staticmethod
    def generate_features(obs, label=None):
        obs["NDVI_mean"] = (obs["B8_mean"] - obs["B4_mean"]) / (
            obs["B8_mean"] + obs["B4_mean"]
        )
        obs["GNDVI_mean"] = (obs["B8_mean"] - obs["B3_mean"]) / (
            obs["B8_mean"] + obs["B3_mean"]
        )
        obs["SAVI_mean"] = (
            (obs["B8_mean"] - obs["B4_mean"])
            / (obs["B8_mean"] + obs["B4_mean"] + 0.428)
            * (1.428)
        )
        obs["NDMI_mean"] = (obs["B8_mean"] - obs["B11_mean"]) / (
            obs["B8_mean"] + obs["B11_mean"]
        )
        obs["MSI_mean"] = obs["B11_mean"] / obs["B8_mean"]
        obs["GCI_mean"] = (obs["B9_mean"] / obs["B3_mean"]) - 1
        obs["BSI_mean"] = (
            (obs["B11_mean"] + obs["B4_mean"]) - (obs["B8_mean"] + obs["B2_mean"])
        ) / ((obs["B11_mean"] + obs["B4_mean"]) + (obs["B8_mean"] + obs["B2_mean"]))
        return obs

    def get_features(self, obs, label=None):
        features = self.generate_features(obs, label=label)
        undesired_cols = ["MSK_SNWPRB_mean", "QA10_mean", "QA20_mean"]
        X_cols = [col for col in obs if col.endswith("mean") and col not in undesired_cols]
        X = {col: obs.get(col) for col in X_cols}
        y = np.array(obs[label]) if label else None
        return X, y


def run_prediction(coordinates):
    pass
