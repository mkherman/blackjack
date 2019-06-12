import numpy as np
import time


def spacing(card):
	space = '' if card=='10' else ' '
	return space


def dealtcards(card1, card2, player):
	space1, space2 = spacing(card1), spacing(card2)

	if player == 'dealer': 
		print '\n\n       Dealer:\n'
	else:
		print '\n\n      Player {0}:\n'.format(player+1)
	
	print '-------     -------'
	print '|     |     |     |'
	print '|  {0}{1} |     |  {2}{3} |'.format(card1, space1, card2, space2)
	print '|     |     |     |'
	print '-------     -------'

	return None


def hitme(draw, player):
	newcard = deck[players*2+1+draw]
	space = spacing(newcard)

	print '      ------- '
	print '      |     |'
	print '      |  {0}{1} |'.format(newcard, space)
	print '      |     |'
	print '      -------'

	return newcard



########################################################


print '\n\n##### Blackjack! #####\n'


# Determine number of players
players = int(raw_input('How many players?\n--->  '))
if players > 5:
	print '\nThe maximum number of players is 5.\n'
	players = int(raw_input('How many players?\n--->  '))

wins, losses, pushes = np.zeros(players), np.zeros(players), np.zeros(players)

play_again = 'y'

while play_again != 'n':

	# Set up deck
	single_deck = range(2,10+1,1)*4 + ['A','J','Q','K']*4
	#faces = {'A':1, 'J':10, 'Q':10, 'K':10}
	deck = np.hstack(single_deck*2)
	np.random.shuffle(deck)
	draw = 0

	# Deal cards
	players1 = deck[:players]
	dealer1 = deck[players]
	players2 = deck[players+1:players*2+1]
	dealer2 = deck[players*2+1]

	# Show half of dealer's hand
	dealtcards(' ', dealer2, 'dealer')

	# Show all players' hands
	for i in range(players):

		card1, card2 = players1[i], players2[i]
		dealtcards(card1, card2, i)

	# Ask if hit or stand
	player_hands = []
	player_totals = []

	for i in range(players):

		hand = [players1[i], players2[i]]
		points = []
		numcards = 2
		
		# Define points
		for card in hand:

			if card in ['J', 'Q', 'K']:
				card = '10' 
			elif card == 'A':
				card = '11'
			points.append(int(card))

		total = sum(points)

		# Lower value of first ace if two aces drawn
		if total > 21:
			points[0] = 1
			total = sum(points)
			decision = raw_input('\n\nPlayer {0}, would you like to hit or stand?\n--->  '.format(i+1))

		elif total == 21:
			print '\nNice, {0}!'.format(total)
			decision = None

		else:
			decision = raw_input('\n\nPlayer {0}, would you like to hit or stand?\n--->  '.format(i+1))

		# Draw another card
		while decision == 'hit':
			dealtcards(hand[0], hand[1], i)

			if draw > 0:
				for c in range(numcards-2):
					lastcard = hitme(draw-(numcards-2)+(c+1),i)

			draw += 1
			newcard = hitme(draw,i)
			hand.append(newcard)
			numcards += 1

			if newcard in ['J', 'Q', 'K']:
				points.append(10)
			elif newcard == 'A' and total <= 10:
				points.append(11)
			elif newcard == 'A' and total > 10:
				points.append(1)
			else: 
				points.append(int(newcard))

			# Reassign ace if total points exceed 21
			total = sum(points)
			if total > 21 and 11 in points:
				ind = np.where((np.array(points)==11))[0]
				if len(ind) < 2:
					points[ind[0]] = 1
				else:
					points[ind[1:]] = 1
				total = sum(points)

			# Check total points
			if total > 21:
				print '\nBust, {0}!'.format(total)
				decision = None

			elif total == 21:
				print '\nNice, {0}!'.format(total)
				decision = None

			elif numcards == 5:
				decision = None

			else:
				decision = raw_input('\n\nPlayer {0}, would you like to hit or stand?\n--->  '.format(i+1))
		
		player_totals.append(total)



	# Show dealer's cards
	showcards = raw_input("\nPress enter to see dealer's cards... ")

	dealtcards(dealer1, dealer2, 'dealer')
	dealer_hand = [dealer1, dealer2]
	dealer_total = 0
	dealer_points = []
	dealer_numcards = 2

	# Define points
	for card in dealer_hand:

		if card in ['J', 'Q', 'K']:
			card = '10' 
		elif card == 'A' and '6' not in dealer_hand:
			card = '11'
		elif card == 'A' and '6' in dealer_hand:
			card = '1'
		dealer_points.append(int(card))

	dealer_total = sum(dealer_points)

	# Lower value of first ace if two aces drawn
	if dealer_total > 21:
		dealer_points[0] = 1
		dealer_total = sum(dealer_points)

	# Dealer draws another card 
	while dealer_total < 17  and dealer_numcards < 5:

		draw += 1
		newcard = hitme(draw,i)
		dealer_hand.append(newcard)
		dealer_numcards += 1

		if newcard in ['J', 'Q', 'K']:
			dealer_points.append(10)
		elif newcard == 'A' and dealer_total <= 10:
			dealer_points.append(11)
		elif newcard == 'A' and dealer_total > 10:
			dealer_points.append(1)
		else: 
			dealer_points.append(int(newcard))

		dealer_total = sum(dealer_points)

		# Reassign ace if total points exceed 21
		if dealer_total > 21 and 11 in dealer_points:
			ind = np.where((np.array(dealer_points)==11))[0]
			if len(ind) < 2:
				dealer_points[ind[0]] = 1
			else:
				dealer_points[ind[1:]] = 1
			dealer_total = sum(dealer_points)



	print '\n\nDealer has {0}'.format(dealer_total)

	for i,val in enumerate(player_totals):
		if val == 21 \
			or (dealer_total < val and dealer_total <= 21 and val <=21) \
			or (dealer_total > 21 and val <=21):
			print '\nPlayer {0} has {1}: You win!'.format(i+1, val)
			wins[i] += 1

		elif dealer_total > val and dealer_total <= 21 and val <=21:
			print '\nPlayer {0} has {1}: Sorry, dealer wins!'.format(i+1, val)
			losses[i] += 1

		elif dealer_total == val and dealer_total < 21:
			print '\nPlayer {0} has {1}: Push!'.format(i+1, val)
			pushes[i] += 1

		elif val > 21:
			print '\nPlayer {0} has {1}: Sorry, you bust!'.format(i+1, val)
			losses[i] += 1

	scores = raw_input("\n\nPress enter to see player scores... ")

	print '\n-----------------------------------'
	for i, val in enumerate(wins):
		print 'Player {0}: won {1}, lost {2}, pushed {3}'.format(i+1,int(wins[i]),int(losses[i]),int(pushes[i]))
	print '-----------------------------------'
	
	play_again = raw_input('\nPlay again? (y/n)\n--->  ')





