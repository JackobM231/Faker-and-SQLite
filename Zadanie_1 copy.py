from faker import Faker
import pandas as pd
import datetime
from datetime import datetime as dt
import time

fake = Faker('pl_PL')


# Podpunkt 1.
def generate_ssns(num):
  lst = []
  for i in range(num):
    lst.append(fake.ssn())
  
  s = pd.Series(lst)
  return s


# Podpunkt 2.
def generate_unique_ssns(*args):
  ''' Generating specific and unique PESEL '''
  
  # Checking that the correct number of arguments is given
  if len(args) != 4:
    return -1
  
  x = check_input(args[0], args[1], args[2], args[3])
  
  num = x[0]
  gender = x[1]
  start = x[2]
  end = x[3]
  
  lst = []
  while len(lst) != num:
    pesel = fake.unique.ssn()
    
    # Gender checking
    if not(gender == 'f' and int(pesel[-2]) % 2 == 0) or (gender == 'm' and int(pesel[-2]) % 2 != 0):
      continue
    
    # Date checking
    date = pesel_to_date(pesel)
    if not(date >= start and date <= end):
      continue
    
    lst.append(pesel)
    
  s = pd.Series(lst)
  return s


def check_input(num, gender, start, end):
    ''' Checking of input data '''
    # Number of SSNs
    while True:
      try:
        num = int(num)
        if num >= 0: break
        else: num = input('\nNumber of SSNs needs to be an integer greater then 0.\nPlease select number: ')
      except:
        num = input('\nNumber of SSNs needs to be an integer greater then 0.\nPlease select number: ')
      
    # Gender of person  
    while True:
      try:
        gender = gender.lower()
        if gender in ['m', 'f']: break
        else: gender = input('\nPlease select gender.\n female: f\n male: m \n: ')
      except:  
        gender = input('\nPlease select gender.\n female: f\n male: m \n: ')
      
    # Date
    # Scope of the adopted method of PESEL encoding
    d1 = datetime.datetime(1800, 1, 1)
    d2 = datetime.datetime(2299, 12, 31)
    while True: 
      try:
        start = dt.fromisoformat(start)
        if (start >= d1) and (start <= d2):
          break
      except:
          start = input('\nWrong date.\nPlease select date from 1800-01-01 to 2299-12-31\n(format YYYY-MM-DD):  ')

    while True:
      try:
        end = dt.fromisoformat(end)
        if (end >= start) and (end <= d2):
          break
      except:
          end = input(f'\nWrong date.\nPlease select date from {start.isoformat()[:10]} to 2299-12-31\n(format YYYY-MM-DD):  ')
          
    return num, gender, start, end
  
  
def pesel_to_date(pesel):
  ''' Extracting the date from pesel '''
  
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

  return datetime.datetime(year, month, day)
  

def main():
  
  num = [1, 10, 100]
  
  for n in num:
    t0 = time.perf_counter()
    generate_ssns(n)
    t1 = time.perf_counter()
    print(f"{n} pesels generated in {t1 - t0} seconds")
  
  print('\n')
    
  for n in num:
    t0 = time.perf_counter()
    generate_unique_ssns(n, 'f', '1990-01-01', '1990-01-19')
    t1 = time.perf_counter()
    print(f"{n} unique pesels generated in {t1 - t0} seconds")
  
main()






  


  
  
  
  
  
  # while not isinstance(start, datetime.date):
  #   start = input('Wrong date. Please select date from 1800-01-01 to 2299-12-31: ')
    
  
    




# print(generate_ssns(3))
# start = '1900-12-12'
# start = '18/09/19'
# try:
#   start = datetime.strptime(start, '%Y-%m-%d')
# except:
#   while not isinstance(start, datetime.date):
#     start = input('Wrong date. Please select date from 1800-01-01 to 2299-12-31: ')
#     start = datetime.strptime(start, '%Y-%m-%d')
# print(start)

  # try:
  #   start = datetime.strptime(start, '%Y-%m-%d')
  # except:
  #   while not isinstance(start, datetime.date):
  #     start = input('Wrong date. Please select date from 1800-01-01 to 2299-12-31: ')
  #     start = datetime.strptime(start, '%Y-%m-%d')