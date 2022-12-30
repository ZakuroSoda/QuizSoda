from challenges import initDatabaseFromFiles
from auth import setupUserDB

initDatabaseFromFiles()
setupUserDB()

import os

os.system('pip install flask')