# Implement the coding tasks or answer the questions below in this format:
# 1: What is your name?
# JH>> John 

my_name = "John"
# 2: Print the variable name
print(my_name)

# ********************************
# key-vaue pairs go in dictionaries
userDictionary = {'name':'John',
          'hometown':'Austin',
          'age':'55',
          'University':'TAMU',
          'graduation date':1986,
          'hometown':'College Station',
          'hometown':'San Jose'
          }

# 1: print the value for the key 'name'
print(userDictionary['name'])

# 2: What if you try to print out a key that is not present, what happens? 
# try this print(userDictionary[0])
print('theres a keyerror')

# Example of Looping to find values
for i in userDictionary:
    values = userDictionary[i]  # i is the key
    print(values)
    

# 3. In a for loop print the keys
for j in userDictionary:
    print(j)

# 4. What happens if there are two keys with the same name and if you do
# this which value is used?
print('the last key and value are used')

# 5. change the value of the 'graduation date' value to 1987 and print
userDictionary['graduation date'] = 1987
print(userDictionary['graduation date'])

# 6. programmatically add a key and value, 'degree':'BMEN' and print
userDictionary['degree'] = 'BMEN'
print(userDictionary['degree'])

# 7. remove the 'age' key and value using the pop() method
userDictionary.pop('age')

# 8. remove the 'degree' key and value using the del statement
del userDictionary['degree']

# 9. Are dictionaries mutable or immutable?
print('mutable')

d2 = userDictionary
# d2 and userDictionary have the same object id, meaning that d2 is another name for userDictionary 
# and if you change userDictionary, d2 also changes.  

# 10. Show that userDictionary and d2 are the same object using the id() function
print('userDictionary ID:', id(userDictionary))
print('d2 ID:', id(d2))
if id(d2) == id(userDictionary):
    print('d2 and userDictionary are the same object')
else:
    print("d2 and userDictionary are not the same object")

# here is a method to copy a dictionary to create a new object
d2 =dict(userDictionary)
print(id(d2))
print(id(userDictionary))

# this is  a set
set1 = {'tree', 'car', 'house'}
# Read https://www.w3schools.com/python/python_sets.asp to understand the difference between sets 
# and dictionaries.

# 11. What are two qualities of sets that are different from dictionaries?
print('sets are not indexed or ordered like dictionaries')

# 12. if you try to print(set1[0]) what happens? If you print(set1) multiple
# times what happens.
print('you get an error for both cases')


set2 = {'house', 'family', 'university', 'tree'}

# 13. Use the intersection method to find the intersection of set1 and set2, print the results
set3 = set1.intersection(set2)
print(set3)

# A feature of sets is that they are fast for operatioins such as unitions and intersections



