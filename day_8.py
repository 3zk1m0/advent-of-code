from collections import Counter

with open("day_8.txt") as f:
    inputs = list(map(int, list(f.readline().strip())))
    #inputs = f.readline().strip()

#25 pixels wide and 6 pixels tall

images = []
while inputs:
    images.append(inputs[:25*6])
    del inputs[:25*6]



result = 25*6, None
for items in images:
    if result[0] > items.count(0):
        result = items.count(0), items.count(1) * items.count(2)


print('Part 1 = {}'.format(result[1]))

base = [2 for i in range(len(images[0]))]

for layer in range(len(images)):
    for index, data in enumerate(images[layer]):
        if data == 1 and base[index] == 2:
            base[index] = 1
        elif data == 0 and base[index] == 2:
            base[index] = 0

print('Parrt 2 = ')
for count in range(0,len(base),25):
    for items in base[count:count+25]:
        if items == 1:
            print("#", end = '')
        elif items == 0:
            print(" ", end = '')
    print('')
