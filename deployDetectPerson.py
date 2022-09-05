import os
import subprocess
import pyodbc
import time


while True:
    #connect database
    connect = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=sa; PWD=123456")
    cursor = connect.cursor()
    cursor = cursor.execute('SELECT status FROM statusPrograms')
    cursor = cursor.fetchall()

    for i in cursor:
        if i[0] == False:
            prgRedey = True
        else:
            prgRedey = False
            break


    if prgRedey == True:
        print('run')

    else:
        print('not run')
    
    # break
    time.sleep(5)