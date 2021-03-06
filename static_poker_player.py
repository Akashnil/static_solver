import random
import pickle
from os import path
from builtins import input
import sys
import time

STREETS = 3
NUM_RANKS = 100
NUM_BETS = 2
POT_MULTIPLIER = 3

try:
	TIME_MULTIPLIER = float(sys.argv[1])
except:
	TIME_MULTIPLIER = 1.0

strat_dict = {}

with open('strat.pickle', 'rb') as handle:
	strat_dict = pickle.load(handle)

def get_children(node_id):
	children = []
	for act in ['F', 'C', 'C_', 'B']:
		if (node_id+act) in strat_dict:
			children.append((node_id+act))
	return children

def get_actions(node_id):
	actions = []
	for act in ['F', 'C', 'C_', 'B']:
		if (node_id+act) in strat_dict:
			actions.append(act)
	return actions

def think_time(parent, child, hand):
	facing_bet = 1. if parent[-1] == 'B' else 0.
	is_betting = 1. if child[-1] == 'B' else 0.
	pot_factor = child.count('B') / 4.
	total_factor = (0.25 + pot_factor*pot_factor) * (1. + facing_bet + is_betting / 2.)
	if child[-1] == 'F' and hand < 40:
		total_factor = 0.
	if child[-1] == 'C' and child.count('B') == 4 and hand == 100:
		total_factor = 0.
	time.sleep(total_factor * TIME_MULTIPLIER)

def get_child(h1, h2, node):
	player, range1, range2 = strat_dict[node]
	if player == 1:
		r = random.random() * range1[h1]
		for child in get_children(node):
			r -= strat_dict[child][1][h1]
			if r <= 0:
				return child
	else:
		assert (player == 2)
		r = random.random() * range2[h2]
		for child in get_children(node):
			r -= strat_dict[child][2][h2]
			if r <= 0:
				return child

def net_value(h1, h2, node, human):
	player = strat_dict[node][0]
	if node[-1] == 'F':
		val = POT_MULTIPLIER ** (node.count('B')-1)
		if player != human:
			val = -val
	else:
		assert(node[-1] == '_')
		val = POT_MULTIPLIER ** node.count('B')
		if h1 == h2:
			val = 0
		if h1 < h2:
			val = -val
		if human == 2:
			val = -val
	return val

total_profit = 0
while True:
	if not path.exists('histories.txt'):
		hand_idx = 0
	else:
		with open("histories.txt") as histories:
			hand_idx = len(histories.readlines())
			histories.close()
	print ('Starting hand #' + str(hand_idx+1))
	h1 = random.randint(1, NUM_RANKS)
	h2 = random.randint(1, NUM_RANKS)
	player = (hand_idx % 2) + 1
	node = '_'
	while len(get_children(node)) > 0:
		if strat_dict[node][0] == player:
			actions = get_actions(node)
			keys = [x.replace('_', '') for x in actions]
			if node[-1] == 'B':
				keys = [x.replace('B', 'R') for x in keys]
			else:
				keys = [x.replace('C', 'V') for x in keys]
			found_action = False
			while not found_action:
				hand_section = 'Hole-card: ' + str(h1 if player == 1 else h2)
				history_section = 'History: ' + node
				actions_section = 'Your Action(' + "/".join(keys) + ')' + ':'
				num_bets = node.count('B') - (1. if node[-1] == 'B' else 0.)
				ps = str(int(2*(3**num_bets)))
				pot_section = 'Pot size:  ' + ps + ('+' + ps if node[-1] == 'B' else '')
				key = input(hand_section.ljust(20) + history_section.ljust(25) + pot_section.ljust(20) + actions_section.ljust(20)).upper()
				if key == 'Q':
					sys.exit(0)
				found_action = False
				for i in range(len(keys)):
					if key == keys[i]:
						node = node + actions[i]
						found_action = True
		else:
			next_node = get_child(NUM_RANKS-h1, NUM_RANKS-h2, node)
			think_time(node, next_node, h2 if player == 1 else h1)
			node = next_node
			if len(get_children(node)) > 0 and strat_dict[node][0] != player:
				hand_section = 'Hole-card: ' + str(h1 if player == 1 else h2)
				history_section = 'History: ' + node
				ps = str(int(2 * (3 ** num_bets)))
				pot_section = 'Pot size:  ' + ps + ('+' + ps if node[-1] == 'B' else '')
				print (hand_section.ljust(20) + history_section.ljust(25) + pot_section.ljust(20))

	hand_section = 'Opponent : ' + str(h2 if player == 1 else h1)
	val = net_value(h1, h2, node, player)
	total_profit += val
	history_section = 'History: ' + node
	result_section = 'Result  : ' + ('+' if val >= 0 else ('-' if val < 0 else ' ')) + str(abs(val))
	profit_section = 'Net won  : ' + ('+' if total_profit >= 0 else ('-' if total_profit < 0 else ' ')) + str(abs(total_profit))
	print(hand_section.ljust(20) + history_section.ljust(25) + result_section.ljust(20) + profit_section.ljust(20))

	with open("histories.txt", 'a') as histories:
		histories.write(str(hand_idx) + '\t' + str(val) + '\t' + str(player) + '\t' + str(h1) + '\t' + str(h2) + '\t' + node + '\n')
		histories.close()
