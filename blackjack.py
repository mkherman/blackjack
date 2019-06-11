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

		aces = [0,0]
		if hand[0] == 'A': 
			aces[0] = int(raw_input('\n\nPlayer {0}, would you like your 1st card to be 1 or 11?\n--->  '.format(i+1)))
		if hand[1] == 'A':
			aces[1] = int(raw_input('\n\nPlayer {0}, would you like your 2nd card to be 1 or 11?\n--->  '.format(i+1)))

		total = 0
		numcards = 2
		
		# Check for blackjack or bust
		for idx,j in enumerate(hand):
			try: 
				total += int(j)
			except:
				if j > 10 and aces[idx] == 0:
					total += 10
				else:
					total += aces[idx]

		if total > 21:
			print '\nBust, {0}!'.format(total)
			decision = None

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

			points = []
			for j in range(len(hand)):
				try:
					points.append(int(hand[j]))
				except:
					if hand[j]== 'A' and j < 2:
						card = aces[j]
					elif hand[j] == 'A' and j == 2:
						card = int(raw_input('\n\nPlayer {0}, would you like this A to be 1 or 11?\n--->  '.format(i+1)))
					else:
						card = 10
					points.append(card)

			total = sum(points)

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
	if dealer1 == 'A' and dealer2 =='A':
		dealer1 = '1'
		dealer2 = '11'

	elif dealer1 == 'A' and dealer2 in ['2','3','4','5','6']:
		dealer1 = '1'

	elif dealer2 == 'A' and dealer1 in ['2','3','4','5','6']:
		dealer2 = '1'

	elif dealer1 == 'A' and dealer2 in ['8','9','10']:
		dealer1 = '11'

	elif dealer2 == 'A' and dealer1 in ['8','9','10']:
		dealer2 = '11'

	elif (dealer1 == 'A' and dealer2 in ['J','Q','K']) \
		or (dealer2 == 'A' and dealer1 in ['J','Q','K']) :
		dealer1, dealer2 = '11', '10'


	dealer_hand = [dealer1, dealer2]
	dealer_total = 0

	# Check for blackjack or bust
	for idx,j in enumerate(dealer_hand):
		try: 
			dealer_total += int(j)
		except:
			dealer_total += 10


	dealer_numcards = 2

	while dealer_total < 17  and dealer_numcards < 5:

		if draw > 0:
			for c in range(dealer_numcards-2):
				lastcard = hitme(draw-(dealer_numcards-2)+(c+1),i)

		draw += 1
		newcard = hitme(draw,i)
		dealer_hand.append(newcard)
		numcards += 1

		try:
			dealer_total += int(newcard)
		except:
			if newcard == 'A' and dealer_total <= 10:
				dealer_total += 11
			elif newcard == 'A' and dealer_total > 10:
				dealer_total += 1
			else:
				dealer_total += 10




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





