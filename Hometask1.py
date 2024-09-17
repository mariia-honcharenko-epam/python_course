#Task_1: create list of 100 random numbers from 0 to 1000

"""
An empty list called random_list is initialized.
This list will be used to store the random numbers generated in the subsequent steps.
The for loop iterates 100 times as specified by range(100).
A new random integer named number is generated between 0 and 1000,
which is appended to the random_list.
"""

import random

random_list=[]
for _ in range(100):
    number=random.randint(0,1000)
    random_list.append(number)
print(random_list)

#Task_2:sort list from min to max(without using sort()).
""" 
I created a new empty list called sorted_list,
which will be appended with elements from an existing 
list called random_list. In this code, I initially assign the minimum value
to the first element of random_list. Then I use a for loop to compare
each element with the current minimum value. If the current element
is less than the stored minimum, I update the minimum.
After iterating through the entire list and finding the minimum value, 
it is added to sorted_list, and that minimum element is removed from random_list. 
This process repeats until random_list becomes empty 
"""

sorted_list=[]
while random_list:
    minimum = random_list[0]
    for el in random_list:
       if el< minimum:
         minimum = el
    sorted_list.append(minimum)
    random_list.remove(minimum)

print(sorted_list)

#Task 3 calculate average for even and odd numbers

""" 
Two empty lists, list_1 and list_2, are initialized for storing even and odd numbers
For each element el in the list: If el is even, it is appended to list_1.
If el is odd, it is appended to list_2.
If a ZeroDivisionError occurs (due to attempting to compute an average of an empty list),
the respective average is set to None.
If both averages are calculable and not None, it prints both averages.
If one or both of the averages are None due to an empty subset -it prints an appropriate message.
"""

list_1 = []  # even numbers
list_2 = []  # odd numbers

for el in sorted_list:
    if el % 2 == 0:
        list_1.append(el)
    else:
        list_2.append(el)

try:
    average_1 = sum(list_1) / len(list_1)
except ZeroDivisionError:
    average_1 = None
try:
    average_2 = sum(list_2) / len(list_2)
except ZeroDivisionError:
    average_2 = None

if average_1 is not None and average_2 is not None:
    print(average_1, average_2)
else:
    if average_1 is None:
        print("No even numbers provided.")
    if average_2 is None:
        print("No odd numbers provided.")