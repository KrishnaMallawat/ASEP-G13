total_cards = int(input("Enter the total number of cards: "))
provided_sum = int(input("Enter the sum of the cards: "))   

missing_card =  (total_cards * (total_cards + 1) // 2) - provided_sum
print(f"The missing card is {missing_card}")