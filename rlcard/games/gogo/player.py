# -*- coding: utf-8 -*-
''' Implement Doudizhu Player class
'''
import functools
import numpy as np

from rlcard.games.doudizhu.utils import get_gt_cards
from rlcard.games.doudizhu.utils import cards2str, doudizhu_sort_card
from rlcard.games.gogo.action_generator import prase_actions, FirstGreaterSecond


class GoGoPlayer:
    ''' Player can store cards in the player's hand and the role,
    determine the actions can be made according to the rules,
    and can perfrom corresponding action
    '''
    def __init__(self, player_id):
        ''' Give the player an id in one game

        Args:
            player_id (int): the player_id of a player

        Notes:
            1. role: A player's temporary role in one game(landlord or peasant)
            2. hand: Initial cards
            3. current_hand: The rest of the cards after playing some of them
        '''
        self.player_id = player_id
        self.current_hand = []
        self.valid_actions = None
        self.last_action = None
        self.trio_num = {3:1, 19:2, 20:3, 21:4, 22:5}

        #record cards removed from self.current_hand for each play()
        self._recorded_played_cards = []

    def update_valid_actions(self):
        if self.valid_actions is None:
            self.valid_actions, _, _ = prase_actions() 
        action_num = self.valid_actions.shape[0]
        valid_action_index = []
        for it in range(action_num):
            if self.contain(self.valid_actions[it,:]):
                valid_action_index.append(it)
        self.valid_actions = self.valid_actions[valid_action_index,:]
        self.valid_actions.reshape(-1, 15)
    
    def get_available_actions(self, last_action = None):
        valid_num = self.valid_actions.shape[0]
        greater_index = []
        for it in range(valid_num):
            is_greater, is_valid = False, True
            if FirstGreaterSecond(self.valid_actions[it,:], last_action) == 1:
                is_greater = True
            if last_action is not None and int(last_action[0]) in self.trio_num:
                expected_length = min(self.current_hand[1], 5 * self.trio_num[int(last_action[0])])
                if sum(self.valid_actions[it,2:]) < expected_length:
                    is_valid = False

            if is_greater and is_valid:  greater_index.append(it)
        if len(greater_index) > 0:
            return self.valid_actions[greater_index,:]
        return self.valid_actions[0,:].reshape(1,-1)

    def get_state(self, public, others_hands, actions):
        state = {}
        state['seen_cards'] = public['seen_cards']
        state['trace'] = public['trace'].copy()
        state['self'] = self.player_id
        state['current_hand'] = self.current_hand
        state['others_hand'] = others_hands
        state['actions'] = actions

        return state

    def play(self, action, last_player_id=None, last_action=None):
        ''' Perfrom action

        Args:
            action (string): specific action
            greater_player (DoudizhuPlayer object): The player who played current biggest cards.

        Returns:
            object of DoudizhuPlayer: If there is a new greater_player, return it, if not, return None
        '''
        if action[0] == 0:
            self._recorded_played_cards.append([])
            return last_player_id, last_action
        
        self.last_action = action
        self.current_hand[2:] -= action[2:]
        self.current_hand[1] -= sum(action[2:]) 
        self.update_valid_actions()
        return self.player_id, action
    
    def contain(self, cards):
        for it in range(2,15):
            if self.current_hand[it] < cards[it]:
                return False
        return True
