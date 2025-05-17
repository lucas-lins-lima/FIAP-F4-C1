
CREATE TABLE climate_data (
	id VARCHAR2(36 CHAR) NOT NULL, 
	timestamp DATE NOT NULL, 
	temperature FLOAT NOT NULL, 
	air_humidity FLOAT NOT NULL, 
	rain_forecast SMALLINT NOT NULL, 
	PRIMARY KEY (id)
)

;


CREATE TABLE producers (
	id VARCHAR2(36 CHAR) NOT NULL, 
	name VARCHAR2(200 CHAR) NOT NULL, 
	email VARCHAR2(200 CHAR) NOT NULL, 
	phone VARCHAR2(30 CHAR) NOT NULL, 
	PRIMARY KEY (id)
)

;


CREATE TABLE crops (
	id VARCHAR2(36 CHAR) NOT NULL, 
	name VARCHAR2(100 CHAR) NOT NULL, 
	type VARCHAR2(50 CHAR) NOT NULL, 
	start_date DATE NOT NULL, 
	end_date DATE, 
	producer_id VARCHAR2(36 CHAR) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(producer_id) REFERENCES producers (id) ON DELETE CASCADE
)

;


CREATE TABLE applications (
	id VARCHAR2(36 CHAR) NOT NULL, 
	crop_id VARCHAR2(36 CHAR) NOT NULL, 
	timestamp DATE NOT NULL, 
	type VARCHAR2(50 CHAR) NOT NULL, 
	quantity FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(crop_id) REFERENCES crops (id) ON DELETE CASCADE
)

;


CREATE TABLE components (
	id VARCHAR2(36 CHAR) NOT NULL, 
	name VARCHAR2(50 CHAR) NOT NULL, 
	type VARCHAR2(30 CHAR) NOT NULL, 
	crop_id VARCHAR2(36 CHAR), 
	PRIMARY KEY (id), 
	FOREIGN KEY(crop_id) REFERENCES crops (id) ON DELETE CASCADE
)

;


CREATE TABLE sensor_records (
	id VARCHAR2(36 CHAR) NOT NULL, 
	sensor_id VARCHAR2(36 CHAR) NOT NULL, 
	timestamp DATE NOT NULL, 
	soil_moisture FLOAT NOT NULL, 
	phosphorus_present SMALLINT NOT NULL, 
	potassium_present SMALLINT NOT NULL, 
	soil_ph FLOAT NOT NULL, 
	irrigation_status VARCHAR2(10 CHAR) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(sensor_id) REFERENCES components (id) ON DELETE CASCADE
)

;

