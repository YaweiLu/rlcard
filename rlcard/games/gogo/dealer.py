# -*- coding: utf-8 -*-
''' Implement Doudizhu Dealer class
'''
import numpy as np
from rlcard.games.gogo.action_generator import CARD_RANK

class GoGoDealer:
    ''' Dealer will shuffle, deal cards, and determine players' roles
    '''
    def __init__(self, np_random):
        '''Give dealer the deck

        Notes:
            1. deck with 54 cards including black joker and red joker
        '''
        self.np_random = np_random
        self.deck = self._init_deck()
    
    def _init_deck(self):
        ret = []
        for c in CARD_RANK:
            timer = 4
            if c == 'R': timer = 1
            if c == 'A': timer = 3
            ret.extend([c] * timer)
        return ret
            

    def shuffle(self):
        ''' Randomly shuffle the deck
        '''
        self.np_random.shuffle(self.deck)

    def deal_cards(self, players):
        ''' Deal cards to players

        Args:
            players (list): list of Player objects
        '''
        hand_num = (len(self.deck) - 3) // len(players)
        self.shuffle()
        for index, player in enumerate(players):
            current_hand = self.deck[index*hand_num:(index+1)*hand_num]
            ch_np = np.zeros(15)
            for c in current_hand:
                ch_np[CARD_RANK.index(c) + 2] += 1
            ch_np[0] = player.player_id
            ch_np[1] = len(current_hand)
            player.current_hand = ch_np
