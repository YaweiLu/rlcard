''' A toy example of self playing for Blackjack
'''

import rlcard
from rlcard.agents import RandomAgent as RandomAgent
from rlcard.agents import GoGoRuleAgent
#from rlcard.agents.human_agents.gogo_human_agent import HumanAgent
from rlcard.agents import GoGoHumanAgent as HumanAgent
from rlcard.utils.utils import print_card
from rlcard.games.gogo.action_generator import np2str


# Make environment
num_players = 3
env = rlcard.make('gogo', config={'game_num_players': num_players})

while (True):
    print(">> Start a new game")
    human_player_id = int(input(">> Input player id (0, 1 or 2):"))
    random_agent = GoGoRuleAgent()
    agents = [random_agent] * 3
    agents[human_player_id] = HumanAgent()
    env.set_agents(agents)

    trajectories, payoffs = env.run(is_training=False)
    # If the human does not take the final action, we need to
    # print other players action

    if len(trajectories[0]) != 0:
        final_state = []
        action_record = []
        state = []
        _action_list = []

        for i in range(num_players):
            final_state.append(trajectories[i][-1])
            state.append(final_state[i]['raw_obs'])

        action_record.append(final_state[i]['action_record'])
        for i in range(1, len(action_record) + 1):
            _action_list.insert(0, action_record[-i])

        for pair in _action_list[0]:
            print('>> Player {} has {}, chooses {}'.format(pair[0], pair[2], np2str(pair[1])[1]))

    print('===============     Result     ===============')

    print("You Win!" if  payoffs == human_player_id else "You Lose!")

    input("\nPress any key to continue...")
