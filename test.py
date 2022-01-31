from faker import Faker
import pandas as pd
import datetime
from datetime import datetime as dt



pesel = '26101482603'

def pesel_to_date(pesel):

  x = int(pesel[2:3])
  century_code = int(pesel[2:4])

  # Day
  day = int(pesel[4:6])

  # Month
  if x % 2 == 0:
    month = century_code - 10*x
  else:
    month = century_code - 10*(x-1)

  # Year
  if century_code > 80:
      century = 18
  else:
    century = 18
    for i in range(0,80,20):
      if century_code < i:
        break
      century += 1
  year = century * 100 + int(pesel[:2])

  return print(datetime.datetime(year, month, day))


# pesel_to_date('34092582603')


# year_thousandth = {18:80, 19:100, 20:120, 21:140, 22:160, 22:180}

# for value in year_thousandth:
#   if y 
        
        
        
# print(year_tenth)
# print(pesel[2:3])
# print(int(pesel[2:4]))



# pesel = 55030101230

# digits_weights = [1,3,7,9,1,3,7,9,1,3,0]

# # converting number to list of integers
# pesel_list = list(map(int, str(pesel)))

# digits_sum = 0

# # sum of the products of numbers
# for i in range(len(pesel_list)):
#   digits_sum += digits_weights[i] * pesel_list[i]
  
# digits_sum_last = digits_sum % 10

# # check digit
# if digits_sum_last == 0: check_digit = 0
# else: check_digit = 10 - digits_sum_last

# print(f'S:{digits_sum}\nM:{digits_sum_last}\ncheck_digit:{check_digit}')


# def gender_check(pesel, gender):
'''
pesel = '00011428200'

digits_weights = [1,3,7,9,1,3,7,9,1,3,0]

# Converting number to list of integers
pesel_list = list(map(int, str(pesel)))

digits_sum = 0

# Sum of the products of numbers
for i in range(len(pesel_list)):
  digits_sum += digits_weights[i] * pesel_list[i]
  
digits_sum_last = digits_sum % 10

# Check digit
if digits_sum_last == 0: check_digit = 0
else: check_digit = 10 - digits_sum_last

if check_digit != pesel_list[-1]:
  print(False)
    
print(True)


pesel = '08241833133'

if int(pesel) >= 0 and len(str(pesel)) == 11: print('git')
else: pesel = input('\nPESEL needs to be an integer consisting of 11 digits\nPlease enter pesel: ')

'''

def fun(x):
  print(x)
  
fun('00023')