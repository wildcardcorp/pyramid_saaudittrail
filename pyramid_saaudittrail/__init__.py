from sqlalchemy.orm.session import SessionExtension
from models import History, Transaction


class AuditExtension(SessionExtension):
    """Record that a flush has occurred on a session's connection. This allows
    the DataManager to rollback rather than commit on read only transactions.
    """

    def __init__(self, *history_aware):
        self.history_aware_classes = history_aware
        self.current_transaction = None

    def before_commit(self, session):
        print 'before_commit'

    def after_commit(self, session):
        print 'after_commit'

    def after_rollback(self, session):
        print 'after_rollback'

    def save_history(self, session, obj, action):
        if type(obj) in self.history_aware:
            klass = type(obj)
            class_path = "%s.%s" % (klass.__module__, klass.__name__)
            if class_path in self.history_aware_classes:
                if self.current_transaction is None:
                    # XXX get current user somehow here
                    self.current_transaction = Transaction()
                    session.add(self.current_transaction)
                history = History(self.current_transaction,
                    obj, action, class_path)
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
        print 'after_flush'

    def after_flush_postexec(self, session, flush_context):
        print 'after_flush_postexec'

    def after_begin(self, session, transaction, connection):
        print 'after_begin'

    def after_attach(self, session, instance):
        print 'after_attach'

    def after_bulk_update(self, session, query, query_context, result):
        print 'after_bulk_update'

    def after_bulk_delete(self, session, query, query_context, result):
        print 'after_bulk_delete'
