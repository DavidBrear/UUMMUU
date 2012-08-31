-- MySQL dump 10.11
--
-- Host: localhost    Database: uummuu_production
-- ------------------------------------------------------
-- Server version	5.0.51b-community-nt

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL auto_increment,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `auth_message_user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_650f49a6` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add message',1,'add_message'),(2,'Can change message',1,'change_message'),(3,'Can delete message',1,'delete_message'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add permission',4,'add_permission'),(11,'Can change permission',4,'change_permission'),(12,'Can delete permission',4,'delete_permission'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add html site',7,'add_htmlsite'),(20,'Can change html site',7,'change_htmlsite'),(21,'Can delete html site',7,'delete_htmlsite'),(22,'Can add queries',8,'add_queries'),(23,'Can change queries',8,'change_queries'),(24,'Can delete queries',8,'delete_queries'),(25,'Can add site',9,'add_site'),(26,'Can change site',9,'change_site'),(27,'Can delete site',9,'delete_site'),(28,'Can add site queue',10,'add_sitequeue'),(29,'Can change site queue',10,'change_sitequeue'),(30,'Can delete site queue',10,'delete_sitequeue'),(31,'Can add log entry',11,'add_logentry'),(32,'Can change log entry',11,'change_logentry'),(33,'Can delete log entry',11,'delete_logentry');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL auto_increment,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'drumma5','','','david.brear.04@cnu.edu','sha1$95248$0ea793770ce6ec6e6df36643018c29f3be3a0490',1,1,1,'2008-06-20 10:33:46','2008-06-20 10:33:46');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL auto_increment,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) default NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `django_admin_log_user_id` (`user_id`),
  KEY `django_admin_log_content_type_id` (`content_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'message','auth','message'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'permission','auth','permission'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'html site','sites','htmlsite'),(8,'queries','sites','queries'),(9,'site','sites','site'),(10,'site queue','sites','sitequeue'),(11,'log entry','admin','logentry');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY  (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('07fe2d2566dd25d3acabcc51307156bd','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kDHAwDGQKUKIVScQRz\nLjQyMDA0NWJjZjFmNDZiYTI2NTYzYzk1OTZjOTNkZWU5\n','2009-04-11 12:03:25'),('0ac5712f3a5723f12ac8780b552788c5','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhQCLAehIIVScQRz\nLmYzNGQ2ZTcyY2Q1MjgzOGExYzY1N2E5ODk0MDk3OTE2\n','2009-11-09 20:02:44'),('0b4e8aa8f345e6a25a20ba6c7ef8b84c','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kFCBQbBgk7SIVScQRz\nLmQ5OGUxNDRhMTcwNjcxODNmYTIyYjBlZGY2MTdiOGIy\n','2009-05-22 20:27:07'),('16647cadd760ead112755a670b2e86e1','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kFGRIRJgwlYIVScQRz\nLmZiNDgxZDU0YjM4MTFlMzA1MTQyNTBkNDVlNTE0ODBk\n','2009-06-08 18:17:38'),('1e18f74ee0f0cdcfbce9464a506b9f05','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGxYJAQKjyIVScQRz\nLjFmZTJjZTQyZWYxZTY1NDA1YTgzMjgzYWFjNDU0Y2U0\n','2009-11-10 22:09:01'),('1e6e791ada7adf7e409675af1fee5ad3','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kFGA8kBwckIIVScQRz\nLmE5NzBjY2MzNmVjZjQzMDI0NmNjMjQzN2IyZWJhNjYz\n','2009-06-07 15:36:07'),('2062f420642d540e75a436d0cd24b267','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhYDGwckIIVScQRz\nLjBjNjg1NTQ0ZjBmMjY0ZjQxNWZjZDUzMzhiOThmYTg2\n','2009-11-09 22:03:27'),('22fde72ccfc1e58cfc768ba27f849d96','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhQEMwTCwIVScQRz\nLjYyYTAzYzQ0YzJkYzVkZjU2ZjZmY2UzMDM4OTY1OTQx\n','2009-11-09 20:04:51'),('23f4aea165a28c3d7e7bd3903a3a1ffb','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhM4CgdioIVScQRz\nLjQ1OGQ5ZWZlMzZiOTY1NDFiOGI2ZjBlYmQ2ODgxYzA5\n','2009-11-09 19:56:11'),('2ce453ccebe2e666a584290285adb53b','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGxYEJAt1mIVScQRz\nLjllNjdiNWQ5YTUxMzAwNWY2MGUxYmU1ZGRhYTZhYzMy\n','2009-11-10 22:04:38'),('31c26e9119792835564b622605f11bda','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhQYLA1Z+IVScQRz\nLmUxNGNiYzY4YWExZWU0OTk4M2VlYjlhY2Y5NjEwYWYx\n','2009-11-09 20:24:44'),('31d3e335f1487338e1dbd4a847c59d2a','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhUHFAJhYIVScQRz\nLmNmZjNhYjk2Y2QxOTMyZTNjNDYyOTA4ZDI0MDZmZjI0\n','2009-11-09 21:07:20'),('33c43214a9fe5ad0ab937785a3217de3','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhQXJwnEAIVScQRz\nLmIwYTY2ODIwNjcyZjU3NzVjN2VmN2YwZmY3ODkzZjE0\n','2009-11-09 20:23:39'),('35b97e5ac1c6c16eb0a1428e53a62eb7','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kDGxcqNQIqsIVScQRz\nLjQyN2Y3ZmU1OTQzMjA5NGQ4ZGM5ZjVjNTJhMjVjMjEw\n','2009-04-10 23:42:53'),('369971d0d6bc0d42a14685dda2c2392b','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kFGRIRGgr0sIVScQRz\nLmZlOGI4MjcyNTI3NzgzMjA1MmJjYjk0YjJkNzVkNGE5\n','2009-06-08 18:17:27'),('3aa988a7f210f95a2b18e80297236577','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKFhIqBAUYsIVScQRz\nLjUzZDJjMzNjMjNjNjdiNTYyM2YwZWZjZTBhNjZlMDg3\n','2009-11-05 18:42:04'),('3f19c4f801d604bb45ce31a86f225978','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKFBYiBQdmiIVScQRz\nLmRlZGMwYTEzMGM2NzIxNzE0OWUyZjJlZmZmNTdmMGJl\n','2009-11-03 22:34:05'),('420fed0263f525a9557c4290e914b1b6','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kFFwIqGQeRgIVScQRz\nLjU0MzlkNGVmMmY1YzRmZWM1M2M2YjU3OTdmNTM5M2E1\n','2009-06-06 02:42:25'),('4729a5ba2fc81427a26797635064d44f','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kFHg8NAwyiYIVScQRz\nLjFmMmY1ZDgyNzAyYWZkMjZmNzg4MDY0N2EyMmEwMjcw\n','2009-06-13 15:13:04'),('477f90b44248d56e18675eb9d654e6e0','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhQHAgRJqIVScQRz\nLjdlNTM1NzViNzAwM2Q1ZDcwOWU5YWYwMGZjYmE2NzNi\n','2009-11-09 20:07:02'),('47c054da289bd212f92dc1e77e85c170','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKHwwTIgb1QIVScQRz\nLmViZmVhZjM0OGUwNGFlOTFlZGVmZDdiMTU4NGYyMTRm\n','2009-11-14 12:19:34'),('4a960c5ee1ca5952907d00a5cc54d6f3','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kFFwIjBQyWqIVScQRz\nLjQ5MWJjZTczZTBlZTE2YzczNmJkOWU2Mjk2MzcyYTYy\n','2009-06-06 02:35:06'),('4b1cf92d448e48c2c553caa6be8f093a','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhQxKAB5GIVScQRz\nLjQwNTkwMjQ0NGEwMTIyMzViOGQxYTZhYWM3N2I3OTFi\n','2009-11-09 20:49:40'),('4d225764d7e563096eda6c1ecf459082','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kEBA0xJAP7iIVScQRz\nLjk2NjljYzk3Y2I3NDRjZjExMjE4ZTE1YjQ1NThjNGRi\n','2009-04-18 13:49:36'),('4fcb6b3febe45187ff5b894571181dd3','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGxcPDAKjyIVScQRz\nLjkxZGE2NmNhM2Y2NzVlYTA3N2JjNjcwYWRhOWZiN2Yy\n','2009-11-10 23:15:12'),('515a355b7c6428fa21f36204b6b62e8a','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGxYwIggiCIVScQRz\nLjYyNzY4MzY4Mzg1MjkyZmY2ZGY0MzI0NjMxZWQ2OGFm\n','2009-11-10 22:48:34'),('54d394cdb80f42a336a1801fecb7233b','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kLERICDg2UkIVScQRz\nLjliMDQ4ZWI5MWQyNzQzMGZlYWYzMzAwMWI0N2M1NGFm\n','2009-12-01 18:02:14'),('5a12e05de527a5f32d8add5618f2a692','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhQDLA0beIVScQRz\nLjZjYzMxMDdkMmVkMzFmY2NhMTBlYmUyZjcxZjVhMTIz\n','2009-11-09 20:03:44'),('6810aed894112863626be8f02b84327d','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhQ0OwoCgIVScQRz\nLmViOTgzMzVjOTM1OTRkOWE2NDFhMzZiYzJkZTkzYTQ5\n','2009-11-09 20:52:59'),('6b10c6206875aacd60d7922489f681de','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhQRHgA6mIVScQRz\nLjlmYmU2OTRlMTI1YTc0NzcyOWY3OTA5ZDc5YzNiNzJk\n','2009-11-09 20:17:30'),('6d91287e3535f6b20a8e946546bcd0d1','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kIHxQVHguBUIVScQRz\nLjk2NzdhZmQxM2UxM2UwNjE2ODg2OTkyMTQ2ZDg1ODQx\n','2009-09-14 20:21:30'),('7007049e1a58313652d27a73bbbc8811','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhYfIAehIIVScQRz\nLjljNmU3ZmUxZWUwOTAyMzNhMjExNTNkZDViYzA5MmY0\n','2009-11-09 22:31:32'),('715c804b56de9df497ae490e4ce45d75','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhYpJwZsiIVScQRz\nLjUxMWJhMjZjN2Y3Mzg5MzliYzBlY2E3OTVmZjkyMTA2\n','2009-11-09 22:41:39'),('722ac2505aa77df145dd689410ae0f75','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGxYNJwC7gIVScQRz\nLjZlZmZkZDczYTgzNGRiNGVmY2Q0MmE4YzM3YzBkMzM2\n','2009-11-10 22:13:39'),('75964ce9cda838d8e484d725debf44b9','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGxcDIQD6AIVScQRz\nLjk0MjkzYjRjNjYyN2UwNTFlMWE1Y2YwYjcwZmI5YmMx\n','2009-11-10 23:03:33'),('78738144e3892f6229e79e0c2631a4ba','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kJDQIADA7sUIVScQRz\nLmFkYWZmZjRkYjIyOWJhOGExOTg0MmQyYThmZWQ4ODhl\n','2009-09-27 02:00:13'),('7bd5fc974d8f004b730a180368fbb18f','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGxYUCgNbYIVScQRz\nLjQ1ZTdiMjc4YTZmMjhlMjZkZTk5Y2RlYTQwNTE2ZTRh\n','2009-11-10 22:20:10'),('7dfcdfa6cb517e45ae44d64a44c7efe6','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kEHhUTHwdHSIVScQRz\nLjI1OTNlMDUxNTM3OGUwMDk2ZGYxMTUyNzBhNWE3ODZi\n','2009-05-14 21:19:31'),('81dc3205781f41a18f7835907169d37f','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kJBhYEOwKYEIVScQRz\nLjBhNWUwNjRlY2YxMmUxZTljZjJkMjA1NDc3MGVmMmFi\n','2009-09-20 22:04:59'),('8330985d82034af2e7288de3820398da','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhQJOQlK6IVScQRz\nLjJkMzczNGU3OTQxYTFiZTFlNjE0NDc3NDYyYjYzYjk3\n','2009-11-09 20:09:57'),('8b379bf9c81b86b77c1410503442671e','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhYlJgo9GIVScQRz\nLjEzZmY5ZDE0ZWE5ZDc5ZGJiOWQ2ZGY0NjQwOTNiYzgz\n','2009-11-09 22:37:38'),('8e1776720357d2f5bddef5eb83cdb131','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kDDxYZJAV6WIVScQRz\nLjZhMThkYzVhYWZjZDQ3ZGZlZTc1MWRkYTAwMDY4OGJm\n','2009-03-29 22:25:36'),('a1baa8094953dc5a7695e86b6463c3df','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhUFAQp7mIVScQRz\nLjlhMWZhMzk0NzRlNmI0MDk4NDA0ZmZkNjNmNmIyZDU2\n','2009-11-09 21:05:01'),('a7fd3aae12ed896b8f99edbaf355d10c','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kMEBUDFwPr6IVScQRz\nLjY1NjEwYTk4OGM1OGI5YWM1MWVhYzQwOTE5YjUwYjlh\n','2009-12-30 21:03:23'),('a987eb4eae717d8f8d31c7d31f0864d6','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGxYKMQpE6IVScQRz\nLmZiM2JiOWM0MWU5YzljNTI3ZWFiZDUzZjEwMjlhNjAz\n','2009-11-10 22:10:49'),('bc2104317042c265ff1bdf0c8838f170','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kMHw4qLwNTkIVScQRz\nLmQ3NDQzZWM5YjllMTZlNWE2MTU4YjNlOWJiOGZlMzhk\n','2010-01-14 14:42:48'),('bd6640f9c9a765596873c9998ad391f3','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kEDxcfOwfrWIVScQRz\nLjZkYzczN2YzYWU3MmEyMmJhYjViODY1NzJlMzVlMjRi\n','2009-04-29 23:31:59'),('c1510ea0581f25f472ce5d54d2285902','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kJBgIlEwi2eIVScQRz\nLmI3ZDI4MzU4ZmE4NjY0MWE0MjMyMDlkMDU2NjQ5YTE4\n','2009-09-20 02:37:19'),('cbb1399b7695a2d95d7987cbd3c547cb','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhQGAgDyMIVScQRz\nLmYwNWFkOTNmNmY2MzYwNmI5ODRmMDQyNmIyNjg2OTIw\n','2009-11-09 20:06:02'),('cd3e23dcc546aaa1f6bf4f11ecfdc7ea','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGxcMHgwtMIVScQRz\nLmUzYWE0ZmI0MGNlZGZjMDM2ZGEyNmYzNWY0OWMxYzMz\n','2009-11-10 23:12:30'),('d35e938ca2f2175c2711559f6f917296','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhQPBAwlYIVScQRz\nLjdlZjlkY2E4YzhmNGJjMDZhMzhlY2VlMmQ0MjlmZWI4\n','2009-11-09 20:15:04'),('d5d486e7cd5cf21120a74c54e50de96a','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhM7KQyiYIVScQRz\nLmJiYTBlMmNhNjFhNDYwZjg5NzgzODA5MmM5N2NjMmZh\n','2009-11-09 19:59:41'),('db72b57cbba957422f8d69661bf162d8','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kIAhMQAgrwyIVScQRz\nLjk0MzgwOGY3Mzg1ZjEzMWVlMjVhMzZmYjUzMDYxZTNm\n','2009-08-16 19:16:02'),('dd5bfd082282fbeaa6a27ad64c96d2be','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kFEhQIOgfbuIVScQRz\nLjY5Y2VlNGMyN2RiZWFiYzI2ZmUwZjI5ZmRkNmYwZjIz\n','2009-06-01 20:08:59'),('dfc2b4e05f2a0cac52991f0a44cb0504','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGxYyAAcr8IVScQRz\nLjkxYTcxYTEyZDc1YjYxZGM1YzdkNzdmODQxNTdjMDQy\n','2009-11-10 22:50:00'),('e3c6050927ecba7efedf468377cf337a','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kLEBcoNwV6WIVScQRz\nLmY3MDdhZWM1ODZlOTFkZTZkMjdjNTAzOWU4NGUyYjRk\n','2009-11-30 23:40:55'),('f1af2bbb08ab462dd890c3728f4019d4','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kKGhUCIQU72IVScQRz\nLmNkMDI3OGJjY2ZhN2JjOTBiNjBjZDk1YTRkZDA1YTIw\n','2009-11-09 21:02:33'),('f47532834bbb08ced94e0dbe676b54d1','gAJ9cQFVCmluaXRDb29raWVxAmNkYXRldGltZQpkYXRldGltZQpxA1UKB9kHChYaMAszMIVScQRz\nLjBlYWZiZjljZDNlOGRiOTJiNjNhZWYxZWE0NmFlOGQx\n','2009-07-24 22:26:49');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL auto_increment,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sites_domains`
--

DROP TABLE IF EXISTS `sites_domains`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `sites_domains` (
  `id` int(11) NOT NULL auto_increment,
  `url` varchar(300) NOT NULL,
  `pages_crawled` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `url` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `sites_domains`
--

LOCK TABLES `sites_domains` WRITE;
/*!40000 ALTER TABLE `sites_domains` DISABLE KEYS */;
INSERT INTO `sites_domains` VALUES (1,'http://localhost:8080/smallerStyleTest.html',0);
/*!40000 ALTER TABLE `sites_domains` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sites_htmlsite`
--

DROP TABLE IF EXISTS `sites_htmlsite`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `sites_htmlsite` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(300) NOT NULL,
  `description` longtext NOT NULL,
  `information` longtext NOT NULL,
  `updated` datetime NOT NULL,
  `indexed` tinyint(1) NOT NULL,
  `last_indexed` datetime NOT NULL,
  `sitequeue_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `sites_htmlsite_sitequeue_id` (`sitequeue_id`),
  CONSTRAINT `sitequeue_id_refs_id_5d000748` FOREIGN KEY (`sitequeue_id`) REFERENCES `sites_sitequeue` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `sites_htmlsite`
--

LOCK TABLES `sites_htmlsite` WRITE;
/*!40000 ALTER TABLE `sites_htmlsite` DISABLE KEYS */;
INSERT INTO `sites_htmlsite` VALUES (-1,'none','none','none','2009-03-18 23:17:11',1,'2009-03-18 23:17:11',-1);
/*!40000 ALTER TABLE `sites_htmlsite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sites_index`
--

DROP TABLE IF EXISTS `sites_index`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `sites_index` (
  `id` int(11) NOT NULL auto_increment,
  `word` varchar(125) NOT NULL,
  `invert_list` longtext NOT NULL,
  `freq` int(11) NOT NULL,
  `length` int(11) NOT NULL,
  `num_docs` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `word` (`word`),
  UNIQUE KEY `word_2` (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `sites_index`
--

LOCK TABLES `sites_index` WRITE;
/*!40000 ALTER TABLE `sites_index` DISABLE KEYS */;
/*!40000 ALTER TABLE `sites_index` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sites_lira`
--

DROP TABLE IF EXISTS `sites_lira`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `sites_lira` (
  `id` int(11) NOT NULL auto_increment,
  `link_list` longtext NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `sites_lira`
--

LOCK TABLES `sites_lira` WRITE;
/*!40000 ALTER TABLE `sites_lira` DISABLE KEYS */;
/*!40000 ALTER TABLE `sites_lira` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sites_lira_transposed`
--

DROP TABLE IF EXISTS `sites_lira_transposed`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `sites_lira_transposed` (
  `id` int(11) NOT NULL auto_increment,
  `inlinks` text NOT NULL,
  `rank` float(10,8) NOT NULL,
  `htmlsite_id` int(11) NOT NULL,
  `curr_vect` float(10,8) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `sites_lira_transposed_htmlsite_id` (`htmlsite_id`),
  CONSTRAINT `htmlsite_id_refs_id_4310f1c` FOREIGN KEY (`htmlsite_id`) REFERENCES `sites_htmlsite` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `sites_lira_transposed`
--

LOCK TABLES `sites_lira_transposed` WRITE;
/*!40000 ALTER TABLE `sites_lira_transposed` DISABLE KEYS */;
/*!40000 ALTER TABLE `sites_lira_transposed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sites_queries`
--

DROP TABLE IF EXISTS `sites_queries`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `sites_queries` (
  `id` int(11) NOT NULL auto_increment,
  `phrase` varchar(150) NOT NULL,
  `sessionID` varchar(100) default NULL,
  `date_queried` datetime NOT NULL,
  `IPAddress` char(15) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `sites_queries`
--

LOCK TABLES `sites_queries` WRITE;
/*!40000 ALTER TABLE `sites_queries` DISABLE KEYS */;
INSERT INTO `sites_queries` VALUES (1,'david','8a73ea930fbfad99b5de8f7498677f19','2009-03-15 22:25:39','127.0.0.1'),(2,'lkjasdlfkjasdf','900e3c80dc89a94bbcd586e229c37838','2009-05-08 20:27:11','127.0.0.1'),(3,'something','b2218d8106c4931a4906c2ae220dd871','2009-05-23 02:35:13','127.0.0.1'),(4,'lkja;lskfj','d47bb8511925cfca92231cda0b5af74b','2009-05-24 15:36:12','127.0.0.1'),(5,';ljka;lskdjf;laksdfj;','2432ff00e18707ec5ed3d9f764a6cfdc','2009-05-25 18:17:46','127.0.0.1'),(6,'fadsf','fd0c0bf161050a294ed6584f87d8b57e','2009-09-13 02:00:36','127.0.0.1'),(7,'something','4cb1ccb8baf267cf3ccf30b1eb6a8616','2009-11-17 18:02:07','127.0.0.1');
/*!40000 ALTER TABLE `sites_queries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sites_sitequeue`
--

DROP TABLE IF EXISTS `sites_sitequeue`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `sites_sitequeue` (
  `id` int(11) NOT NULL auto_increment,
  `url` varchar(716) NOT NULL,
  `crawled` tinyint(1) NOT NULL,
  `domain` varchar(300) NOT NULL,
  `date_submitted` datetime NOT NULL,
  `last_crawl` datetime NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `url` (`url`),
  UNIQUE KEY `url_2` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `sites_sitequeue`
--

LOCK TABLES `sites_sitequeue` WRITE;
/*!40000 ALTER TABLE `sites_sitequeue` DISABLE KEYS */;
INSERT INTO `sites_sitequeue` VALUES (-1,'none',1,'none','2009-03-18 23:17:11','2009-03-18 23:17:11',200),(1,'http://localhost:8080/smallerStyleTest.html',0,'http://localhost:8080/smallerStyleTest.html','2009-03-18 23:17:11','2009-03-18 23:17:11',200);
/*!40000 ALTER TABLE `sites_sitequeue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sites_worddoc`
--

DROP TABLE IF EXISTS `sites_worddoc`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `sites_worddoc` (
  `id` int(11) NOT NULL auto_increment,
  `doc_id` int(10) unsigned NOT NULL,
  `occurrence` int(11) NOT NULL,
  `weight` int(11) NOT NULL,
  `in_title` smallint(6) NOT NULL,
  `word` varchar(125) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `sites_worddoc`
--

LOCK TABLES `sites_worddoc` WRITE;
/*!40000 ALTER TABLE `sites_worddoc` DISABLE KEYS */;
/*!40000 ALTER TABLE `sites_worddoc` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-01-05  5:00:02
