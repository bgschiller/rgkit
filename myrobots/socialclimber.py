import rg
import json

class Robot(object):
    def __init__(self, *args, **kwargs):
        self.first = True

    def act(self, game):
        action = self.move_in(game) or self.attack_nearby(game) or ['guard']
        return action

    def move_in(self,game):
        '''The enemy's base is down!'''
        to_center = rg.toward(self.location, rg.CENTER_POINT)
        if to_center in game['robots']:
            #someone is standing there!
            return None #don't move in.
        return ['move',to_center]
    
    def attack_nearby(self,game):
        loc_choices = rg.locs_around(self.location,filter_out=['invalid'])
        for loc in sorted(filter(lambda l: l in game['robots'], loc_choices),
                          key=lambda loc: game['robots'][loc]['hp']):
            if loc in game and game[loc]['player_id'] != self.player_id:
                return ['attack',loc]
        return None