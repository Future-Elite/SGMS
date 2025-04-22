from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.models import User, DeviceState, GestureMap, OperationLog

# 数据库配置
engine = create_engine("sqlite:///data/database.db", echo=False)
Session = sessionmaker(bind=engine)

# 表映射
TABLE_MAP = {
    "user": User,
    "gesture_map": GestureMap,
    "device_state": DeviceState,
    "operation_log": OperationLog
}


class ResultWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据表查看器")
        self.resize(900, 600)

        self.layout = QVBoxLayout()

        # 顶部按钮区域
        self.button_layout = QHBoxLayout()
        self.table_buttons = {}

        for table_name in TABLE_MAP.keys():
            btn = QPushButton(table_name)
            btn.clicked.connect(self.make_table_loader(table_name))
            self.button_layout.addWidget(btn)
            self.table_buttons[table_name] = btn

        self.layout.addLayout(self.button_layout)

        # 当前表名提示
        self.label = QLabel("请选择要查看的表")
        self.layout.addWidget(self.label)

        # 表格控件
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.setLayout(self.layout)

    def make_table_loader(self, table_name):
        def load_table():
            self.label.setText(f"当前表：{table_name}")
            session = Session()
            model = TABLE_MAP[table_name]
            records = session.query(model).all()
            session.close()

            columns = model.__table__.columns.keys()
            self.table_widget.setColumnCount(len(columns))
            self.table_widget.setHorizontalHeaderLabels(columns)
            self.table_widget.setRowCount(len(records))

            for row_idx, record in enumerate(records):
                for col_idx, col_name in enumerate(columns):
                    value = getattr(record, col_name)
                    self.table_widget.setItem(
                        row_idx, col_idx, QTableWidgetItem(str(value))
                    )

        return load_table
