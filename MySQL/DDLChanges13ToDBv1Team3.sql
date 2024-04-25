-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: theapp
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `CategoryId` int NOT NULL AUTO_INCREMENT,
  `CategoryName` varchar(45) NOT NULL,
  `isActive` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`CategoryId`),
  UNIQUE KEY `CategoryName_UNIQUE` (`CategoryName`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Medicine',1),(2,'Fruits',1),(3,'Canned Food',1),(4,'Dry Rations',1),(5,'Water and Beverages',1);
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `event_name` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`event_id`),
  FULLTEXT KEY `Event_Search` (`event_name`),
  FULLTEXT KEY `Location_Search` (`location`),
  FULLTEXT KEY `Description Search` (`description`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (11,'Test Event','Test Location',123.456,789.012,'2024-03-15','2024-03-20','This is a test event'),(12,'Test Event','Test Location',123.456,789.012,'2024-03-15','2024-03-20','This is a test event'),(13,'Tornado','Oklahoma City, OK',123.456,789.012,'2024-03-12',NULL,'A category 5 hurricane has struck New Orleans, LA. The city is in need of food, water, and medical supplies.'),(14,'Hurricane','New Orleans, LA',123.456,789.012,'2021-10-10',NULL,'A category 5 hurricane has struck New Orleans, LA. The city is in need of food, water, and medical supplies.'),(15,'Earthquake','Iowa City, IA',123.456,789.012,'2021-10-10',NULL,'A 7.0 magnitude earthquake has struck Iowa City, IA. The city is in need of food, water, and medical supplies.'),(16,'Earthquake','Texas City, Texas',29.396,-94.9175,'2024-03-28',NULL,'Test Earthquake to see if items work'),(17,'Test Event','Iowa City, Iowa',41.6613,-91.5299,'2024-03-31',NULL,'This is a test event for sprint 2'),(18,'This is a test','Iowa City, Iowa',41.6613,-91.5299,'2024-03-31',NULL,'test description');
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventitem`
--

DROP TABLE IF EXISTS `eventitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventitem` (
  `event_item_id` int NOT NULL AUTO_INCREMENT,
  `event_id` int NOT NULL,
  `item_id` int NOT NULL,
  `isActive` int DEFAULT '1',
  PRIMARY KEY (`event_item_id`),
  KEY `eventitem_ibfk_1_idx` (`event_id`),
  KEY `eventitem_ibfk_2_idx` (`item_id`),
  CONSTRAINT `eventitem_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`),
  CONSTRAINT `eventitem_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`ItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventitem`
--

LOCK TABLES `eventitem` WRITE;
/*!40000 ALTER TABLE `eventitem` DISABLE KEYS */;
INSERT INTO `eventitem` VALUES (10,11,101,1),(11,11,102,1),(12,11,103,1),(13,12,101,1),(14,12,102,1),(15,12,103,1),(24,16,101,1),(25,16,102,1),(26,16,105,1),(27,17,101,1),(28,17,105,1),(29,17,103,1),(30,18,101,1),(31,18,103,1),(32,18,105,1);
/*!40000 ALTER TABLE `eventitem` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `item`;


--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `items` (
  `ItemID` int NOT NULL AUTO_INCREMENT,
  `ItemName` varchar(45) NOT NULL,
  `CategoryId` int NOT NULL,
  `ItemDescription` text,
  `isActive` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`ItemID`),
  UNIQUE KEY `ItemName_UNIQUE` (`ItemName`),
  KEY `CategoryId_idx` (`CategoryId`),
  CONSTRAINT `CategoryId` FOREIGN KEY (`CategoryId`) REFERENCES `category` (`CategoryId`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (101,'Apple',2,'Apple is a Fruit',1),(102,'Biscuits',4,'Ideally in small packs distributable to individuals',1),(103,'Water-500ml',5,'Water in 500ml bottles',1),(104,'Ibf-50',1,'',1),(105,'Canned Beef',3,'',1);
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notification` (
  `notification_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `message` text,
  `is_dismissed` tinyint(1) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `title` text,
  PRIMARY KEY (`notification_id`),
  KEY `notification_ibfk_1_idx` (`user_id`),
  CONSTRAINT `notification_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pledge`
--

DROP TABLE IF EXISTS `pledge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pledge` (
  `pledge_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `item_id` int DEFAULT NULL,
  `quantity_given` int DEFAULT NULL,
  `quantity_remaining` int DEFAULT NULL,
  `is_fulfilled` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`pledge_id`),
  KEY `pledge_ibfk_1_idx` (`user_id`),
  KEY `pledge_ibfk_2_idx` (`item_id`),
  CONSTRAINT `pledge_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`UserId`),
  CONSTRAINT `pledge_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`ItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pledge`
--

LOCK TABLES `pledge` WRITE;
/*!40000 ALTER TABLE `pledge` DISABLE KEYS */;
INSERT INTO `pledge` VALUES (1,1,102,100,100,0);
/*!40000 ALTER TABLE `pledge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `event_id` int NOT NULL,
  `user_id` int NOT NULL,
  `event_item_id` int NOT NULL,
  `quantity_requested` int DEFAULT NULL,
  `quantity_remaining` int DEFAULT NULL,
  `is_fulfilled` tinyint(1) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `modified_date` datetime DEFAULT NULL,
  PRIMARY KEY (`request_id`),
  KEY `request_ibfk_2_idx` (`user_id`),
  KEY `request_ibfk_1` (`event_id`),
  CONSTRAINT `request_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`),
  CONSTRAINT `request_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`UserId`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request`
--

LOCK TABLES `request` WRITE;
/*!40000 ALTER TABLE `request` DISABLE KEYS */;
INSERT INTO `request` VALUES (1,16,1,25,15,0,1,'2024-03-28 14:05:54',NULL),(2,16,1,24,15,0,1,'2024-03-28 14:09:30',NULL),(3,16,1,26,15,0,1,'2024-03-29 08:52:33',NULL),(4,16,1,25,890,0,1,'2024-03-29 08:52:57',NULL),(5,16,1,25,789,0,1,'2024-03-29 08:54:17',NULL),(6,16,1,24,15,0,1,'2024-03-29 10:28:48',NULL),(7,18,1,30,25,25,0,'2024-03-31 15:33:28',NULL);
/*!40000 ALTER TABLE `request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `requestitem`
--

DROP TABLE IF EXISTS `requestitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `requestitem` (
  `request_item_id` int NOT NULL,
  `request_id` int DEFAULT NULL,
  `event_item_id` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `shipping_number` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`request_item_id`),
  KEY `request_id` (`request_id`),
  KEY `event_item_id` (`event_item_id`),
  CONSTRAINT `requestitem_ibfk_1` FOREIGN KEY (`request_id`) REFERENCES `request` (`request_id`),
  CONSTRAINT `requestitem_ibfk_2` FOREIGN KEY (`event_item_id`) REFERENCES `eventitem` (`event_item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `requestitem`
--

LOCK TABLES `requestitem` WRITE;
/*!40000 ALTER TABLE `requestitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `requestitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `response`
--

DROP TABLE IF EXISTS `response`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `response` (
  `response_id` int NOT NULL AUTO_INCREMENT,
  `request_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `is_fulfilled` tinyint(1) DEFAULT NULL,
  `quantity_donated` int DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `shipped_date` datetime DEFAULT NULL,
  PRIMARY KEY (`response_id`),
  KEY `response_ibfk_2_idx` (`user_id`),
  CONSTRAINT `response_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`UserId`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `response`
--

LOCK TABLES `response` WRITE;
/*!40000 ALTER TABLE `response` DISABLE KEYS */;
INSERT INTO `response` VALUES (1,1,1,0,15,'2024-03-28 14:41:13',NULL),(2,2,1,0,15,'2024-03-29 08:50:30',NULL),(3,3,1,0,15,'2024-03-29 08:52:37',NULL),(4,4,1,0,890,'2024-03-29 08:52:59',NULL),(5,5,1,0,789,'2024-03-29 08:56:30',NULL),(6,6,1,0,15,'2024-03-31 15:33:04',NULL),(7,6,1,0,0,'2024-03-31 15:33:04',NULL);
/*!40000 ALTER TABLE `response` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `role_id` int NOT NULL,
  `role_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `RoleID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  PRIMARY KEY (`RoleID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Admin'),(2,'Donor'),(3,'Recipient');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phonenumber` int DEFAULT NULL,
  `password` binary(1) DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  `is_verified` tinyint(1) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `zipcode` int DEFAULT NULL,
  `latitude` decimal(8,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `UserId` int NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  `Email` varchar(45) NOT NULL,
  `Password` char(255) NOT NULL,
  `PhoneNumber` int DEFAULT NULL,
  `RoleID` int NOT NULL,
  `IsVerified` int NOT NULL,
  `State` varchar(16) DEFAULT NULL,
  `City` varchar(45) DEFAULT NULL,
  `Address` varchar(45) DEFAULT NULL,
  `Latitude` decimal(8,6) DEFAULT NULL,
  `Longitude` decimal(9,6) DEFAULT NULL,
  `ZipCode` int DEFAULT NULL,
  `verify_code` int DEFAULT NULL,
  PRIMARY KEY (`UserId`),
  UNIQUE KEY `Email_UNIQUE` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,NULL,NULL,'samuelnicklaus1@gmail.com','scrypt:32768:8:1$M4OVKxEihK5R0XqS$c98dc50da19fd1c0273f39ebf5b67c9622df18cfabcaf21e330d95860b327858e26094d68497521a123f04d0d084a198442d209ba85a43a01c207768a47af90a',NULL,1,1,'Iowa','Iowa City','229 South Dubuque Street',41.658192,-91.533464,52240,NULL),(2,NULL,NULL,'snicklaus@uiowa.edu','scrypt:32768:8:1$K95GO4dcZVHJuork$408d3fca22d84e3391d650fcd0120f804b8ed573c2f3ce7fc4c111b64471c44b194357900e725fbae84301a3581293e7b6db331ed4ef6f1d8f007086983965f4',NULL,2,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,NULL,NULL,'udithaj7@gmail.com','scrypt:32768:8:1$DFksqltv5RNNkRG9$edde554550a6d773811947251945cf050f1a2a332dcc45f3535f5e34959f595ea41b89b269cd8740b29e2496722b1457a89db40705d26379c8b835fe047f80ec',NULL,1,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,NULL,NULL,'spenholman@uiowa.edu','scrypt:32768:8:1$IxZmK0StCgOuO3mQ$58c5433538c911a4082b753f05914895e001f972cbdd16285f0318a0337cc1621d924e6906e71a88f2294805c0060817371177f3e0677dc52b5562739a7f3da6',NULL,1,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'theapp'
--
/*!50003 DROP PROCEDURE IF EXISTS `GetAllCategories` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetAllCategories`()
BEGIN
    SELECT * FROM category
    WHERE isActive = 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetAllEvents` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetAllEvents`()
BEGIN
	SELECT * FROM event WHERE end_date is NULL;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetEventByID` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetEventByID`(IN EventID INT)
BEGIN
    SELECT e.*, GROUP_CONCAT(i.ItemName) AS allowed_items
    FROM event e
    LEFT JOIN eventitem ei ON e.event_id = ei.event_id
    LEFT JOIN items i ON ei.item_id = i.ItemID
    WHERE e.event_id = EventID
    GROUP BY e.event_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetItemsByCategory` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetItemsByCategory`(IN category_id INT)
BEGIN
    SELECT * FROM items WHERE CategoryId = category_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetRequestsByEventID` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetRequestsByEventID`(IN EventID INT)
BEGIN
SELECT 
  e.event_id, 
  e.event_name, 
  e.location, 
  e.start_date, 
  e.description,
  (SELECT JSON_ARRAYAGG(
      JSON_OBJECT(
        'request_id', r.request_id,
        'quantity_requested', r.quantity_requested,
        'quantity_remaining', r.quantity_remaining,
        'is_fulfilled', r.is_fulfilled,
        'created_date', r.created_date,
        'item_name', i.ItemName
      )
   )
   FROM request r
   JOIN eventitem ei ON r.event_item_id = ei.event_item_id AND r.event_id = ei.event_id
   JOIN items i ON ei.item_id = i.ItemID
   WHERE r.event_id = e.event_id
  ) AS requests
FROM event e
WHERE e.event_id = EventID
AND e.end_date is NULL;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetResponsesByEventID` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetResponsesByEventID`(IN event_id_param INT)
BEGIN
    SELECT 
        r.response_id,
        r.request_id,
        r.user_id,
        r.is_fulfilled,
        r.created_date,
        r.shipped_date,
        JSON_ARRAYAGG(JSON_OBJECT(
            'response_item_id', ri.response_item_id,
            'item_id', ri.item_id,
            'quantity', ri.quantity
        )) AS response_items
    FROM 
        response r
    INNER JOIN 
        request dr ON r.request_id = dr.request_id
    LEFT JOIN 
        responseitem ri ON r.response_id = ri.response_id
    WHERE 
        dr.event_id = event_id_param
    GROUP BY 
        r.response_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetResponsesByRequestId` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetResponsesByRequestId`(IN req_id INT)
BEGIN
    SELECT 
        r.response_id,
        r.user_id,
        r.is_fulfilled,
        r.created_date,
        r.shipped_date,
        JSON_ARRAYAGG(
            JSON_OBJECT(
                'quantity', ri.quantity,
                'ItemName', i.ItemName
            )
        ) AS items
    FROM 
        response r
        INNER JOIN responseitem ri ON r.response_id = ri.response_id
        INNER JOIN items i ON ri.item_id = i.ItemID
    WHERE 
        r.request_id = req_id
    GROUP BY 
        r.response_id, r.user_id, r.is_fulfilled, r.created_date, r.shipped_date;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetResponsesByRequestIdJSON` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetResponsesByRequestIdJSON`(IN req_id INT)
BEGIN
    SELECT 
        r.response_id,
        r.user_id,
        r.is_fulfilled,
        r.created_date,
        r.shipped_date,
        JSON_ARRAYAGG(
            JSON_OBJECT(
                'quantity', ri.quantity,
                'ItemName', i.ItemName
            )
        ) AS items
    FROM 
        response r
        INNER JOIN responseitem ri ON r.response_id = ri.response_id
        INNER JOIN items i ON ri.item_id = i.ItemID
    WHERE 
        r.request_id = req_id
    GROUP BY 
        r.response_id, r.user_id, r.is_fulfilled, r.created_date, r.shipped_date;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetValidEventItems` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetValidEventItems`( eventId INT)
BEGIN
	SELECT i.ItemID AS item_id,
           i.ItemName AS item_name,
           c.CategoryName AS category,
           i.ItemDescription AS description
    FROM eventitem ei
    INNER JOIN items i ON ei.item_id = i.ItemID
    INNER JOIN category c ON i.CategoryId = c.CategoryId
    WHERE ei.event_id = eventId;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-22 15:14:34
