from attrs import define
from typing import Optional
from pyplanet.apps.core.maniaplanet.models import Player

@define
class PlayerConfiguration:
    player: Player
    leader: Optional[bool] = False
