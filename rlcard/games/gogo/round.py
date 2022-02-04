# -*- coding: utf-8 -*-
''' Implement Doudizhu Round class
'''

import numpy as np


class GoGoRound:
    ''' Round can call other Classes' functions to keep the game running
    '''

    def __init__(self, np_random):
        self.np_random = np_random
        self.trace = []

        self.last_player_id = 0
        self.last_action = None
        self.current_player = 0

    def initiate(self, players):
        ''' Call dealer to deal cards and bid landlord.

        Args:
            players (list): list of DoudizhuPlayer objects
        '''
        for player in players:
            player.update_valid_actions()
        seen_cards = np.zeros((3, 15))
        for it in range(3):
            seen_cards[it, 0] = it
        self.seen_cards = seen_cards
        self.current_player = 0
        self.public = {'seen_cards': self.seen_cards,
                       'trace': self.trace}

    def update_public(self, action):
        ''' Update public trace and played cards

        Args:
            action(str): string of legal specific action
        '''
        self.trace.append((self.current_player, action))
        self.seen_cards[self.current_player,2:] += action[2:]
        self.seen_cards[self.current_player,1] += sum(action[2:])
        self.public['seen_cards'] = self.seen_cards

    def proceed_round(self, player, action):
        ''' Call other Classes's functions to keep one round running

        Args:
            player (object): object of DoudizhuPlayer
            action (str): string of legal specific action

        Returns:
            object of DoudizhuPlayer: player who played current biggest cards.
        '''
        self.update_public(action)
        self.last_player_id, self.last_action = player.play(action, self.last_player_id, self.last_action)