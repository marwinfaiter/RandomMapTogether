from attrs import define
from typing import Optional
from pyplanet.apps.core.maniaplanet.models import Player
from ..enums.medals import Medals

@define
class PlayerConfiguration:
    player: Player
    goal_medal: Optional[Medals] = None
    skip_medal: Optional[Medals] = None
    enabled: Optional[bool] = None
