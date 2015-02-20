import input_handler
import api_interface
import urllib2
import json
import string
import private_info
from game_obj import Game
from team_obj import Team

west_threshold = 11
east_threshold = 6

my_team = [ {"name": "John Wall", "team": "Wizards"},
        {"name": "Jonas Valanciunas", "team": "Raptors"}, 
        {"name": "Kawhi Leonard", "team": "Spurs"},
        {"name": "Tim Duncan", "team": "Spurs"},
        {"name": "Kyle Lowry", "team": "Raptors"},
        {"name": "Giannis Antetokounmpo", "team": "Bucks"},
        {"name": "Khris Middleton", "team": "Bucks"},
        {"name": "Jose Calderon", "team": "Knicks"},
        {"name": "Rudy Gobert", "team": "Jazz"},
        {"name": "Eric Gordon", "team": "Pelicans"},
        {"name": "Jrue Holiday", "team": "Pelicans"},
        {"name": "Gerald Henderson", "team": "Hornets"},
        {"name": "Robin Lopez", "team": "Trail Blazers"}]

#loads private information (passcodes, emails) from JSON
def load_private_info():
    return private_info.privates

# returns true if the teams in the game are
# the tenth seed or above if they're in the western
# conference or fifth seed and above in the eastern conference
def find_good_games(games, teams):
    good_games = []

    for game in games:
        if teams[game.home_team].is_worthy() and teams[game.away_team].is_worthy():
            good_games.append(game)

    return good_games

# makes a dictionary of Team objects given the standings
# from the XMLStats API
def make_team_dict(standings):
    team_dict = {}
    for team in standings:
        new_team = Team(team)
        team_dict[new_team.team_name] = new_team
    return team_dict

# makes a dictionary of Game objects given the schedule
# from the XMLStats API
def make_game_dict(schedule):
    games_arr = []
    for game in schedule:
        games_arr.append(Game(game))
    return games_arr

# formats each game in @param games in a string
def list_games(games):
    message = "These are the good games today:\n"
    for game in games:
        message += game.print_self()
    message = message[:-3]
    message += "."
    return message

def find_active_players(games):
    actives = []
    for game in games:
        for player in my_team:
            if player["team"] == game.away_team or player["team"] == game.home_team:
                actives.append(player)
    return actives

def list_players(players):
    message = "\n----------------------------------------------------------------\nAnd your active fantasy players today are:\n"
    for player in players:
        message += "\n" + player["name"] + "\n"

    return message

# runs main
def main():
    # loads passwords into local variable
    private_info = load_private_info()

    # fetches NBA standings and schedule from XMLStats API
    standings = api_interface.fetch("https://erikberg.com/nba/standings.json", private_info["Access Token"])["standing"]
    schedule = api_interface.fetch("https://erikberg.com/events.json", private_info["Access Token"])["event"]

    # formats API information into custom dict of Team and Game objects
    teams = make_team_dict(standings)
    games = make_game_dict(schedule)

    # finds which players on my team are active today
    # and string-ifys them  
    active_players = find_active_players(games)

    # short circuit return if there are no good games
    if len(games) is 0:
        print "No good games today."
        return False
    
    # finds good matchups within the games dict
    good_games = find_good_games(games, teams)    

    # returns a list of the good games and activ
    # players in a nice format
    message_body = list_games(good_games)
    return message_body

