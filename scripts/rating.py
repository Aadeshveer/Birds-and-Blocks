import numpy as np
import os

class ELO:
    def __init__(self, game, user_file, rating_file):
        self.game = game
        self.user_file=user_file
        self.rating_file=rating_file
        self.load_files()
        self.cache = {}
    
    def load_files(self):

        user_read=False
        while True:
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
                    break
            except FileNotFoundError:
                os.mknod(self.rating_file)

    def add_playing(self, name):
        if name not in self.users and name != '':
            self.users.append(name)
            self.ratings.append(1000)
    
    def update_rating(self, winner, loser):
        idx_a = self.users.index(winner)
        idx_b = self.users.index(loser)
        Ra = self.ratings[idx_a]
        Rb = self.ratings[idx_b]
        Ea = 1/(1 + 10**((Rb-Ra)/400))
        Eb = 1/(1 + 10**((Ra-Rb)/400))
        delta_a = int(32*(1-Ea))
        delta_b = int(32*(0-Eb))
        if not self.game.tutorial:
            self.ratings[idx_a] += delta_a
            self.ratings[idx_b] += delta_b
            with open(self.rating_file, 'w') as file:
                for i in self.ratings:
                    file.write(str(i)+"\n")
            with open(self.user_file, 'w') as file:
                for i in self.users:
                    file.write(str(i)+"\n")
        return (Ra, Rb, delta_a, delta_b)
    
    def get_rating_str(self, player):
        if player in self.cache:
            return ':' + str(self.cache[player]) 
        elif player in self.users:
            self.cache[player] = self.ratings[self.users.index(player)]
            return ':' + str(self.cache[player])
        else:
            return ''