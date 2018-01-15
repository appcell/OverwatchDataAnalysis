class Killfeed:
    def __init__(self, frame):
        # player and chara might be different from analysis of current frame!
        # Thus extra variables needed.
        self.player1 = {
            "name": "",   # name of chara, or "empty"
            "player": "",  #name of player, or "empty"
            "team": ""   # name of team, or "empty"
        }
        self.player2 = {
            "name": "",   # name of chara, or "empty"
            "player": "",  #name of player, or "empty"
            "team": ""   # name of team, or "empty"
        }
        self.ability = 0  # ability code, see overwatch.py line 282
        self.assists = [{
            "name": "",   # name of chara
            "player": "",  #name of player
            "team": ""
        }]