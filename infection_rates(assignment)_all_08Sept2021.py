# Reference for estimated doubling rates 
# https://wwwnc.cdc.gov/eid/article/26/8/20-0219_article

#############  Inputs ##############
italy = 1_000                           # number of people infected in italy
china = 10_000                          # number of people infected in china
italy_infection_growth_rate = 0.30      # growth rate per day, china
china_infection_growth_rate = 0.10      # growth rate per day, china

####################################

'''
Use a for loop and break statement to find the number of hours until Italy has the same number
of infected people as China


Use this simple model:
    
    final_infected = initial_infected*(1+growth_rate)**time

    
'''

print("{} hours until the number of infections in Italy is greater than the number of infections in China.".format(round(hours,2)))
print("{} the number of people infected in Italy".format(round(total_italy)))
print("{} the number of people infected in China".format(round(total_china)))



"""
Use a while loop and break statement to calculate how many days 
until the virus infections 350 million people are infected

Other assumptions:
- 100,000 are infected initially
- 40% infection growth rate per day

"""

print("The number of days until 350,000,000 = " + str(days))

"""
In addition to the prompt above, print to the console the number of days 
for 1, 10, and 50 million infections

"""

"""
Bonus 1 point
import matplotlib and numpy and plot the infection curve to show the number
of days it takes to reach 350M
"""