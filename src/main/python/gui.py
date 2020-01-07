from fbs_runtime.application_context.PyQt5 import ApplicationContext
from rgbfinder import RGBFinder
from PyQt5.QtWidgets import QTableWidget, QWidget, QVBoxLayout, QLabel, QAbstractItemView, QHBoxLayout, \
    QSlider, QGridLayout, QGroupBox, QCheckBox, QHeaderView, QPushButton, QProgressBar, QTableWidgetItem, QDialog, QDialogButtonBox
from PyQt5.QtGui import QIcon, QPixmap, QImage, QBrush, QColor
from PyQt5.QtCore import Qt, QThread, QTimer, QSettings
from functools import partial


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Vindictus Dye Finder")
        self.image_label = None
        self.table = None
        self.layout = None
        self.rgb_finder = None

        self.init_image()
        self.init_table()
        self.set_layout()
        self.show()
        self.setFixedSize(self.layout.sizeHint())

    def set_layout(self):
        settings_button_box = self.make_settings_button_box()
        bot_box = self.make_bot_box()

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addSpacing(-12)
        self.layout.addLayout(settings_button_box)
        self.layout.addWidget(bot_box)

        self.setLayout(self.layout)

    def make_bot_box(self):
        bot_layout = QHBoxLayout()

        bot_layout.addWidget(self.image_label)
        bot_layout.addWidget(self.table)
        bot_box = QGroupBox()
        bot_box.setLayout(bot_layout)
        return bot_box

    def show_preferences(self):
        print("pref")

    def make_settings_button_box(self):
        settings_button = QPushButton()
        # Gear icon is from: https://iconscout.com/icon/gear-222
        style_sheet = """
        QPushButton {
            qproperty-icon: url(" ");
            qproperty-iconSize: 15px 15px;
            border-image: url("resources/Gear.svg");
            background-color: rgba(255, 255, 255, 0);
        }

        QPushButton:hover {
            border-image: url("resources/SelectedGear.svg");
        }"""
        settings_button.setStyleSheet(style_sheet)
        # settings_button.setStyleSheet("background-color: rgba(0, 0, 0, 255); font-size: 23px;")
        settings_button.clicked.connect(self.show_preferences)
        settings_button.setFixedWidth(30)
        settings_button.setFixedHeight(30)

        settings_button_hb = QHBoxLayout()
        settings_button_hb.setAlignment(Qt.AlignRight)
        settings_button_hb.addWidget(settings_button)
        settings_button_hb.addSpacing(-11)
        return settings_button_hb

    def init_table(self):
        self.table = QTableWidget(7, 6)
        self.table.setHorizontalHeaderLabels(['Color', 'Name', 'Red', 'Green', 'Blue', 'Move Mouse'])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = self.table.horizontalHeader()
        for i in range(6):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setFixedWidth(300)

    def insert_colors(self,colors):
        # ["black", 25, 25, 25, 765, 0, 0]
        for i in range(len(colors)):
            color = colors[i]
            brush = QBrush(QColor(color[1],color[2],color[3],255))
            colored_item = QTableWidgetItem()
            colored_item.setBackground(brush)
            self.table.setItem(i, 0, colored_item)
            for j in range(1, 5):
                self.table.setItem(i, j, QTableWidgetItem(str(colors[i][j-1])))
            button = QPushButton("({},{})".format(color[5], color[6]))
            button.clicked.connect(partial(self.move_mouse, color[5], color[6]))
            layout = QHBoxLayout()
            layout.addWidget(button)
            layout.setAlignment(Qt.AlignTop)
            layout.setContentsMargins(0, 0, 0, 0)
            widget = QWidget()
            widget.setLayout(layout)
            self.table.setCellWidget(i, 5, widget)

    def move_mouse(self, x, y):
        #print("moved mouse to {},{}".format(x, y))
        self.rgb_finder.move_mouse(x, y)

    def init_image(self):
        self.image_label = QLabel()
        image = QPixmap('resources\\screencap.bmp')
        self.image_label.setPixmap(image)

    def set_rgb_finder(self, rgb_finder):
        self.rgb_finder = rgb_finder


class App:
    def run(self):
        app_ctx = ApplicationContext()
        window = Window()
        rgb_finder = RGBFinder(window)
        rgb_finder.run()
        return app_ctx.app.exec_()


if __name__ == "__main__":
    app = App()
    app.run()