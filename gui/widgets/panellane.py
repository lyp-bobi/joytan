# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html


from gui.qt import *
from gui.utils import getFile
from joytan.routine.gimage import GimageThread


class Panel(QPushButton):
    _STATE_MSG = {'INIT': None,
                  'WORK': 'Downloading',
                  'WAIT': 'Waiting',
                  'DONE': ''}
    LOCAL_MSG = "Image locally uploaded"
    FIXED_SIZE = (148, 148)

    delete = pyqtSignal(int)
    upload = pyqtSignal(int, str)

    def __init__(self, state, count):
        super().__init__()
        self.state = None
        self.count = count
        self.state_manager(state)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self._click_menu()

    def _click_menu(self):
        m = QMenu()
        a = m.addAction("Delete")
        a.triggered.connect(lambda: self.delete.emit(self.count))
        if self.state != 'DONE':
            a.setDisabled(True)
        a = m.addAction("Set image")
        a.triggered.connect(self._on_file_select)

        m.exec_(QCursor.pos())

    def _on_file_select(self):
        try:
            imgpath = getFile(None, "Select an Image", filter="Images (*.jpg *.jpeg *.png)",
                              dir=os.getcwd())
            self.set_image(imgpath)
            self.upload.emit(self.count, imgpath)
        except:
            return

    def set_image(self, imgpath):
        pixmap = QPixmap(imgpath).scaled(*self.FIXED_SIZE)
        self.setIcon(QIcon(pixmap))
        self.setIconSize(pixmap.rect().size())
        self.state_manager('DONE')

    def state_manager(self, state):
        # List of state:
        # 'INIT': Initial state. Show the indices of panels in the lane and disable clicking,
        # 'WORK' Downloading in process. Use defined message and disable clicking
        # 'WAIT': Waiting for download thread. Use defined message and disable clicking
        # 'DONE': Image successfully downloaded and set. Enable right clicking.
        if state == 'INIT':
            self.setIcon(QIcon())
            self.setText('%d' % (self.count + 1))
            self.setDisabled(False)
        elif state == 'WORK':
            self.setText(self._STATE_MSG[state])
            self.setDisabled(True)
        elif state == 'WAIT':
            self.setText(self._STATE_MSG[state])
            self.setDisabled(True)
        elif state == 'DONE':
            self.setText(self._STATE_MSG[state])
            self.setDisabled(False)
        else:
            raise Exception("Invalid Panel state %s" % state)

        self.state = state


class PanelLane(QListWidget):

    def __init__(self, group, following, destdir, maximg):
        super(PanelLane, self).__init__()
        self.group = group
        self.destdir = destdir
        self.maximg = maximg
        self.thread = GimageThread(' '.join([self.group, following]), destdir)
        self.thread.upload.connect(self.on_set_image)
        self.thread.finished.connect(self.on_finish_working)

        # Because QPixmap doesn't store the path of they image they display,
        # all paths of images and URL are stored as tuple like ('imgpath', 'link')
        self.imglist = [('', '') for _ in range(self.maximg)]

        self.setFlow(QListView.LeftToRight)
        self.setFixedHeight(150)

        for i in range(self.maximg):
            panel = Panel('INIT', i)
            panel.delete.connect(self.on_image_delete)
            panel.upload.connect(self.on_local_upload)
            panel.setFixedSize(*Panel.FIXED_SIZE)
            lwi = QListWidgetItem()
            lwi.setSizeHint(panel.size())
            self.addItem(lwi)
            self.setItemWidget(lwi, panel)

    def on_image_delete(self, count):
        self.imglist[count] = ('', '')
        self._get_panel(count).state_manager('INIT')

    @pyqtSlot(int, str)
    def on_local_upload(self, count, imgpath):
        self.on_image_delete(count)
        p = self._get_panel(count)
        p.set_image(imgpath)
        self.imglist[count] = (imgpath, 'Image locally uploaded')
        return

    def on_set_image(self, imgpath, link):
        """
        Check from left to right among panels,
        set the new image to any panel not in "DONE" state. 
        """
        for i in range(self.count()):
            p = self._get_panel(i)
            if p.state != 'DONE':
                p.set_image(imgpath)
                self.imglist[i] = (imgpath, link)
                break

    def on_download(self):
        ready = self.count_initial()
        if ready:
            self.set_panels_state("WORK")
            self.thread.set_total(ready)
            self.thread.start()

    def count_initial(self):
        """
        Count the number of panels in the "INIT" state, 
        which is ready to spawn a new thread for downloading images
        """
        initial = 0
        for i in range(self.count()):
            p = self._get_panel(i)
            if p.state == 'INIT':
                initial += 1
        return initial

    def set_panels_state(self, new_state):
        """
        Unify the state of panels 
        """
        assert new_state != "DONE"
        for i in range(self.count()):
            p = self._get_panel(i)
            if p.state in ['INIT', 'WAIT']:
                p.state_manager(new_state)

    def clear_all(self):
        """
        Clear all images of panels in the lane 
        """
        for i in range(self.count()):
            self.on_image_delete(i)

    @pyqtSlot(str)
    def on_update_following(self, following):
        self.thread.update_keyword(' '.join([self.group, following]))

    @pyqtSlot()
    def on_finish_working(self):
        for i in range(self.count()):
            p = self._get_panel(i)
            if p.state  == 'WORK':
                p.state_manager('INIT')
            elif p.state == 'WAIT':
                raise Exception("Thread finishes in invalid time. (Some of panel is still waiting)")

    def force_finish(self):
        for i in range(self.count()):
            p = self._get_panel(i)
            if p.state != 'DONE':
                p.state_manager('INIT')

    def _get_panel(self, cnt):
        return self.itemWidget(self.item(cnt))
