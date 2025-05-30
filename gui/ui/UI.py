# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UI.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QFrame, QHBoxLayout,
    QLabel, QLayout, QMainWindow, QPushButton,
    QSizePolicy, QSlider, QSplitter, QTextEdit,
    QVBoxLayout, QWidget)

from qfluentwidgets import ComboBox
from gui.ui.utils.UpdateFrame import DoubleClickQFrame
import gui.ui.UI_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(768, 458)
        MainWindow.setStyleSheet(u"")
        self.mainWindow = QWidget(MainWindow)
        self.mainWindow.setObjectName(u"mainWindow")
        self.mainWindow.setStyleSheet(u"QWidget#mainWindow{\n"
"	border:none\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(self.mainWindow)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(9, -1, -1, -1)
        self.mainBody = QFrame(self.mainWindow)
        self.mainBody.setObjectName(u"mainBody")
        self.mainBody.setStyleSheet(u"QFrame#mainBody{\n"
"	border: 0px solid rgba(0, 0, 0, 40%);\n"
"	border-bottom:none;\n"
"	border-bottom-left-radius: 0;\n"
"	border-bottom-right-radius: 0;\n"
"	border-radius:30%;\n"
"	background-color: white;\n"
"	/*	\n"
"	background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #B5FFFC, stop:0.2 #e0c3fc, stop:1 #FFDEE9);\n"
"	*/\n"
"}")
        self.mainBody.setFrameShape(QFrame.Shape.StyledPanel)
        self.mainBody.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.mainBody)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.topbox = DoubleClickQFrame(self.mainBody)
        self.topbox.setObjectName(u"topbox")
        self.topbox.setMaximumSize(QSize(16777215, 40))
        self.topbox.setStyleSheet(u"")
        self.topBox = QHBoxLayout(self.topbox)
        self.topBox.setSpacing(0)
        self.topBox.setObjectName(u"topBox")
        self.topBox.setContentsMargins(0, 8, 0, 8)
        self.right_top = QFrame(self.topbox)
        self.right_top.setObjectName(u"right_top")
        self.right_top.setStyleSheet(u"QLabel#title{\n"
"    background-color: none;\n"
"	font-size: 22px;\n"
"	font-family: \"Shojumaru\";\n"
"	color: black;\n"
"}\n"
"Spacer{\n"
"	border:none;\n"
"}")
        self.right_top.setFrameShape(QFrame.Shape.StyledPanel)
        self.right_top.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.right_top)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel(self.right_top)
        self.title.setObjectName(u"title")
        self.title.setStyleSheet(u"")
        self.title.setIndent(-1)

        self.horizontalLayout.addWidget(self.title)


        self.topBox.addWidget(self.right_top, 0, Qt.AlignmentFlag.AlignHCenter)

        self.left_top = QFrame(self.topbox)
        self.left_top.setObjectName(u"left_top")
        self.left_top.setMinimumSize(QSize(80, 0))
        self.left_top.setMaximumSize(QSize(150, 16777215))
        self.left_top.setAutoFillBackground(False)
        self.left_top.setStyleSheet(u"/* QFrame#left_top{\n"
"	border: 1px solid red;\n"
"} */\n"
"QPushButton#closeButton {\n"
"    background-color: rgb(255, 59, 48); /* \u7ea2\u8272 */\n"
"    border: none;\n"
"    border-radius: 10px; /* \u4f7f\u6309\u94ae\u5706\u5f62 */\n"
"    min-width: 20px;\n"
"    max-width: 20px;\n"
"    min-height: 20px;\n"
"    max-height: 20px;\n"
"}\n"
"\n"
"QPushButton#maximizeButton {\n"
"    background-color: rgb(40, 205, 65); /* \u9ec4\u8272 */\n"
"    border: none;\n"
"    border-radius: 10px; /* \u4f7f\u6309\u94ae\u5706\u5f62 */\n"
"    min-width: 20px;\n"
"    max-width: 20px;\n"
"    min-height: 20px;\n"
"    max-height: 20px;\n"
"}\n"
"\n"
"QPushButton#minimizeButton {\n"
"    background-color: rgb(255, 214, 10); /* \u7eff\u8272 */\n"
"    border: none;\n"
"    border-radius: 10px; /* \u4f7f\u6309\u94ae\u5706\u5f62 */\n"
"    min-width: 20px;\n"
"    max-width: 20px;\n"
"    min-height: 20px;\n"
"    max-height: 20px;\n"
"}\n"
"")
        self.left_top.setFrameShape(QFrame.Shape.StyledPanel)
        self.left_top.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.left_top)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.minimizeButton = QPushButton(self.left_top)
        self.minimizeButton.setObjectName(u"minimizeButton")
        self.minimizeButton.setStyleSheet(u"QPushButton:hover{\n"
"	background-color:rgb(139, 29, 31);\n"
"	border-image: url(:/leftbox/images/newsize/min.png);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color:  rgb(255, 214, 5);\n"
"}\n"
"\n"
"")

        self.horizontalLayout_2.addWidget(self.minimizeButton)

        self.maximizeButton = QPushButton(self.left_top)
        self.maximizeButton.setObjectName(u"maximizeButton")
        self.maximizeButton.setStyleSheet(u"QPushButton:hover{\n"
"	background-color:rgb(139, 29, 31);\n"
"	border-image: url(:/leftbox/images/newsize/max.png);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: rgb(40, 205, 60);\n"
"}")

        self.horizontalLayout_2.addWidget(self.maximizeButton)

        self.closeButton = QPushButton(self.left_top)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setStyleSheet(u"QPushButton:hover{\n"
"	background-color:rgb(139, 29, 31);\n"
"	border-image: url(:/leftbox/images/newsize/close.png);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: rgb(232, 59, 35);\n"
"}")

        self.horizontalLayout_2.addWidget(self.closeButton)


        self.topBox.addWidget(self.left_top)

        self.topBox.setStretch(0, 9)

        self.verticalLayout.addWidget(self.topbox)

        self.mainbox = QFrame(self.mainBody)
        self.mainbox.setObjectName(u"mainbox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainbox.sizePolicy().hasHeightForWidth())
        self.mainbox.setSizePolicy(sizePolicy)
        self.mainbox.setStyleSheet(u"QFrame#mainbox{\n"
"	border: 1px solid rgba(0, 0, 0, 15%);\n"
"   /*\n"
"	background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #B5FFFC, stop:0.2 #e0c3fc, stop:1 #FFDEE9);\n"
"	 */\n"
"	border-bottom-left-radius: 0;\n"
"	border-bottom-right-radius: 0;\n"
"	border-radius:30%;\n"
"}\n"
"")
        self.mainBox = QHBoxLayout(self.mainbox)
        self.mainBox.setSpacing(0)
        self.mainBox.setObjectName(u"mainBox")
        self.mainBox.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.mainBox.setContentsMargins(0, 0, 0, 0)
        self.leftBox = QFrame(self.mainbox)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy1)
        self.leftBox.setMinimumSize(QSize(100, 0))
        self.leftBox.setMaximumSize(QSize(100, 16777215))
        self.leftBox.setStyleSheet(u"QFrame#leftBox  {\n"
"    /*background-color: rgba(255, 255, 255, 80%);*/\n"
"    border: 0px solid rgba(0, 0, 0, 40%);\n"
"	border-top:none;\n"
"	border-bottom:none;\n"
"	border-left:none;\n"
"}\n"
"")
        self.leftBox.setFrameShape(QFrame.Shape.StyledPanel)
        self.leftBox.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.leftBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.leftbox_bottom = QFrame(self.leftBox)
        self.leftbox_bottom.setObjectName(u"leftbox_bottom")
        sizePolicy.setHeightForWidth(self.leftbox_bottom.sizePolicy().hasHeightForWidth())
        self.leftbox_bottom.setSizePolicy(sizePolicy)
        self.leftbox_bottom.setMinimumSize(QSize(0, 0))
        self.leftbox_bottom.setMaximumSize(QSize(100, 16777215))
        self.leftbox_bottom.setStyleSheet(u"QPushButton#src_menu{\n"
"	background-image: url(:/leftbox/images/newsize/menu.png);\n"
"}\n"
"QPushButton#src_folder{\n"
"	background-image: url(:/leftbox/images/newsize/folder.png);\n"
"\n"
"}\n"
"QPushButton#src_camera{\n"
"	background-image: url(:/leftbox/images/newsize/security-camera.png);\n"
"}\n"
"QPushButton#src_img{\n"
"	background-image: url(:/leftbox/images/newsize/gallery.png);\n"
"}\n"
"QPushButton#src_webcam{\n"
"	background-image: url(:/leftbox/images/newsize/photo-camera.png);\n"
"}\n"
"QPushButton#src_setting{\n"
"	background-image:url(:/leftbox/images/newsize/setting.png);\n"
"}\n"
"QPushButton#src_vsmode{\n"
"	background-image:url(:/leftbox/images/newsize/vs.png);\n"
"}\n"
"QPushButton#src_result{\n"
"	background-image:url(:/leftbox/images/newsize/statistics.png);\n"
"}\n"
"QPushButton#src_table{\n"
"	background-image:url(:/leftbox/images/newsize/table.png);\n"
"}\n"
"QPushButton{\n"
"	border:none;\n"
"	text-align: center;\n"
"	background-repeat: no-repeat;\n"
"	background-position: left ce"
                        "nter;\n"
"	border-left: 23px solid transparent;\n"
"	color: rgba(0, 0, 0, 199);\n"
"	font: 12pt \"Times New Roman\";\n"
"	font-weight: bold;\n"
"	padding-left: 15px;\n"
"}\n"
"QFrame#cameraBox:hover{\n"
"	background-color: rgba(114, 129, 214, 59);\n"
"}\n"
"QFrame#folderBox:hover{\n"
"	background-color: rgba(114, 129, 214, 59);\n"
"}\n"
"QFrame#imgBox:hover{\n"
"	background-color: rgba(114, 129, 214, 59);\n"
"}\n"
"QFrame#menuBox:hover{\n"
"	background-color: rgba(114, 129, 214, 59);\n"
"}\n"
"QFrame#webcamBox:hover{\n"
"	background-color: rgba(114, 129, 214, 59);\n"
"}\n"
"QFrame#manageBox:hover{\n"
"	background-color: rgba(114, 129, 214, 59);\n"
"}\n"
"QFrame#vsBox:hover{\n"
"	background-color: rgba(114, 129, 214, 59);\n"
"}\n"
"QFrame#resultBox:hover{\n"
"	background-color: rgba(114, 129, 214, 59);\n"
"}\n"
"QFrame#tableBox:hover{\n"
"	background-color: rgba(114, 129, 214, 59);\n"
"}")
        self.leftbox_bottom.setFrameShape(QFrame.Shape.StyledPanel)
        self.leftbox_bottom.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftbox_bottom)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 10, 0, 0)
        self.ControlBox = QFrame(self.leftbox_bottom)
        self.ControlBox.setObjectName(u"ControlBox")
        self.ControlBox.setMinimumSize(QSize(100, 120))
        self.ControlBox.setMaximumSize(QSize(100, 120))
        self.ControlBox.setFrameShape(QFrame.Shape.StyledPanel)
        self.ControlBox.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.ControlBox)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.src_cam = QPushButton(self.ControlBox)
        self.src_cam.setObjectName(u"src_cam")
        self.src_cam.setMinimumSize(QSize(0, 60))
        self.src_cam.setMaximumSize(QSize(120, 16777215))
        self.src_cam.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.src_cam.setStyleSheet(u"image: url(:/leftbox/images/newsize/photo-camera.png);")

        self.verticalLayout_8.addWidget(self.src_cam)

        self.src_database = QPushButton(self.ControlBox)
        self.src_database.setObjectName(u"src_database")
        self.src_database.setMinimumSize(QSize(100, 60))
        self.src_database.setMaximumSize(QSize(100, 16777215))
        self.src_database.setMouseTracking(True)
        self.src_database.setTabletTracking(True)
        self.src_database.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.src_database.setStyleSheet(u"image: url(:/leftbox/images/newsize/table.png);")

        self.verticalLayout_8.addWidget(self.src_database)


        self.verticalLayout_3.addWidget(self.ControlBox, 0, Qt.AlignmentFlag.AlignHCenter)

        self.leftbox_top = QFrame(self.leftbox_bottom)
        self.leftbox_top.setObjectName(u"leftbox_top")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.leftbox_top.sizePolicy().hasHeightForWidth())
        self.leftbox_top.setSizePolicy(sizePolicy2)
        self.leftbox_top.setMinimumSize(QSize(100, 180))
        self.leftbox_top.setMaximumSize(QSize(100, 16777215))
        self.leftbox_top.setFrameShape(QFrame.Shape.StyledPanel)
        self.leftbox_top.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.leftbox_top)
        self.horizontalLayout_8.setSpacing(5)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(10, 10, 15, 3)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.verticalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.run_button = QPushButton(self.leftbox_top)
        self.run_button.setObjectName(u"run_button")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.run_button.sizePolicy().hasHeightForWidth())
        self.run_button.setSizePolicy(sizePolicy3)
        self.run_button.setMinimumSize(QSize(40, 40))
        self.run_button.setMaximumSize(QSize(60, 60))
        self.run_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.run_button.setMouseTracking(True)
        self.run_button.setStyleSheet(u"QPushButton{\n"
"background-repeat: no-repeat;\n"
"background-position: center;\n"
"background-size: 100% 100%;\n"
"border: none;\n"
"background-color: transparent;\n"
"}\n"
"QPushButton:hover{\n"
"\n"
"}")
        self.run_button.setIconSize(QSize(40, 40))
        self.run_button.setCheckable(True)
        self.run_button.setChecked(False)

        self.verticalLayout_7.addWidget(self.run_button, 0, Qt.AlignmentFlag.AlignHCenter)

        self.stop_button = QPushButton(self.leftbox_top)
        self.stop_button.setObjectName(u"stop_button")
        sizePolicy3.setHeightForWidth(self.stop_button.sizePolicy().hasHeightForWidth())
        self.stop_button.setSizePolicy(sizePolicy3)
        self.stop_button.setMinimumSize(QSize(40, 40))
        self.stop_button.setMaximumSize(QSize(60, 60))
        self.stop_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.stop_button.setStyleSheet(u"QPushButton{\n"
"background-image: url(:/rightbox/images/newsize/stop.png);\n"
"background-repeat: no-repeat;\n"
"background-position: center;\n"
"background-size: 100% 100%;\n"
"border: none;\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"\n"
"}")
        self.stop_button.setIconSize(QSize(40, 40))

        self.verticalLayout_7.addWidget(self.stop_button, 0, Qt.AlignmentFlag.AlignHCenter)

        self.control_button = QPushButton(self.leftbox_top)
        self.control_button.setObjectName(u"control_button")
        sizePolicy3.setHeightForWidth(self.control_button.sizePolicy().hasHeightForWidth())
        self.control_button.setSizePolicy(sizePolicy3)
        self.control_button.setMinimumSize(QSize(40, 40))
        self.control_button.setMaximumSize(QSize(60, 60))
        self.control_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.control_button.setMouseTracking(True)
        self.control_button.setStyleSheet(u"border-image: url(../images/icon.png);")

        self.verticalLayout_7.addWidget(self.control_button, 0, Qt.AlignmentFlag.AlignHCenter)


        self.horizontalLayout_8.addLayout(self.verticalLayout_7)


        self.verticalLayout_3.addWidget(self.leftbox_top)

        self.verticalLayout_3.setStretch(0, 4)

        self.verticalLayout_2.addWidget(self.leftbox_bottom)

        self.verticalLayout_2.setStretch(0, 80)

        self.mainBox.addWidget(self.leftBox)

        self.rightBox = QFrame(self.mainbox)
        self.rightBox.setObjectName(u"rightBox")
        sizePolicy.setHeightForWidth(self.rightBox.sizePolicy().hasHeightForWidth())
        self.rightBox.setSizePolicy(sizePolicy)
        self.rightBox.setMinimumSize(QSize(0, 0))
        self.rightBox.setStyleSheet(u"QFrame#rightBox{\n"
"	margin-top: -1px;\n"
"	margin-right: -1px;\n"
"	margin-bottom: -1px;\n"
"    background-color:  #ffffff;\n"
"    border: 1px solid rgba(0, 0, 0, 15%);\n"
"	background-color: rgb(245, 249, 254);\n"
"}\n"
"QFrame#rightbox_top{\n"
"	border:2px solid rgb(255, 255, 255);\n"
"	background-color: rgb(238, 242, 255);\n"
"}\n"
"\n"
"QFrame#main_leftbox{\n"
"	border:2px solid rgb(255, 255, 255);\n"
"	background-color: rgb(238, 242, 255);\n"
"}\n"
"QFrame#main_rightbox{\n"
"	border:2px solid rgb(255, 255, 255);\n"
"	background-color: rgb(238, 242, 255);\n"
"}\n"
"/*QFrame#rightbox_bottom{\n"
"	border:2px solid rgb(255, 255, 255);\n"
"}*/")
        self.rightBox.setFrameShape(QFrame.Shape.StyledPanel)
        self.rightBox.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.rightBox)
        self.verticalLayout_5.setSpacing(3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(8, 8, 8, 8)
        self.rightbox_top = QFrame(self.rightBox)
        self.rightbox_top.setObjectName(u"rightbox_top")
        self.rightbox_top.setStyleSheet(u"")
        self.rightbox_top.setFrameShape(QFrame.Shape.StyledPanel)
        self.rightbox_top.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.rightbox_top)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_5.addWidget(self.rightbox_top)

        self.rightbox_main = QFrame(self.rightBox)
        self.rightbox_main.setObjectName(u"rightbox_main")
        self.rightbox_main.setStyleSheet(u"")
        self.rightbox_main.setFrameShape(QFrame.Shape.StyledPanel)
        self.rightbox_main.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.rightbox_main)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.rightbox_main)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.main_rightbox = QLabel(self.splitter)
        self.main_rightbox.setObjectName(u"main_rightbox")
        self.main_rightbox.setMinimumSize(QSize(200, 100))
        self.splitter.addWidget(self.main_rightbox)

        self.horizontalLayout_9.addWidget(self.splitter)


        self.verticalLayout_5.addWidget(self.rightbox_main)

        self.user_info = QTextEdit(self.rightBox)
        self.user_info.setObjectName(u"user_info")
        self.user_info.setMinimumSize(QSize(110, 110))
        self.user_info.setMaximumSize(QSize(16777215, 100))
        self.user_info.setMouseTracking(False)
        self.user_info.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.user_info.setAcceptDrops(False)
        self.user_info.setFrameShape(QFrame.Shape.WinPanel)
        self.user_info.setUndoRedoEnabled(False)
        self.user_info.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.verticalLayout_5.addWidget(self.user_info)

        self.rightbox_play = QFrame(self.rightBox)
        self.rightbox_play.setObjectName(u"rightbox_play")
        self.rightbox_play.setFrameShape(QFrame.Shape.StyledPanel)
        self.rightbox_play.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.rightbox_play)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(5, 5, 5, 5)

        self.verticalLayout_5.addWidget(self.rightbox_play)

        self.verticalLayout_5.setStretch(1, 86)

        self.mainBox.addWidget(self.rightBox)

        self.settingBox = QFrame(self.mainbox)
        self.settingBox.setObjectName(u"settingBox")
        self.settingBox.setMinimumSize(QSize(0, 200))
        self.settingBox.setMaximumSize(QSize(250, 16777215))
        self.settingBox.setStyleSheet(u"")
        self.settingBox.setFrameShape(QFrame.Shape.StyledPanel)
        self.settingBox.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.settingBox)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.setting_page = QFrame(self.settingBox)
        self.setting_page.setObjectName(u"setting_page")
        self.setting_page.setMinimumSize(QSize(0, 0))
        self.setting_page.setMaximumSize(QSize(250, 16777215))
        self.setting_page.setStyleSheet(u"QFrame#setting_page {\n"
"       background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8ED5FC, stop:1 #E0F3FC);\n"
"        border-top-left-radius: 0px;\n"
"        border-top-right-radius: 20px;\n"
"        border-bottom-right-radius: 20px;\n"
"        border-bottom-left-radius: 0px;\n"
"        border: none;\n"
"    }")
        self.setting_page.setFrameShape(QFrame.Shape.StyledPanel)
        self.setting_page.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.setting_page)
        self.verticalLayout_22.setSpacing(15)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(15, 15, 15, 15)
        self.label_2 = QLabel(self.setting_page)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 30))
        self.label_2.setStyleSheet(u"padding-left: 0px;\n"
"padding-bottom: 2px;\n"
"color: white;\n"
"font: 700 italic 16pt \"Segoe UI\";")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_22.addWidget(self.label_2)

        self.Model_QF_2 = QWidget(self.setting_page)
        self.Model_QF_2.setObjectName(u"Model_QF_2")
        self.Model_QF_2.setMinimumSize(QSize(200, 90))
        self.Model_QF_2.setMaximumSize(QSize(200, 90))
        self.Model_QF_2.setStyleSheet(u"QWidget#Model_QF_2{\n"
"border:2px solid rgba(255, 255, 255, 70);\n"
"border-radius:15px;\n"
"}")
        self.verticalLayout_21 = QVBoxLayout(self.Model_QF_2)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(9, 9, 9, 9)
        self.ToggleBotton_6 = QPushButton(self.Model_QF_2)
        self.ToggleBotton_6.setObjectName(u"ToggleBotton_6")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.ToggleBotton_6.sizePolicy().hasHeightForWidth())
        self.ToggleBotton_6.setSizePolicy(sizePolicy4)
        self.ToggleBotton_6.setMinimumSize(QSize(0, 30))
        self.ToggleBotton_6.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setFamilies([u"Nirmala UI"])
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        self.ToggleBotton_6.setFont(font)
        self.ToggleBotton_6.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.ToggleBotton_6.setMouseTracking(True)
        self.ToggleBotton_6.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.ToggleBotton_6.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.ToggleBotton_6.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.ToggleBotton_6.setAutoFillBackground(False)
        self.ToggleBotton_6.setStyleSheet(u"QPushButton{\n"
"background-image: url(:/setting /images/newsize/model.png);\n"
"background-repeat: no-repeat;\n"
"background-position: left center;\n"
"border: none;\n"
"border-left: 20px solid transparent;\n"
"\n"
"text-align: left;\n"
"padding-left: 40px;\n"
"padding-bottom: 2px;\n"
"color: white;\n"
"font: 700 13pt \"Nirmala UI\";\n"
"}")
        self.ToggleBotton_6.setAutoDefault(False)
        self.ToggleBotton_6.setFlat(False)

        self.verticalLayout_21.addWidget(self.ToggleBotton_6)

        self.model_box = ComboBox(self.Model_QF_2)
        self.model_box.setObjectName(u"model_box")
        self.model_box.setMinimumSize(QSize(240, 22))
        self.model_box.setMaximumSize(QSize(240, 20))
        self.model_box.setStyleSheet(u"ComboBox {\n"
"            background-color: rgba(255,255,255,90);\n"
"			color: rgba(0, 0, 0, 200);\n"
"            border: 1px solid lightgray;\n"
"            border-radius: 10px;\n"
"			padding: 2px;\n"
"			text-align: left;\n"
"			font: 600 9pt \"Segoe UI\";\n"
"			padding-left: 15px;\n"
"}      \n"
"ComboBox:on {\n"
"            border: 1px solid #63acfb;       \n"
" }\n"
"\n"
"ComboBox::drop-down {\n"
"            width: 22px;\n"
"            border-left: 1px solid lightgray;\n"
"            border-top-right-radius: 15px;\n"
"            border-bottom-right-radius: 15px; \n"
"}\n"
"ComboBox::drop-down:on {\n"
"            border-left: 1px solid #63acfb;\n"
" }\n"
"\n"
"ComboBox::down-arrow {\n"
"            width: 16px;\n"
"            height: 16px;\n"
"            image: url(:/setting /images/newsize/box_down.png);\n"
" }\n"
"\n"
"ComboBox::down-arrow:on {\n"
"            image: url(:/setting /images/newsize/box_up.png);\n"
" }\n"
"")
        self.model_box.setProperty(u"minimumContentsLength", 0)

        self.verticalLayout_21.addWidget(self.model_box)


        self.verticalLayout_22.addWidget(self.Model_QF_2)

        self.IOU_QF = QFrame(self.setting_page)
        self.IOU_QF.setObjectName(u"IOU_QF")
        self.IOU_QF.setMinimumSize(QSize(200, 90))
        self.IOU_QF.setMaximumSize(QSize(200, 90))
        self.IOU_QF.setStyleSheet(u"QFrame#IOU_QF{\n"
"border:2px solid rgba(255, 255, 255, 70);\n"
"border-radius:15px;\n"
"}")
        self.verticalLayout_15 = QVBoxLayout(self.IOU_QF)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.ToggleBotton_2 = QPushButton(self.IOU_QF)
        self.ToggleBotton_2.setObjectName(u"ToggleBotton_2")
        sizePolicy4.setHeightForWidth(self.ToggleBotton_2.sizePolicy().hasHeightForWidth())
        self.ToggleBotton_2.setSizePolicy(sizePolicy4)
        self.ToggleBotton_2.setMinimumSize(QSize(0, 30))
        self.ToggleBotton_2.setMaximumSize(QSize(16777215, 30))
        self.ToggleBotton_2.setFont(font)
        self.ToggleBotton_2.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.ToggleBotton_2.setMouseTracking(True)
        self.ToggleBotton_2.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.ToggleBotton_2.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.ToggleBotton_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.ToggleBotton_2.setAutoFillBackground(False)
        self.ToggleBotton_2.setStyleSheet(u"QPushButton{\n"
"background-image:url(:/setting /images/newsize/IOU.png);\n"
"background-repeat: no-repeat;\n"
"background-position: left center;\n"
"border: none;\n"
"border-left: 20px solid transparent;\n"
"\n"
"text-align: left;\n"
"padding-left: 40px;\n"
"padding-bottom: 4px;\n"
"color: white;\n"
"font: 700 13pt \"Nirmala UI\";\n"
"}")
        self.ToggleBotton_2.setAutoDefault(False)
        self.ToggleBotton_2.setFlat(False)

        self.verticalLayout_15.addWidget(self.ToggleBotton_2)

        self.frame_3 = QFrame(self.IOU_QF)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QSize(0, 20))
        self.frame_3.setMaximumSize(QSize(16777215, 20))
        self.horizontalLayout_16 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_16.setSpacing(10)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(8, 0, 10, 0)
        self.iou_spinbox = QDoubleSpinBox(self.frame_3)
        self.iou_spinbox.setObjectName(u"iou_spinbox")
        self.iou_spinbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.iou_spinbox.setStyleSheet(u"QDoubleSpinBox {\n"
"border: 0px solid lightgray;\n"
"border-radius: 2px;\n"
"background-color: rgba(255,255,255,90);\n"
"font: 600 9pt \"Segoe UI\";\n"
"}\n"
"        \n"
"QDoubleSpinBox::up-button {\n"
"width: 10px;\n"
"height: 9px;\n"
"margin: 0px 3px 0px 0px;\n"
"border-image: url(:/setting /images/newsize/box_up.png);\n"
"}\n"
"QDoubleSpinBox::up-button:pressed {\n"
"margin-top: 1px;\n"
"}\n"
"            \n"
"QDoubleSpinBox::down-button {\n"
"width: 10px;\n"
"height: 9px;\n"
"margin: 0px 3px 0px 0px;\n"
"border-image:url(:/setting /images/newsize/box_down.png);\n"
"}\n"
"QDoubleSpinBox::down-button:pressed {\n"
"margin-bottom: 1px;\n"
"}")
        self.iou_spinbox.setMinimum(0.010000000000000)
        self.iou_spinbox.setMaximum(1.000000000000000)
        self.iou_spinbox.setSingleStep(0.050000000000000)
        self.iou_spinbox.setValue(0.450000000000000)

        self.horizontalLayout_16.addWidget(self.iou_spinbox)

        self.iou_slider = QSlider(self.frame_3)
        self.iou_slider.setObjectName(u"iou_slider")
        self.iou_slider.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.iou_slider.setStyleSheet(u"QSlider::groove:horizontal {\n"
"border: none;\n"
"height: 10px;\n"
"background-color: rgba(255,255,255,90);\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"width: 10px;\n"
"margin: -1px 0px -1px 0px;\n"
"border-radius: 3px;\n"
"background-color: white;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #59969b, stop:1 #04e7fa);\n"
"border-radius: 5px;\n"
"}")
        self.iou_slider.setMinimum(1)
        self.iou_slider.setMaximum(100)
        self.iou_slider.setValue(45)
        self.iou_slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_16.addWidget(self.iou_slider)

        self.horizontalLayout_16.setStretch(0, 3)
        self.horizontalLayout_16.setStretch(1, 7)

        self.verticalLayout_15.addWidget(self.frame_3)


        self.verticalLayout_22.addWidget(self.IOU_QF)

        self.Conf_QF = QFrame(self.setting_page)
        self.Conf_QF.setObjectName(u"Conf_QF")
        self.Conf_QF.setMinimumSize(QSize(200, 90))
        self.Conf_QF.setMaximumSize(QSize(200, 90))
        self.Conf_QF.setStyleSheet(u"QFrame#Conf_QF{\n"
"border:2px solid rgba(255, 255, 255, 70);\n"
"border-radius:15px;\n"
"}")
        self.verticalLayout_18 = QVBoxLayout(self.Conf_QF)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.ToggleBotton_3 = QPushButton(self.Conf_QF)
        self.ToggleBotton_3.setObjectName(u"ToggleBotton_3")
        sizePolicy4.setHeightForWidth(self.ToggleBotton_3.sizePolicy().hasHeightForWidth())
        self.ToggleBotton_3.setSizePolicy(sizePolicy4)
        self.ToggleBotton_3.setMinimumSize(QSize(0, 30))
        self.ToggleBotton_3.setMaximumSize(QSize(16777215, 30))
        self.ToggleBotton_3.setFont(font)
        self.ToggleBotton_3.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.ToggleBotton_3.setMouseTracking(True)
        self.ToggleBotton_3.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.ToggleBotton_3.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.ToggleBotton_3.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.ToggleBotton_3.setAutoFillBackground(False)
        self.ToggleBotton_3.setStyleSheet(u"QPushButton{\n"
"background-image: url(:/setting /images/newsize/conf.png);\n"
"background-repeat: no-repeat;\n"
"background-position: left center;\n"
"border: none;\n"
"border-left: 20px solid transparent;\n"
"\n"
"text-align: left;\n"
"padding-left: 40px;\n"
"padding-bottom: 4px;\n"
"color: white;\n"
"font: 700 13pt \"Nirmala UI\";\n"
"}")
        self.ToggleBotton_3.setAutoDefault(False)
        self.ToggleBotton_3.setFlat(False)

        self.verticalLayout_18.addWidget(self.ToggleBotton_3)

        self.frame = QFrame(self.Conf_QF)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(0, 20))
        self.frame.setMaximumSize(QSize(16777215, 20))
        self.horizontalLayout_17 = QHBoxLayout(self.frame)
        self.horizontalLayout_17.setSpacing(10)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(8, 0, 10, 0)
        self.conf_spinbox = QDoubleSpinBox(self.frame)
        self.conf_spinbox.setObjectName(u"conf_spinbox")
        self.conf_spinbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.conf_spinbox.setStyleSheet(u"QDoubleSpinBox {\n"
"border: 0px solid lightgray;\n"
"border-radius: 2px;\n"
"background-color: rgba(255,255,255,90);\n"
"font: 600 9pt \"Segoe UI\";\n"
"}\n"
"        \n"
"QDoubleSpinBox::up-button {\n"
"width: 10px;\n"
"height: 9px;\n"
"margin: 0px 3px 0px 0px;\n"
"border-image: url(:/setting /images/newsize/box_up.png);\n"
"}\n"
"QDoubleSpinBox::up-button:pressed {\n"
"margin-top: 1px;\n"
"}\n"
"            \n"
"QDoubleSpinBox::down-button {\n"
"width: 10px;\n"
"height: 9px;\n"
"margin: 0px 3px 0px 0px;\n"
"border-image: url(:/setting /images/newsize/box_down.png);\n"
"}\n"
"QDoubleSpinBox::down-button:pressed {\n"
"margin-bottom: 1px;\n"
"}")
        self.conf_spinbox.setMinimum(0.010000000000000)
        self.conf_spinbox.setMaximum(1.000000000000000)
        self.conf_spinbox.setSingleStep(0.050000000000000)
        self.conf_spinbox.setValue(0.250000000000000)

        self.horizontalLayout_17.addWidget(self.conf_spinbox)

        self.conf_slider = QSlider(self.frame)
        self.conf_slider.setObjectName(u"conf_slider")
        self.conf_slider.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.conf_slider.setStyleSheet(u"QSlider::groove:horizontal {\n"
"border: none;\n"
"height: 10px;\n"
"background-color: rgba(255,255,255,90);\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"width: 10px;\n"
"margin: -1px 0px -1px 0px;\n"
"border-radius: 3px;\n"
"background-color: white;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #59969b, stop:1 #04e7fa);\n"
"border-radius: 5px;\n"
"}")
        self.conf_slider.setMinimum(1)
        self.conf_slider.setMaximum(100)
        self.conf_slider.setValue(25)
        self.conf_slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_17.addWidget(self.conf_slider)

        self.horizontalLayout_17.setStretch(0, 3)
        self.horizontalLayout_17.setStretch(1, 7)

        self.verticalLayout_18.addWidget(self.frame)


        self.verticalLayout_22.addWidget(self.Conf_QF)


        self.verticalLayout_6.addWidget(self.setting_page)


        self.mainBox.addWidget(self.settingBox)


        self.verticalLayout.addWidget(self.mainbox)

        self.verticalLayout.setStretch(0, 5)
        self.verticalLayout.setStretch(1, 95)

        self.verticalLayout_4.addWidget(self.mainBody)

        MainWindow.setCentralWidget(self.mainWindow)

        self.retranslateUi(MainWindow)

        self.ToggleBotton_6.setDefault(False)
        self.ToggleBotton_2.setDefault(False)
        self.ToggleBotton_3.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"SGMS", None))
        self.minimizeButton.setText("")
        self.maximizeButton.setText("")
        self.closeButton.setText("")
        self.src_cam.setText(QCoreApplication.translate("MainWindow", u"Cam", None))
        self.src_database.setText(QCoreApplication.translate("MainWindow", u"Data", None))
        self.run_button.setText("")
        self.stop_button.setText("")
        self.control_button.setText("")
        self.main_rightbox.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.ToggleBotton_6.setText(QCoreApplication.translate("MainWindow", u"Model", None))
        self.model_box.setProperty(u"placeholderText", "")
        self.ToggleBotton_2.setText(QCoreApplication.translate("MainWindow", u"IOU", None))
        self.ToggleBotton_3.setText(QCoreApplication.translate("MainWindow", u"Confidence", None))
    # retranslateUi

