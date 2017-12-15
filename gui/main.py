# Copyright: Koki Mametani <kokimametani@gmail.com>
from gui.qt import *
from gui.utils import isMac, isLin, isWin
from gui import ICONS
import gui


def defaultSetting():
    import os, json
    cwd = os.getcwd()
    setting = None

    with open(os.path.join(cwd, "mysetting.json"), 'r') as f:
        setjs = json.loads(f.read())

    if isLin:
        setting = setjs['linux']
    elif isMac:
        setting = setjs['mac']
    elif isWin:
        setting = setjs['windows']


    return {
        "workspace": os.path.join(*setting['workspace']),
        "tts": setting['tts'],
        "title": setjs['title'],
        "sfxdir": os.path.join(cwd, "templates", "sfx"),
        "worddir": os.path.join(cwd, "templates", "wordlist"),
        "bgmdir": os.path.join(cwd, "templates", "song"),
    }

class EmotanMW(QMainWindow):
    def __init__(self, app, args):
        QMainWindow.__init__(self)
        gui.mw = self
        self.app = app

        self.setting = defaultSetting()
        print(self.setting)

        self.initUi()
        self.entryMode = "View"

        self.center()
        self.show()

    def initUi(self):
        self.setupMainWindow()
        self.setupMenus()
        self.setupEntryList()
        self.setupButtons()
        self.setupProgress()

    def getProjectPath(self):
        return os.path.join(self.setting['workspace'], self.setting['title'])

    def setupMainWindow(self):
        self.form = gui.forms.main.Ui_MainWindow()
        self.form.setupUi(self)

    def setupEntryList(self):
        import gui.entrylist
        self.entrylist = gui.entrylist.EntryList()
        self.form.verticalLayout.insertWidget(0, self.entrylist)

    def setupMenus(self):
        form = self.form
        # Fixme: Failed to use the original name 'actionExtract' on Qt Designer
        form.actionExtract_2.triggered.connect(self.onExtract)
        form.actionPreferences.triggered.connect(self.onPreferences)
        form.actionCopy.triggered.connect(self.onCopy)
        form.actionSave.triggered.connect(self.onSave)
        form.actionOpen.triggered.connect(self.onOpen)

    def setupButtons(self):
        form = self.form
        form.addButton.setIcon(QIcon('{}/plus_button_green.png'.format(ICONS)))
        form.delButton.setIcon(QIcon('{}/minus_button_red.png'.format(ICONS)))
        form.dlButton.setIcon(QIcon('{}/dl_button.png'.format(ICONS)))
        form.modeButton.setIcon(QIcon('{}/edit_button.png'.format(ICONS)))
        form.transButton.setIcon(QIcon('{}/translate_button2.png'.format(ICONS)))
        form.configButton.setIcon(QIcon('{}/config_button.png'.format(ICONS)))
        form.addButton.clicked.connect(lambda: self.entrylist.addEntry('', self.entryMode))
        form.delButton.clicked.connect(self.entrylist.deleteSelected)
        form.dlButton.clicked.connect(self.onDownload)
        form.modeButton.clicked.connect(self.onUpdateMode)
        form.transButton.clicked.connect(self.onTranslate)
        form.configButton.clicked.connect(self.onConfigure)
        form.audioButton.clicked.connect(self.onCreateMp3)
        form.textButton.clicked.connect(self.onCreateText)

    def setupProgress(self):
        import gui.progress
        self.progress = gui.progress.ProgressManager(self)

    def onPreferences(self):
        gui.dialogs.open("Preferences", self)

    def onOpen(self):
        import gui.open
        gui.open.onOpen(self)

    def onSave(self):
        import gui.save
        gui.save.onSave(self)

    def onExtract(self):
        import gui.extract
        gui.extract.onExtract(self)

    def onUpdateMode(self):
        if self.entryMode == "View":
            # Change EntryList Mode to "Edit" and the icon to "View"
            self.form.modeButton.setIcon(QIcon("{}/disp_button.png".format(ICONS)))
            self.entrylist.updateMode("Edit")
            self.entryMode = "Edit"
        elif self.entryMode == "Edit":
            self.form.modeButton.setIcon(QIcon("{}/edit_button.png".format(ICONS)))
            self.entrylist.updateMode("View")
            self.entrylist.updateAll()
            self.entryMode = "View"


    def onDownload(self):
        # To update 'Empty entry' if a name is added to it
        self.entrylist.updateAll()
        import gui.download
        gui.download.onDownload(self)

    def onTranslate(self):
        # To update 'Empty entry' if a name is added to it
        self.entrylist.updateAll()
        import gui.translate
        gui.translate.onTranslate(self)

    def onConfigure(self):
        gui.dialogs.open("Preferences", self, tab="TTS")

    def onCreateMp3(self):
        # To update 'Empty entry' if a name is added to it
        self.entrylist.updateAll()
        import gui.audiodialog
        gui.audiodialog.onMp3Dialog(self)

    def onCreateText(self):
        import gui.textdialog
        gui.textdialog.onTextDialog(self)


    def onCopy(self):
        import gui.smartcopy
        gui.smartcopy.onCopy(self)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
