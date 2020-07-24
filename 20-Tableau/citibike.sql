CREATE TABLE tripdata (
	tripduration      		INTEGER,
	starttime         		TIMESTAMP, 
	stoptime          		TIMESTAMP, 
	startstationid    		INTEGER,
    startstationname  		VARCHAR(100), 
	startstationlatitude    NUMERIC(12, 8),
	startstationlongitude	NUMERIC(12, 8),
    endstationid            INTEGER,
	endstationname          VARCHAR(100),
	endstationlatitude      NUMERIC(12, 8),
	endstationlongitude     NUMERIC(12, 8),
	bikeid                  INTEGER,
	usertype                VARCHAR(25),
	birthyear               INTEGER,
	gender                  VARCHAR(10)
);

SELECT * FROM tripdata
ORDER BY tripduration DESC
LIMIT 100;

-- Find out how many rows in this table --
SELECT COUNT (*) FROM tripdata;

-- Each day's number of trip and total trip duration --
COPY (
	SELECT date(starttime), COUNT(tripduration), SUM(tripduration) FROM tripdata
	GROUP BY date(starttime)
	)
TO 'C:\Temp\total_trip_duration.csv'
DELIMITER ','
CSV HEADER;


-- YTD --
COPY (
	SELECT * FROM tripdata
	WHERE date(starttime) > '2019-12-31'
	)
TO 'C:\Temp\YTD_data.csv'
DELIMITER ','
CSV HEADER;