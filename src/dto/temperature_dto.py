from src.dto.temperature_entity import TemperatureEntity
from src import time_utils

class TemperatureDto:
    def __init__(
        self,
        stations_id: int,
        mess_datum: int,
        qn: int,
        pp_10: float,
        tt_10: float,
        rf_10: float,
        td_10: float,
    ):
        self.stations_id = stations_id
        self.mess_datum = mess_datum
        self.qn = qn
        self.pp_10 = pp_10
        self.tt_10 = tt_10
        self.rf_10 = rf_10
        self.td_10 = td_10

    # Convert to dict for JSON serialization
    def to_dict(self):
        return {
            "STATIONS_ID": self.stations_id,
            "MESS_DATUM": self.mess_datum,
            "QN": self.qn,
            "PP_10": self.pp_10,
            "TT_10": self.tt_10,
            "RF_10": self.rf_10,
            "TD_10": self.td_10,
        }

    def to_entity(self):
        return TemperatureEntity(
            stations_id=self.stations_id,
            mess_datum=time_utils.parse_date(self.mess_datum),
            qn=self.qn,
            pp_10=self.pp_10,
            tt_10=self.tt_10,
            rf_10=self.rf_10,
            td_10=self.td_10,
        )

    def __str__(self):
        return f"TemperatureDto(STATIONS_ID={self.stations_id}, MESS_DATUM={self.mess_datum}, QN={self.qn}, PP_10={self.pp_10}, TT_10={self.tt_10}, RF_10={self.rf_10}, TD_10={self.td_10})"

    # Optional: good for debugging in REPL/logs
    def __repr__(self):
        return self.__str__()
