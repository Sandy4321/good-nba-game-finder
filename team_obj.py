west_threshold = 11
east_threshold = 6

# a Team object that holds vital data for a basketball team
class Team:

    #initializes a Team object given information from the API
    def __init__(self, team_dict):
        if team_dict["streak_type"] is "win":
            self.win_streak = team_dict["streak_total"]
        else:
            self.win_streak = 0
        self.team_name = str(team_dict["last_name"])
        self.win_pct = float(team_dict["win_percentage"])
        self.playoff_seed = team_dict["rank"]
        self.conference = team_dict["conference"]

    #checks whether the team is in the western conference
    def is_west(self):
        return self.conference[0] == 'W'

    #checks whether the team is in the eastern conference
    def is_east(self):
        return self.conference[0] == "E"

    #determines if a team meets the criteria to be worthy
    #to watch
    def is_worthy(self):
        if self.is_east():
            return (self.playoff_seed < east_threshold)
        else:
            return (self.playoff_seed < west_threshold)
