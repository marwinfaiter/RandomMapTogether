from attrs import define, field

from ....views.rmt.ingame import RandomMapsTogetherIngameView
from ....views.rmt.scoreboard import RandomMapsTogetherScoreBoardView
from ....views.rmt.settings import RandomMapsTogetherSettingsView
from .. import GameViews


@define
class RandomMapsTogetherViews(GameViews):
    settings_view: RandomMapsTogetherSettingsView = field(init=False)
    ingame_view: RandomMapsTogetherIngameView = field(init=False)
    scoreboard_view: RandomMapsTogetherScoreBoardView = field(init=False)
