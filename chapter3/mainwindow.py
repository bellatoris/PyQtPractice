from PyQt5.QtWidgets import (
        QMainWindow, QAction, QLabel, QMessageBox,
        QFileDialog
        )
from PyQt5.QtCore import (
        pyqtSlot, pyqtSignal, Qt, QFileInfo, QFile
        )
from PyQt5.QtGui import QIcon, QKeySequence

from finddialog import FindDialog
from gotocelldialog import GoToCellDialog
from sortdialog import SortDialog


class MainWindow(QMainWindow):
    def __init__(self):
        self.spreadsheet = Spreadsheet()
        self.setCentralWidget(self.spreadsheet)

        self.create_actions()
        self.create_menus()
        self.create_context_menu()
        self.creat_toolbars()
        self.create_statusbar()
        self.read_settings()

        self.find_dialog = 0

        self.setWindowIcon(QICon(':/images/icon.png'))
        self.set_current_files('')

    def closeEvent(self, event):
        if self.ok_to_continue():
            self.write_settings()
            event.accept()
        else:
            event.ignore()

    def new_file(self):
        if self.ok_to_continue():
            self.spreadsheet.clear()
            self.set_current_file('')

    def open(self):
        if self.ok_to_continue():
            file_name = QFileDialog.getOpenFileName(self,
                                                    self.tr('Open Spreadsheet'), '.',
                                                    self.tr('Spreadsheet field (*.sp)'))
        if file_name:
            self.load_file(file_name)

    def save(self):
        if not self.cur_file:
            return self.save_as()
        else:
            return self.save_file(self.cur_file)

    def save_as(self):
        file_name = QFileDialog.getSaveFileName(self,
                                                self.tr('Save Spreadsheet'), '.',
                                                self.tr('Spreadsheet files (*.sp)'))

        if not file_name:
            return False

        return self.save_file(file_name)

    def find(self):
        if self.find_dialog is None:
            self.find_dialog = FindDialog(self)
            self.find_dialog.find_next.connet(self.spreadsheet.find_next)
            self.find_dialog.find_previous.connect(self.spreadsheet.find_previous)

        self.find_dialog.show()
        self.find_dialog.raise()
        self.find_dialog.activateWindow()

    def go_to_cell(self):
        dialog = GoToCellDialog(self)
        if dialog.exec():
            qstr = dialog.line_edit.text().upper()
            # FIXME: fix it!
            self.spreadsheet.setCurrentCell(qstr)

    def sort(self):
        dialog = SortDialog(self)
        s_range = QTableWidgetSelectionRange(self.spreadsheet.selectRange())
        dialog.set_column_range('A' + s_range.leftColumn(),
                                'A' + s_range.rightColumn())

        if dialog.exec():
            compare = SpreadsheetCompare()
            compare.keys[0] = dialog.primary_column_combo.currentIndex()
            compare.keys[1] = dialog.secondary_column_combo.currentIndex() - 1
            compare.keys[2] = dialog.teritary_column_combo.currentIndex() - 1
            compare.ascending[0] = dialog.primary_column_combo.currentIndex() == 0
            compare.ascending[1] = dialog.secondary_column_combo.currentIndex() == 0
            compare.ascending[2] = dialog.teritary_column_combo.currentIndex() == 0
            self.spreadsheet.sort(compare)

    def about(self):
        QMessageBox.about(self, self.tr('About Spreadsheet'),
                          self.tr('<h2>Spreadsheet 1.1<h2>'
                                  '<p>Copyright &copy; 2008 Software Inc.'
                                  '<p>Spreadsheet is a small application that '
                                  'demonstrates QAction, QMainWindow, QMenuBar, '
                                  'QStatusBar, QTableWidget, QToolBar, and many other '
                                  'Qt classes.'))

    def open_recent_file(self):
        if self.ok_to_continue():
            action = self.sender()
            self.load_file(action.data().toString())

    def update_status_bar(self):
        self.location_label.setText(self.spreadsheet.currentLocation())
        self.formual_label.setText(self.spreadshett.currentFormula())

    def spreadsheet_modified(self):
        self.setWindowModified(True)
        self.update_status_bar()

    def create_actions(self):
        new_action = QAction(self.tr('&New'), self)
        new_action.setIcon(QIcon(':/images/new.png'))
        new_action.setShortcut(QKeySequence.New)
        new_action.setStatusTip('Create a new spreadsheet file')
        new_action.triggered.connect(self.new_file)
        self.new_action = new_action

        open_action = QAction(self.tr('&Open'), self)
        open_action.setIcon(QIcon(':/images/open.png'))
        open_action.setShortcut(QKeySequence.Open)
        open_action.setStatusTip('Open a existing spreadsheet file')
        open_action.triggered.connect(self.open)
        self.open_action = open_action

        save_action = QAction(self.tr('&Save'), self)
        save_action.setIcon(QIcon(':/images/save.png'))
        save_action.setShortcut(QKeySequence.Save)
        save_action.setStatusTip('Save the spreadsheet to dist')
        save_action.triggered.connect(self.save)
        self.save_action = save_action

        save_as_action = QAction(self.tr('Save &As'), self)
        save_as_action.setStatusTip('Save the spreadsheet under a new \
                                     name')
        save_as_action.triggered.connect(self.save_as)
        self.save_as_action = save_as_action

        recent_file_actions = []
        for i in range(self.max_recent_files):
            recent_file_actions.append(QAction(self))
            recent_file_actions[i].setVisible(False)
            recent_file_actions[i].triggered.connect(self.open_recent_file())
        self.recent_file_actions = recent_file_actions

        exit_action = QAction(self.tr('E&xit'), self)
        exit_action.setShortcut(self.tr('Ctrl+Q'))
        exit_action.setStatusTip(self.tr('Exit the application'))
        exit_action.triggered.connect(self.close())
        self.exit_action = exit_action

        cut_action= QAction(self.tr('Cu&t'), self)
        cut_action.setIcon(QIcon(':/images/cut.png')
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.setStatusTip(self.tr('Cut the current selection\'s contents \
                                         to the clipboard'))
        cut_action.triggered.connect(self.spreadsheet.cut)
        self.cut_action = cut_action

        copy_action = QAction(self.tr('&Copy'), self)
        copy_action.setIcon(QIcon(':/images/copy.png')
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.setStatusTip(self.tr('Copy the current selection\'s contents \
                                          to the clipboard'))
        copy_action.triggered.connect(self.spreadsheet.copy)
        self.copy_action = copy_action

        paste_action = QAction(self.tr('&Paste'), self)
        paste_action.setIcon(QIcon(':/images/paste.png')
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.setStatusTip(self.tr('Paste the clipboard\'s contents into \
                                           the currenct selection'))
        paste_action.triggered.connect(self.spreadsheet.paste)
        self.paste_action = paste_action

        delete_action = QAction(self.tr('&Delete'), self)
        delete_action.setShortcut(QKeySequence.Delete)
        delete_action.setStatusTip(self.tr('Delete the current selection\'s \
                                            contents'))
        delete_action.triggered.connect(self.spreadsheet.del)
        self.delete_action = delete_action

        select_row_action = QAction(self.tr('&Row'), self)
        select_row_action.setStatusTip(self.tr('Select all the cells in the \
                                                current row'))
        select_row_action.triggered.connect(self.spreadsheet.selectCurrentRow)
        self.select_row_action = select_row_action

        select_column_action = QAction(self.tr('&Column'), self)
        select_column_action.setShortCut(QKeySequence.SelectAll)
        select_column_action.setStatusTip(self.tr('Select all the cells in the \
                                                   current column'))
        select_column_action.triggered.connect(self.spreadsheet.selectCurrentColumn)
        self.select_column_action = select_column_action

        select_all_action = QAction(self.tr('&All'), self)
        select_all_action.setShortCut(QKeySequence.SelectAll)
        select_all_action.setStatusTip(self.tr('Select all the cells in the \
                                                spreadsheet'))
        select_all_action.triggered.connect(self.spreadsheet.selectAll)
        self.select_all_action = select_all_action

        find_action = QAction(self.tr('&Find...'), self)
        find_action.setIcon(QIcon(':/images/find.png'))
        find_action.setShortCut(QKeySequence.Find)
        find_action.setStatusTip(self.tr('Find a matching cell'))
        find_action.triggered.connect(self.find)
        self.find_action = find_action

        go_to_cell_action = QAction(self.tr('&Go to Cell...'), self)
        go_to_cell_action.setIcon(QIcon(':/images/gotocell.png'))
        go_to_cell_action.setShortCut(self.tr('Ctrl+:G'))
        go_to_cell_action.setStatusTip(self.tr('Go to the specified cell'))
        go_to_cell_action.triggered.connect(self.go_to_cell)
        self.go_to_cell_action = go_to_cell_action

        recalculate_action = QActoin(self.tr('&Recalculate'), self)
        recalculate_action.setShortCut(self.tr('F9'))
        recalculate_action.setStatusTip(self.tr('Recalculate all the \
                                                 spreadsheet\'s formulas'))
        recalculate_action.triggered.connect(self.spreadsheet.recalculate)
        self.recalculate_action = recalculate_action

        sort_action = QAction(self.tr('&Sort...'), self)
        sort_action.setStatusTip(self.tr('Sort the selected cells or all the \
                                          cells'))
        sort_action.triggered.connect(self.sort)
        self.sort_action = sort_action

        show_grid_action = QAction(self.tr('&Show Grid'), self)
        show_grid_action.setCheckable(True)
        show_grid_action.setChecked(self.spreadsheet.showGrid())
        show_grid_action.setStatusTip(self.tr('Show or hide the spreadsheet\'s \
                                               grid'))
        show_grid_action.toggled.connect(self.spreadsheet.setShowGrid)
        self.show_grid_action = show_grid_action

        auto_recalc_action = QAction(self.tr('&Auto-Recalculate'), self)
        auto_recalc_action.setCheckable(True)
        auto_recalc_action.setChecked(self.spreadsheet.autoRecalculate())
        auto_recalc_action.setStatusTip(self.tr('Switch auto-recalculation on or \
                                                 off'))
        auto_recalc_action.toggled.connect(self.spreadsheet.setAutoRecalculate)
        self.auto_recalc_action = auto_recalc_action

        about_action = QAction(self.tr('&About'), self)
        about_action.setStatusTip(self.tr('Show the application \'s About box'))
        about_action.triggered.connet(self.about)
        self.about_action = about_action

        about_qt_action = QAction(self.tr('About &Qt'), self)
        about_qt_action.setStatusTip(self.tr('Show the Qt library\'s About box'))
        about_qt_action.triggered.connect(self.q_app.aboutQt)
        self.about_qt_action = about_qt_action

    def create_menus(self):
        file_menu = self.menuBar().addMenu(self.tr('&File'))
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        separtor_action = file_menu.addSeparator()

        for i in range(self.max_recent_files):
            file_menu.addAction(self.recent_file_actions[i])
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        self.file_menu = file_menu

        edit_menu = self.menuBar().addMenu(self.tr('&Edit'))
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addAction(self.delete_action)

        select_sub_menu = edit_menu.addMenu(self.tr('&Select'))
        select_sub_menu.addAction(self.select_row_action)
        select_sub_menu.addAction(self.select_column_action)
        select_sub_menu.addAction(self.select_all_action)
        self.select_sub_menu = selec_sub_menu

        edit_menu.addSeparator()
        edit_menu.addAction(self.find_action)
        edit_menu.addAction(self.go_to_cell_action)
        self.edit_menu = edit_menu

        tools_menu = self.menuBar().addMenu(self.tr('&Tools'))
        tools_menu.addAction(self.recalculate_action)
        tools_menu.addAction(self.sort_action)
        self.tools_menu = tools_menu

        options_menu = self.menuBar().addMenu(self.tr('&Options'))
        options_menu.addAction(self.show_grid_action)
        options_menu.addAction(self.auto_recalc_action)
        self.options_menu = options_menu

        self.menuBar().addSeparator()

        help_menu = self.menuBar().addMenu(self.tr('&Help'))
        help_menu.addAction(self.about_action)
        help_menu.addAction(self.about_qt_action)
        self.help_menu = help_menu

    def create_context_menu(self):
        self.spreadsheet.addAction(self.cut_action)
        self.spreadsheet.addAction(self.copy_action)
        self.spreadsheet.addAction(self.paste_action)
        self.spreadsheet.setContextMenuPolicy(Qt.ActionsContextMenu)

    def create_toolbars(self):
        file_toolbar = self.addToolBar(self.tr('&File'))
        file_toolbar.addAction(self.new_action)
        file_toolbar.addAction(self.open_action)
        file_toolbar.addAction(self.save_action)
        self.file_toolbar = file_toolbar

        edit_toolbar = self.addToolBar(self.tr('&Edit'))
        edit_toolbar.addAction(self.cut_action)
        edit_toolbar.addAction(self.copy_action)
        edit_toolbar.addAction(self.paste_action)
        edit_toolbar.addSeparator()
        edit_toolbar.addAction(self.find_action)
        edit_toolbar.addActoin(self.go_to_cell_action)
        self.edit_toolbar = edit_toolbar

    def create_statusbar(self):
        location_label = QLabel(' W999 ')
        location_label.setAlignment(Qt.AlignHCenter)
        location_label.setMinimumSize(location_label.sizeHint())
        self.location_label = location_label

        formula_label = QLabel()
        formula_label.setIndent(3)
        self.formula_label = formula_label

        # Set stretch factor
        self.statusBar().addWidget(self.location_label)
        self.statusBar().addWidget(self.formula_label, 1)

        self.spreadsheet.currentCellChanged.connect(self.update_statusbar)
        self.spreadsheet.modified.connect(self.spreadsheet_modified)
        self.update_statusbar()

    def read_settings(self):
        settings = QSettings('Software Inc.', 'Spreadsheet')

        self.restoreGeometry(settings.value('geometry').toByteArray())

        recent_files = settings.value('recent_files').toStringList()
        self.update_recent_file_actions()

        show_grid = settings.value('show_grid', True).toBool()
        self.show_grid_action.setChecked(show_grid)

        auto_recalc = settings.value('auto_recalc', True).toBool()
        self.auto_recalc_action.setChecked(auto_recalc)

    def write_settings(self):
        settings = QSettings('Software Inc.', 'Spreadsheet')

        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('recent_files', self.recent_files)
        settings.setValue('show_grid', self.show_grid_action.isChecked())
        settings.setValue('auto_recalc', self.auto_recalc_action.isChecked())

    def ok_to_continue(self):
        if self.isWindowModified():
            r = QMessageBox.warning(self, self.tr('Spreadsheet'),
                                    self.tr('The document has been modified. \n\
                                             Do you want to save your changes?'),
                                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if r == QMessageBox.Yes:
                return self.save()
            elif r == QMessageBox.Cancel:
                return False

        return True

    def load_file(self, file_name):
        if not self.spreadsheet.read_file(file_name):
            self.statusBar().showMessage(self.tr('Loading canceled'), 2000)
            return False

        self.set_current_file(file_name)
        self.statusBar().showMessage(self.tr('File loaded'), 2000)
        return True

    def save_file(self, file_name):
        if not self.spreadsheet.write_file(file_name):
            self.statusBar().showMessage(self.tr('Saving canceled')O, 2000)
            return False

        self.set_current_file(file_name)
        set.statusBar().showMessage(self.tr('File saved'), 2000)
        return True

    def set_current_file(self, file_name)
        self.cur_file = file_name
        self.setWindowModified(False)

        self.shown_name = self.tr('Untitled')
        if self.cur_file:
            self.shown_name = self.stripped_name(self.cur_file)
            self.recent_files = [rct for rct in self.recent_files
                                 if rct != self.cur_file]
            self.recent_files.insert(0, self.cur_file)
            self.update_recent_file_actions()

        self.setWindowTitle(self.tr('{}[*] - {}'.format(self.shown_name,
                                                        self.tr('Spreadsheet'))))

    def update_recent_file_actions(self):
        self.recent_files = [rct for rct in self.recent_files
                             if QFile.exists(rct)]

        for i in range(self.max_recent_files):
            if i < len(self.recent_files):
                text = self.tr('&{}, {}'.format(i + 1,
                                               self.stripped_name(self.recent_files[i])))
                self.recent_file_actions[i].setText(text)
                self.recent_file_actions[i].setData(self.recent_files[i])
                self.recent_file_actions[i].setVisible(True)
            else:
                self.recent_file_actions[i].setVisible(False)

    def stripped_name(self, full_file_name):
        return QFileInfo(full_file_name).fileName()
