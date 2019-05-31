import Card
from appJar import gui 


############################### Initialize stuff ########################################
"""
Lists contain player names, Card objects, hand values
"""

player_name = []
player_obj = []
player_values = []

# Dealer's hand value
dealer_value = 0

# Create and shuffle the deck
deck = Card.Deck()
deck.createDeck()
deck.shuffleDeck()

# Ask for number of players
name = ""
while name != "q":

	name = input("Enter player name or [q]uit: ")
	if name == "q":
		break
	player_name.append(name)
	player_obj.append(Card.Player())

# Create a dealer
Dealer = Card.Player()

for playerObj in player_obj:
	playerObj.addToHand(deck.getTopCard())

Dealer.addToHand(deck.getTopCard())


for playerObj in player_obj:
	playerObj.addToHand(deck.getTopCard())

Dealer.addToHand(deck.getTopCard())

counter = 0 # keep track of current player
img_num = 0 # keep track of which card should be displayed for the player
dealer_img_num = 0 # keep track of which card should be displayed for the dealer

################################## HELPER FUNCTION ######################################

"""
Takes a tuple containing card information and converts it to a string of the form rank_of_suit.png
"""

def card_to_image(card):
	rank = card[0]
	suit = card[1].lower()

	image_name = str(rank) + "_of_" + suit + ".png"

	return image_name

################################# BUTTON FUNCTION #######################################

