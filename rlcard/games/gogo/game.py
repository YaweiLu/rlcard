# -*- coding: utf-8 -*-
''' Implement GoGo Game class
'''
import numpy as np
from rlcard.games.gogo import Player, Round


class GoGoGame:
    ''' Provide game APIs for env to run doudizhu and get corresponding state
    information.
    '''
    def __init__(self):
        self.np_random = np.random.RandomState()
        self.num_players = 3

    def init_game(self):
        ''' Initialize players and state.

        Returns:
            dict: first state in one game
            int: current player's id
        '''
        # initialize public variables
        self.winner_id = None

        # initialize players
        self.players = [Player(num, self.np_random)
                        for num in range(self.num_players)]

        # initialize round to deal cards and determine landlord
        self.round = Round(self.np_random)
        self.round.initiate(self.players)

        # get state of first player
        player_id = self.round.current_player
        self.state = self.get_state(player_id)

        return self.state, player_id

    def step(self, action):
        ''' Perform one draw of the game

        Args:
            action (str): specific action of doudizhu. Eg: '33344'

        Returns:
            dict: next player's state
            int: next player's id
        '''
        # perfrom action
        player = self.players[self.round.current_player]
        self.round.proceed_round(player, action)

        if player.current_hand[1] == 0:
            self.winner_id = player.player_id

        next_id = (player.player_id+1) % len(self.players)
        self.round.current_player = next_id

        # get next state
        state = self.get_state(next_id)
        self.state = state

        return state, next_id

    def get_state(self, player_id):
        ''' Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''
        player = self.players[player_id]
        others_hands = self._get_others_current_hand(player)
        if self.is_over():
            actions = None
        else:
            last_action = None
            if self.round.last_player_id != player_id:
                last_player = self.players[self.round.last_player_id]
                last_action = last_player.last_action

            actions = player.get_available_actions(last_action)
        state = player.get_state(self.round.public, others_hands, actions)

        return state

    def get_player_id(self):
        ''' Return current player's id

        Returns:
            int: current player's id
        '''
        return self.round.current_player

    def get_num_players(self):
        ''' Return the number of players in doudizhu

        Returns:
            int: the number of players in doudizhu
        '''
        return self.num_players

    def is_over(self):
        ''' Judge whether a game is over

        Returns:
            Bool: True(over) / False(not over)
        '''
        if self.winner_id is None:
            return False
        return True

    def _get_others_current_hand(self, player):
        player_up = self.players[(player.player_id+1) % len(self.players)]
        player_down = self.players[(player.player_id-1) % len(self.players)]
        others_hand = player_up.current_hand + player_down.current_hand
        return others_hand
