from player import Player
players_on_team = 1

#input handlers--------------------------------------------------------------------------------------------------------

def take_str_input(str):
    answer = raw_input(str)
    words = answer.split(' ')
    toReturn = ''
    for word in words:
        if word.isalpha() is False:
            return take_str_input('Invalid input. \n' + str)
        else:
            toReturn += word + ' '
    return toReturn[:-1]    

#prompts the user to input data for all member variables in @param player
def player_query(player):
    player.set_name(take_str_input('Input player name: '))
    player.team = take_str_input('What team is he on? ')

#prompts the user to input each player in a team along with their individual stats
#@return team_arr, an array of all of the players that were input
def getTeam():
        team_arr = []
        players = 0
        while players < players_on_team:
            player_new = Player()
            player_query(player_new)
            team_arr.append(player_new)
            players += 1

        return team_arr

