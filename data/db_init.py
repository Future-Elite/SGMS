from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, GestureMap, OperationTypeEnum
from datetime import datetime


# 手势初始数据
gesture_data = [
    {"gesture_name": "Left_Double_Click", "operation_type": OperationTypeEnum.click, "operation_param": "double_left"},
    {"gesture_name": "backward", "operation_type": OperationTypeEnum.swipe, "operation_param": "prev"},
    {"gesture_name": "forward", "operation_type": OperationTypeEnum.swipe, "operation_param": "next"},
    {"gesture_name": "high", "operation_type": OperationTypeEnum.zoom, "operation_param": "increase"},
    {"gesture_name": "left_click", "operation_type": OperationTypeEnum.click, "operation_param": "left"},
    {"gesture_name": "low", "operation_type": OperationTypeEnum.zoom, "operation_param": "decrease"},
    {"gesture_name": "mouse", "operation_type": OperationTypeEnum.move, "operation_param": "move"},
    {"gesture_name": "pause", "operation_type": OperationTypeEnum.click, "operation_param": "pause"},
    {"gesture_name": "right_click", "operation_type": OperationTypeEnum.click, "operation_param": "right"},
    {"gesture_name": "start", "operation_type": OperationTypeEnum.click, "operation_param": "start"},
]


# 插入数据
def init_gestures():
    session = SessionLocal()
    try:
        for item in gesture_data:
            exists = session.query(GestureMap).filter_by(gesture_name=item["gesture_name"]).first()
            if not exists:
                gesture = GestureMap(
                    gesture_name=item["gesture_name"],
                    operation_type=item["operation_type"],
                    operation_param=item["operation_param"],
                    created_at=datetime.utcnow()
                )
                session.add(gesture)
        session.commit()
        print("✅ 手势初始化完成")
    except Exception as e:
        session.rollback()
        print("❌ 初始化出错:", e)
    finally:
        session.close()


if __name__ == "__main__":
    # 如果数据库文件存在，则删除
    import os
    if os.path.exists('database.db'):
        os.remove('database.db')
        print("✅ 删除旧数据库文件")
    else:
        print("❌ 数据库文件不存在")

    # 数据库连接地址
    DATABASE_URL = 'sqlite:///database.db'

    # 初始化数据库连接
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(bind=engine)

    # 创建所有表
    Base.metadata.create_all(engine)

    # 初始化手势数据
    init_gestures()
