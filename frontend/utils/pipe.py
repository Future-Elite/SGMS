from multiprocessing import Pipe

# 创建 pipe 对象
parent_conn, child_conn = Pipe()


def get_parent_conn():
    return parent_conn


def get_child_conn():
    return child_conn
