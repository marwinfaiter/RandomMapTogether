from typing import Union

from peewee import IntegerField
from pyplanet.core.db import TimedModel


class ChessScore(TimedModel):
    total_time: Union[int, IntegerField] = IntegerField(default=0)
