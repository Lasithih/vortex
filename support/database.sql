CREATE DATABASE  IF NOT EXISTS `downloads` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `downloads`;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jobs` (
  `job_id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(1000) NOT NULL,
  `start_at_midnight` int(1) NOT NULL DEFAULT '1',
  `path` varchar(1000) NOT NULL DEFAULT '~/Downloads',
  `job_type` int(11) NOT NULL,
  `format` varchar(45) NOT NULL DEFAULT 'mp4',
  `status` int(1) NOT NULL DEFAULT '0',
  `comment` varchar(2000) DEFAULT NULL,
  `start_time` varchar(45) DEFAULT NULL,
  `end_time` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`job_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;