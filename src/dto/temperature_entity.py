from sqlalchemy import Column, Integer, DateTime, func, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid

from src.models_base import Base


class TemperatureEntity(Base):
    __tablename__ = "temperature"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  #
    stations_id = Column(Integer)
    messdatum = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    qn = Column(Integer)
    pp_10 = Column(Float)
    tt_10 = Column(Float)
    rf_10 = Column(Float)
    td_10 = Column(Float)

    def __str__(self):
        return f"StatusPollEntity: ({self.id}, {self.stations_id}, {self.messdatum}, {self.qn}, {self.pp_10}, {self.tt_10}, {self.rf_10}, {self.td_10})"
