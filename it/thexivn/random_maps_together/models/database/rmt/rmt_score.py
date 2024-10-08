from typing import Union

from peewee import CharField, IntegerField, fn
from playhouse.hybrid import hybrid_property
from pyplanet.core.db import TimedModel


class RMTScore(TimedModel):
    game_mode = CharField(max_length=50)
    goal_medal = CharField(max_length=7)
    skip_medal = CharField(max_length=7)
    game_time_seconds = IntegerField(default=0)
    total_time: Union[int, IntegerField] = IntegerField(default=0)

    @hybrid_property
    async def total_goal_medals(self) -> int:
        return sum(
            player_score.total_goal_medals
            for player_score in await RMTScore.execute(self.player_scores)
        )

    @total_goal_medals.expression # type: ignore[no-redef]
    def total_goal_medals(cls): # noqa: N805
        return cls.player_scores.rel_model.select(
                fn.SUM(
                    cls.player_scores.rel_model.total_goal_medals,
                ),
            ).where(
                cls.player_scores.rel_model.game_score_id == cls.id,
            )

    @hybrid_property
    async def total_skip_medals(self) -> int:
        return sum(
            player_score.total_skip_medals
            for player_score in await RMTScore.execute(self.player_scores)
        )

    @total_skip_medals.expression # type: ignore[no-redef]
    def total_skip_medals(cls): # noqa: N805
        return cls.player_scores.rel_model.select(
                fn.SUM(
                    cls.player_scores.rel_model.total_skip_medals,
                ),
            ).where(
                cls.player_scores.rel_model.game_score_id == cls.id,
            )

    @hybrid_property
    async def medal_sum(self) -> int:
        return sum(
            player_score.medal_sum
            for player_score in await RMTScore.execute(self.player_scores)
        )

    @medal_sum.expression # type: ignore[no-redef]
    def medal_sum(cls): # noqa: N805
        return cls.player_scores.rel_model.select(
                fn.SUM(
                    cls.player_scores.rel_model.medal_sum,
                ),
            ).where(
                cls.player_scores.rel_model.game_score_id == cls.id,
            )

    @hybrid_property
    async def modified_player_settings(self) -> bool:
        return any(
            any([
                player_score.goal_medal is not None and player_score.goal_medal != self.goal_medal,
                player_score.skip_medal is not None and player_score.game_score.skip_medal != self.skip_medal,
            ])
            for player_score in await RMTScore.execute(self.player_scores)
        )

    @modified_player_settings.expression # type: ignore[no-redef]
    def modified_player_settings(cls) -> bool: # noqa: N805
        return fn.EXISTS(
            cls.player_scores.rel_model.select().where(
            (
                (
                    cls.player_scores.rel_model.goal_medal.is_null(False)
                    &
                    (cls.player_scores.rel_model.goal_medal != cls.goal_medal)
                )
                |
                (
                    cls.player_scores.rel_model.skip_medal.is_null(False)
                    &
                    (cls.player_scores.rel_model.skip_medal != cls.skip_medal)
                )
            )
            &
            (cls.player_scores.rel_model.game_score_id == cls.id),
        ))
