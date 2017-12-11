#  -*- coding: utf-8 -*-
import datetime
import sys
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL

sys.path = [ "." ] + sys.path

import config
import logging
import model

logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

class BaseRepository:
    '''
    Base class for data access repositories.
    Delegates all database operations to a SqlAlchemy session object.
    '''    
    def __init__(self, db, entity_class, pkey):
        self.db = db
        self.entity_class = entity_class
        self.pkey = pkey
        
    def get_query_base(self):
        return self.db.query(self.entity_class)
            
    def get_restricted_query(self):
        return self.restrict_query(self.get_query_base())

    def get_by_id(self, id):
        return self.get_restricted_query().filter(getattr(self.entity_class, self.pkey)==id).first()
    
    def get_all(self):
        return self.get_restricted_query().all() 

    def restrict_query(self, query):
        return query

    def add(self, instance):
        self.db.add(instance)

    def commit(self):
        self.db.commit()

    def save(self, instance):
        self.db.add(instance)
        self.db.commit()

    def expunge(self, instance):
        self.db.expunge(instance)

    def execute_raw_sql(self, query):
        sql = text(query)
        result = self.db.execute(sql)
        return result

    def get_table(self, table):
        sql = 'SELECT * FROM {}'.format(table)
        result = self.execute_raw_sql(sql)
        return result

class QueryFarmRepository(BaseRepository):
    '''
    Repository for access (and update) of farms entities.
    Inherits from BaseRepository
    Example:
        repository = registry.get(QueryFarmRepository)
        farm = repositoty.get_by_id(farm_id) 
    '''
    
    def __init__(self, db):
        super(QueryFarmRepository, self).__init__(db, model.QueryFarm, "isleif_farms_id")
        
    def find_by_key(self,key):
        return self.db.query(model.QueryFarm).filter(model.QueryFarm.jardabok_text_vector.match(key)).all()

    def get_resource_network(self):
        return self.db.query(model.QueryResourceNetwork).all()

    def get_property_network(self):
        return self.db.query(model.QueryPropertyNetwork).all()

    def get_by_text_search(self, searchText):
        return self.db.query(model.QueryFarm).filter(model.QueryFarm.jardabok_full_text.like('%'+searchText+'%')).all()


class PeopleHistoricalRepository(BaseRepository):
    
    def __init__(self, db):
        super(PeopleHistoricalRepository, self).__init__(db, model.LookupPeopleHistorical, "entity_historical_id")

class IsleifFarmRepository(BaseRepository):
    
    def __init__(self, db):
        super(IsleifFarmRepository, self).__init__(db, model.IsleifFarm, "isleif_farms_id")

class JamFullTextRepository(BaseRepository):
    
    def __init__(self, db):
        super(JamFullTextRepository, self).__init__(db, model.JamFullText, "jardabok_full_text_id")

    def get_all_by_farm_id(self,farm_id):
        return self.db.query(model.JamFullText).filter(model.JamFullText.isleif_farms_id == farm_id).all()

class RepositoryRegistry():
    '''
    Registry for singleton access of repositories.
    Example:
        repository = registry.get(FarmRepository) 
    '''

    def __init__(self):
        self.engine = ConnectionFactory.create_new_engine(config.DATABASE)
        self.session = ConnectionFactory.create_new_scoped_session(self.engine)
        self.repositories = dict()
    
    def get(self, cls):
        if cls not in self.repositories:
            self.repositories[cls] = cls(self.session)
        return self.repositories[cls]

    def __del__(self):
        try:
            self.session.close()
            self.engine.dispose()
        except:
            pass
        
    def add(self, instance):
        self.session.add(instance)    

class ConnectionFactory:

    @staticmethod
    def create_new_engine(options):
        return create_engine(URL(**options))

    @staticmethod
    def create_new_scoped_session(engine):
        return scoped_session(
            sessionmaker(
                bind=engine,
                autoflush=True,
                autocommit=False,
                expire_on_commit=True
        ))
    
'''    @staticmethod
    def create_new_session(engine):
        return sessionmaker(bind=engine)()

    @staticmethod
    def create_new(options):
        engine = create_engine(URL(**options))
        Session = sessionmaker(bind=engine)
        session = Session()
        return engine, session
    
    @staticmethod
    def create_new_scoped(options):
        engine = create_engine(URL(**options))
        session = scoped_session(sessionmaker(bind=engine))
        return engine, session'''