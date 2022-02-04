from rlcard.utils.utils import print_card
from rlcard.games.gogo.action_generator import np2str


class HumanAgent(object):
    ''' A human agent for GoGo. It can be used to play alone for understand how the blackjack code runs
    '''

    def __init__(self, player_id = 0):
        ''' Initilize the human agent

        Args:
            num_actions (int): the size of the output action space
        '''
        self.use_raw = True
        self.player_id = player_id

    @staticmethod
    def step(state):
        ''' Human agent will display the state and make decisions through interfaces

        Args:
            state (dict): A dictionary that represents the current state

        Returns:
            action (int): The action decided by human
        '''
        _print_state(state['raw_obs'], state['legal_actions'])
        action = int(input('>> You choose action (integer): '))
        while action < 0 or action >= len(state['legal_actions']):
            print('Action illegel...')
            action = int(input('>> Re-choose action (integer): '))
        return state['legal_actions'][action]

    def eval_step(self, state):
        ''' Predict the action given the current state for evaluation. The same to step here.

        Args:
            state (numpy.array): an numpy array that represents the current state

        Returns:
            action (int): the action predicted (randomly chosen) by the random agent
        '''
        return self.step(state), {}

def _print_state(state, legal_actions):
    ''' Print out the state

    Args:
        state (dict): A dictionary of the raw state
        action_record (list): A list of the each player's historical actions
    '''
    print('\n=============   Rest Cards   ===============')
    seen_cards = state['seen_cards']
    for id in range(3):
        print("Player {} has {} cards".format(id, 16 - sum(seen_cards[id, 2:])))
    
    print('=============   Last Actions  ===============')
    trace = state['trace'], range(min(3, len(iter)))
    view_length = min(3, len(trace))

    for it in range(-view_length, 0):
        it_id, it_action = trace[it]
        print("Player {} played".format(it_id))
        print_card(np2str(it_action))    

    print('===============   Player\'s Hand   ===============')
    current_hand = state['current_hand']
    hand_str = np2str(current_hand)
    print_card(hand_str)

    print('\n=========== Actions You Can Choose ===========')
    print(', '.join([str(index) + ': ' + np2str(action) for index, action in enumerate(legal_actions)]))
    print('')
