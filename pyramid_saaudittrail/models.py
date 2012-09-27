from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import (Text, Integer, DateTime, Column, Enum, String)
Base = declarative_base()


class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    action = Column(Enum('add', 'delete', 'modify', name="action_types"))
    created_on = Column(DateTime, default=datetime.utcnow)
    class_path = Column(String(200))
    data = Column(Text, nullable=True)

    def __init__(self, obj, action, class_path):
        self.action = action
        self.created_on = datetime.utcnow()
        self.class_path = class_path
        if action in ('delete', 'modify'):
            # XXX need to store a copy of the previous object
            # values
            pass
