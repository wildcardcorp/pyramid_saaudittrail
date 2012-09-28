from sqlalchemy.orm.session import SessionExtension
from models import History, Transaction
from sqlalchemy import func
from sqlalchemy.orm.attributes import NO_VALUE


class AuditExtension(SessionExtension):
    """Record that a flush has occurred on a session's connection. This allows
    the DataManager to rollback rather than commit on read only transactions.
    """

    def __init__(self, *history_aware, **kwargs):
        self.history_aware_classes = history_aware
        self.current_transaction = None
        ignored = list(kwargs.get('ignored_fields', ()))
        ignored.append('_sa_instance_state')
        self.ignored_fields = set(ignored)

    def get_transaction(self, session):
        if self.current_transaction is None:
            trn_id = session.query(func.MAX(Transaction.id)).one()[0]
            if trn_id is None:
                trn_id = 0
            else:
                trn_id += 1
            self.current_transaction = Transaction(trn_id)
            session.add(self.current_transaction)
        return self.current_transaction

    def get_changed_data(self, obj):
        data = {}
        state = obj._sa_instance_state
        for name, value in state.committed_state.items():
            if name in self.ignored_fields or value == NO_VALUE:
                continue
            data[name] = value
        return data

    def save_history(self, session, obj, action):
        klass = type(obj)
        class_path = "%s.%s" % (klass.__module__, klass.__name__)
        if class_path in self.history_aware_classes:
            data = self.get_changed_data(obj)
            if data or action in ('delete', 'add'):
                transaction = self.get_transaction(session)
                history = History(transaction.id, obj, action,
                                  class_path, data)
                session.add(history)

    def before_flush(self, session, flush_context, instances):
        for obj in session.new:
            # just added objects
            self.save_history(session, obj, 'add')

        for obj in session.deleted:
            self.save_history(session, obj, 'delete')

        for obj in session.dirty:
            self.save_history(session, obj, 'modify')

    def after_flush(self, session, flush_context):
        self.current_transaction = None
