import json
import csv
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QFileDialog, QMessageBox
)

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import User, DeviceState, GestureMap, OperationLog

# 数据库配置
engine = create_engine("sqlite:///data/database.db")
Session = sessionmaker(bind=engine)

# 表映射
TABLE_MAP = {
    "user": User,
    "gesture_map": GestureMap,
    "device_state": DeviceState,
    "operation_log": OperationLog
}


class ResultWindow(QWidget):
    def __init__(self, allowed_tables=None, current_user=None):
        super().__init__()
        self.setWindowTitle("数据表查看器")
        self.resize(750, 500)

        self.session = Session()
        self.allowed_tables = allowed_tables
        self.current_data = []
        self.current_columns = []
        self.current_table_name = None
        self.current_user = current_user

        # 总布局
        self.layout = QVBoxLayout()

        # 按钮区域
        self.button_layout = QHBoxLayout()
        for table_name in TABLE_MAP.keys():
            if self.allowed_tables is not None and table_name not in self.allowed_tables:
                continue  # 如果指定了允许的表名且当前表名不在其中，则跳过
            btn = QPushButton(table_name)
            btn.clicked.connect(self.make_table_loader(table_name))
            self.button_layout.addWidget(btn)
        self.layout.addLayout(self.button_layout)

        # 搜索 + 操作区域
        self.action_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 输入关键词搜索")
        self.search_input.textChanged.connect(self.filter_table)
        self.action_layout.addWidget(self.search_input)

        self.export_csv_btn = QPushButton("导出 CSV")
        self.export_csv_btn.clicked.connect(self.export_csv)
        self.action_layout.addWidget(self.export_csv_btn)

        self.export_excel_btn = QPushButton("导出 Excel")
        self.export_excel_btn.clicked.connect(self.export_excel)
        self.action_layout.addWidget(self.export_excel_btn)

        self.clear_btn = QPushButton("❌ 清空表")
        self.clear_btn.clicked.connect(self.clear_table)
        self.action_layout.addWidget(self.clear_btn)

        self.layout.addLayout(self.action_layout)

        # 当前表标签
        self.label = QLabel("请选择要查看的表")
        self.layout.addWidget(self.label)

        # 表格控件
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.setLayout(self.layout)

    def make_table_loader(self, table_name):
        def load_table():
            self.label.setText(f"当前表：{table_name}")
            self.current_table_name = table_name

            model = TABLE_MAP[table_name]

            if table_name == "operation_log" and self.current_user is not None and not self.current_user.is_admin:
                records = (
                    self.session.query(model)
                    .filter_by(user_id=self.current_user.id)
                    .all()
                )
            else:
                records = self.session.query(model).all()

            self.current_columns = model.__table__.columns.keys()
            self.current_data = []

            for record in records:
                row = []
                for col in self.current_columns:
                    val = getattr(record, col)
                    if isinstance(val, dict):
                        val = json.dumps(val, indent=2, ensure_ascii=False)
                    row.append(str(val))
                self.current_data.append(row)

            self.populate_table(self.current_data, self.current_columns)

        return load_table

    def populate_table(self, data, columns):
        self.table_widget.clear()
        self.table_widget.setColumnCount(len(columns))
        self.table_widget.setRowCount(len(data))
        self.table_widget.setHorizontalHeaderLabels(columns)

        for row_idx, row in enumerate(data):
            for col_idx, val in enumerate(row):
                item = QTableWidgetItem(val)
                item.setTextAlignment(0x0080)  # Align left
                self.table_widget.setItem(row_idx, col_idx, item)

    def filter_table(self):
        keyword = self.search_input.text().strip().lower()
        if not keyword:
            self.populate_table(self.current_data, self.current_columns)
            return

        filtered = [row for row in self.current_data if any(keyword in cell.lower() for cell in row)]
        self.populate_table(filtered, self.current_columns)

    def export_csv(self):
        if not self.current_data:
            return
        path, _ = QFileDialog.getSaveFileName(self, "保存为 CSV 文件", f"{self.current_table_name}.csv", "CSV 文件 (*.csv)")
        if path:
            with open(path, mode='w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.current_columns)
                writer.writerows(self.current_data)

    def export_excel(self):
        if not self.current_data:
            return
        path, _ = QFileDialog.getSaveFileName(self, "保存为 Excel 文件", f"{self.current_table_name}.xlsx", "Excel 文件 (*.xlsx)")
        if path:
            df = pd.DataFrame(self.current_data, columns=self.current_columns)
            df.to_excel(path, index=False)

    def clear_table(self):
        if not self.current_table_name:
            return
        reply = QMessageBox.question(
            self,
            "确认清空表",
            f"你确定要清空 [{self.current_table_name}] 表的所有数据吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            model = TABLE_MAP[self.current_table_name]
            self.session.query(model).delete()
            self.session.commit()
            self.current_data = []
            self.populate_table([], self.current_columns)
            QMessageBox.information(self, "已清空", f"{self.current_table_name} 表已清空。")
