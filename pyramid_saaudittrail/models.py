from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pyramid.threadlocal import get_current_request
from pyramid.security import authenticated_userid
import ajson as json
from sqlalchemy import (Text, Integer, DateTime, Column, Enum, String,
                        ForeignKey, Unicode)
from sqlalchemy.orm import relationship
Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    user = Column(Unicode(200))
    history = relationship("History")

    def __init__(self, id=None):
        if id is not None:
            self.id = id
        req = get_current_request()
        self.user = authenticated_userid(req)
        self.created_on = datetime.utcnow()


class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    action = Column(Enum('add', 'delete', 'modify', name="action_types"))
    class_path = Column(String(200))
    data = Column(Text, nullable=True)

    def __init__(self, transaction_id=None, obj=None, action=None,
                 class_path=None, change_data={}):
        if transaction_id is None:
            return
        self.transaction_id = transaction_id
        self.action = action
        self.created_on = datetime.utcnow()
        self.class_path = class_path
        if action in ('delete', 'modify'):
            data = obj.__dict__.copy()
            if '_sa_instance_state' in data:
                del data['_sa_instance_state']
            data.update(change_data)
            self.data = json.dumps(data)
