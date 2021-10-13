class UserRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    using = 'admin'
    route_app_labels = ['auth', 'contenttypes', 'admin', 'core', 'sessions', 'migrations']

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return self.using
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return self.using
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if (obj1._meta.app_label in self.route_app_labels or \
                obj2._meta.app_label in self.route_app_labels):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label in self.route_app_labels:
            return db == self.using
        return None


UltraTech_APP = ['ultratech_analysis', 'ultratech_core', 'ultratech_new_destination']


class UltraTechRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """

    using = 'ultra_tech'

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label in UltraTech_APP:
            return self.using
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label in UltraTech_APP:
            return self.using
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label in UltraTech_APP or \
                obj2._meta.app_label in UltraTech_APP:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label in UltraTech_APP:
            return db == self.using
        return None


Chemicals_APP = ['chemical_analysis', 'chemical_core']


class ChemicalsRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """

    using = 'chemicals'

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label in Chemicals_APP:
            return self.using
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label in Chemicals_APP:
            return self.using
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label in Chemicals_APP or \
                obj2._meta.app_label in Chemicals_APP:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label in Chemicals_APP:
            return db == self.using
        return None
