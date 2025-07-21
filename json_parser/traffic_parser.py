"""
traffic_parser.py
Module for fetching live traffic data from NSW API and running congestion prediction.
"""

import json
from predictor import predict
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import http.client as httplib
from urllib.request import Request, urlopen  # Python 3
import os
import logging



def get_traffic(query):
    """
    Fetch traffic camera data for a given region and predict congestion type for each camera image.
    Args:
        query (str): Region code to filter traffic cameras.
    Returns:
        list: List of dictionaries with traffic camera info and prediction results.
    """
    try:
        api_key = os.environ.get('NSW_API_KEY')
        if not api_key:
            logging.error('NSW_API_KEY environment variable not set')
            raise ValueError('NSW_API_KEY environment variable not set')
        headers = {
            "Authorization": f"apikey {api_key}",
            "Connection": "keep-alive"
        }

        featureJson = {
            "properties": {
                "region": query,
            }
        }

        region = featureJson['properties']['region']
        url = 'https://api.transport.nsw.gov.au/v1/live/cameras'
        request = Request(url, None, headers)

        try:
            data = urlopen(request).read()
        except Exception as e:
            logging.error(f'Error fetching data from NSW API: {e}')
            return []

        try:
            features = json.loads(data).get('features')
        except Exception as e:
            logging.error(f'Error parsing JSON response: {e}')
            return []
        traffic = []

        for feature in features:
            response = feature['properties']
            camera_title = response.get("title", "Unknown")
            camera_region = response.get("region", "Unknown")
            camera_url = response.get("href", "")
            if not response.get("region"):
                logging.info(f"Skipping camera '{camera_title}' (no region)")
                continue
            # logging.info(f"Camera: '{camera_title}' | Region: {camera_region} | URL: {camera_url}")
            if response.get("region") == region:
                try:
                    prediction = predict.tensorflow_pred(camera_url)
                except Exception as e:
                    logging.error(f'Prediction error for image {camera_url}: {e}')
                    prediction = 'Prediction error'
                traffic.append({
                    "region": response["region"],
                    "title": response["title"],
                    "view": response["view"],
                    "direction": response["direction"],
                    "href": response["href"],
                    "predict": prediction
                })

        return traffic
    except Exception as e:
        logging.error(f'Unhandled error in get_traffic: {e}')
        return []
