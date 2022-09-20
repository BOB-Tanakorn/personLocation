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

def _lineNotify(payload,file=None):
    import requests
    url = 'https://notify-api.line.me/api/notify'
    token = 'L6EXQTUrlZT0Bz7D9LV5HLwDTiG4BkQ1FI6yvnVJdSa'	#กลุ่มตรวจสอบวัตถุดิบ
    # token = "EVPO0TRxPKQO8QtoIkX2p1uQFVuumR2FEUccTjYDoOY" #กลุ่มเทส she
    # token = '8edczGWSP1hnMeLXKfXseH8Ck1CATRTvLRL5CFSb3PW'	#she
    headers = {'Authorization':'Bearer '+token}
    return requests.post(url, headers=headers , data = payload, files=file)


def notifyFile(filename, person):
    file = {'imageFile':open(filename,'rb')}
    payload = {'message':'แจ้งเตือน ตรวจพบบุคคลในห้องประชุมจำนวนคน : {} คน'.format(person)}
    return _lineNotify(payload,file)

try:
    #aws
    mydb = mysql.connector.connect(
    host="db-rds-ptf.cpuqyug93oho.ap-southeast-1.rds.amazonaws.com",
    user="ptfadmin",
    password="5DkMvfUgD6gE7aSREq7a57L92ssfWV",
    database="smartenergy"
    )
except:
    print('{} >>> not connect cloud AWS !!!'.upper().format(datetime.datetime.now()))

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

path_camera = "rtsp://admin:888888@192.168.1.207:10554/tcp/av0_0"
timeStrf = time.strftime("%d-" "%m-" "%Y""_" "%H." "%M." "%S")

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
        skip_boxes=False,
        min_score_thresh=0.9,
        line_thickness=2)

    countLen = 0
    countPerson = 0
    # print('class', (output_dict['detection_classes']))
    for i in (output_dict['detection_classes']):
        if i == 1:
            valuesPerson = output_dict['detection_scores'][countLen] >= 0.9
            if valuesPerson == True:
                countPerson += 1
        countLen += 1

    image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    cv2.imwrite(path_img_after, image_np)

    if countPerson >= 1:
        cv2.imwrite(path + '/utils/picture/dataPicture/meetingRoom_{}.png'.format(timeStrf), frame)
        try:
            notifyFile(path_img_after, countPerson)
        except:
            print('{} >>> not send line check internet connection'.title().format(datetime.datetime.now()))

        try:
            mycursor = mydb.cursor()
            mycursor.execute('UPDATE machine_noload_status SET status=1 WHERE id=1')
            mydb.commit()
        except:
            print('{} >>> not update value to data base check internet connection'.title().format(datetime.datetime.now()))

    else:
        # notifyFile(path_img_after, countPerson)
        try:
            mycursor = mydb.cursor()
            mycursor.execute('UPDATE machine_noload_status SET status=0 WHERE id=1')
            mydb.commit()
        except:
            print('{} >>> not update value to data base check internet connection'.title().format(datetime.datetime.now()))

    # cv2.imshow('frame', image_np)
    # cv2.waitKey(0)

cap.release()
# cv2.destroyAllWindows()

elapsed = time.time() - start_time
print("Done in ", elapsed, " second(s)")

print('{} >>> end detect person location meeting room'.title().format(datetime.datetime.now()))