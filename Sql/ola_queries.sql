-- OLA Ride Insights - SQL Queries
-- Author: [Shubham Sao]

-- Query 1: Retrieve all successful bookings
SELECT * FROM ola_rides 
WHERE Booking_Status = 'Success'
LIMIT 10;

-- Query 2: Average ride distance per vehicle type
SELECT Vehicle_Type, ROUND(AVG(Ride_Distance), 2) AS Avg_Distance
FROM ola_rides
GROUP BY Vehicle_Type
ORDER BY Avg_Distance DESC;

-- Query 3: Total cancelled rides by customers
SELECT COUNT(*) AS Total_Cancelled_by_Customer
FROM ola_rides
WHERE Booking_Status = 'Canceled by Customer';

-- Query 4: Top 5 customers by number of rides
SELECT Customer_ID, COUNT(*) AS Total_Rides
FROM ola_rides
GROUP BY Customer_ID
ORDER BY Total_Rides DESC
LIMIT 5;

-- Query 5: Rides cancelled by drivers due to personal and car issues
SELECT COUNT(*) AS Cancelled_by_Driver_Personal_Car
FROM ola_rides
WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue';

-- Query 6: Max and min driver ratings for Prime Sedan
SELECT MAX(Driver_Ratings) AS Max_Rating,
       MIN(Driver_Ratings) AS Min_Rating
FROM ola_rides
WHERE Vehicle_Type = 'Prime Sedan'
AND Booking_Status = 'Success';

-- Query 7: All rides where payment was made using UPI
SELECT Booking_ID, Customer_ID, Booking_Value, Payment_Method
FROM ola_rides
WHERE Payment_Method = 'UPI'
LIMIT 10;

-- Query 8: Average customer rating per vehicle type
SELECT Vehicle_Type, ROUND(AVG(Customer_Rating), 2) AS Avg_Customer_Rating
FROM ola_rides
WHERE Booking_Status = 'Success'
GROUP BY Vehicle_Type
ORDER BY Avg_Customer_Rating DESC;

-- Query 9: Total booking value of successful rides
SELECT SUM(Booking_Value) AS Total_Revenue
FROM ola_rides
WHERE Booking_Status = 'Success';

-- Query 10: All incomplete rides with reason
SELECT Booking_ID, Customer_ID, Vehicle_Type, 
       Incomplete_Rides_Reason
FROM ola_rides
WHERE Incomplete_Rides = 'Yes'
LIMIT 10;