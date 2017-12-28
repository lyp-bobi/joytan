import gui
from gui.qt import *
from gui.widgets.fileselector import FileSelector
from gui.widgets.panellane import *
from gui.utils import path2filename, showCritical


def on_textdialog(mw):
    gui.dialogs.open("TextDialog", mw)


# Not in use
class TxtThread(QThread):
    def __init__(self, mw, dest):
        QThread.__init__(self)
        self.mw = mw
        self.dest = dest

    def run(self):
        ftxt = open("{dest}/{title}.txt".format(dest=self.dest, title=self.mw.setting['title']), 'w')
        for i in range(self.mw.entrylist.count()):
            ew = self.mw.entrylist.get_entry_at(i)
            ftxt.write("{index}. {name}\n".format(
                index=ew.row+1, name=ew.editors['atop'].text()))
            for j in range(0, ew.lv1):
                if ew.editors['def-%d' % (j + 1)].text() != '':
                    ftxt.write(ew.editors['def-%d' % (j + 1)].text() + '\n')
                for k in range(0, ew.lv2):
                    if ew.editors['ex-%d-%d' % (j + 1, k + 1)].text() != '':
                        ftxt.write('\t' + ew.editors['ex-%d-%d' % (j + 1, k + 1)].text() + '\n')
            ftxt.write('\n')
        ftxt.close()


# Not in use
class HtmlThread(QThread):
    def __init__(self, mw, dest):
        QThread.__init__(self)
        self.mw = mw
        self.dest = dest

    def run(self):
        datas = [ew.data() for ew in self.mw.entrylist.get_entry_all()]

        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader('templates/html'))
        temp = env.get_template('words.html')
        rendered_temp = temp.render(entries=datas)

        with open('{dest}/{title}.html'.format(dest=self.dest, title=self.mw.setting['title']), 'w') as f:
            f.write(rendered_temp)


class BookDesign:
    def __init__(self, path):
        self.path = path
        self.name = path2filename(path)
        self.maximg = self._parse_maximg(path)
        self.info = "%s / image:%d" % (self.name, self.maximg)

    def _parse_maximg(self, path):
        import re

        with open(path, 'r') as f:
            vimg = re.compile(r'<!---maximg:(\d*)--->')
            res = vimg.search(f.readline())
            assert res

        return int(res.group(1))


class TextDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.book = None
        self.destdir = os.path.join(mw.basepath(), "text")
        if os.path.isdir(self.destdir):
            import shutil
            shutil.rmtree(self.destdir)
        os.makedirs(self.destdir)
        self.form = gui.forms.textdialog.Ui_TextDialog()
        self.form.setupUi(self)
        self.form.startBtn.clicked.connect(self._on_create)
        self._ui()
        self.show()

    def _ui(self):
        # Use QLineEdit as QLabel with disabling selection
        label = self.form.designLbl
        label.selectionChanged.connect(label.deselect)
        self.form.designBtn.clicked.connect(self._on_design_select)
        self.form.dlall.clicked.connect(self._autodownload)
        self.form.clearAll.clicked.connect(self._clear_all_images)

        # FIXME: Temporal default setting
        path  = os.path.abspath('./templates/html/words.html')
        os.path.abspath(path)
        bd = BookDesign(path)
        self.book = bd
        self._activate_imglist()
        self.form.designLbl.setText(bd.info)

    def _autodownload(self):
        if not self.book:
            showCritical("Please select book design.")
            return

        for i in range(self.mw.entrylist.count()):
            lane = self._get_lane(i)
            lane.wait_all()

        # The actual class to be run in the following pool
        class Worker(QRunnable):
            def __init__(self, lane):
                QRunnable.__init__(self)
                self.lane = lane

            def run(self):
                self.lane.start_working()
                self.lane.thread.run()

        self.pool = QThreadPool()
        # Only 4 threads working at the same time
        self.pool.setMaxThreadCount(4)

        for i in range(self.mw.entrylist.count()):
            lane = self._get_lane(i)
            waiting = lane.is_waiting()
            if waiting:
                lane.thread.set_total(waiting)
                self.pool.start(Worker(lane))

    def _activate_imglist(self):
        assert self.book, "Book design is not defined"

        _list = self.form.imgList
        for i, ew in enumerate(self.mw.entrylist.get_entry_all()):
            if ew.editors['atop'].text() == '':
                # if ew is empty, ignore it
                # FIXME: Change 'pass' to 'continue' on final version
                pass
            group = ew.editors['atop'].text()
            destdir = os.path.join(self.destdir, ew.str_index())
            lwi1 = QListWidgetItem()
            lwi2 = QListWidgetItem()
            pb = QPushButton('+ Download %s' % group)
            ip = PanelLane(group, self.form.followEdit.text(), destdir, self.book.maximg)
            pb.clicked.connect(ip.on_download)
            lwi1.setSizeHint(pb.sizeHint())
            self.form.followEdit.textChanged.connect(ip.on_update_following)
            lwi2.setSizeHint(ip.size())

            _list.addItem(lwi1)
            _list.setItemWidget(lwi1, pb)
            _list.addItem(lwi2)
            _list.setItemWidget(lwi2, ip)

    def _on_design_select(self):
        from gui.utils import getFile
        try:
            path = getFile(self, "Select book design", dir=os.getcwd(),
                           filter="Jinja template HTML file (*.html)")
        except:
            return
        try:
            bd = BookDesign(path)
            self.book = bd
            self._activate_imglist()
            self.form.designLbl.setText(bd.info)
        except AssertionError:
            showCritical("Invalid book design (Image number not found)")

    @pyqtSlot()
    def _clear_all_images(self):
        for i in range(self.mw.entrylist.count()):
            lane = self._get_lane(i)
            lane.clear_all()


    def _get_lane(self, i):
        _list = self.form.imgList
        return _list.itemWidget(_list.item(2 * i + 1))

    def _on_create(self):
        if not self.book:
            showCritical("Book design is not selected.")
            return
        datas = []
        for i, ew in enumerate(self.mw.entrylist.get_entry_all()):
            data = ew.data()
            panel = self._get_lane(i)
            for j, tup in enumerate(panel.imglist):
                data['img-%d' % (j + 1)] = tup[0]
                data['cite-%d' % (j + 1)] = tup[1]
            datas.append(data)
            print(panel.imglist)

        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader('/'))
        temp = env.get_template(self.book.path)
        rendered_temp = temp.render(entries=datas)

        with open('{dest}.html'.format(dest=self.destdir), 'w', encoding='utf-8') as f:
            f.write(rendered_temp)

    def reject(self):
        self.done(0)

        gui.dialogs.close("TextDialog")
