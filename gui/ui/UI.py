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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QFormLayout, QFrame,
    QHBoxLayout, QLabel, QLayout, QMainWindow,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QSplitter, QTextEdit, QVBoxLayout, QWidget)

from gui.ui.utils.UpdateFrame import DoubleClickQFrame
import gui.ui.UI_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(745, 550)
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
"	border-radius:15%;\n"
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
        self.title.setMinimumSize(QSize(0, 25))
        font = QFont()
        font.setFamilies([u"Shojumaru"])
        font.setBold(True)
        self.title.setFont(font)
        self.title.setMouseTracking(True)
        self.title.setTabletTracking(True)
        self.title.setStyleSheet(u"")
        self.title.setIndent(-1)

        self.horizontalLayout.addWidget(self.title, 0, Qt.AlignmentFlag.AlignVCenter)


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

        self.verticalLayout.addWidget(self.topbox, 0, Qt.AlignmentFlag.AlignVCenter)

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
"	border-radius:15%;\n"
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
        self.run_button.setMinimumSize(QSize(60, 60))
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

        self.label = QLabel(self.leftbox_top)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 12))
        font1 = QFont()
        font1.setFamilies([u"Yu Gothic UI"])
        font1.setPointSize(9)
        font1.setBold(True)
        self.label.setFont(font1)

        self.verticalLayout_7.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.stop_button = QPushButton(self.leftbox_top)
        self.stop_button.setObjectName(u"stop_button")
        sizePolicy3.setHeightForWidth(self.stop_button.sizePolicy().hasHeightForWidth())
        self.stop_button.setSizePolicy(sizePolicy3)
        self.stop_button.setMinimumSize(QSize(60, 60))
        self.stop_button.setMaximumSize(QSize(60, 60))
        self.stop_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.stop_button.setStyleSheet(u"QPushButton{\n"
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

        self.label_3 = QLabel(self.leftbox_top)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 12))
        font2 = QFont()
        font2.setFamilies([u"Yu Gothic UI"])
        font2.setBold(True)
        self.label_3.setFont(font2)

        self.verticalLayout_7.addWidget(self.label_3, 0, Qt.AlignmentFlag.AlignHCenter)


        self.horizontalLayout_8.addLayout(self.verticalLayout_7)


        self.verticalLayout_3.addWidget(self.leftbox_top)

        self.ControlBox = QFrame(self.leftbox_bottom)
        self.ControlBox.setObjectName(u"ControlBox")
        self.ControlBox.setMinimumSize(QSize(100, 100))
        self.ControlBox.setMaximumSize(QSize(100, 100))
        self.ControlBox.setFrameShape(QFrame.Shape.StyledPanel)
        self.ControlBox.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.ControlBox)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.src_database = QPushButton(self.ControlBox)
        self.src_database.setObjectName(u"src_database")
        self.src_database.setMinimumSize(QSize(60, 60))
        self.src_database.setMaximumSize(QSize(60, 60))
        self.src_database.setMouseTracking(True)
        self.src_database.setTabletTracking(True)
        self.src_database.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.src_database.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.src_database, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.label_5 = QLabel(self.ControlBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 20))
        self.label_5.setFont(font1)

        self.verticalLayout_8.addWidget(self.label_5, 0, Qt.AlignmentFlag.AlignLeft)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer)


        self.verticalLayout_3.addWidget(self.ControlBox)


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
        self.main_rightbox.setMinimumSize(QSize(200, 80))
        self.main_rightbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.splitter.addWidget(self.main_rightbox)

        self.horizontalLayout_9.addWidget(self.splitter)


        self.verticalLayout_5.addWidget(self.rightbox_main)

        self.user_info = QTextEdit(self.rightBox)
        self.user_info.setObjectName(u"user_info")
        self.user_info.setMinimumSize(QSize(110, 110))
        self.user_info.setMaximumSize(QSize(16777215, 120))
        self.user_info.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.CrossCursor))
        self.user_info.setMouseTracking(True)
        self.user_info.setTabletTracking(True)
        self.user_info.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.user_info.setAcceptDrops(True)
        self.user_info.setFrameShape(QFrame.Shape.WinPanel)
        self.user_info.setUndoRedoEnabled(False)
        self.user_info.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.verticalLayout_5.addWidget(self.user_info)

        self.verticalLayout_5.setStretch(1, 86)

        self.mainBox.addWidget(self.rightBox)

        self.settingBox = QFrame(self.mainbox)
        self.settingBox.setObjectName(u"settingBox")
        self.settingBox.setMinimumSize(QSize(0, 200))
        self.settingBox.setMaximumSize(QSize(140, 16777215))
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
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.iou_slider = QSlider(self.setting_page)
        self.iou_slider.setObjectName(u"iou_slider")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.iou_slider.sizePolicy().hasHeightForWidth())
        self.iou_slider.setSizePolicy(sizePolicy4)
        self.iou_slider.setMinimumSize(QSize(45, 0))
        self.iou_slider.setMaximumSize(QSize(45, 16777215))
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
        self.iou_slider.setOrientation(Qt.Orientation.Vertical)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.iou_slider)

        self.conf_slider = QSlider(self.setting_page)
        self.conf_slider.setObjectName(u"conf_slider")
        sizePolicy4.setHeightForWidth(self.conf_slider.sizePolicy().hasHeightForWidth())
        self.conf_slider.setSizePolicy(sizePolicy4)
        self.conf_slider.setMinimumSize(QSize(45, 0))
        self.conf_slider.setMaximumSize(QSize(45, 16777215))
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
        self.conf_slider.setOrientation(Qt.Orientation.Vertical)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.conf_slider)

        self.label_2 = QLabel(self.setting_page)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(40, 40))
        font3 = QFont()
        font3.setFamilies([u"Yu Gothic UI"])
        font3.setPointSize(10)
        font3.setBold(True)
        self.label_2.setFont(font3)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.label_4 = QLabel(self.setting_page)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(40, 40))
        self.label_4.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.label_4)

        self.iou_spinbox = QDoubleSpinBox(self.setting_page)
        self.iou_spinbox.setObjectName(u"iou_spinbox")
        self.iou_spinbox.setMaximumSize(QSize(45, 16777215))
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

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.iou_spinbox)

        self.conf_spinbox = QDoubleSpinBox(self.setting_page)
        self.conf_spinbox.setObjectName(u"conf_spinbox")
        self.conf_spinbox.setMinimumSize(QSize(45, 0))
        self.conf_spinbox.setMaximumSize(QSize(45, 16777215))
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

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.conf_spinbox)


        self.verticalLayout_22.addLayout(self.formLayout)

        self.status = QLabel(self.setting_page)
        self.status.setObjectName(u"status")
        self.status.setMinimumSize(QSize(250, 40))
        self.status.setMouseTracking(True)
        self.status.setTabletTracking(True)

        self.verticalLayout_22.addWidget(self.status)


        self.verticalLayout_6.addWidget(self.setting_page)


        self.mainBox.addWidget(self.settingBox)


        self.verticalLayout.addWidget(self.mainbox)

        self.verticalLayout.setStretch(0, 5)
        self.verticalLayout.setStretch(1, 95)

        self.verticalLayout_4.addWidget(self.mainBody)

        MainWindow.setCentralWidget(self.mainWindow)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u591a\u573a\u666f\u624b\u52bf\u667a\u80fd\u4ea4\u4e92\u63a7\u5236\u7cfb\u7edf", None))
        self.minimizeButton.setText("")
        self.maximizeButton.setText("")
        self.closeButton.setText("")
        self.run_button.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb/\u6682\u505c", None))
        self.stop_button.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u7ec8\u6b62", None))
        self.src_database.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"        \u6570\u636e\u5e93", None))
        self.main_rightbox.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"   IOU", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u7f6e\u4fe1\u5ea6", None))
        self.status.setText("")
    # retranslateUi

