from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SessionType
from src import logging_conf
from typing import Any

from src.models_base import Base

class TemperatureDbSession:
    logger = logging_conf.config("DbSession")
    session: SessionType

    def __init__(
        self,
        db_url: str = None,
        db_port: str = None,
        db_user: str = None,
        db_pass: str = None,
        db_name: str = None,
    ):
        self.logger.debug(
            f"url: {db_url}, user: {db_user}, pass: {db_pass}, name: {db_name}"
        )
        database_url = (
            f"postgresql+psycopg2://{db_user}:{db_pass}@{db_url}:{db_port}/{db_name}"
        )
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = None

    def __enter__(self):
        self.session = self.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                self.session.rollback()
                self.logger.error(f"Rolling back due to exception: {exc_val}")
            else:
                self.session.commit()
                self.logger.info("Transaction committed successfully")
        finally:
            self.session.close()
            self.logger.info("Session closed")

    def write(self, data: Any):
        self.session.add(data)
        self.session.commit()
        self.logger.info(f"Added {data} to session")
