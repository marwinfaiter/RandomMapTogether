from typing import Union

import peeweedbevolve as _
from peewee import IntegerField
from pyplanet.core.db import TimedModel


class ChessScore(TimedModel):
    total_time: Union[int, IntegerField] = IntegerField(default=0)
