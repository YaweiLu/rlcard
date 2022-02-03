import os
import json
import csv
from itertools import combinations
import numpy as np


CARD_TYPE = ['solo', 'pair', 'trio', 'solo_chain', 'pair_chain', 'trio_chain', 'bomb']
DETAIL_CARD_TYPE = {'pass': 0, 'solo': 1, 'pair': 2, 'trio': 3, 'solo_chain_5': 4, 'solo_chain_6': 5, \
    'solo_chain_7': 6, 'solo_chain_8': 7, 'solo_chain_9': 8, 'solo_chain_10': 9, 'solo_chain_11': 10, \
    'solo_chain_12': 11, 'pair_chain_2': 12, 'pair_chain_3': 13, 'pair_chain_4': 14, 'pair_chain_5': 15, \
    'pair_chain_6': 16, 'pair_chain_7': 17, 'pair_chain_8': 18, 'trio_chain_2': 19, 'trio_chain_3': 20, \
    'trio_chain_4': 21, 'trio_chain_5': 22, 'bomb': 23}
CARD_RANK = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', 'R'] 

def solo_action():
    return {"solo": CARD_RANK}

def pair_action():
    actions = [card * 2 for card in CARD_RANK[:-1]]
    return {"pair": actions}

def trio_action():
    actions = []
    trios = [card * 3 for card in CARD_RANK[:-1]]
    pairs = [f + s for f in CARD_RANK[:-1] for s in CARD_RANK]
    pairs = [''] + CARD_RANK + pairs
    for t in trios:
        for p in pairs:
            if p.find(t[0]) == -1:
                actions.append(t+p)
    return {"trio": actions}

def solo_chain_action():
    actions = {}
    total_avial = len(CARD_RANK[:-1])

    for length in range(5, 13):
        sub_action_type = "solo_chain_" + str(length)
        sub_action = []
        for start in range(total_avial):
            if start + length > total_avial:
                break
            action = ""
            for card in CARD_RANK[start:start+length]:
                action += card
            sub_action.append(action)
        actions[sub_action_type] = sub_action
    return actions

def pair_chain_action():
    actions = {}
    total_avial = len(CARD_RANK[:-1])

    for length in range(2, 9):
        sub_action_type = "pair_chain_" + str(length)
        sub_action = []
        for start in range(total_avial):
            if start + length > total_avial:
                break
            action = ""
            for card in CARD_RANK[start:start+length]:
                action += card * 2
            sub_action.append(action)
        actions[sub_action_type] = sub_action
    return actions

def trio_chain_action():
    actions = {}
    total_avial = len(CARD_RANK[:-1])

    for length in range(2, 6):
        sub_action_type = "trio_chain_" + str(length)
        sub_action = []
        pref_length = min(length * 2, 16 - length * 3)

        for start in range(total_avial):
            if start + length > total_avial:
                break
            action = ""
            for card in CARD_RANK[start:start+length]:
                action += card * 3
            
            pref_avail = CARD_RANK[:start] + CARD_RANK[start+length:]
            pref_list = []
            for card in pref_avail:
                if card == 'R':
                    pref_list.extend([card])
                else:
                    pref_list.extend([card] * 3)
        
            sub_action.append(action)
            visited_pref = set()
            invalid_pref = '-1'
            if start >= 1: invalid_pref = CARD_RANK[start - 1] * 3
            for pl in range(pref_length + 1):
                for c in combinations(pref_list, pl):
                    pref_str = ''.join(c)
                    if pref_str.find(invalid_pref) != -1: continue
                    if pref_str in visited_pref: continue
                    visited_pref.add(pref_str)

                    action_with_pref = action + pref_str
                    sub_action.append(action_with_pref)
        actions[sub_action_type] = sub_action
    return actions

def bomb_action():
    actions = [card * 4 for card in CARD_RANK[:-2]]
    return {'bomb': actions} 

def get_all_action():
    actions = {"pass":[""]}
    for type in CARD_TYPE:
        curr_action = globals()[type + '_action']()
        actions.update(curr_action)
    
    for key in actions:
        print("{} has action {}".format(key, len(actions[key])))
    return actions

def prase_actions():
    actions = get_all_action()
    
    action_mat, action_cnt, type_to_order, action_map = [], 0, {}, {}
    for type in DETAIL_CARD_TYPE:
        sub_action = actions[type]
        sub_list = []
        for it in range(len(sub_action)):
            action_map[sub_action[it]] = action_cnt
            action_list = [DETAIL_CARD_TYPE[type], it] 
            action_list.extend(str2list(sub_action[it]))
            sub_list.append(action_list)
            action_cnt += 1
        type_to_order[DETAIL_CARD_TYPE[type]] = (type, action_cnt - len(sub_action) , action_cnt - 1)
        action_mat.append(np.asarray(sub_list))
    total_mat = np.concatenate(tuple(action_mat))
    return total_mat, type_to_order, action_map
   

def str2list(cards):
    ret = [0] * 13
    for c in cards:
        ret[CARD_RANK.index(c)] += 1
    return ret

def np2str(cards):
    ret = ''
    clist = []
    for it in range(13):
        clist.append((CARD_RANK[it], int(cards[it])))
    clist.sort(key = lambda x: -x[1] * 100 + CARD_RANK.index(x[0]))
    for c in clist:
        ret += c[0] * c[1]
    return ret



if __name__ == "__main__":
    action_mat, type2order = prase_actions()
    print(type2order)
    print(action_mat)
            