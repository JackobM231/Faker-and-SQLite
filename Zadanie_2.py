import sqlite3
import csv

def main():
  
  # Connecting to the database
  connection = sqlite3.connect('new.db')

  # Creating a Cursour object
  cursor = connection.cursor()

  try:
    cursor.execute('DROP TABLE FlightLeg')
  except:
    pass
    
  # Podpunkt 1.
  # Creating table in our database
  cursor.execute('''CREATE TABLE FlightLeg(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              tailNumber TEXT,
              sourceAirportCode TEXT,
              destinationAirportCode TEXT,
              sourceCountryCode TEXT,
              destinationCountryCode TEXT,
              departureTimeUtc NUMERIC,
              landingTimeUtc NUMERIC);''')

  # Podpunkt 2.
  # Opening file
  with open('flightlegs.csv', 'r') as file:
    
    # Reading the content from file
    rows = csv.reader(file, delimiter=';')
    
    # Skip through the headers
    next(rows)
    
    insert_records = '''INSERT INTO FlightLeg
          (tailNumber, sourceAirportCode, destinationAirportCode,
          sourceCountryCode, destinationCountryCode, departureTimeUtc,
          landingTimeUtc) VALUES(?, ?, ?, ?, ?, ?, ?);'''
    
    cursor.executemany(insert_records, rows)
    
    connection.commit()


  # Podpunkt 3.
  # Add new columns
  cursor.execute('''ALTER TABLE FlightLeg ADD COLUMN flightDuration INTEGER;''')
  cursor.execute('''ALTER TABLE FlightLeg ADD COLUMN flightType TEXT;''')

  # Update new columns
  cursor.execute('''UPDATE FlightLeg
              SET flightDuration = (ROUND((JULIANDAY(landingTimeUtc) - JULIANDAY(departureTimeUtc)) * 1440));''')

  cursor.execute('''UPDATE FlightLeg
              SET flightType = CASE
              WHEN sourceCountryCode != destinationCountryCode THEN 'I'
              ELSE 'D' END;''')

  connection.commit()


  # Podpunkt 4.
  # 4.1.
  most_flights = cursor.execute(
    '''SELECT tailNumber, COUNT(*) AS Flights
      FROM FlightLeg
      GROUP BY tailNumber
      HAVING Flights = (SELECT COUNT(*) AS Flights
                        FROM FlightLeg
                        GROUP BY tailNumber
                        ORDER BY Flights DESC LIMIT 1);''')

  print('4.1. Most flights:')
  for plane in most_flights:
    print(f'\tPlane {plane[0]} made {plane[1]} flights.')


  # 4.2.
  most_minutes = cursor.execute(
  '''SELECT tailNumber, SUM(flightDuration) AS flightDurationSum
    FROM FlightLeg
    GROUP BY tailNumber
    HAVING flightDurationSum = (SELECT SUM(flightDuration) AS flightDurationSum
                              FROM FlightLeg
                              GROUP BY tailNumber
                              ORDER BY flightDurationSum DESC LIMIT 1);''')

  print('4.2. Most minutes:')
  for plane in most_minutes:
    print(f'\tPlane {plane[0]} made {plane[1]} minutes in the air.')
    

  # 4.3.
  longest = cursor.execute(
  '''SELECT tailNumber, departureTimeUtc, flightDuration, flightType
    FROM FlightLeg
    WHERE flightDuration IN (
          SELECT MAX(flightDuration)
          FROM FlightLeg
          GROUP BY flightType);''')

  print('4.3.\nLongest flight depanding on flight type:')
  for plane in longest:
    f_type = 'international'
    if plane[3] == 'D':
      f_type = 'domestic'
    print(f'\tFlight: {plane[0]} - {plane[1]} made {plane[2]} minutes on the {f_type} flight.')


  shortest = cursor.execute(
  '''SELECT tailNumber, departureTimeUtc, flightDuration, flightType
    FROM FlightLeg
    WHERE flightDuration IN (
          SELECT MIN(flightDuration)
          FROM FlightLeg
          GROUP BY flightType);''')

  print('\nShortest flight depanding on flight type:')
  for plane in shortest:
    f_type = 'international'
    if plane[3] == 'D':
      f_type = 'domestic'
    print(f'\tFlight: {plane[0]} - {plane[1]} made {plane[2]} minutes on the {f_type} flight.')
    
    
  # 4.4.
  wrong_records = cursor.execute(
  '''WITH Flights as (
    SELECT tailNumber, departureTimeUtc, landingTimeUtc
    FROM FlightLeg)
          
    SELECT *
    FROM Flights AS F1 LEFT JOIN Flights AS F2
    ON F1.tailNumber = F2.tailNumber
    WHERE (F1.departureTimeUtc < F2.departureTimeUtc 
          AND F1.landingTimeUtc > F2.departureTimeUtc
          AND F1.LandingTimeUtc < F2.landingTimeUtc) 
    OR
          (F1.departureTimeUtc < F2.departureTimeUtc
          AND F1.landingTimeUtc > F2.landingTimeUtc);''')

  print(f'\n4.4. Wrong records:')
  num = 0
  for flight in wrong_records:
    num += 1
    print(f'\t{flight[0]} - ({flight[1]} - {flight[2]}) --- {flight[3]} - ({flight[4]} - {flight[5]})')
  print(f'The number of pairs of incorrect flights: {num}')
    
    
  # 4.5.
  min_difference = cursor.execute(
  '''WITH Flights as (
    SELECT tailNumber, departureTimeUtc, landingTimeUtc
    FROM FlightLeg)

    SELECT F1.TailNumber, F1.departureTimeUtc, F1.landingTimeUtc,
    F2.TailNumber, F2.departureTimeUtc, F2.landingTimeUtc,
      (ROUND((JULIANDAY(F2.departureTimeUtc) - JULIANDAY(F1.landingTimeUtc)) * 24*60)) as DifferenceMin
    FROM Flights AS F1 LEFT JOIN Flights AS F2
    ON F1.tailNumber = F2.tailNumber
    WHERE DifferenceMin = (
                SELECT (ROUND((JULIANDAY(F2.departureTimeUtc) - JULIANDAY(F1.landingTimeUtc)) * 24*60)) as DifferenceMin
                FROM Flights AS F1 LEFT JOIN Flights AS F2
                ON F1.tailNumber = F2.tailNumber
                WHERE DifferenceMin >= 0
                ORDER BY DifferenceMin ASC LIMIT 1);'''
  )

  print('\n4.5. Shortest break before next departure:')
  for flight in wrong_records:
    print(f'\t{flight[0]} - ({flight[1]} - {flight[2]}) --- {flight[3]} - ({flight[4]} - {flight[5]}) break: {flight[6]} minutes.')
  
main()    