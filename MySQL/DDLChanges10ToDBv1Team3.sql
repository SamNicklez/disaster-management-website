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
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (11,'Test Event','Test Location',123.456,789.012,'2024-03-15','2024-03-20','This is a test event'),(12,'Test Event','Test Location',123.456,789.012,'2024-03-15','2024-03-20','This is a test event'),(13,'Tornado','Oklahoma City, OK',123.456,789.012,'2024-03-12',NULL,'A category 5 hurricane has struck New Orleans, LA. The city is in need of food, water, and medical supplies.'),(14,'Hurricane','New Orleans, LA',123.456,789.012,'2021-10-10',NULL,'A category 5 hurricane has struck New Orleans, LA. The city is in need of food, water, and medical supplies.'),(15,'Earthquake','Iowa City, IA',123.456,789.012,'2021-10-10',NULL,'A 7.0 magnitude earthquake has struck Iowa City, IA. The city is in need of food, water, and medical supplies.'),(16,'Earthquake','Texas City, Texas',29.396,-94.9175,'2024-03-28',NULL,'Test Earthquake to see if items work');
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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventitem`
--

LOCK TABLES `eventitem` WRITE;
/*!40000 ALTER TABLE `eventitem` DISABLE KEYS */;
INSERT INTO `eventitem` VALUES (10,11,101,1),(11,11,102,1),(12,11,103,1),(13,12,101,1),(14,12,102,1),(15,12,103,1),(24,16,101,1),(25,16,102,1),(26,16,105,1);
/*!40000 ALTER TABLE `eventitem` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pledge`
--

LOCK TABLES `pledge` WRITE;
/*!40000 ALTER TABLE `pledge` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request`
--

LOCK TABLES `request` WRITE;
/*!40000 ALTER TABLE `request` DISABLE KEYS */;
INSERT INTO `request` VALUES (1,16,1,25,15,0,1,'2024-03-28 14:05:54',NULL),(2,16,1,24,15,15,0,'2024-03-28 14:09:30',NULL);
/*!40000 ALTER TABLE `request` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `response`
--

LOCK TABLES `response` WRITE;
/*!40000 ALTER TABLE `response` DISABLE KEYS */;
INSERT INTO `response` VALUES (1,1,1,0,15,'2024-03-28 14:41:13',NULL);
/*!40000 ALTER TABLE `response` ENABLE KEYS */;
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
  PRIMARY KEY (`UserId`),
  UNIQUE KEY `Email_UNIQUE` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,NULL,NULL,'samuelnicklaus1@gmail.com','scrypt:32768:8:1$NEFTCfa9wYMpH9dA$cc187448ce7a22b5c048c12379bd5cf7ddace70bec942950c10178b5f08e28c3ca07120e1262a1cf01b22ca5f7fe317685c48168b812ffa362fd090423685f78',NULL,1,1,'Iowa','Iowa City','229 South Dubuque Street Apt 204',NULL,NULL,52240),(2,NULL,NULL,'snicklaus@uiowa.edu','scrypt:32768:8:1$K95GO4dcZVHJuork$408d3fca22d84e3391d650fcd0120f804b8ed573c2f3ce7fc4c111b64471c44b194357900e725fbae84301a3581293e7b6db331ed4ef6f1d8f007086983965f4',NULL,2,1,NULL,NULL,NULL,NULL,NULL,NULL),(3,NULL,NULL,'udithaj7@gmail.com','scrypt:32768:8:1$DFksqltv5RNNkRG9$edde554550a6d773811947251945cf050f1a2a332dcc45f3535f5e34959f595ea41b89b269cd8740b29e2496722b1457a89db40705d26379c8b835fe047f80ec',NULL,1,1,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-28 14:42:21
