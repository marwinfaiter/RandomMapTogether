from typing import Optional

from attrs import define
from pyplanet.apps.core.maniaplanet.models import Player


@define
class PlayerConfiguration:
    player: Player
    leader: Optional[bool] = False
