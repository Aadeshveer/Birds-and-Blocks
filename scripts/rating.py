import os

class ELO:
    '''
    Manages the ELO rating of players
    '''
    def __init__(self, game, user_file, rating_file):
        self.game = game
        self.user_file=user_file
        self.rating_file=rating_file
        self.rating_map = {}
        self.load_files()
    
    def load_files(self):
        '''
        Loads files, reads in data and fills a map of players
        '''
        user_read=False
        fail_counter = 0
        while fail_counter < 10:
            try:
                with open(self.user_file) as f:
                    content=f.read().strip("\n").split("\n")
                    if content == ['']:
                        self.users=[]
                    else:
                        self.users=content
                user_read=True
            except FileNotFoundError:
                os.mknod(self.user_file)
            
            try:
                with open(self.rating_file) as f:
                    content = f.read().strip("\n").split("\n")
                    if content == ['']:
                        self.ratings=[]
                    else:
                        self.ratings=list(map(int,content))
                if user_read:
                    for i in range(len(self.users)):
                        self.rating_map[self.users[i]] = self.ratings[i]
                    break
            except FileNotFoundError:
                os.mknod(self.rating_file)

            fail_counter += 1
        else:
            print("Rating file loading failed, please run with proper permissions")
            

    def add_playing(self, name):
        '''
        Adds a player to user list
        if already exists no change
        '''
        if name not in self.users and name != '':
            self.users.append(name)
            self.ratings.append(1000)
            self.rating_map[name] = 1000
    
    def update_rating(self, winner, loser):
        '''
        Updates the rating at end of game and returns the updated ones along with change
        '''
        idx_a = self.users.index(winner)
        idx_b = self.users.index(loser)
        Ra = self.ratings[idx_a]
        Rb = self.ratings[idx_b]
        Ea = 1/(1 + 10**((Rb-Ra)/400))
        Eb = 1/(1 + 10**((Ra-Rb)/400))
        delta_a = int(32*(1-Ea))
        delta_b = int(32*(0-Eb))
        self.rating_map[winner] += delta_a
        self.rating_map[loser] += delta_b
        if not self.game.tutorial:
            self.ratings[idx_a] += delta_a
            self.ratings[idx_b] += delta_b
            with open(self.rating_file, 'w') as file:
                for i in self.ratings:
                    file.write(str(i)+"\n")
            with open(self.user_file, 'w') as file:
                for i in self.users:
                    file.write(str(i)+"\n")
        return (Ra + delta_a, Rb + delta_b, delta_a, delta_b)
    
    def get_rating_str(self, player):
        '''
        Return a string of format :[0-9]{4} with the digits being the ELO rating if player is in user list
        '''
        if player in self.rating_map:
            return ':' + str(self.rating_map[player]).rjust(4)
        elif player in self.users:
            self.rating_map[player] = self.ratings[self.users.index(player)]
            return ':' + str(self.rating_map[player]).rjust(4)
        else:
            return ''
        
    def get_leaderboard(self, top=10, width=40, size = 38):
        '''
        Returns a text surface object with given player, of give character width and font size
        '''
        self.ranked_users = sorted(self.rating_map, key= lambda x : -self.rating_map[x])
        string=''
        for i in range(top):
            string += str(i+1).ljust(2) + '.'
            string += self.ranked_users[i].ljust(width-8, '.')
            string += ':' + str(self.rating_map[self.ranked_users[i]])
            string +="\n"
        text = self.game.get_font(size).render(string, False, 'black')
        return text