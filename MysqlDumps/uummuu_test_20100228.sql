-- MySQL dump 10.11
--
-- Host: localhost    Database: uummuu_test
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
INSERT INTO `sites_domains` VALUES (1,'http://localhost:8080/',0);
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
INSERT INTO `sites_htmlsite` VALUES (-1,'none','none','none','2009-09-19 18:46:02',1,'2009-09-19 18:46:02',-1);
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
-- Table structure for table `sites_new_urls`
--

DROP TABLE IF EXISTS `sites_new_urls`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `sites_new_urls` (
  `url` varchar(255) NOT NULL,
  UNIQUE KEY `url` (`url`),
  KEY `url_2` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `sites_new_urls`
--

LOCK TABLES `sites_new_urls` WRITE;
/*!40000 ALTER TABLE `sites_new_urls` DISABLE KEYS */;
/*!40000 ALTER TABLE `sites_new_urls` ENABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `sites_queries`
--

LOCK TABLES `sites_queries` WRITE;
/*!40000 ALTER TABLE `sites_queries` DISABLE KEYS */;
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
INSERT INTO `sites_sitequeue` VALUES (-1,'none',1,'none','2009-09-19 18:46:02','2009-09-19 18:46:02',200),(1,'http://localhost:8080/LiRa/',0,'http://localhost:8080/','2009-09-19 18:46:02','2009-09-19 18:46:02',200);
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

-- Dump completed on 2010-02-28  5:00:00
