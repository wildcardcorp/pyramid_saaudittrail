from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import (Text, Integer, DateTime, Column, Enum, String,
                        ForeignKey, Unicode)
Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    user = Column(Unicode(200))

    def __init__(self, user='nobody'):
        self.user = user
        self.created_on = datetime.utcnow()


class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    action = Column(Enum('add', 'delete', 'modify', name="action_types"))
    class_path = Column(String(200))
    data = Column(Text, nullable=True)

    def __init__(self, transaction, obj, action, class_path):
        self.transaction_id = transaction.id
        self.action = action
        self.created_on = datetime.utcnow()
        self.class_path = class_path
        if action in ('delete', 'modify'):
            # XXX need to store a copy of the previous object
            # values
            pass
