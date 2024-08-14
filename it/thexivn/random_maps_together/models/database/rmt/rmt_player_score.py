from it.thexivn.random_maps_together.models.database.rmt.rmt_score import \
    RMTScore
from it.thexivn.random_maps_together.models.enums.medals import Medals
from peewee import CharField, ForeignKeyField, IntegerField
from playhouse.hybrid import hybrid_property
from pyplanet.apps.core.maniaplanet.models import Player
from pyplanet.core.db import TimedModel


class RMTPlayerScore(TimedModel):
    game_score = ForeignKeyField(RMTScore, related_name="player_scores")
    player = ForeignKeyField(Player)
    goal_medal = CharField(max_length=7, null=True)
    skip_medal = CharField(max_length=7, null=True)
    author_medals = IntegerField(default=0)
    gold_medals = IntegerField(default=0)
    silver_medals = IntegerField(default=0)
    bronze_medals = IntegerField(default=0)
    total_goal_medals = IntegerField(default=0)
    total_skip_medals = IntegerField(default=0)

    class Meta:
        indexes = (
            (("game_score", "player"), True),
        )

    @hybrid_property
    def medal_sum(self) -> int:
        assert isinstance(self.author_medals, int)
        assert isinstance(self.gold_medals, int)
        assert isinstance(self.silver_medals, int)
        assert isinstance(self.bronze_medals, int)
        return sum([
            self.author_medals * Medals.AUTHOR.value,
            self.gold_medals * Medals.GOLD.value,
            self.silver_medals * Medals.SILVER.value,
            self.bronze_medals * Medals.BRONZE.value,
        ])

    @staticmethod
    async def get_top_20_players(game_id: int):
        return await RMTPlayerScore.execute(
            RMTPlayerScore
            .select(RMTPlayerScore, Player)
            .join(Player)
            .where(RMTPlayerScore.game_score == game_id)
            .order_by(
                RMTPlayerScore.goal_medal,
                RMTPlayerScore.skip_medal,
                RMTPlayerScore.total_goal_medals.desc(),
                RMTPlayerScore.total_skip_medals.desc(),
                RMTPlayerScore.author_medals.desc(),
                RMTPlayerScore.gold_medals.desc(),
                RMTPlayerScore.silver_medals.desc(),
                RMTPlayerScore.bronze_medals.desc(),
            )
            .limit(20),
        )

    async def increase_medal_count(self, medal: Medals):
        assert isinstance(self.author_medals, int)
        assert isinstance(self.gold_medals, int)
        assert isinstance(self.silver_medals, int)
        assert isinstance(self.bronze_medals, int)
        assert isinstance(self.total_goal_medals, int)
        assert isinstance(self.total_skip_medals, int)

        game_score = (
            self.game_score
            if isinstance(self.game_score, RMTScore)
            else await self.game_score
         )

        if self.goal_medal:
            if medal.name == self.goal_medal:
                self.total_goal_medals += 1
        elif medal.name == game_score.goal_medal:
            self.total_goal_medals += 1

        if self.skip_medal:
            if medal.name == self.skip_medal:
                self.total_skip_medals += 1
        elif medal.name == game_score.skip_medal:
            self.total_skip_medals += 1

        if medal == Medals.AUTHOR:
            self.author_medals += 1
        elif medal == Medals.GOLD:
            self.gold_medals += 1
        elif medal == Medals.SILVER:
            self.silver_medals += 1
        elif medal == Medals.BRONZE:
            self.bronze_medals += 1
