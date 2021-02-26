import random
import pickle
from os import path

STREETS = 3
NUM_RANKS = 100
NUM_BETS = 2
POT_MULTIPLIER = 3

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

def get_child(h1, h2, node):
	player, range1, range2 = strat_dict[node]
	if player == 1:
		r = random.random() * range1[h1]
		for child in get_children(node):
			r -= strat_dict[child][1][h1]
			if r <= 0:return child
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
	player = random.randint(1, 2)
	node = '_'
	while len(get_children(node)) > 0:
		if strat_dict[node][0] == player:
			actions = get_actions(node)
			keys = [x.replace('_', '') for x in actions]
			while True:
				key = raw_input(str(h1 if player == 1 else h2) + node + "(" + "/".join(keys) + "):").upper()
				if key in keys:
					for act in actions:
						if act[0] == key:
							node = node + act
					break
		else:
			node = get_child(NUM_RANKS-h1, NUM_RANKS-h2, node)
	print (str(h2 if player == 1 else h1) + node)
	val = net_value(h1, h2, node, player)
	print ('Won ' + str(val) + ' as player ' + str(player) + ' with hand ' + str(h1 if player == 1 else h2) + ' vs ' + str(h2 if player == 1 else h1))
	with open("histories.txt", 'a') as histories:
		histories.write(str(hand_idx) + '\t' + str(val) + '\t' + str(player) + '\t' + str(h1) + '\t' + str(h2) + '\t' + node + '\n')
		histories.close()
