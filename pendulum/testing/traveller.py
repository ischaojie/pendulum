from __future__ import annotations

from typing import Optional
from typing import Type

from pendulum.datetime import DateTime
from pendulum.utils._compat import PYPY


class BaseTraveller:
    def __init__(self, datetime_class: Type[DateTime] = DateTime) -> None:
        self._datetime_class: Type[DateTime] = datetime_class

    def freeze(self: BaseTraveller) -> BaseTraveller:
        raise NotImplementedError()

    def travel_back(self: BaseTraveller) -> BaseTraveller:
        raise NotImplementedError()

    def travel(
        self: T,
        years: int = 0,
        months: int = 0,
        weeks: int = 0,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        microseconds: int = 0,
    ) -> BaseTraveller:
        raise NotImplementedError()

    def travel_to(self, dt: DateTime) -> BaseTraveller:
        raise NotImplementedError()


if not PYPY:
    import time_machine

    class Traveller(BaseTraveller):
        def __init__(self, datetime_class: Type[DateTime] = DateTime) -> None:
            super().__init__(datetime_class)

            self._started: bool = False
            self._traveller: Optional[time_machine.travel] = None
            self._coordinates: Optional[time_machine.Coordinates] = None

        def freeze(self) -> Traveller:
            if self._started:
                self._coordinates.move_to(self._datetime_class.now(), tick=False)
            else:
                self._start(freeze=True)

            return self

        def travel_back(self) -> Traveller:
            if not self._started:
                return self

            self._traveller.stop()
            self._coordinates = None
            self._traveller = None
            self._started = False

            return self

        def travel(
            self,
            years: int = 0,
            months: int = 0,
            weeks: int = 0,
            days: int = 0,
            hours: int = 0,
            minutes: int = 0,
            seconds: int = 0,
            microseconds: int = 0,
            *,
            freeze: bool = False
        ) -> Traveller:
            self._start(freeze=freeze)

            self._coordinates.move_to(
                self._datetime_class.now().add(
                    years=years,
                    months=months,
                    weeks=weeks,
                    days=days,
                    hours=hours,
                    minutes=minutes,
                    seconds=seconds,
                    microseconds=microseconds,
                )
            )

            return self

        def travel_to(self, dt: DateTime, *, freeze: bool = False) -> Traveller:
            self._start(freeze=freeze)

            self._coordinates.move_to(dt)

            return self

        def _start(self, freeze: bool = False) -> None:
            if self._started:
                return

            if not self._traveller:
                self._traveller = time_machine.travel(
                    self._datetime_class.now(), tick=not freeze
                )

            self._coordinates = self._traveller.start()

            self._started = True

        def __enter__(self) -> Traveller:
            self._start()

            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.travel_back()

else:
    Traveller = BaseTraveller
