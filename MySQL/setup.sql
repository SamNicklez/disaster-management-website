CREATE TABLE Role (
  role_id INT PRIMARY KEY,
  role_name VARCHAR(50)
);

CREATE TABLE User (
  user_id INT PRIMARY KEY,
  user_name VARCHAR(255),
  email VARCHAR(255),
  phonenumber INT,
  password BINARY,
  role_id INT,
  is_verified BOOL,
  state VARCHAR(255),
  city VARCHAR(255),
  address VARCHAR(255),
  zipcode INT,
  latitude DECIMAL(8,6),
  longitude DECIMAL(9,6),
  FOREIGN KEY (role_id) REFERENCES Role(role_id)
);

CREATE TABLE Event (
  event_id INT PRIMARY KEY,
  event_name VARCHAR(255),
  location VARCHAR(255),
  latitude DECIMAL(8,6),
  longitude DECIMAL(9,6),
  start_date DATE,
  end_date DATE,
  description TEXT
);

CREATE TABLE Item (
  item_id INT PRIMARY KEY,
  name VARCHAR(255),
  category VARCHAR(255),
  description TEXT
);

CREATE TABLE EventItem (
  event_item_id INT PRIMARY KEY,
  event_id INT,
  item_id INT,
  FOREIGN KEY (event_id) REFERENCES Event(event_id),
  FOREIGN KEY (item_id) REFERENCES Item(item_id)
);

CREATE TABLE Request (
  request_id INT PRIMARY KEY,
  event_id INT,
  user_id INT,
  is_fulfilled BOOL,
  created_date DATETIME,
  modified_date DATETIME,
  FOREIGN KEY (event_id) REFERENCES Event(event_id),
  FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE RequestItem (
  request_item_id INT PRIMARY KEY,
  request_id INT,
  event_item_id INT,
  quantity INT,
  shipping_number VARCHAR(255),
  FOREIGN KEY (request_id) REFERENCES Request(request_id),
  FOREIGN KEY (event_item_id) REFERENCES EventItem(event_item_id)
);

CREATE TABLE Response (
  response_id INT PRIMARY KEY,
  request_id INT,
  user_id INT,
  is_fulfilled BOOL,
  created_date DATETIME,
  shipped_date DATETIME,
  FOREIGN KEY (request_id) REFERENCES Request(request_id),
  FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE Pledge (
  pledge_id INT PRIMARY KEY,
  user_id INT,
  item_id INT,
  quantity_given INT,
  quantity_remaining INT,
  is_fulfilled BOOL,
  FOREIGN KEY (user_id) REFERENCES User(user_id),
  FOREIGN KEY (item_id) REFERENCES Item(item_id)
);

CREATE TABLE Notification (
  notification_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  message TEXT,
  title TEXT,
  is_dismissed BOOL,
  created_date DATETIME,
  FOREIGN KEY (user_id) REFERENCES User(user_id)
);