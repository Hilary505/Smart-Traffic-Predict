"""
predict.py
Module for running TensorFlow-based congestion prediction on traffic images.
"""
import tensorflow.compat.v1 as tf
import sys
import os
import logging

try:
    from urllib.request import Request, urlopen  # Python 3
except ImportError:
    from urllib2 import Request, urlopen  # Python 2
import numpy as np


def tensorflow_pred(imageUrl):
    #suppress TF log-info messages - remove to display TF logs 
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
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
            # Do not log or print anything for unsupported images
            return 'Not an image'
        image_data = response.read()
    except Exception as e:
        logging.error(f'Error fetching image from {imageUrl}: {e}')
        return 'Image fetch error'
    try:
        label_lines = [line.rstrip() for line 
                    in tf.io.gfile.GFile("./predictor/retrained_labels.txt")]
    except Exception as e:
        logging.error(f'Error loading label file: {e}')
        return 'Label file error'
    
    try:
        
        graph = tf.Graph()
        with graph.as_default(): 
            # Unpersists graph from file
                with tf.gfile.GFile("./predictor/retrained_graph.pb", 'rb') as f:
                    graph_def = tf.GraphDef()
                    graph_def.ParseFromString(f.read())
                    _ = tf.import_graph_def(graph_def, name='')

        with tf.Session(graph=graph) as sess:
                    # Feed the image_data as input to the graph and get first prediction
                    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
                    
                    predictions = sess.run(softmax_tensor, \
                            {'DecodeJpeg/contents:0': image_data})
                    
                    # Sort to show labels of first prediction in order of confidence
                    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
                    
                    for node_id in top_k:
                        congestion_type = label_lines[node_id]
                        score = predictions[0][node_id]
                        logging.info(f"Label: {congestion_type}, Score: {score}")  # Debug: print each label and score
                        if (score >=0.5):
                            
                            return ('%s (score = %.5f)' % (congestion_type, score))
                        
    except Exception as e:
        logging.error(f'Error during TensorFlow prediction: {e}')
        return 'Prediction error'
   
   
