
# PLAYER CLASS ------------------------------------------------------------------------
class Player(object):

    # default constructor
    def __init__(self):
        self.name = ''
        self.team = "DEFAULT"
    
    # alternate constructor with each member variable
    # provided as parameters    
    def alt_ctor(self, name, team_name):
        self.name = name
        self.team = team_name
        return self

    # sets player's name to @param name
    def set_name(self, name):
        self.name = name

    # sets player's num_of_games to @param num
    def set_team(self, team_name):
        self.team = team_name
    
    def get_name(self):
        return self.name
