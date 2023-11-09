from attrs import define, field
from pyplanet.views.generics.widget import WidgetView


@define
class GameViews:
    settings_view: WidgetView = field(init=False)
    ingame_view: WidgetView = field(init=False)
