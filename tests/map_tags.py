from it.thexivn.random_maps_together.models.map_tag import MapTag


class TestMapTags:
    def expected_map_tags_as_objects(self):
        return [MapTag.from_json(map_tag_json) for map_tag_json in self.expected_map_tags()]

    def expected_map_tags(self):
        return [
            {"ID":1,"Name":"Race","Color":""},
            {"ID":2,"Name":"FullSpeed","Color":""},
            {"ID":3,"Name":"Tech","Color":""},
            {"ID":4,"Name":"RPG","Color":""},
            {"ID":5,"Name":"LOL","Color":""},
            {"ID":6,"Name":"Press Forward","Color":""},
            {"ID":7,"Name":"SpeedTech","Color":""},
            {"ID":8,"Name":"MultiLap","Color":""},
            {"ID":9,"Name":"Offroad","Color":"705100"},
            {"ID":10,"Name":"Trial","Color":""},
            {"ID":11,"Name":"ZrT","Color":"1a6300"},
            {"ID":12,"Name":"SpeedFun","Color":""},
            {"ID":13,"Name":"Competitive","Color":""},
            {"ID":14,"Name":"Ice","Color":"05767d"},
            {"ID":15,"Name":"Dirt","Color":"5e2d09"},
            {"ID":16,"Name":"Stunt","Color":""},
            {"ID":17,"Name":"Reactor","Color":"d04500"},
            {"ID":18,"Name":"Platform","Color":""},
            {"ID":19,"Name":"Slow Motion","Color":"004388"},
            {"ID":20,"Name":"Bumper","Color":"aa0000"},
            {"ID":21,"Name":"Fragile","Color":"993366"},
            {"ID":22,"Name":"Scenery","Color":""},
            {"ID":23,"Name":"Kacky","Color":""},
            {"ID":24,"Name":"Endurance","Color":""},
            {"ID":25,"Name":"Mini","Color":""},
            {"ID":26,"Name":"Remake","Color":""},
            {"ID":27,"Name":"Mixed","Color":""},
            {"ID":28,"Name":"Nascar","Color":""},
            {"ID":29,"Name":"SpeedDrift","Color":""},
            {"ID":30,"Name":"Minigame","Color":"7e0e69"},
            {"ID":31,"Name":"Obstacle","Color":""},
            {"ID":32,"Name":"Transitional","Color":""},
            {"ID":33,"Name":"Grass","Color":"06a805"},
            {"ID":34,"Name":"Backwards","Color":"83aa00"},
            {"ID":35,"Name":"Freewheel","Color":"f2384e"},
            {"ID":36,"Name":"Signature","Color":"f1c438"},
            {"ID":37,"Name":"Royal","Color":"ff0010"},
            {"ID":38,"Name":"Water","Color":"69dbff"},
            {"ID":39,"Name":"Plastic","Color":"fffc00"},
            {"ID":40,"Name":"Arena","Color":""},
            {"ID":41,"Name":"Freestyle","Color":""},
            {"ID":42,"Name":"Educational","Color":""},
            {"ID":43,"Name":"Sausage","Color":""},
            {"ID":44,"Name":"Bobsleigh","Color":""},
            {"ID":45,"Name":"Pathfinding","Color":""},
            {"ID":46,"Name":"FlagRush","Color":"7a0000"},
            {"ID":47,"Name":"Puzzle","Color":"459873"}
        ]
