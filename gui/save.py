import os
import json

import gui
from gui.qt import *
from gui.utils import getFileToSave

def onSave(mw):
    # Save contents of framelist as a file, temporally whose extension is original '.emt'.
    filter = "Emotan Wordlist format (*.ewl)"
    newfile = getFileToSave(mw, "Save Wordlist", dir=mw.pref['workspace'], filter=filter)

    # Ignore if selected file is a directory by accident
    if os.path.isdir(newfile):
        return

    dataToSave = []
    with open(newfile, "w") as f:
        dataToSave.append(mw.framelist.setting.data())

        for ew in mw.framelist.getCurrentEntryWidgets():
            dataToSave.append(ew.data())

        json.dump(dataToSave, f, indent=4)