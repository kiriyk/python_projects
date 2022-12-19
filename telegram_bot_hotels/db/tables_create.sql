CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	userid TEXT NOT NULL UNIQUE,
	username TEXT(120) NOT NULL,
	CONSTRAINT users_PK PRIMARY KEY (id)
);

-- Create foreign key request_FK

CREATE TABLE request (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id VARCHAR(255) NOT NULL,
	name TEXT NOT NULL,
	address TEXT NOT NULL,
	user_rating INTEGER NOT NULL,
	star INTEGER NOT NULL,
	distance_from_city_centre TEXT NOT NULL,
	check_in DATE NOT NULL,
	check_out DATE NOT NULL,
	price TEXT NOT NULL,
	total_price TEXT NOT NULL,
	photo TEXT NOT NULL,
	CONSTRAINT request_FK FOREIGN KEY (user_id) REFERENCES users(userid) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE shortrequest (
	id INTEGER NOT NULL,
	userid TEXT NOT NULL,
	requestdate REAL NOT NULL,
	hotelinfo TEXT NOT NULL,
	CONSTRAINT shortrequest_PK PRIMARY KEY (id),
	CONSTRAINT shortrequest_FK FOREIGN KEY (userid) REFERENCES users(id)
);