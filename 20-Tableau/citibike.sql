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
WHERE bikeid = '39852'
LIMIT 100;