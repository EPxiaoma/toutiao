from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from utils.exception import http_exception_handler, integrity_error_handler, sqlalchemy_error_handler, \
    general_exception_handler


def register_exception_handlers(app):
    """
    注册全局异常处理：子类在前，父类在后；具体在前，抽象在后
    """
    app.add_exception_handler(HTTPException, http_exception_handler) # 业务异常
    app.add_exception_handler(IntegrityError, integrity_error_handler) # 数据约束异常（子类）
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler) # 数据库异常（父类）
    app.add_exception_handler(Exception, general_exception_handler) # 其它异常