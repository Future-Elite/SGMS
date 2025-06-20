from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from data.models import OperationLog, DeviceTypeEnum, ResultEnum

celery_app = Celery('tasks', broker='memory://', backend='rpc://')
celery_app.conf.update(task_always_eager=True, broker_connection_retry_on_startup=True)


engine = create_engine('sqlite:///data/database.db', echo=False)
SessionLocal = scoped_session(sessionmaker(bind=engine))


@celery_app.task
def async_commit_log(log_data):
    session = SessionLocal()
    try:
        log_entry = OperationLog(
            user_id=log_data['user_id'],
            gesture_id=log_data["gesture_id"],
            operation_type=log_data["operation_type"],
            device_type=DeviceTypeEnum[log_data["device_type"]],
            result=ResultEnum[log_data["result"]],
            detail=log_data["detail"]
        )
        session.add(log_entry)
        session.commit()
    except Exception as e:
        print("Celery error:", e)
        session.rollback()
    finally:
        session.close()
