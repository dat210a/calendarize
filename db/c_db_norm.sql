CREATE DATABASE  IF NOT EXISTS `calendarize_db` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `calendarize_db`;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: calendarize_db
-- ------------------------------------------------------
-- Server version	5.7.20-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_date_created` datetime NOT NULL,
  `user_email` varchar(45) NOT NULL,
  `user_password` varchar(80) NOT NULL,
  `user_name` varchar(45) DEFAULT NULL,
  `user_type` int DEFAULT NULL,
  `user_phone` int DEFAULT NULL,
  `user_record` varchar(45) DEFAULT NULL,
  `user_extra` varchar(45) DEFAULT NULL,
  `verify_key` varchar(15) DEFAULT NULL,    
  `resetkey` varchar(80) DEFAULT NULL,  
  `expires` datetime DEFAULT NULL,  
  `active` tinyint(1) NOT NULL DEFAULT '0',
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `calendars`
--

DROP TABLE IF EXISTS `calendars`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `calendars` (
  `calendar_id` int NOT NULL AUTO_INCREMENT,
  `calendar_owner` int NOT NULL,
  `calendar_date_created` datetime NOT NULL,
  `calendar_name` varchar(45) NOT NULL,
  `calendar_color` varchar(6) DEFAULT NULL,
  `calendar_details` varchar(45) DEFAULT NULL,
  `calendar_extra` varchar(45) DEFAULT NULL,
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`calendar_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calendars`
--

LOCK TABLES `calendars` WRITE;
/*!40000 ALTER TABLE `calendars` DISABLE KEYS */;
/*!40000 ALTER TABLE `calendars` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `events` (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `event_calendar_id` int NOT NULL,  
  `event_date_created` datetime NOT NULL,
  `event_owner` int NOT NULL,
  `event_name` varchar(45) NOT NULL,
  `event_start` datetime NOT NULL,
  `event_end` datetime NOT NULL,
  `event_recurring` tinyint(1) NOT NULL DEFAULT '0',
  `event_location` varchar(45) DEFAULT NULL,
  `event_details` varchar(1000) DEFAULT NULL,
  `event_extra` varchar(45) DEFAULT NULL,
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_children`
--

DROP TABLE IF EXISTS `event_children`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_children` (
  `child_id` int NOT NULL AUTO_INCREMENT,
  `child_parent_id` int NOT NULL, 
  `child_date_created` datetime NOT NULL,
  `child_owner` int NOT NULL,
  `child_year` int NOT NULL,  
  `child_start` datetime DEFAULT NULL,
  `child_end` datetime DEFAULT NULL,
  `child_location` varchar(45) DEFAULT NULL,
  `child_details` varchar(1000) DEFAULT NULL,
  `child_extra` varchar(45) DEFAULT NULL,
  `skip_year` tinyint(1) NOT NULL DEFAULT '0',
  `deleted` tinyint(1) NOT NULL DEFAULT '0',  
  PRIMARY KEY (`child_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_children`
--

LOCK TABLES `event_children` WRITE;
/*!40000 ALTER TABLE `event_children` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_children` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_calendars`
--

DROP TABLE IF EXISTS `user_calendars`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_calendars` (
  `user_id` int NOT NULL,
  `calendar_id` int NOT NULL,
  `role` int NOT NULL,
  `unique_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`unique_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_calendars`
--

LOCK TABLES `user_calendars` WRITE;
/*!40000 ALTER TABLE `user_calendars` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_calendars` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `calendar_invites`
--

DROP TABLE IF EXISTS `calendar_invites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE IF NOT EXISTS `calendar_invites` (
  `unique_id` INT NOT NULL,
  `calendar_id` INT NOT NULL,
  `invited_user_id` INT NOT NULL,
  `sender_user_id` INT NOT NULL,
  `role` INT NOT NULL DEFAULT '0',
  PRIMARY KEY (`unique_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_calendars`
--

LOCK TABLES `calendar_invites` WRITE;
/*!40000 ALTER TABLE `calendar_invites` DISABLE KEYS */;
/*!40000 ALTER TABLE `calendar_invites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_friends`
--

DROP TABLE IF EXISTS `user_friends`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_friends` (
  `user_id` int NOT NULL,
  `friend_id` int NOT NULL,
  `unique_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`unique_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_friends`
--

LOCK TABLES `user_friends` WRITE;
/*!40000 ALTER TABLE `user_friends` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_friends` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_files`
--

DROP TABLE IF EXISTS `event_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_files` (
  `event_id` int NOT NULL,
  `file_name` varchar(160) NOT NULL,
  `unique_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`unique_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_files`
--

LOCK TABLES `event_files` WRITE;
/*!40000 ALTER TABLE `event_files` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_files` ENABLE KEYS */;
UNLOCK TABLES;



/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-30 10:06:23
