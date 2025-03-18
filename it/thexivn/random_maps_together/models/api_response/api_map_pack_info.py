from attrs import define


@define(frozen=True)
class APIMapPackInfo:
    id: int
    name: str
    track_count: int

    @classmethod
    def from_json(cls, json):
        return cls(
            json["MappackId"],
            json["Name"],
            json["MapCount"],
        )
