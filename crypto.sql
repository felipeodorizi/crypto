
CREATE DATABASE `crypto1`;

use crypto1;

CREATE TABLE `yf_crypto` (
  `idyf_crypto` int NOT NULL AUTO_INCREMENT,
  `ticker` text,
  `date` date DEFAULT NULL,
  `close` double DEFAULT NULL,
  `adjclose` double DEFAULT NULL,
  `volume` bigint DEFAULT NULL,
  `is_last` int DEFAULT NULL,
  PRIMARY KEY (`idyf_crypto`)
) ENGINE=InnoDB AUTO_INCREMENT=2691 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
