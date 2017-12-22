import gui
from gui.qt import *
from gui.utils import getFile


class GroupButton(QPushButton):
    sig = pyqtSignal(str, str, int)

    def __init__(self, mw, group, dir, idx=0, filter="*.mp3", msg='Select a file'):
        super(GroupButton, self).__init__()
        self.mw = mw
        self.group = group
        self.idx = idx
        self.filter = filter
        self.dir = dir
        self.msg = msg
        self._ui()

    def _ui(self):
        self.setStyleSheet("QPushButton { background-color: rgb(200,200,200); "
                           "Text-align: left; }")

        self.setText("+ {group}".format(group=self.group))
        self.clicked.connect(self._on_file_select)

    def _on_file_select(self):
        file = getFile(self.mw, self.msg, dir=self.dir, filter=self.filter)
        if file:
            self.sig.emit(file, self.group, self.idx)

