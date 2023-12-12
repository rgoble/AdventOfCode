from functools import cmp_to_key
class Hand:
    cardStrength = {'2': 2, '3': 3, '4': 4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':1, 'Q':12, 'K':13, 'A':14}

    def __init__(self, str) -> None:
        # Split out the hand and the bid
        self.hand,bid = str.split(' ')
        self.bid = int(bid)
        self.rank = self.calcHandRank()

    def __lt__(self, other):
        if self.rank != other.rank:
            # Ranks are different so no more checking is needed
            return self.rank < other.rank
        
        print("Checking cards (%s) < (%s)" % (self, other))
        # Ranks are the same so need to compare on the cards
        for i in range(5):
            # print("\t#%d: %s vs %s" % (i, self.hand[i], other.hand[i]))
            if self.hand[i] != other.hand[i]:                
                # Different so no more checking
                return Hand.cardStrength[self.hand[i]] < Hand.cardStrength[other.hand[i]]
        
        # If we got here then they are the same
        return False        

    def calcHandRank(self):
        group = {}
        # Group the cards by their value
        for c in self.hand:
            if group.get(c) is None:                
                group[c] = 1
            else:
                group[c] += 1
        
        # Jokers are wild, so if there are any in the hand then we want to count them
        # and add that many to all of the other groups
        numWilds = 0
        if group.get('J') is not None:
            # There are jokers so we will save the number of them
            # an then remove them from the groups to make it easier
            # to compute hands
            numWilds = group['J']
            del group['J']

        keys = list(group.keys())
        numGroups = len(keys)
        if numGroups == 1 or numWilds == 5:
            # Only 1 kind of card, so its a 5 of a kind
            return 6
        elif numGroups == 2:
            # 2 kinds of cards, so it has to be either
            # 4 of a kind, or full house
            fourOfKind = [4, 4 - numWilds]
            if group[keys[0]] in fourOfKind or group[keys[1]] in fourOfKind:
                # 4 of a kind
                return 5
            else:
                # Has to be a full house
                return 4
        else:            
            # 3 or more groups of cards
            # If we get here and we have 2 jokers, then we must have 3 of a kind
            if numWilds == 2:
                return 3

            numPairs = 0
            for c in keys:
                if group[c] == 3 or (group[c] == 2 and numWilds == 1):
                    # 3 of a kind
                    return 3
                elif group[c] == 2:
                    numPairs += 1
            
            if numPairs >= 2:
                return 2
            elif numPairs == 1:
                return 1
            
            # If there are no natural pairs, but we have a joker
            # then that will make a pair
            if numWilds == 1:
                return 1
            elif numWilds > 1:
                print("Error: Have %d wilds left in hand %s, this shouldn't be possible!!!" % (numWilds, self.hand))
            
        # High card only
        return 0

    def __str__(self) -> str:
        return "Cards=%s Bid=%d" % (self.hand, self.bid)

def compareHands(hand1, hand2):
    if hand1.rank < hand2.rank:
        return -1
    elif hand1.rank > hand2.rank:
        return 1
    else:
        # Ranks are the same so now we have to compare the cards
        for i in range(5):
            if hand1.hand[i] < hand2.hand[i]:
                return -1
            elif hand1.hand[i] > hand2.hand[i]:
                return 1
        
        # The hands are the same
        print("Same Hands: (%s) and (%s)" % (hand1, hand2))
        return 0
            
# Parse the input
hands = []
with open("input.txt", "rt") as inp:
    for line in inp:
        hands.append(Hand(line))

# Sort the list
# hands.sort(key=compareHands)
# sorted(hands, cmp=compareHands)
hands.sort()

winnings = 0
for i in range(len(hands)):
    winnings += (i+1) * hands[i].bid

print('='*8)
print("Winnings: %d" % winnings)