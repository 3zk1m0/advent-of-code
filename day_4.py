
from collections import Counter 
  


def double(password):
    result = False  

    for items in range(len(str(password))):
        try:
            if str(password)[int(items)] == str(password)[int(items)+1]:
                if str(password)[int(items)] != str(password)[int(items)+2]:
                    result = True
        except IndexError:
            pass
    return result


def rising(password):
    for items in range(len(str(password))):
        try:
            if str(password)[int(items)] > str(password)[int(items)+1]:
                return False
        except IndexError:
            pass
    return True


def double2(password):
    count = Counter(str(password))
    for x in count.values():
        if x == 2:
            return True
    return False



if __name__ == "__main__":
    result = []
    for number in range(264360,746325+1):
        if double2(number) and rising(number):
            result.append(number)

    print(len(result))




    















