from sqlalchemy.orm.session import SessionExtension
from models import History, Transaction
from sqlalchemy import func


class AuditExtension(SessionExtension):
    """Record that a flush has occurred on a session's connection. This allows
    the DataManager to rollback rather than commit on read only transactions.
    """

    def __init__(self, *history_aware):
        self.history_aware_classes = history_aware
        self.current_transaction = None

    def save_history(self, session, obj, action):
        klass = type(obj)
        class_path = "%s.%s" % (klass.__module__, klass.__name__)
        if class_path in self.history_aware_classes:
            if self.current_transaction is None:
                trn_id = session.query(func.MAX(Transaction.id)).one()[0]
                if trn_id is None:
                    trn_id = 0
                else:
                    trn_id += 1
                self.current_transaction = Transaction(trn_id)
                session.add(self.current_transaction)
            history = History(trn_id, obj, action, class_path)
            session.add(history)

    def before_flush(self, session, flush_context, instances):
        for obj in session.new:
            # just added objects
            self.save_history(session, obj, 'add')
            print 'added', obj

        for obj in session.deleted:
            self.save_history(session, obj, 'delete')
            print 'deleted', obj

        for obj in session.dirty:
            self.save_history(session, obj, 'modify')
            print 'modified', obj
        print 'before_flush'

    def after_flush(self, session, flush_context):
        self.current_transaction = None
