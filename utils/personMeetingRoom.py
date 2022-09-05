import os
import tensorflow as tf
from inferenceutils import *
import cv2
import time
import datetime
import mysql.connector
import pyodbc

#connect database
connect = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=sa; PWD=123456")
cursor = connect.cursor()

programsName = 'personMeetingRoom'
programsName = programsName.replace("'", "")

cursor = cursor.execute('UPDATE statusPrograms SET status=? WHERE programs=?', (True, programsName))
cursor.commit()

#aws
mydb = mysql.connector.connect(
  host="db-rds-ptf.cpuqyug93oho.ap-southeast-1.rds.amazonaws.com",
  user="ptfadmin",
  password="5DkMvfUgD6gE7aSREq7a57L92ssfWV",
  database="smartenergy"
)

path = os.getcwd().replace('\\', '/')

labelmap_path = path + '/utils/mscoco_label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(labelmap_path, use_display_name=True)
tf.keras.backend.clear_session()
model = tf.saved_model.load(path + "/utils/model")

path_img_after = path + "/utils/picture/img_after.png"

try:
    os.remove(path_img_after)
except:
    pass

path_camera = "rtsp://admin:999999999@192.168.1.207:10554/tcp/av0_0"
time_strf = time.strftime("%d-" "%m-" "%Y"" " "%H." "%M." "%S")

try:
    cap = cv2.VideoCapture(path_camera)
    while True:
        _, frame = cap.read()
        cv2.imwrite(path_img_after, frame)
        save_picture_success = True
        break
except:
    save_picture_success = False
    print('error ; not image for detect person'.upper())

if save_picture_success == True:
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
        min_score_thresh=0.5,
        line_thickness=2)

    count_len = 0
    count_person = 0
    print('class', (output_dict['detection_classes']))
    for i in (output_dict['detection_classes']):
        if i == 1:
            values_person = output_dict['detection_scores'][count_len] >= 0.9
            if values_person == True:
                count_person += 1
        count_len += 1

    image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    cv2.imwrite(path_img_after, image_np)
    if count_person >= 1:
        mycursor = mydb.cursor()
        mycursor.execute('UPDATE machine_noload_status SET status=1 WHERE id=1')
        mydb.commit()

    else:
        mycursor = mydb.cursor()
        mycursor.execute('UPDATE machine_noload_status SET status=0 WHERE id=1')
        mydb.commit()

    cv2.imshow('frame', image_np)
    cv2.waitKey(0)

cursor = cursor.execute('UPDATE statusPrograms SET status=? WHERE programs=?', (False, programsName))
cursor.commit()
print("------------------------------------------------------------------------")