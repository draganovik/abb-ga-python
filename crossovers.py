import random
from collections import deque

def cxOrdered(parent1, parent2):

    indx1 = random.randint(0, min(len(parent1), len(parent2)))
    indx2 = random.randint(0, min(len(parent1), len(parent2)))

    if indx1 > indx2:
        indx1, indx2 = indx2, indx1

    child = deque(parent1[indx1 : indx2])

    if indx2==len(parent2):
        indx2 = 0

    while len(child) < len(parent2):
        if parent2[indx2] not in child:
            child.append(parent2[indx2])

        indx2 = (indx2 + 1) % len(parent2)

    child.rotate(indx1)

    return child

def cxPartialyMatched(ind1, ind2):
    size = min(len(ind1), len(ind2))
    p1, p2 = [0] * size, [0] * size

    # Initialize the position of each indices in the individuals
    for i in range(size):
        p1[ind1[i]] = i
        p2[ind2[i]] = i
    # Choose crossover points
    cxpoint1 = random.randint(0, size)
    cxpoint2 = random.randint(0, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    # Apply crossover between cx points
    for i in range(cxpoint1, cxpoint2):
        # Keep track of the selected values
        temp1 = ind1[i]
        temp2 = ind2[i]
        # Swap the matched value
        ind1[i], ind1[p1[temp2]] = temp2, temp1
        ind2[i], ind2[p2[temp1]] = temp1, temp2
        # Position bookkeeping
        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp2] = p2[temp2], p2[temp1]

    return ind1
