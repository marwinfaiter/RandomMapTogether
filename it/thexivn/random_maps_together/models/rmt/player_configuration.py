from typing import Optional

from attrs import define
from it.thexivn.random_maps_together.models.enums.medals import Medals
from pyplanet.apps.core.maniaplanet.models import Player


@define
class PlayerConfiguration:
    player: Player
    goal_medal: Optional[Medals] = None
    skip_medal: Optional[Medals] = None
    enabled: Optional[bool] = None
