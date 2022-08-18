import os
import subprocess

path = os.getcwd().replace('\\', '/')

subprocess.call([path + '/utils/detectPerson.bat'])