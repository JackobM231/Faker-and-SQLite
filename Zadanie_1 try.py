from faker import Faker
import pandas as pd
import datetime
from datetime import datetime as dt
import time

fake = Faker('pl_PL')


# Podpunkt 1.
'''
Założenia:
- Dane wejściowe: liczba rekordów
- Wygenerowanie liczby numerów PESEL
  odpowiadającej liczbie rekordów
- Zwrócenie obiektu typu Series
'''
def generate_ssns(num):
  lst = []
  for i in range(num):
    lst.append(fake.ssn())
  
  s = pd.Series(lst)
  print(s)
  return s
#////////////////////////////////


# Podpunkt 2.
'''
Założenia:
- Dane wejściowe: liczba rekordów, płeć(female: f, male: m),
  data początkowa: YYYY-MM-DD, data końcowa: YYYY-MM-DD
- Sprawdzenie poprawności wprowadzonych danych
- Wygenerowanie liczby (odpowiadającej liczbie rekordów)
  unikatowych numerów PESEL spełniających warunki wprowadzone
  w parametrach wejściowych
- Zwrócenie obiektu typu Series
'''
def generate_unique_ssns(*args):
  ''' Generating specific and unique PESEL '''
  
  # Checking the correct number of arguments
  if len(args) != 4:
    return -1
  
  x = check_input_unique(args[0], args[1], args[2], args[3])
  
  num = x[0]
  gender = x[1]
  start = x[2]
  end = x[3]
  
  lst = []
  while len(lst) != num:
    pesel = fake.unique.ssn()
    
    # Gender checking
    if not ((gender == 'f' and int(pesel[-2]) % 2 == 0) or (gender == 'm' and int(pesel[-2]) % 2 != 0)):
      continue
    
    # Date checking
    date = pesel_to_date(pesel)
    if not(date >= start and date <= end):
      continue
    
    lst.append(pesel)
    
  s = pd.Series(lst)
  print(s)
  return s


# Funkcje pomocniczne Podpunkt 2.
def check_input_unique(num, gender, start, end):
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
  ''' Extracting the date from PESEL '''
  
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

  try:
    return datetime.datetime(year, month, day)
  except:
    return -1
#////////////////////////////////


# Podpunkt 3.
'''
Założenia:
- Wywołanie funkcji generate_ssns z liczbą rekordów równą
  1000, 10000, 100000 razy oraz wyświetlenie czasu ich wykonywania
- Wywołanie funkcji generate_unique_ssns z liczbą rekordów równą
  1000, 10000, 100000, wybraną płcią 'f', przedziałem daty urodzenia
  od 1990-01-01 do 1990-01-19 oraz wyświetleniem czasu wykonywania
'''
def subsection_3():
  
  num = [1, 10, 100]
  
  for n in num:
    t0 = time.perf_counter()
    generate_ssns(n)
    t1 = time.perf_counter()
    print(f"{n} PESELs generated in {t1 - t0} seconds\n")
  
  print('\n')
    
  for n in num:
    t0 = time.perf_counter()
    generate_unique_ssns(n, 'f', '1990-01-01', '1990-01-19')
    t1 = time.perf_counter()
    print(f"{n} unique PESELs generated in {t1 - t0} seconds\n")
#//////////////////////////////// 
  
  
# Podpunkt 4.
'''
Założenia:
- Dane wejściowe: PESEL w postaci 11 cyfrowej,
  płeć(female: f, male: m, any: a),
  data:
   1. Brak określonej daty: a
   2. Konkretna data: YYYY-MM-DD
   3. Przedział: od YYYY-MM-DD, do YYYY-MM-DD
- Sprawdzenie poprawności wprowadzonych danych
- Sprawdzenie czy wprowadzony PESEL spełnia założenia
  z informacją zwrotną
'''
def validate_ssn(pesel, gender, *args):
  
  # Checking the correct number of arguments
  if len(locals()) != 3:
    print('Incorrect number of arguments')
    return -1
  
  x = check_input(pesel, gender, *args)
  
  pesel = x[0]
  gender = x[1]
  start = x[2]
  
  # Check digit
  if not check_digit(pesel):
    print("Invalid PESEL number")
    return -1

  # Gender checking
  pesel = str(pesel)
  if not ((gender == 'f' and int(pesel[-2]) % 2 == 0) or (gender == 'm' and int(pesel[-2]) % 2 != 0) or (gender == 'a')):
    print('Gender does not match this PESEL number')
    return -1
  
  # Date checking
  if start != 'a':
    pesel_date = pesel_to_date(pesel)
    if pesel_date == -1:
      print("Date is incorrect")
      return -1
    
    # Date from YYYY-MM-DD to YYYY-MM-DD
    if len(args) == 2:
      end = x[3]
      if not(pesel_date >= start and pesel_date <= end):
        print('The date of the PESEL is not within the given range')
        return -1
    # Specified date YYYY-MM-DD
    else:
      if pesel_date != start:
        print('The PESEL date does not match the given date')
        return -1
  
  print('PESEL number is correct')
  return 1
  
  
# Funkcje pomocnicze Podpunkt 4.
def check_input(pesel, gender, *date):
    ''' Checking of input data '''
    # PESEL
    while True:
      try:
        if int(pesel) >= 0 and len(str(pesel)) == 11: break
        else: pesel = input('\nPESEL needs to be an integer consisting of 11 digits\nPlease enter pesel: ')
      except:
        pesel = input('\nPESEL needs to be an integer consisting of 11 digits\nPlease enter pesel: ')
      
    # Gender of person  
    while True:
      try:
        gender = gender.lower()
        if gender in ['m', 'f', 'a']: break
        else: gender = input('\nPlease select gender.\n female: f\n male: m\n any: a\n: ')
      except:  
        gender = input('\nPlease select gender.\n female: f\n male: m\n any: a\n: ')
      
    # Date
    # Scope of the adopted method of PESEL encoding
    d1 = datetime.datetime(1800, 1, 1)
    d2 = datetime.datetime(2299, 12, 31)
    
    start = date[0]
    
    if start != 'a':
      while True:
        try:
          start = dt.fromisoformat(start)
          if (start >= d1) and (start <= d2):
            break
        except:
            start = input('\nWrong date.\nPlease select date from 1800-01-01 to 2299-12-31\n(format YYYY-MM-DD):  ')

      if len(date) == 2:
        end = date[1]
        while True:
          try:
            end = dt.fromisoformat(end)
            if (end >= start) and (end <= d2):
              break
          except:
              end = input(f'\nWrong date.\nPlease select date from {start.isoformat()[:10]} to 2299-12-31\n(format YYYY-MM-DD):  ')
    
    if len(date) == 2: return pesel, gender, start, end  
    else: return pesel, gender, start
    
def check_digit(pesel):
  ''' checking PESEL's digits '''
  try:
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
      return False
    
    return True
      
  except:
    return False
#////////////////////////////////
  

# Wywołanie funkcji

# 1.
generate_ssns(100)

# 2.
generate_unique_ssns(100, 'f', '1990-01-01', '1990-01-19')

# 3.
subsection_3()

# # 4.
y = []
z = []
for i in range(100):
  x = generate_ssns(1)[0]
  if validate_ssn(x, 'f', '1995-01-02', '2022-01-01') == -1:
    y.append(x)
  else:
    z.append(x)
    
print(f'Incorrect PESEL number: {y}')
print(f'Correct PESEL number: {z}')