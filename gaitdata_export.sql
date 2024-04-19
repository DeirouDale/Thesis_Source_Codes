-- MariaDB dump 10.19  Distrib 10.11.6-MariaDB, for debian-linux-gnu (aarch64)
--
-- Host: localhost    Database: gaitdata
-- ------------------------------------------------------
-- Server version	10.11.6-MariaDB-0+deb12u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `assessment`
--

DROP TABLE IF EXISTS `assessment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assessment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` varchar(250) NOT NULL,
  `side` varchar(250) NOT NULL,
  `date_time` date DEFAULT NULL,
  `assessment_num` int(11) DEFAULT NULL,
  `phase` int(11) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `frame` int(11) DEFAULT NULL,
  `hips` varchar(250) DEFAULT NULL,
  `knees` varchar(250) DEFAULT NULL,
  `ankle` varchar(250) DEFAULT NULL,
  `insole` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `assessment_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `patient_details` (`client_id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assessment`
--

LOCK TABLES `assessment` WRITE;
/*!40000 ALTER TABLE `assessment` DISABLE KEYS */;
INSERT INTO `assessment` VALUES
(7,'2400001','Left','2024-04-17',1,2,'image1.jpg',1,'normal','normal','normal','101'),
(8,'2400002','Right','2024-04-17',1,2,'image2.jpg',1,'normal','normal','normal','111'),
(34,'2400001','Right','2024-04-18',1,2,'Database/2400001/2024-04-18/1/Right/19.jpg',19,'3.56°','0.82°','44.41°','000'),
(35,'2400001','Right','2024-04-18',1,3,'Database/2400001/2024-04-18/1/Right/20.jpg',20,'0.76°','0.62°','46.24°','000'),
(36,'2400001','Right','2024-04-18',1,3,'Database/2400001/2024-04-18/1/Right/22.jpg',22,'Unknown','Unknown','Unknown','Unknown'),
(37,'2400001','Left','2024-04-18',1,3,'Database/2400001/2024-04-18/1/Left/2.jpg',2,'4.06°','0.02°','41.3°','000'),
(38,'2400001','Left','2024-04-18',1,3,'Database/2400001/2024-04-18/1/Left/24.jpg',24,'5.49°','15.77°','45.04°','000'),
(39,'2400001','Left','2024-04-18',1,3,'Database/2400001/2024-04-18/1/Left/29.jpg',29,'0.47°','3.57°','63.55°','000'),
(40,'2400001','Left','2024-04-18',1,3,'Database/2400001/2024-04-18/1/Left/3.jpg',3,'3.99°','0.19°','39.36°','000'),
(41,'2400001','Left','2024-04-18',1,3,'Database/2400001/2024-04-18/1/Left/30.jpg',30,'2.02°','8.12°','69.55°','000'),
(42,'2400001','Left','2024-04-18',1,3,'Database/2400001/2024-04-18/1/Left/31.jpg',31,'7.04°','19.77°','66.57°','000'),
(43,'2400001','Left','2024-04-18',1,3,'Database/2400001/2024-04-18/1/Left/34.jpg',34,'3.81°','15.45°','64.5°','000'),
(44,'2400001','Left','2024-04-18',1,3,'Database/2400001/2024-04-18/1/Left/35.jpg',35,'2.52°','20.82°','35.5°','000'),
(45,'2400001','Left','2024-04-18',1,3,'Database/2400001/2024-04-18/1/Left/36.jpg',36,'5.02°','11.81°','52.27°','000'),
(46,'2400001','Left','2024-04-18',1,3,'Database/2400001/2024-04-18/1/Left/37.jpg',37,'5.35°','10.16°','51.36°','000'),
(47,'2400001','Left','2024-04-18',1,3,'Database/2400001/2024-04-18/1/Left/38.jpg',38,'6.97°','1.73°','53.52°','000'),
(48,'2400001','Left','2024-04-18',1,3,'Database/2400001/2024-04-18/1/Left/39.jpg',39,'7.29°','0.97°','51.03°','000'),
(49,'2400001','Left','2024-04-18',1,3,'Database/2400001/2024-04-18/1/Left/4.jpg',4,'3.96°','0.15°','39.88°','000'),
(50,'2400001','Left','2024-04-18',1,4,'Database/2400001/2024-04-18/1/Left/32.jpg',32,'0.57°','8.94°','73.35°','000'),
(51,'2400001','Left','2024-04-18',1,4,'Database/2400001/2024-04-18/1/Left/33.jpg',33,'3.73°','6.01°','70.03°','000'),
(52,'2400001','Right','2024-04-18',1,6,'Database/2400001/2024-04-18/1/Right/2.jpg',2,'2.71°','1.28°','44.33°','000'),
(53,'2400001','Right','2024-04-18',1,6,'Database/2400001/2024-04-18/1/Right/21.jpg',21,'0.51°','1.51°','42.68°','000'),
(54,'2400001','Right','2024-04-18',1,6,'Database/2400001/2024-04-18/1/Right/23.jpg',23,'3.17°','6.27°','53.67°','000'),
(55,'2400001','Left','2024-04-18',1,6,'Database/2400001/2024-04-18/1/Left/19.jpg',19,'2.66°','0.1°','42.38°','000'),
(56,'2400001','Left','2024-04-18',1,6,'Database/2400001/2024-04-18/1/Left/20.jpg',20,'2.6°','0.08°','43.21°','000'),
(57,'2400001','Left','2024-04-18',1,6,'Database/2400001/2024-04-18/1/Left/21.jpg',21,'2.6°','0.01°','41.13°','000'),
(58,'2400001','Left','2024-04-18',1,6,'Database/2400001/2024-04-18/1/Left/22.jpg',22,'2.54°','1.02°','44.3°','000'),
(59,'2400001','Left','2024-04-18',1,6,'Database/2400001/2024-04-18/1/Left/23.jpg',23,'1.65°','7.06°','55.56°','000'),
(60,'2400001','Left','2024-04-18',1,6,'Database/2400001/2024-04-18/1/Left/26.jpg',26,'10.28°','3.54°','63.57°','000'),
(61,'2400001','Left','2024-04-18',1,6,'Database/2400001/2024-04-18/1/Left/27.jpg',27,'7.24°','3.44°','58.46°','000'),
(62,'2400001','Left','2024-04-18',1,6,'Database/2400001/2024-04-18/1/Left/28.jpg',28,'6.0°','6.25°','57.94°','000'),
(63,'2400001','Left','2024-04-18',1,6,'Database/2400001/2024-04-18/1/Left/40.jpg',40,'6.31°','5.85°','53.76°','000'),
(64,'2400001','Left','2024-04-18',1,6,'Database/2400001/2024-04-18/1/Left/41.jpg',41,'5.47°','5.52°','49.84°','000'),
(65,'2400001','Left','2024-04-18',1,7,'Database/2400001/2024-04-18/1/Left/25.jpg',25,'8.19°','11.11°','45.13°','000'),
(66,'2400001','Right','2024-04-19',1,1,'Database/2400001/2024-04-19/1/Right/19.jpg',19,'8.48°','1.58°','71.62°','000'),
(67,'2400001','Right','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Right/2.jpg',2,'8.38°','2.1°','50.87°','000'),
(68,'2400001','Right','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Right/20.jpg',20,'7.93°','0.21°','55.42°','000'),
(69,'2400001','Right','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Right/21.jpg',21,'2.05°','2.23°','47.7°','000'),
(70,'2400001','Right','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Right/22.jpg',22,'3.66°','9.18°','51.7°','000'),
(71,'2400001','Right','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Right/23.jpg',23,'2.62°','3.56°','58.56°','000'),
(72,'2400001','Right','2024-04-19',1,3,'Database/2400001/2024-04-19/1/Right/24.jpg',24,'4.81°','1.1°','54.71°','000'),
(73,'2400001','Right','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Right/25.jpg',25,'5.57°','1.89°','60.72°','000'),
(74,'2400001','Right','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Right/26.jpg',26,'7.57°','3.77°','60.53°','000'),
(75,'2400001','Right','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Right/27.jpg',27,'11.33°','5.79°','61.8°','000'),
(76,'2400001','Right','2024-04-19',1,8,'Database/2400001/2024-04-19/1/Right/28.jpg',28,'12.18°','7.42°','58.38°','000'),
(77,'2400001','Right','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Right/29.jpg',29,'5.73°','46.45°','33.66°','unknown'),
(78,'2400001','Right','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Right/3.jpg',3,'8.54°','2.0°','49.88°','000'),
(79,'2400001','Right','2024-04-19',1,3,'Database/2400001/2024-04-19/1/Right/30.jpg',30,'17.36°','73.26°','45.86°','000'),
(80,'2400001','Right','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Right/31.jpg',31,'21.93°','85.71°','47.56°','000'),
(81,'2400001','Right','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Right/32.jpg',32,'73.53°','78.17°','52.75°','000'),
(82,'2400001','Right','2024-04-19',1,3,'Database/2400001/2024-04-19/1/Right/33.jpg',33,'43.83°','51.8°','30.81°','000'),
(83,'2400001','Right','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Right/34.jpg',34,'8.0°','9.38°','68.94°','000'),
(84,'2400001','Right','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Right/35.jpg',35,'3.03°','4.58°','64.8°','000'),
(85,'2400001','Right','2024-04-19',1,3,'Database/2400001/2024-04-19/1/Right/36.jpg',36,'3.78°','6.93°','62.15°','000'),
(86,'2400001','Right','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Right/37.jpg',37,'3.05°','5.09°','60.5°','000'),
(87,'2400001','Left','2024-04-19',1,4,'Database/2400001/2024-04-19/1/Left/20.jpg',20,'8.55°','3.32°','58.76°','000'),
(88,'2400001','Left','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Left/21.jpg',21,'10.68°','3.8°','57.3°','000'),
(89,'2400001','Left','2024-04-19',1,4,'Database/2400001/2024-04-19/1/Left/22.jpg',22,'15.23°','2.34°','59.99°','000'),
(90,'2400001','Left','2024-04-19',1,4,'Database/2400001/2024-04-19/1/Left/23.jpg',23,'15.31°','7.05°','57.16°','000'),
(91,'2400001','Left','2024-04-19',1,3,'Database/2400001/2024-04-19/1/Left/24.jpg',24,'4.87°','11.23°','45.98°','unknown'),
(92,'2400001','Left','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Left/25.jpg',25,'29.68°','76.84°','46.41°','000'),
(93,'2400001','Left','2024-04-19',1,6,'Database/2400001/2024-04-19/1/Left/26.jpg',26,'79.87°','111.31°','44.85°','000'),
(94,'2400001','Left','2024-04-19',1,3,'Database/2400001/2024-04-19/1/Left/27.jpg',27,'96.01°','107.11°','48.1°','000'),
(95,'2400001','Left','2024-04-19',1,3,'Database/2400001/2024-04-19/1/Left/28.jpg',28,'89.57°','101.89°','44.23°','unknown'),
(96,'2400001','Left','2024-04-19',1,3,'Database/2400001/2024-04-19/1/Left/29.jpg',29,'0.36°','10.14°','78.55°','000');
/*!40000 ALTER TABLE `assessment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_details`
--

DROP TABLE IF EXISTS `patient_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patient_details` (
  `client_id` varchar(250) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_details`
--

LOCK TABLES `patient_details` WRITE;
/*!40000 ALTER TABLE `patient_details` DISABLE KEYS */;
INSERT INTO `patient_details` VALUES
('2400001','Sha Boo'),
('2400002','Hakk Dog');
/*!40000 ALTER TABLE `patient_details` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-19 17:59:16
