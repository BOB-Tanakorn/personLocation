@echo on

SET mypath=%~dp0

call C:\ProgramData\anaconda3\Scripts\activate.bat
C:\Users\PTF\anaconda3\envs\tf\python.exe %mypath:~0,-1%"\meetingRoom.py"