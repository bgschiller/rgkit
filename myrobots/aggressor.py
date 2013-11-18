import rg

class Robot(object):
    def act(self, game):
        return self.attack_nearby(game) or self.move_in(game) or ['guard']
        
    def move_in(self,game):
        '''The enemy's base is down!'''
        print 'move_in'
        to_center = rg.toward(self.location, rg.CENTER_POINT)
        if set(['invalid','obstacle']) & set(rg.loc_types(to_center)):
            #no one is standing there
            return ['move',to_center]
        return None
    
    def attack_nearby(self,game):
        enemy_locations = [loc for loc in game['robots'] \
                           if game['robots'][loc]['player_id'] != self.player_id]
        print self.location, enemy_locations
        adjacent = rg.locs_around(self.location)
        print adjacent
        for adj in adjacent:
            if adj in enemy_locations:
                return ['attack',adj]

        choices = set([(self.cost(loc,game), loc) for loc in enemy_locations ])
        
        while choices:
            best_choice = min(choices)
            step = rg.toward(self.location,best_choice[1])
            if not 'invalid' in rg.loc_types(step): break
            choices.discard(best_choice)
        if not set(['obstacle','invalid']) & set(rg.loc_types(step)) :
            return ['move',step ]
            
    def cost(self,loc,game):
        '''Given an enemy location, score the location for whether we should move toward it.'''
        wdist = rg.wdist(self.location,loc)
        enemy_hp = game['robots'][loc]['hp']
        return enemy_hp + 5 * wdist