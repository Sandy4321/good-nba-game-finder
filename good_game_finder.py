# TODO show more interesting information for each game: win streak, last 10, etc

import urllib2
import json
import string
import smtplib

west_threshold = 11
east_threshold = 6

#dumps private information (passcodes, emails) to JSON
def dump_to_json(passwords):

        output = json.dumps(passwords, default=lambda obj: obj.__dict__)
        with open('private_info.json', 'w') as outfile:
            outfile.write(output)
            outfile.close()


#loads private information (passcodes, emails) from JSON
def load_private_info():

        with open('private_info.json') as infile:
                json_data = json.load(infile)
                passwords = json_data
                return passwords



#sends an email through Gmail with the given message
def send_email(from_addr, to_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login, password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

#a Team object that holds vital data for a basketball team
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


#an Game object that holds vital data about a game
class Game:

    #initializes a game object given information from the API
    def __init__(self, game_dict):
        self.away_team = game_dict["away_team"]["last_name"]
        self.home_team = game_dict["home_team"]["last_name"]
        start_time = game_dict["start_date_time"]
        self.start_time = convert_to_12_hour_time(start_time[len(start_time) - 14: -8])

    #prints out the game information
    def print_self(self):
        message = "\n" + self.away_team + " @ " + self.home_team + " at " + self.start_time + " Central Time, \n"
        return message

#converts military PM time to 12 hour time
def convert_to_12_hour_time(time_str):
    hour = int(time_str[:2])
    hour = hour - 13
    return str(hour) + time_str[2:-1]


#returns true if the teams in the game are
#the tenth seed or above if they're in the western
#conference or fifth seed and above in the eastern conference
def find_good_games(games, teams):
    good_games = []

    for game in games:
        if teams[game.home_team].is_worthy() and teams[game.away_team].is_worthy():
            good_games.append(game)

    return good_games


# unpacks the JSON data from a given url and returns it as a dict
def fetch(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    json_data = response.read()
    return json.loads(json_data)

#unpacks the JSON data from a given url with the given access code
def fetch_with_access_code(url, access_code):
    req = urllib2.Request(url)
    req.add_header("Authorization", "Bearer " + access_code)
    response = urllib2.urlopen(req)
    json_data = response.read()
    return json.loads(json_data)


# runs main
def main():
    private_info = load_private_info()
    team_dict = {}
    games_arr = []
    standings = fetch("https://erikberg.com/nba/standings.json")["standing"]
    schedule = fetch_with_access_code("https://erikberg.com/events.json", private_info["Access Token"])["event"]

    for team in standings:
        new_team = Team(team)
        team_dict[new_team.team_name] = new_team

    for game in schedule:
        games_arr.append(Game(game))

    good_games = find_good_games(games_arr, team_dict)

    message = "GoodGameFinder found these good games today:\n"
    for game in good_games:
        message += game.print_self()

    message = message[:-3]
    message += "."
    print message
    
    if len(good_games) is 0:
        message = "None."

    send_email(private_info["Email"], private_info["Recipient List"],
              "Good NBA Games Today", message,
              private_info["Email"], private_info["Email Pass"])

main()
