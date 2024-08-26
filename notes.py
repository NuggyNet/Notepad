import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QStatusBar, QLabel
from PyQt5.QtGui import QIcon, QFont, QPalette
from PyQt5.QtCore import Qt, QTimer, QSettings, QCoreApplication

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Notepad")

        self.setWindowIcon(QIcon("icon.ico"))  

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.text_edit.setFont(QFont("Consolas", 11))

        self.text_edit.setContextMenuPolicy(Qt.NoContextMenu)

        self.create_menu_bar()

        self.create_status_bar()

        self.text_edit.cursorPositionChanged.connect(self.update_status_bar)

        self.setGeometry(100, 100, 800, 600)

        self.set_theme_from_system()
        self.start_theme_watcher()

    def create_menu_bar(self):

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")

        new_action = QAction("New", self)
        new_window_action = QAction("New Window", self)
        open_action = QAction("Open...", self)
        save_action = QAction("Save", self)
        save_as_action = QAction("Save As...", self)
        page_setup_action = QAction("Page Setup...", self)
        print_action = QAction("Print...", self)
        exit_action = QAction("Exit", self)

        file_menu.addAction(new_action)
        file_menu.addAction(new_window_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addSeparator()  
        file_menu.addAction(page_setup_action)
        file_menu.addAction(print_action)
        file_menu.addSeparator()  
        file_menu.addAction(exit_action)

        exit_action.triggered.connect(self.close)

        edit_menu = menu_bar.addMenu("Edit")

        undo_action = QAction("Undo", self)
        undo_action.setEnabled(False)  
        redo_action = QAction("Redo", self)
        redo_action.setEnabled(False)  
        cut_action = QAction("Cut", self)
        copy_action = QAction("Copy", self)
        paste_action = QAction("Paste", self)
        delete_action = QAction("Delete", self)
        look_up_action = QAction("Look Up", self)
        find_replace_action = QAction("Find and Replace", self)
        select_all_action = QAction("Select All", self)
        timestamp_action = QAction("Insert Timestamp", self)

        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()  
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addAction(delete_action)
        edit_menu.addSeparator()  
        edit_menu.addAction(look_up_action)
        edit_menu.addAction(find_replace_action)
        edit_menu.addSeparator()  
        edit_menu.addAction(select_all_action)
        edit_menu.addAction(timestamp_action)

        format_menu = menu_bar.addMenu("Format")

        word_wrap_action = QAction("Word Wrap", self)
        word_wrap_action.setCheckable(True)
        word_wrap_action.setEnabled(False)  
        format_menu.addAction(word_wrap_action)

        font_action = QAction("Font", self)
        format_menu.addAction(font_action)

        dark_theme_action = QAction("Dark Theme", self, checkable=True)
        dark_theme_action.triggered.connect(self.toggle_dark_theme)
        format_menu.addAction(dark_theme_action)

    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.encoding_label = QLabel("Encoding: UTF-8")
        self.line_ending_label = QLabel("Windows (CRLF)")
        self.zoom_label = QLabel("100% Zoom")
        self.cursor_position_label = QLabel("Line 1, Column 1")

        separator_style = "border-left: 1px solid #999999; padding-left: 8px; margin-left: 8px;"
        self.line_ending_label.setStyleSheet(separator_style)
        self.zoom_label.setStyleSheet(separator_style)
        self.cursor_position_label.setStyleSheet(separator_style)

        self.encoding_label.setAlignment(Qt.AlignCenter)
        self.line_ending_label.setAlignment(Qt.AlignCenter)
        self.zoom_label.setAlignment(Qt.AlignCenter)
        self.cursor_position_label.setAlignment(Qt.AlignCenter)

        self.status_bar.addPermanentWidget(self.encoding_label)
        self.status_bar.addPermanentWidget(self.line_ending_label)
        self.status_bar.addPermanentWidget(self.zoom_label)
        self.status_bar.addPermanentWidget(self.cursor_position_label)

        self.status_bar.setStyleSheet("QStatusBar::item { border: none; }")
        self.status_bar.setSizeGripEnabled(False)

    def toggle_dark_theme(self, checked):
        if checked:

            self.text_edit.setStyleSheet("background-color: #000000; color: #FFFFFF;")
        else:

            self.text_edit.setStyleSheet("background-color: #FFFFFF; color: #000000;")

    def update_status_bar(self):

        cursor = self.text_edit.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.columnNumber() + 1

        self.cursor_position_label.setText(f"Line {line}, Column {column}")

    def set_theme_from_system(self):

        settings = QSettings("org.qt-project.Qt", "Qt")
        theme = settings.value("Theme", "light")  

        if theme == "dark":
            self.text_edit.setStyleSheet("background-color: #000000; color: #FFFFFF;")
        else:
            self.text_edit.setStyleSheet("background-color: #FFFFFF; color: #000000;")

    def start_theme_watcher(self):

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_theme_change)
        self.timer.start(5000)  

    def check_theme_change(self):

        settings = QSettings("org.qt-project.Qt", "Qt")
        theme = settings.value("Theme", "light")

        if (theme == "dark" and not self.text_edit.styleSheet().startswith("background-color: #000000")) or \
           (theme == "light" and not self.text_edit.styleSheet().startswith("background-color: #FFFFFF")):
            self.set_theme_from_system()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Notepad()
    window.show()
    sys.exit(app.exec_())