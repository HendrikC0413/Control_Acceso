-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: controlacceso
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `escuelas`
--

DROP TABLE IF EXISTS `escuelas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `escuelas` (
  `rbd` varchar(12) NOT NULL,
  `nombre_establecimiento` varchar(100) DEFAULT NULL,
  `activa` int DEFAULT '0',
  PRIMARY KEY (`rbd`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eventos`
--

DROP TABLE IF EXISTS `eventos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventos` (
  `idevento` int NOT NULL AUTO_INCREMENT,
  `idregistro` int NOT NULL,
  `tipo_evento` int NOT NULL,
  `hora` time NOT NULL,
  PRIMARY KEY (`idevento`),
  KEY `eventos_ibfk_1` (`idregistro`),
  CONSTRAINT `eventos_ibfk_1` FOREIGN KEY (`idregistro`) REFERENCES `registros_diarios` (`idregistro`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registros_diarios`
--

DROP TABLE IF EXISTS `registros_diarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registros_diarios` (
  `idregistro` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `idtarjeta` varchar(15) NOT NULL,
  PRIMARY KEY (`idregistro`),
  KEY `tarjeta_registro_idx` (`idtarjeta`),
  CONSTRAINT `tarjeta_registro` FOREIGN KEY (`idtarjeta`) REFERENCES `tarjeta` (`idtarjeta`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tarjeta`
--

DROP TABLE IF EXISTS `tarjeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tarjeta` (
  `idtarjeta` varchar(15) NOT NULL,
  `rbd` varchar(12) NOT NULL,
  `run` varchar(12) NOT NULL,
  PRIMARY KEY (`idtarjeta`),
  UNIQUE KEY `idtarjeta_UNIQUE` (`idtarjeta`),
  KEY `id_rbd_idx` (`rbd`),
  KEY `id_run_idx` (`run`),
  CONSTRAINT `id_rbd` FOREIGN KEY (`rbd`) REFERENCES `escuelas` (`rbd`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `id_run` FOREIGN KEY (`run`) REFERENCES `usuario` (`run`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_usuario`
--

DROP TABLE IF EXISTS `tipo_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_usuario` (
  `idtipo_usuario` int NOT NULL,
  `descripción_tipo` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idtipo_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `run` varchar(12) NOT NULL,
  `nombre` varchar(45) DEFAULT NULL,
  `apellido_1` varchar(45) DEFAULT NULL,
  `apellido_2` varchar(45) DEFAULT NULL,
  `id_tipo_usuario` int DEFAULT NULL,
  `disponible` int DEFAULT NULL,
  `clave` varchar(33) DEFAULT NULL,
  `huella` blob,
  PRIMARY KEY (`run`),
  KEY `tipo_usuario_idx` (`id_tipo_usuario`),
  CONSTRAINT `tipo_usuario` FOREIGN KEY (`id_tipo_usuario`) REFERENCES `tipo_usuario` (`idtipo_usuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `vista_tipo_usuario`
--

DROP TABLE IF EXISTS `vista_tipo_usuario`;
/*!50001 DROP VIEW IF EXISTS `vista_tipo_usuario`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_tipo_usuario` AS SELECT 
 1 AS `idtipo_usuario`,
 1 AS `descripción_tipo`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping routines for database 'controlacceso'
--
/*!50003 DROP PROCEDURE IF EXISTS `BuscarEscuelaPorRBD` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `BuscarEscuelaPorRBD`(
    IN rbd_param VARCHAR(12)
)
BEGIN
    -- Seleccionar el nombre del establecimiento donde el RBD coincida
    SELECT nombre_establecimiento
    FROM escuelas
    WHERE rbd = rbd_param AND activa = 0;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `EliminarUsuario` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `EliminarUsuario`(
    IN p_run VARCHAR(12)
)
BEGIN
    UPDATE usuario
    SET 
        disponible = 0
    WHERE 
        run = p_run;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `InsertarEscuela` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `InsertarEscuela`(
    IN p_rbd VARCHAR(12),
    IN p_nombre_establecimiento VARCHAR(100)
)
BEGIN
    -- Insertar los datos en la tabla escuelas
    INSERT INTO escuelas (rbd, nombre_establecimiento, activa)
    VALUES (p_rbd, p_nombre_establecimiento, 0);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insertar_empleados` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `insertar_empleados`(IN RUT varchar(12),IN NOMBRE VARCHAR(45), IN APE_1 VARCHAR (45),IN APE_2 VARCHAR (45), IN ID_TU INT,IN CLAVE VARCHAR(33),IN HUELLA BLOB)
BEGIN
   INSERT INTO `controlacceso`.`usuario`
(`run`,`nombre`,`apellido_1`,`apellido_2`,`id_tipo_usuario`,`disponible`,`clave`,`huella`) VALUES(RUT,NOMBRE, APE_1, APE_2, ID_TU, 1, CLAVE,HUELLA);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insertar_tarjeta` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `insertar_tarjeta`(IN IDTARJ varchar(15),IN RBD VARCHAR(12), IN RUN VARCHAR (12))
BEGIN
   INSERT INTO `controlacceso`.`tarjeta`
(`idtarjeta`,
`rbd`,
`run`)
VALUES
(IDTARJ,RBD,RUN);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `ModificarEscuela` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `ModificarEscuela`(
    IN p_opcion INT,
    IN p_rbd VARCHAR(12),
    IN p_nombre_establecimiento VARCHAR(100)
)
BEGIN
    -- Opción 1: Modificar solo el nombre del establecimiento cuando activa = 0
    IF p_opcion = 1 THEN
        UPDATE escuelas
        SET nombre_establecimiento = p_nombre_establecimiento
        WHERE rbd = p_rbd AND activa = 0;
    
    -- Opción 2: Modificar solo el campo activa (la deja en 1)
    ELSEIF p_opcion = 2 THEN
        UPDATE escuelas
        SET activa = 1
        WHERE rbd = p_rbd;
    
    -- Si la opción no es válida, no se realiza ninguna acción
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Opción no válida. Use 1 para modificar nombre o 2 para activar.';
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `ModificarUsuario` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `ModificarUsuario`(
    IN p_run VARCHAR(12),
    IN p_nombre VARCHAR(45),
    IN p_apellido_1 VARCHAR(45),
    IN p_apellido_2 VARCHAR(45),
    IN p_id_tipo_usuario INT,
    IN p_clave VARCHAR(33)
)
BEGIN
    UPDATE usuario
    SET 
        nombre = p_nombre,
        apellido_1 = p_apellido_1,
        apellido_2 = p_apellido_2,
        id_tipo_usuario = p_id_tipo_usuario,
        clave = p_clave
    WHERE run = p_run AND disponible = 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `obtener_asistencia_completa` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `obtener_asistencia_completa`(
    IN opcion INT,
    IN fecha_inicio DATE,
    IN fecha_fin DATE,
    IN mes INT,
    IN anio INT,
    IN rbd_param VARCHAR(10)
)
BEGIN
    IF opcion = 1 THEN
        -- Opción 1: Entre dos fechas distintas
        SELECT 
            d.run, d.nombre, d.apellido_1,
            COUNT(DISTINCT a.fecha) AS Dias_Asistidos,
            SUM(subquery.Dias_Completos) AS Dias_Completos
        FROM 
            registros_diarios AS a
            INNER JOIN tarjeta AS b ON a.idtarjeta = b.idtarjeta
            INNER JOIN escuelas AS c ON c.rbd = b.rbd
            INNER JOIN usuario AS d ON d.run = b.run
            INNER JOIN (
                SELECT a.idtarjeta, a.fecha, COUNT(e.idevento) AS eventos_por_dia,
                       CASE WHEN COUNT(e.idevento) = 4 THEN 1 ELSE 0 END AS Dias_Completos
                FROM registros_diarios AS a
                INNER JOIN eventos AS e ON a.idregistro = e.idregistro
                WHERE a.fecha BETWEEN fecha_inicio AND fecha_fin
                GROUP BY a.idtarjeta, a.fecha
            ) AS subquery ON a.idtarjeta = subquery.idtarjeta AND a.fecha = subquery.fecha
        WHERE 
            a.fecha BETWEEN fecha_inicio AND fecha_fin
            AND c.rbd = rbd_param
            AND d.disponible = 1
        GROUP BY 
            a.idtarjeta, d.run, d.nombre, d.apellido_1;
    ELSEIF opcion = 2 THEN
        -- Opción 2: Del mes enviado
        SELECT 
            d.run, d.nombre, d.apellido_1,
            COUNT(DISTINCT a.fecha) AS Dias_Asistidos,
            SUM(subquery.Dias_Completos) AS Dias_Completos
        FROM 
            registros_diarios AS a
            INNER JOIN tarjeta AS b ON a.idtarjeta = b.idtarjeta
            INNER JOIN escuelas AS c ON c.rbd = b.rbd
            INNER JOIN usuario AS d ON d.run = b.run
            INNER JOIN (
                SELECT a.idtarjeta, a.fecha, COUNT(e.idevento) AS eventos_por_dia,
                       CASE WHEN COUNT(e.idevento) = 4 THEN 1 ELSE 0 END AS Dias_Completos
                FROM registros_diarios AS a
                INNER JOIN eventos AS e ON a.idregistro = e.idregistro
                WHERE MONTH(a.fecha) = mes
                GROUP BY a.idtarjeta, a.fecha
            ) AS subquery ON a.idtarjeta = subquery.idtarjeta AND a.fecha = subquery.fecha
        WHERE 
            MONTH(a.fecha) = mes
            AND c.rbd = rbd_param
            AND d.disponible = 1
        GROUP BY 
            a.idtarjeta, d.run, d.nombre, d.apellido_1;
    ELSEIF opcion = 3 THEN
        -- Opción 3: Del año enviado
        SELECT 
            d.run, d.nombre, d.apellido_1,
            COUNT(DISTINCT a.fecha) AS Dias_Asistidos,
            SUM(subquery.Dias_Completos) AS Dias_Completos
        FROM 
            registros_diarios AS a
            INNER JOIN tarjeta AS b ON a.idtarjeta = b.idtarjeta
            INNER JOIN escuelas AS c ON c.rbd = b.rbd
            INNER JOIN usuario AS d ON d.run = b.run
            INNER JOIN (
                SELECT a.idtarjeta, a.fecha, COUNT(e.idevento) AS eventos_por_dia,
                       CASE WHEN COUNT(e.idevento) = 4 THEN 1 ELSE 0 END AS Dias_Completos
                FROM registros_diarios AS a
                INNER JOIN eventos AS e ON a.idregistro = e.idregistro
                WHERE YEAR(a.fecha) = anio
                GROUP BY a.idtarjeta, a.fecha
            ) AS subquery ON a.idtarjeta = subquery.idtarjeta AND a.fecha = subquery.fecha
        WHERE 
            YEAR(a.fecha) = anio
            AND c.rbd = rbd_param
            AND d.disponible = 1
        GROUP BY 
            a.idtarjeta, d.run, d.nombre, d.apellido_1;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `obtener_dato_por_run` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `obtener_dato_por_run`(
    IN run_param VARCHAR(12)
)
BEGIN
    SELECT clave
    FROM usuario
    WHERE run = run_param
    AND disponible = 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `obtener_eventos` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `obtener_eventos`(
    IN p_idtarjeta VARCHAR(15),
    IN p_fecha DATE,
    IN p_tipo_evento INT
)
BEGIN
    SELECT 
        rd.idregistro,
        e.hora AS Hora
    FROM 
        registros_diarios rd
    LEFT JOIN 
        (SELECT * FROM eventos WHERE tipo_evento = p_tipo_evento) e
    ON 
        rd.idregistro = e.idregistro
    WHERE 
        rd.idtarjeta = p_idtarjeta 
        AND rd.fecha = p_fecha;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `obtener_id_tarjeta` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `obtener_id_tarjeta`(
    IN run_param VARCHAR(12), -- Ajusta el tipo de dato según el tipo de la columna "run" en tu tabla
    IN rbd_param varchar(12)          -- Ajusta el tipo de dato según el tipo de la columna "rbd" en tu tabla
)
BEGIN
    -- Selecciona el idtarjeta correspondiente al run y rbd proporcionados
    SELECT idtarjeta 
    FROM tarjeta 
    WHERE run = run_param 
      AND rbd = rbd_param;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `obtener_reporte_individual` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `obtener_reporte_individual`(
    IN opcion INT,
    IN fecha_inicio DATE,
    IN fecha_fin DATE,
    IN mes INT,
    IN rbd_param VARCHAR(10),
    IN idtarjeta_param VARCHAR(15)
)
BEGIN
    IF opcion = 1 THEN
        -- Opción 1: Entre dos fechas distintas
        SELECT 
            d.run, c.rbd, a.fecha,
            MAX(CASE WHEN e.tipo_evento = 1 THEN e.hora END) AS Hora_entrada,
            MAX(CASE WHEN e.tipo_evento = 4 THEN e.hora END) AS Hora_salida,
            MAX(CASE WHEN e.tipo_evento = 2 THEN e.hora END) AS Hora_salida_colacion,
            MAX(CASE WHEN e.tipo_evento = 3 THEN e.hora END) AS Hora_entrada_colacion,
            CASE WHEN COUNT(e.idevento) = 4 THEN 'SI' ELSE 'NO' END AS Completo
        FROM 
            registros_diarios AS a
            INNER JOIN tarjeta AS b ON a.idtarjeta = b.idtarjeta
            INNER JOIN escuelas AS c ON c.rbd = b.rbd
            INNER JOIN usuario AS d ON d.run = b.run
            INNER JOIN eventos AS e ON a.idregistro = e.idregistro
        WHERE 
            a.fecha BETWEEN fecha_inicio AND fecha_fin 
            AND c.rbd = rbd_param
            AND a.idtarjeta = idtarjeta_param
            AND d.disponible = 1
        GROUP BY 
            d.run, c.rbd, a.fecha
        ORDER BY a.fecha;
        
    ELSEIF opcion = 2 THEN
        -- Opción 2: Del mes enviado
        SELECT 
            d.run, c.rbd, a.fecha,
            MAX(CASE WHEN e.tipo_evento = 1 THEN e.hora END) AS Hora_entrada,
            MAX(CASE WHEN e.tipo_evento = 4 THEN e.hora END) AS Hora_salida,
            MAX(CASE WHEN e.tipo_evento = 2 THEN e.hora END) AS Hora_salida_colacion,
            MAX(CASE WHEN e.tipo_evento = 3 THEN e.hora END) AS Hora_entrada_colacion,
            CASE WHEN COUNT(e.idevento) = 4 THEN 'SI' ELSE 'NO' END AS Completo
        FROM 
            registros_diarios AS a
            INNER JOIN tarjeta AS b ON a.idtarjeta = b.idtarjeta
            INNER JOIN escuelas AS c ON c.rbd = b.rbd
            INNER JOIN usuario AS d ON d.run = b.run
            INNER JOIN eventos AS e ON a.idregistro = e.idregistro
        WHERE 
            MONTH(a.fecha) = mes
            AND c.rbd = rbd_param
            AND a.idtarjeta = idtarjeta_param
            AND d.disponible = 1
        GROUP BY 
            d.run, c.rbd, a.fecha
        ORDER BY a.fecha;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `registrar_evento` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `registrar_evento`(
    IN fecha_param DATE,
    IN idtarjeta_param VARCHAR(15),
    IN tipo_evento_param INT,
    IN hora_param TIME
)
BEGIN
    DECLARE idregistro_param INT;
    DECLARE evento_existe INT;
    
    -- Buscar el registro en la tabla registros_diarios
    SELECT idregistro INTO idregistro_param
    FROM registros_diarios
    WHERE fecha = fecha_param AND idtarjeta = idtarjeta_param;
    
    -- Si no se encontró el registro, insertarlo
    IF idregistro_param IS NULL THEN
        INSERT INTO registros_diarios (fecha, idtarjeta)
        VALUES (fecha_param, idtarjeta_param);
        
        -- Obtener el idregistro del nuevo registro
        SELECT LAST_INSERT_ID() INTO idregistro_param;
    END IF;
    
    -- Comprobar si el evento ya existe para este idregistro
    SELECT COUNT(*) INTO evento_existe
    FROM eventos
    WHERE idregistro = idregistro_param AND tipo_evento = tipo_evento_param;
    
    -- Lanzar un error si el evento ya existe
    IF evento_existe > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El evento ya existe para este registro.';
    ELSE
        -- Insertar el evento en la tabla eventos
        INSERT INTO eventos (idregistro, tipo_evento, hora)
        VALUES (idregistro_param, tipo_evento_param, hora_param);
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `verificar_usuario` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `verificar_usuario`(
    IN run_param VARCHAR(12),
    IN clave_param VARCHAR(33)
)
BEGIN
    -- Seleccionar el id_tipo_usuario si el run y la clave coinciden
    SELECT id_tipo_usuario
    FROM usuario
    WHERE run = run_param
    AND clave = clave_param
    AND disponible = 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `VerUsuario` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `VerUsuario`(
    IN p_run VARCHAR(12)
)
BEGIN
    SELECT 
        nombre,
        apellido_1,
        apellido_2,
        id_tipo_usuario,
        clave
    FROM 
        usuario
    WHERE 
        run = p_run AND disponible = 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `vista_tipo_usuario`
--

/*!50001 DROP VIEW IF EXISTS `vista_tipo_usuario`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_tipo_usuario` AS select `tipo_usuario`.`idtipo_usuario` AS `idtipo_usuario`,`tipo_usuario`.`descripción_tipo` AS `descripción_tipo` from `tipo_usuario` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-11 22:26:37
