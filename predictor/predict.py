"""
predict.py
Module for running TensorFlow-based congestion prediction on traffic images.
"""
import tensorflow as tf
tf.compat.v1.disable_eager_execution()
import sys
import os
import logging
import threading

from urllib.request import Request, urlopen  # Python 3
import numpy as np

# Suppress TF log-info messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Global variables to cache the model and labels
_model_graph = None
_label_lines = None
_session = None
_graph_lock = threading.Lock()  # Multi-thread safe inference

MODEL_PATH = "./predictor/retrained_graph.pb"
LABEL_PATH = "./predictor/retrained_labels.txt"


def _load_model_and_labels():
    global _model_graph, _label_lines, _session
    if _model_graph is None or _session is None or _label_lines is None:
        _model_graph = tf.Graph()
        with _model_graph.as_default():
            with tf.io.gfile.GFile(MODEL_PATH, 'rb') as f:
                graph_def = tf.compat.v1.GraphDef()
                graph_def.ParseFromString(f.read())
                tf.import_graph_def(graph_def, name='')
        # Load labels
        _label_lines = [line.rstrip() for line in tf.io.gfile.GFile(LABEL_PATH)]
        # Create one session to be reused
        _session = tf.compat.v1.Session(graph=_model_graph)


def tensorflow_pred(imageUrl):
    """
    Predict congestion type for an image via TensorFlow retrained model.
    Loads the model and labels only once; uses thread lock for concurrency.
    """
    try:
        req = Request(
            imageUrl,
            headers={
                'User-Agent': 'Mozilla/5.0',
                'Referer': 'https://www.livetraffic.com/'
            }
        )
        response = urlopen(req)
        content_type = response.info().get_content_type()
        if content_type not in ['image/jpeg', 'image/png', 'image/gif', 'image/bmp']:
            return 'Not an image'
        image_data = response.read()
    except Exception as e:
        logging.error(f'Error fetching image from {imageUrl}: {e}')
        return 'Image fetch error'
    try:
        # Load model/labels if not already loaded
        with _graph_lock:
            _load_model_and_labels()
            sess = _session
            graph = _model_graph
            label_lines = _label_lines
            softmax_tensor = graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(
                softmax_tensor,
                {'DecodeJpeg/contents:0': image_data}
            )
            # Sort and get results
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            for node_id in top_k:
                congestion_type = label_lines[node_id]
                score = predictions[0][node_id]
                logging.info(f"Label: {congestion_type}, Score: {score}")
                if score >= 0.5:
                    return f'{congestion_type} (score = {score:.5f})'
            return 'Uncertain (no score >0.5)'
    except Exception as e:
        logging.error(f'Error during TensorFlow prediction: {e}')
        return 'Prediction error'
