import os
import subprocess
import pyodbc
import time

pathBacthFile = os.getcwd().replace('\\', '/')

countMeetingRoom = 0

startMeetingRoom = 10

while True:
    countMeetingRoom += 1

    if countMeetingRoom == startMeetingRoom:
        detectMeetingRoom = True
        while detectMeetingRoom:
            #connect database
            connect = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=sa; PWD=123456")
            cursorMeetingRoom = connect.cursor()
            cursorMeetingRoom = cursorMeetingRoom.execute('SELECT status FROM statusPrograms')
            cursorMeetingRoom = cursorMeetingRoom.fetchall()

            for iMeetingRoom in cursorMeetingRoom:
                if iMeetingRoom[0] == False:
                    prgRedey = True
                else:
                    prgRedey = False
                    break
            time.sleep(5)
            if prgRedey == True:
                os.system(pathBacthFile + '/utils/meetingRoom.bat')
                timeProcess = 1
                countMeetingRoom = 0
                startMeetingRoom = 10
                detectMeetingRoom = False
    
    # break
    time.sleep(1)