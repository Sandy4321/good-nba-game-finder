# converts military PM time to 12 hour time
def convert_to_12_hour_time(time_str):
    hour = int(time_str[:2])
    hour = hour - 13
    return str(hour) + time_str[2:-1]

# a Game object that holds vital data about a game
class Game:

    # initializes a game object given information from the API
    def __init__(self, game_dict):
        self.away_team = game_dict["away_team"]["last_name"]
        self.home_team = game_dict["home_team"]["last_name"]
        start_time = game_dict["start_date_time"]
        self.start_time = convert_to_12_hour_time(start_time[len(start_time) - 14: -8])

    # converts military PM time to 12 hour time
    def convert_to_12_hour_time(time_str):
        hour = int(time_str[:2])
        hour = hour - 13
        return str(hour) + time_str[2:-1]

    # prints out the game information
    def print_self(self):
        message = "\n" + self.away_team + " @ " + self.home_team + " at " + self.start_time + " Central Time, \n"
        return message
