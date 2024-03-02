"""Module specifying the data to pass between different components"""

from datetime import datetime
from typing import Any, Optional


class Data:
    """Data class for sending messages between modules"""

    def __init__(
        self,
        header: str = None,
        payload: Any = None,
        timestamp: Optional[datetime] = None,
    ) -> None:
        self._header: str = header
        self._payload: Any = payload
        self._timestamp: datetime = (
            timestamp if timestamp is not None else datetime.now()
        )

    @property
    def header(self) -> str:
        return self._header

    @header.setter
    def header(self, value: str) -> None:
        self._header = value

    @property
    def payload(self) -> Any:

        return self._payload

    @payload.setter
    def payload(self, value: Any) -> None:
        self._payload = value

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: datetime) -> None:
        self._timestamp = value

    def __repr__(self) -> str:
        return f"Data(header={self.header}, timestamp={self.timestamp}, payload={self.payload})"


class StopData(Data):
    """A stop message to tell queues to stop processing"""

    def __init__(self):
        super().__init__(header="STOP", payload=None)
