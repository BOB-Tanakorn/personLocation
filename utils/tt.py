import os
import tensorflow as tf
from inferenceutils import *
import cv2
import time
import datetime
import mysql.connector
import pyodbc


print('{} >>> start detect person location meeting room'.title().format(datetime.datetime.now()))
start_time = time.time()

#connect database
connect = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=comVision; PWD=123456")
cursor = connect.cursor()

path = os.getcwd().replace('\\', '/')

labelmap_path = path + '/utils/mscoco_label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(labelmap_path, use_display_name=True)
tf.keras.backend.clear_session()
model = tf.saved_model.load(path + "/utils/model")

path_img_after = 'D:/computerVision/personLocation/utils/person.jpeg'

image_name = path_img_after
# image_name = path + '/utils/person.jpeg'
image_np = load_image_into_numpy_array(image_name)
output_dict = run_inference_for_single_image(model, image_np)
vis_util.visualize_boxes_and_labels_on_image_array(
    image_np,
    output_dict['detection_boxes'],
    output_dict['detection_classes'],
    output_dict['detection_scores'],
    category_index,
    instance_masks=output_dict.get('detection_masks_reframed', None),
    use_normalized_coordinates=True,
    skip_labels=False,
    skip_scores=True,
    skip_boxes=False,
    min_score_thresh=0.9,
    line_thickness=2)

print(output_dict['detection_classes'])