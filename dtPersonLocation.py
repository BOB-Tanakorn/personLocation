import os
import subprocess
import pyodbc
import time

pathBacthFile = os.getcwd().replace('\\', '/')

connect = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=sa; PWD=123456")

locationMeeting = 'personMeetingRoom'
locationMeeting = locationMeeting.replace("'", "")
cursorMeeting = connect.execute('UPDATE statusPrograms SET status=? WHERE programs=?', (False, locationMeeting))
cursorMeeting.commit()

countMeetingRoom = 0

startMeetingRoom = 600

while True:
    countMeetingRoom += 1

    if countMeetingRoom == startMeetingRoom:
        detectMeetingRoom = True
        while detectMeetingRoom:
            #connect database
            connect = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=sa; PWD=123456")
            cursorMeetingRoom = connect.cursor()
            runMeetingRoom = connect.cursor()
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
                programsName = 'personMeetingRoom'
                programsName = programsName.replace("'", "")
                runMeetingRoom = runMeetingRoom.execute('UPDATE statusPrograms SET status=? WHERE programs=?', (True, programsName))
                runMeetingRoom.commit()
                os.system(pathBacthFile + '/utils/meetingRoom.bat')
                timeProcess = 1
                countMeetingRoom = 0
                startMeetingRoom = 600
                detectMeetingRoom = False
                runMeetingRoom = runMeetingRoom.execute('UPDATE statusPrograms SET status=? WHERE programs=?', (False, programsName))
                runMeetingRoom.commit()
    
    # break
    time.sleep(1)