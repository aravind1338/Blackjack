import itertools, random
class Deck:

	# 11 = Jack, 12 = Queen, 13 = King, 14 = Ace

	def __init__(self):
		self.deck = []

	### Creates the deck of cards ###
	def createDeck(self):
		self.deck = list(itertools.product(range(2, 15),['Spades', 'Diamonds', 'Clubs', 'Hearts']))

	### Shuffles the deck ###
	def shuffleDeck(self):
		random.shuffle(self.deck)

	### Draw the top card from the deck ###
	def getTopCard(self):
		return self.deck.pop(0)

	### Get the value of the card ###
	def getValue(self, card):
		if card[0] <= 10 or card[0] == 14:
			return card[0]
		else:
			return 10


class Player:

	def __init__(self):
		self.cards = []	# The cards the player has in their hand
		self.money = 100 # Each player starts with $100

	### Add a card to the player's hand ###
	def addToHand(self, card):
		self.cards.append(card)

	### Get the value of a player's hand ###
	def getHandValue(self, player):
		first = False
		total = 0
		numAces = 0
		for card in self.cards:
			value = player.getValue(card)
			if value != 14:
				total += value
			else:
				numAces += 1

		if numAces == 1:
			first = True

		while numAces != 0:
			if total < 10:
				total += 11
				numAces -= 1
			else:
				if numAces == 1 and total == 10: # The case of a ten + Ace
					total += 11
					numAces -= 1

				else:
					total += 1
					numAces -= 1

		return total

	def bet(self, amount):
		self.money -= amount