def launch(button):

	global counter
	global dealer_value
	global img_num
	global dealer_img_num

	if button == "hit":

		################# If a player hits ######################

		app.setLabel("Hand value", "Hand value is " + str(player_obj[counter].getHandValue(deck)))
		app.setMessage("Play", "Do you want to hit or stand?")

		# If the player goes bust
		if player_obj[counter].getHandValue(deck) > 21:

			# Stop the player's card window
			app.stopSubWindow()

			player_values.append(player_obj[counter].getHandValue(deck)) # Store the player's final value
			app.setMessage("Play", "Sorry, you went bust!")

			counter += 1 # Move to the next player
			img_num = 0 # Reset

			if counter >= len(player_obj):

				# If there is no next player

				# Get back to the dealer's window
				app.showSubWindow("Dealer's cards")
				app.addImage("dealer_cards"+str(dealer_img_num), card_to_image(Dealer.cards[1]), row=0, column=dealer_img_num) # Show the dealer's other card
				dealer_img_num += 1

				while Dealer.getHandValue(deck) < 17:
					# While the dealer is below 17, keep hitting

					card = deck.getTopCard()
					Dealer.addToHand(card)

					app.addImage("dealer_cards"+str(dealer_img_num), card_to_image(card), row=0, column=dealer_img_num)
					dealer_img_num += 1

					if Dealer.getHandValue(deck) > 21:
						# Check if the dealer busts after each drawn card
						break

				
				dealer_value = Dealer.getHandValue(deck) # Store dealer's final value


				##### Calculate results ######
				app.startSubWindow("results")
				app.showSubWindow("results")
				app.addLabel("Dealer_final_value", "Dealer: " + str(dealer_value))

				if dealer_value > 21:
					# If the dealer busts, any player that does not bust wins
					for index, value in enumerate(player_values):

						app.addLabel(player_name[index], player_name[index] + ": " + str(value))

						if value <= 21:
							app.addMessage(player_name[index], player_name[index] + " WINS!")
						else:
							app.addMessage(player_name[index], player_name[index] + " LOSES :(")
				else:
					for index, value in enumerate(player_values):

						app.addLabel(player_name[index], player_name[index] + ": " + str(value))

						if value > 21:
							# Player busts
							app.addMessage(player_name[index], player_name[index] + " LOSES :(")
						elif value < dealer_value:
							app.addMessage(player_name[index], player_name[index] + " LOSES :(")
						elif value > dealer_value:
							app.addMessage(player_name[index], player_name[index] + " WINS!")
						else:
							app.addMessage(player_name[index], player_name[index] + ", ITS A PUSH!")

			else:
				# Move on to the next player

				app.setLabel("Hand value", "Hand value is " + str(player_obj[counter].getHandValue(deck)))
				app.setMessage("Play", "Do you want to hit or stand?")

				# Create a separate card window for the new player
				app.startSubWindow(player_name[counter])
				app.showSubWindow(player_name[counter])

				for card in player_obj[counter].cards:
					# Display all of the players cards

					app.addImage(player_name[counter]+str(img_num), card_to_image(card), row=0, column=img_num)
					img_num += 1

		else:
			# Player does not bust, draw a card and display it in the player's window

			card = deck.getTopCard()
			player_obj[counter].addToHand(card)
			app.setLabel("Hand value", "Hand value is " + str(player_obj[counter].getHandValue(deck)))

			app.addImage(player_name[counter]+str(img_num), card_to_image(card), row=0, column=img_num)
			img_num += 1

	else:

		############# IF A PLAYER STANDS #############
		app.stopSubWindow() # Stop the player's card window
		app.setLabel("Hand value", "Final hand value is: " + str(player_obj[counter].getHandValue(deck)))

		player_values.append(player_obj[counter].getHandValue(deck)) # Store the player's final value

		counter += 1 # Move on to the next player
		img_num = 0 # Reset
		
		if counter >= len(player_obj):
			# If there is no next player, it's the dealer's turn

			app.showSubWindow("Dealer's cards") # Switch to dealer's card window
			app.addImage("dealer_cards"+str(dealer_img_num), card_to_image(Dealer.cards[1]), row=0, column=dealer_img_num) # Show the dealer's other card
			dealer_img_num += 1

			while Dealer.getHandValue(deck) < 17:
				# While dealer is below 17, keep hitting and display his new card

				card = deck.getTopCard()
				Dealer.addToHand(card)

				app.addImage("dealer_cards"+str(dealer_img_num), card_to_image(card), row=0, column=dealer_img_num)
				dealer_img_num += 1

				if Dealer.getHandValue(deck) > 21:
					# Check if dealer busts
					break


			dealer_value = Dealer.getHandValue(deck) # Store dealer's final value

			##### Calculate results ######
			app.startSubWindow("results")
			app.showSubWindow("results")
			app.addLabel("Dealer_final_value", "Dealer: " + str(dealer_value))

			if dealer_value > 21:
				# If the dealer busts, any player that does not bust wins
				for index, value in enumerate(player_values):

					app.addLabel(player_name[index], player_name[index] + ": " + str(value))

					if value <= 21:
						app.addMessage(player_name[index], player_name[index] + " WINS!")
					else:
						app.addMessage(player_name[index], player_name[index] + " LOSES :(")
			else:
				for index, value in enumerate(player_values):

					app.addLabel(player_name[index], player_name[index] + ": " + str(value))

					if value > 21:
						app.addMessage(player_name[index], player_name[index] + " LOSES :(")
					elif value < dealer_value:
						app.addMessage(player_name[index], player_name[index] + " LOSES :(")
					elif value > dealer_value:
						app.addMessage(player_name[index], player_name[index] + " WINS!")
					else:
						app.addMessage(player_name[index], player_name[index] + ", ITS A PUSH!")

		else:
			# Move on to the next player, create a separate card window and display his cards

			app.setLabel("Hand value", "Hand value is " + str(player_obj[counter].getHandValue(deck)))
			app.setMessage("Play", "Do you want to hit or stand?")

			app.startSubWindow(player_name[counter])
			app.showSubWindow(player_name[counter])

			for card in player_obj[counter].cards:
				app.addImage(player_name[counter]+str(img_num), card_to_image(card), row=0, column=img_num)
				img_num += 1

################################ APPJAR INITIALIZATION ##################################


app=gui()

app.addButtons(["hit", "stand"], launch)

app.addMessage("Play")
app.setMessage("Play", "Do you want to hit or stand?")

app.addLabel("Hand value")
app.setLabel("Hand value", "Hand value is " + str(player_obj[counter].getHandValue(deck)))


# Show the dealer's face up card
app.startSubWindow("Dealer's cards")
app.showSubWindow("Dealer's cards")
app.addImage("dealer_cards"+str(dealer_img_num), card_to_image(Dealer.cards[0]), row=0, column=dealer_img_num)
dealer_img_num += 1

# Show the player's cards
app.startSubWindow(player_name[counter])
app.showSubWindow(player_name[counter])
for card in player_obj[counter].cards:
	app.addImage(player_name[counter]+str(img_num), card_to_image(card), row=0, column=img_num)
	img_num += 1
app.go()