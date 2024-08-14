from attrs import define, field
from it.thexivn.random_maps_together.models.game_views import GameViews
from it.thexivn.random_maps_together.views.rmt.ingame import \
    RandomMapsTogetherIngameView
from it.thexivn.random_maps_together.views.rmt.scoreboard import \
    RandomMapsTogetherScoreBoardView
from it.thexivn.random_maps_together.views.rmt.settings import \
    RandomMapsTogetherSettingsView


@define
class RandomMapsTogetherViews(GameViews):
    settings_view: RandomMapsTogetherSettingsView = field(init=False)
    ingame_view: RandomMapsTogetherIngameView = field(init=False)
    scoreboard_view: RandomMapsTogetherScoreBoardView = field(init=False)
