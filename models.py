from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time

@dataclass()
class Direction:
    name: str
    url: str
    subway: Station = None


@dataclass()
class Train:
    _id: int
    stations: list[StationLink] = field(default_factory=list)


@dataclass(unsafe_hash=True)
class Station:
    _id: int
    name: str = field(compare=False)
    zone: int = field(compare=False, default=-1)
    metro: bool = field(compare=False, default=False)
    subway: bool = field(compare=False, default=False)

    @property
    def url(self):
        return f'/station.php?nnst={self._id}'


@dataclass(unsafe_hash=True)
class StationLink:
    station_id: int
    time: datetime
    stop: bool = True


@dataclass()
class ScheduleItem:
    url: str
    time: datetime
    period: str
