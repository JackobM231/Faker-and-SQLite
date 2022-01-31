-- SQLite
select *
from FlightLeg;

-- select ROUND((JULIANDAY(landingTimeUtc) - JULIANDAY(departureTimeUtc)) * 1440) as Difference
-- from FlightLeg;


ALTER TABLE FlightLeg
ADD COLUMN flightDuration INTEGER GENERATED ALWAYS AS (
ROUND((JULIANDAY(landingTimeUtc) - JULIANDAY(departureTimeUtc)) * 1440)) VIRTUAL;


UPDATE FlightLeg 
SET flightType = 'I'
WHERE sourceCountryCode != destinationCountryCode;

UPDATE FlightLeg
SET flightType = CASE
  WHEN sourceCountryCode != destinationCountryCode THEN 'I'
  ELSE 'D' END;

UPDATE FlightLeg
SET flightDuration = (ROUND((JULIANDAY(landingTimeUtc) - JULIANDAY(departureTimeUtc)) * 1440));

-- Podpunkt 4.
-- 4.1.
SELECT tailNumber, COUNT(*) AS Flights
FROM FlightLeg
GROUP BY tailNumber
ORDER BY Flights DESC;


SELECT tailNumber, COUNT(*) AS Flights
FROM FlightLeg
GROUP BY tailNumber
HAVING Flights = 13;


SELECT tailNumber, COUNT(*) AS Flights
FROM FlightLeg
GROUP BY tailNumber
HAVING Flights = (SELECT COUNT(*) AS Flights
                  FROM FlightLeg
                  GROUP BY tailNumber
                  ORDER BY Flights DESC LIMIT 1);


SELECT COUNT(*) AS Flights
FROM FlightLeg
GROUP BY tailNumber
ORDER BY Flights DESC LIMIT 1;


-- 4.2.
SELECT tailNumber, SUM(flightDuration) AS flightDurationSum
FROM FlightLeg
GROUP BY tailNumber
ORDER BY flightDurationSum DESC;

SELECT tailNumber, SUM(flightDuration) AS flightDurationSum
FROM FlightLeg
GROUP BY tailNumber
HAVING flightDurationSum = (SELECT SUM(flightDuration) AS flightDurationSum
                          FROM FlightLeg
                          GROUP BY tailNumber
                          ORDER BY flightDurationSum DESC LIMIT 1);

SELECT SUM(flightDuration) AS flightDurationSum
FROM FlightLeg
GROUP BY tailNumber
ORDER BY flightDurationSum DESC LIMIT 1;

-- 4.3.
SELECT tailNumber, MAX(flightDuration) as flightDurationMAX,
flightType, departureTimeUtc
FROM FlightLeg
GROUP BY flightType;

SELECT tailNumber, MIN(flightDuration) as flightDurationMIN,
flightType, departureTimeUtc
FROM FlightLeg
GROUP BY flightType;

SELECT tailNumber, departureTimeUtc, flightDuration, flightType
FROM FlightLeg
WHERE flightDuration IN (738, 966, 59, 42);

SELECT tailNumber, departureTimeUtc, flightDuration, flightType
FROM FlightLeg
WHERE flightDuration IN (
      SELECT MIN(flightDuration)
      FROM FlightLeg
      GROUP BY flightType);

SELECT tailNumber, departureTimeUtc, flightDuration, flightType
FROM FlightLeg
WHERE flightDuration IN (
      SELECT MAX(flightDuration)
      FROM FlightLeg
      GROUP BY flightType);


SELECT tailNumber, MAX(flightDuration) as flightDurationMAX,
 MIN(flightDuration) as flightDurationMIN
FROM FlightLeg
WHERE flightType = 'D';

SELECT tailNumber, MAX(flightDuration) as flightDurationMAX,
 MIN(flightDuration) as flightDurationMIN
FROM FlightLeg
WHERE flightType = 'I';

-- 4.4.
WITH Flights as (
SELECT tailNumber, departureTimeUtc, landingTimeUtc
FROM FlightLeg)

SELECT *
FROM Flights AS F1 LEFT JOIN Flights AS F2
ON F1.tailNumber = F2.tailNumber
WHERE F1.landingTimeUtc > F2.departureTimeUtc;


WITH Flights as (
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
      AND F1.landingTimeUtc > F2.landingTimeUtc);


SELECT *
FROM Flights
WHERE landingTimeUtc > '2021-11-30'
ORDER BY landingTimeUtc ASC;

-- 4.5.

WITH Flights as (
SELECT tailNumber, departureTimeUtc, landingTimeUtc
FROM FlightLeg)

SELECT F1.TailNumber, F1.departureTimeUtc, F1.landingTimeUtc,
 F2.TailNumber, F2.departureTimeUtc, F2.landingTimeUtc,
  (ROUND((JULIANDAY(F2.departureTimeUtc) - JULIANDAY(F1.landingTimeUtc)) * 24*60)) as DifferenceMin
FROM Flights AS F1 LEFT JOIN Flights AS F2
ON F1.tailNumber = F2.tailNumber
WHERE DifferenceMin >= 0
ORDER BY DifferenceMin ASC;


WITH Flights as (
SELECT tailNumber, departureTimeUtc, landingTimeUtc
FROM FlightLeg)

SELECT (ROUND((JULIANDAY(F2.departureTimeUtc) - JULIANDAY(F1.landingTimeUtc)) * 24*60)) as DifferenceMin
FROM Flights AS F1 LEFT JOIN Flights AS F2
ON F1.tailNumber = F2.tailNumber
WHERE DifferenceMin >= 0
ORDER BY DifferenceMin ASC;



WITH Flights as (
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
            ORDER BY DifferenceMin ASC LIMIT 1);


WITH Flights as (
SELECT tailNumber, departureTimeUtc, landingTimeUtc
FROM FlightLeg)

SELECT (ROUND((JULIANDAY(F2.departureTimeUtc) - JULIANDAY(F1.landingTimeUtc)) * 24*60)) as DifferenceMin
FROM Flights AS F1 LEFT JOIN Flights AS F2
ON F1.tailNumber = F2.tailNumber
WHERE DifferenceMin >= 0
ORDER BY DifferenceMin ASC LIMIT 1;












SELECT 'Flight: ' + F1.TailNumber + ' - (' +  F1.departureTimeUtc + ' - ' + F1.landingTimeUtc + ')' AS Flight1, F2.TailNumber, (ROUND((JULIANDAY(F2.departureTimeUtc) - JULIANDAY(F1.landingTimeUtc)) * 24*60)) as DifferenceMin
FROM Flights AS F1 LEFT JOIN Flights AS F2
ON F1.tailNumber = F2.tailNumber
WHERE DifferenceMin >= 0
ORDER BY DifferenceMin ASC;


drop table FlightLeg; A6-EVF 3426

select *
from FlightLeg;