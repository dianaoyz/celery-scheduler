from app.extensions import db
from sqlalchemy.inspection import inspect
from psycopg2.extensions import register_adapter, AsIs
import numpy as np
def adapt_numpy_int64(numpy_int64):
    """ Adapting numpy.int64 type to SQL-conform int type using psycopg extension, see [1]_ for more info.
     References
    ----------
    .. [1] http://initd.org/psycopg/docs/advanced.html#adapting-new-python-types-to-sql-syntax
    """
    return AsIs(numpy_int64)

register_adapter(np.int64, adapt_numpy_int64) 

class MethodsMixin(object):
    """
    This class mixes in some common Class table functions like
    delete and save
    """
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def update(self):
        db.session.commit()
        return self.id

    def delete(self):
        ret = self.id
        db.session.delete(self)
        db.session.commit()
        return ret

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    def serialize_list(self, lis):
        return [m.serialize() for m in lis]

        
class Race(db.Model, MethodsMixin):
    __tablename__ = 'races'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    season = db.Column(db.Integer)
    raceName = db.Column(db.String(120))
    roundId = db.Column(db.Integer)

    def __init__(self, **kwargs):
        keys = ['id', 'season', 'raceName', 'roundId']
        for key in keys:
            setattr(self, key, kwargs.get(key))

class Results(db.Model, MethodsMixin):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    constructorRef = db.Column(db.String(120))
    driverRef = db.Column(db.String(120))
    season = db.Column(db.Integer)
    roundId = db.Column(db.Integer)
    grid = db.Column(db.Integer)
    laps = db.Column(db.Integer)
    position = db.Column(db.Integer)
    status = db.Column(db.String(120))
    raceName = db.Column(db.String(120))

    def __init__(self, **kwargs):
        keys = ['id', 'constructorRef', 'driverRef', 'season', 'roundId', 'grid', 'laps',  'position', 'status', 'raceName']
        for key in keys:
            setattr(self, key, kwargs.get(key))

class Schedule(db.Model, MethodsMixin):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.String(50))
    
    def __init__(self, **kwargs):
        keys = ["task_id"]
        for key in keys:
            setattr(self, key, kwargs.get(key))

