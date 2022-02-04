from collections import Counter, OrderedDict
import numpy as np
from rlcard.envs import Env



class GoGoEnv(Env):
    ''' Doudizhu Environment
    '''

    def __init__(self, config):     
        from rlcard.games.gogo import Game   
        self.name = 'gogo'
        self.game = Game()
        super().__init__(config)

    def _extract_state(self, state):
        ''' Encode state

        Args:
            state (dict): dict of original state
        '''
        current_hand = state['current_hand']
        others_hand = state['others_hand']
        seen_cards = state['seen_cards']
        obs = np.concatenate((current_hand,
                              others_hand,
                              seen_cards
                            ))
        extracted_state = OrderedDict({'obs': obs, 'legal_actions': self._get_legal_actions()})
        extracted_state['raw_obs'] = state
        extracted_state['action_record'] = self.action_recorder
        return extracted_state
            
    def get_payoffs(self):
        ''' Get the payoffs of players. Must be implemented in the child class.

        Returns:
            payoffs (list): a list of payoffs for each player
        '''
        return 1

    def _get_legal_actions(self):
        ''' Get all legal actions for current state

        Returns:
            legal_actions (list): a list of legal actions' id
        '''
        legal_actions = self.game.state['actions'].tolist()
        return legal_actions


if __name__ == "__main__":
    print(0)