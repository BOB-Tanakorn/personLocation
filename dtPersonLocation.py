import os
import subprocess
import pyodbc
import time

pathBacthFile = os.getcwd().replace('\\', '/')

connect = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=comVision; PWD=123456")

locationMeeting = 'personMeetingRoom'
locationMeeting = locationMeeting.replace("'", "")
cursorMeeting = connect.execute('UPDATE statusPrograms SET status=? WHERE programs=?', (False, locationMeeting))
cursorMeeting.commit()

countMeetingRoom = 0

startMeetingRoom = 6

while True:
    countMeetingRoom += 1

    if countMeetingRoom == startMeetingRoom:
        detectMeetingRoom = True
        while detectMeetingRoom:
            timeMeetingRoom = 5
            #connect database
            connect = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=comVision; PWD=123456")
            cursorMeetingRoom = connect.cursor()
            runMeetingRoom = connect.cursor()
            cursorMeetingRoom = cursorMeetingRoom.execute('SELECT status FROM statusPrograms')
            cursorMeetingRoom = cursorMeetingRoom.fetchall()
            
            ltMeetingRoom = []
            for iMeetingRoom in cursorMeetingRoom:
                ltMeetingRoom.append(iMeetingRoom[0])

            if True in ltMeetingRoom:
                prgRedey = False
                pass
            else:
                prgRedey = True
                timeMeetingRoom = 1
                break

            time.sleep(timeMeetingRoom)
        if prgRedey == True:
            programsName = 'personMeetingRoom'
            programsName = programsName.replace("'", "")
            runMeetingRoom = runMeetingRoom.execute('UPDATE statusPrograms SET status=? WHERE programs=?', (True, programsName))
            runMeetingRoom.commit()
            os.system(pathBacthFile + '/utils/meetingRoom.bat')
            timeProcess = 1
            countMeetingRoom = 0
            startMeetingRoom = 900
            detectMeetingRoom = False
            runMeetingRoom = runMeetingRoom.execute('UPDATE statusPrograms SET status=? WHERE programs=?', (False, programsName))
            runMeetingRoom.commit()
    
    # break
    time.sleep(1)