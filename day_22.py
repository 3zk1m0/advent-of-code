#with open("test.txt") as f:
with open("day_22.txt") as f:
    result = f.readlines()
    input_data = []
    for line in result:
        if line.strip() == "deal into new stack":
            input_data.append([line.strip(), None])
        else:
            tmp = line.strip().rsplit(' ', 1)
            input_data.append([tmp[0], int(tmp[1])])



def deal_into_new_stack(cards):
    cards.reverse()
    return cards

def cut(cards, pos):
    return cards[pos:]+cards[:pos]

def deal_with_increment(cards, increment):
    new_cards = [None]*len(cards)
    pos = 0
    lenght = len(cards)
    while any([x == None for x in new_cards]):
        if new_cards[pos] != None:
            print("FUck")
        new_cards[pos] = cards[0]
        del cards[0]
        pos += increment
        if pos >= lenght:
            pos -= lenght
    return new_cards

def part_1():
    cards = [x for x in range(10006+1)]

    for (command, argument) in input_data:
        if command == "deal into new stack":
            cards = deal_into_new_stack(cards)
        elif command == "cut":
            cards = cut(cards, argument)
        elif command == "deal with increment":
            cards = deal_with_increment(cards, argument)

    return cards.index(2019)

def part_2():
    m = 119315717514047
    n = 101741582076661
    pos = 2020
    shuffles = { 
        'deal with increment ': lambda x,m,a,b: (a*x %m, b*x %m),
        'deal into new stack': lambda _,m,a,b: (-a %m, (m-1-b)%m),
        'cut ': lambda x,m,a,b: (a, (b-x)%m) 
        }
        
    a,b = 1,0
    with open('day_22.txt') as f:
        for s in f.read().strip().split('\n'):
            for name,fn in shuffles.items():
                if s.startswith(name):
                    arg = int(s[len(name):]) if name[-1] == ' ' else 0
                    a,b = fn(arg, m, a, b)
                    break
    r = (b * pow(1-a, m-2, m)) % m
    return f"Card at #{pos}: {((pos - r) * pow(a, n*(m-2), m) + r) % m}"

if __name__ == "__main__":
    #print(part_1())
    print(part_2())




