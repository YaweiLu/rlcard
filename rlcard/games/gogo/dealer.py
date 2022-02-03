# -*- coding: utf-8 -*-
''' Implement Doudizhu Dealer class
'''
import functools

from rlcard.utils import init_54_deck
from rlcard.games.gogo.action_generator import CARD_RANK, str2list, prase_actions, np2str

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
        self.action_mat, self.type2order, self.action_map = prase_actions()
    
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
            ch_list = str2list(current_hand)
            ch_index = 

            player.set_current_hand(current_hand)
            player.initial_hand = cards2str(player.current_hand)
