-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 17, 2018 at 06:19 AM
-- Server version: 5.7.14
-- PHP Version: 5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `incubator`
--

-- --------------------------------------------------------

--
-- Table structure for table `antibiotics`
--

CREATE TABLE `antibiotics` (
  `abx_id` int(50) NOT NULL,
  `abx_name` varchar(100) DEFAULT NULL,
  `abx_content` varchar(20) DEFAULT NULL,
  `abx_code` varchar(20) DEFAULT NULL,
  `sus` int(3) DEFAULT NULL,
  `res` int(3) DEFAULT NULL,
  `abx_descriptor` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `antibiotics`
--

INSERT INTO `antibiotics` (`abx_id`, `abx_name`, `abx_content`, `abx_code`, `sus`, `res`, `abx_descriptor`) VALUES
(7, 'Trimeth-Sulfamethox', '1.25/23.75ug', 'TS25', 14, 11, ''),
(8, 'Erythromycin', '15ug', 'E15', 21, 18, 'assets/antibiotics/Erythromycin.pkl'),
(9, 'Penicillin G', '1ug', 'PG1', 26, 26, 'assets/antibiotics/Penicillin G.pkl'),
(10, 'Gentamicin', '10ug', 'GM10', 17, 14, 'assets/antibiotics/Gentamicin.pkl'),
(11, 'Clindamycin', '2ug', 'CD2', 22, 19, 'assets/antibiotics/Clindamycin.pkl'),
(12, 'Fusidic Acid', '10ug', 'CF10', 24, 24, 'assets/antibiotics/Fusidic Acid.pkl'),
(13, 'Ceftriaxone', '30ug', 'CRO30', 19, 19, 'assets/antibiotics/Ceftriaxone.pkl'),
(14, 'Piperacillin(Tazobactam)', '75-10ug', 'PTZ85C', 0, 0, ''),
(15, 'Cefoxitin', '10ug', 'FOX10', 0, 0, 'assets/antibiotics/Cefoxitin.pkl'),
(16, 'Ceftazidime', '30ug', 'CAZ30', 0, 0, 'assets/antibiotics/Ceftazidime.pkl');

-- --------------------------------------------------------

--
-- Table structure for table `bacteria`
--

CREATE TABLE `bacteria` (
  `bacteria_id` int(50) NOT NULL,
  `bacteria_name` varchar(100) DEFAULT NULL,
  `timelimit` int(3) DEFAULT '24'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `bacteria`
--

INSERT INTO `bacteria` (`bacteria_id`, `bacteria_name`, `timelimit`) VALUES
(1, 'Acetobacter aurantius', 24),
(2, 'Acinetobacter baumannii', 24),
(3, 'Anaplasma', 24),
(4, 'Bartonella', 24),
(5, 'Bordetella', 24),
(6, 'Bartonella henselae', 24),
(7, 'Azotobacter vinelandii', 24),
(8, 'Anaplasma phagocytophilum', 24),
(10, 'Brucella', 24),
(11, 'Bacillus subtilis', 24),
(12, 'Bordetella bronchiseptica', 24),
(13, 'Bordetella pertussis', 24),
(14, 'Borrelia burgdorfer', 24),
(15, 'Brucella abortus ', 24),
(16, 'Burkholderia  ', 24),
(18, 'Anaplasma Cannon', 24),
(19, 'Acetobacter aurantius_1', 24),
(20, 'Staphlococci Aureus', 24),
(21, 'Escherichia Coli', 24);

-- --------------------------------------------------------

--
-- Table structure for table `discs`
--

CREATE TABLE `discs` (
  `disc_id` int(50) NOT NULL,
  `abx_id` int(50) DEFAULT NULL,
  `diameter` int(3) DEFAULT NULL,
  `dish_id` int(50) DEFAULT NULL,
  `sample_id` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `discs`
--

INSERT INTO `discs` (`disc_id`, `abx_id`, `diameter`, `dish_id`, `sample_id`) VALUES
(29, 15, 30, 1, 6),
(30, 16, 14, 1, 6),
(31, 13, 6, 1, 6),
(32, 11, 19, 1, 6),
(33, 8, 24, 1, 6),
(34, 12, 15, 1, 6),
(35, 9, 6, 1, 6),
(36, 15, 21, 1, 7),
(37, 16, 15, 1, 7),
(38, 13, 7, 1, 7),
(39, 11, 16, 1, 7),
(40, 8, 11, 1, 7),
(41, 12, 0, 1, 7),
(42, 9, 0, 1, 7);

-- --------------------------------------------------------

--
-- Table structure for table `eucast`
--

CREATE TABLE `eucast` (
  `interpetation_id` int(50) NOT NULL,
  `abx_id` int(50) DEFAULT NULL,
  `bacteria_id` int(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `flags`
--

CREATE TABLE `flags` (
  `disc_id` int(50) DEFAULT NULL,
  `colonies` tinyint(1) DEFAULT NULL,
  `double_innoc` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `images`
--

CREATE TABLE `images` (
  `image_id` int(50) NOT NULL,
  `sample_id` int(50) DEFAULT NULL,
  `imagelocation` varchar(200) DEFAULT NULL,
  `state` tinyint(1) NOT NULL DEFAULT '0',
  `img_date` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `images`
--

INSERT INTO `images` (`image_id`, `sample_id`, `imagelocation`, `state`, `img_date`) VALUES
(1, 6, 'assets/img/zonesfound6.png', 3, '2018-08-15 18:55:03'),
(2, 7, 'assets/img/zonesfound7.png', 3, '2018-08-15 21:04:44');

-- --------------------------------------------------------

--
-- Table structure for table `petri_dish`
--

CREATE TABLE `petri_dish` (
  `petri_dishID` int(100) NOT NULL,
  `dish_id` int(50) NOT NULL,
  `state` tinyint(1) DEFAULT '1',
  `sample_id` int(50) NOT NULL,
  `startTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `endTime` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `petri_dish`
--

INSERT INTO `petri_dish` (`petri_dishID`, `dish_id`, `state`, `sample_id`, `startTime`, `endTime`) VALUES
(5, 1, 1, 6, '2018-08-16 01:28:58', '2018-08-17 06:28:58'),
(6, 2, 3, 7, '2018-08-16 03:50:26', '2018-08-16 03:50:26');

-- --------------------------------------------------------

--
-- Table structure for table `pocket_state`
--

CREATE TABLE `pocket_state` (
  `pocket_id` int(1) NOT NULL,
  `state` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pocket_state`
--

INSERT INTO `pocket_state` (`pocket_id`, `state`) VALUES
(1, 0),
(2, 1),
(3, 1),
(4, 1);

-- --------------------------------------------------------

--
-- Table structure for table `samples`
--

CREATE TABLE `samples` (
  `sample_id` int(50) NOT NULL,
  `accession_number` varchar(50) DEFAULT NULL,
  `bacteria_id` int(50) DEFAULT NULL,
  `patient_id` int(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `samples`
--

INSERT INTO `samples` (`sample_id`, `accession_number`, `bacteria_id`, `patient_id`) VALUES
(6, '98769870', 7, NULL),
(7, '67858545', 11, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `zones`
--

CREATE TABLE `zones` (
  `discId` int(200) NOT NULL,
  `disc` varchar(20) DEFAULT NULL,
  `sample_id` int(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `zones`
--

INSERT INTO `zones` (`discId`, `disc`, `sample_id`) VALUES
(16, '(1122, 1957)', 6),
(17, '(1800, 1880)', 6),
(18, '(470, 1552)', 6),
(19, '(1271, 1262)', 6),
(20, '(2056, 1091)', 6),
(21, '(598, 746)', 6),
(22, '(1413, 531)', 6),
(23, '(1122, 1957)', 7),
(24, '(1800, 1880)', 7),
(25, '(470, 1552)', 7),
(26, '(1271, 1262)', 7),
(27, '(2056, 1091)', 7),
(28, '(598, 746)', 7),
(29, '(1413, 531)', 7);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `antibiotics`
--
ALTER TABLE `antibiotics`
  ADD PRIMARY KEY (`abx_id`);

--
-- Indexes for table `bacteria`
--
ALTER TABLE `bacteria`
  ADD PRIMARY KEY (`bacteria_id`),
  ADD UNIQUE KEY `bacteria_name` (`bacteria_name`),
  ADD UNIQUE KEY `bacteria_name_2` (`bacteria_name`);

--
-- Indexes for table `discs`
--
ALTER TABLE `discs`
  ADD PRIMARY KEY (`disc_id`),
  ADD KEY `dish_id` (`dish_id`),
  ADD KEY `abx_id` (`abx_id`),
  ADD KEY `sample_id` (`sample_id`);

--
-- Indexes for table `eucast`
--
ALTER TABLE `eucast`
  ADD PRIMARY KEY (`interpetation_id`),
  ADD KEY `abx_id` (`abx_id`),
  ADD KEY `bacteria_id` (`bacteria_id`);

--
-- Indexes for table `flags`
--
ALTER TABLE `flags`
  ADD KEY `test_id` (`disc_id`);

--
-- Indexes for table `images`
--
ALTER TABLE `images`
  ADD PRIMARY KEY (`image_id`),
  ADD KEY `dish_id` (`sample_id`);

--
-- Indexes for table `petri_dish`
--
ALTER TABLE `petri_dish`
  ADD PRIMARY KEY (`petri_dishID`),
  ADD KEY `sample_id` (`sample_id`),
  ADD KEY `dish_id` (`dish_id`);

--
-- Indexes for table `pocket_state`
--
ALTER TABLE `pocket_state`
  ADD PRIMARY KEY (`pocket_id`);

--
-- Indexes for table `samples`
--
ALTER TABLE `samples`
  ADD PRIMARY KEY (`sample_id`),
  ADD KEY `bacteria_id` (`bacteria_id`),
  ADD KEY `patient_id` (`patient_id`);

--
-- Indexes for table `zones`
--
ALTER TABLE `zones`
  ADD PRIMARY KEY (`discId`),
  ADD KEY `sample_id` (`sample_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `antibiotics`
--
ALTER TABLE `antibiotics`
  MODIFY `abx_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
--
-- AUTO_INCREMENT for table `bacteria`
--
ALTER TABLE `bacteria`
  MODIFY `bacteria_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;
--
-- AUTO_INCREMENT for table `discs`
--
ALTER TABLE `discs`
  MODIFY `disc_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;
--
-- AUTO_INCREMENT for table `eucast`
--
ALTER TABLE `eucast`
  MODIFY `interpetation_id` int(50) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `images`
--
ALTER TABLE `images`
  MODIFY `image_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `petri_dish`
--
ALTER TABLE `petri_dish`
  MODIFY `petri_dishID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT for table `pocket_state`
--
ALTER TABLE `pocket_state`
  MODIFY `pocket_id` int(1) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `samples`
--
ALTER TABLE `samples`
  MODIFY `sample_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `zones`
--
ALTER TABLE `zones`
  MODIFY `discId` int(200) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `discs`
--
ALTER TABLE `discs`
  ADD CONSTRAINT `discs_ibfk_3` FOREIGN KEY (`sample_id`) REFERENCES `samples` (`sample_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `discs_ibfk_4` FOREIGN KEY (`abx_id`) REFERENCES `antibiotics` (`abx_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `eucast`
--
ALTER TABLE `eucast`
  ADD CONSTRAINT `eucast_ibfk_1` FOREIGN KEY (`abx_id`) REFERENCES `antibiotics11` (`abx_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `eucast_ibfk_2` FOREIGN KEY (`bacteria_id`) REFERENCES `bacteria` (`bacteria_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `flags`
--
ALTER TABLE `flags`
  ADD CONSTRAINT `flags_ibfk_1` FOREIGN KEY (`disc_id`) REFERENCES `discs` (`disc_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `images`
--
ALTER TABLE `images`
  ADD CONSTRAINT `images_ibfk_1` FOREIGN KEY (`sample_id`) REFERENCES `samples` (`sample_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `petri_dish`
--
ALTER TABLE `petri_dish`
  ADD CONSTRAINT `petri_dish_ibfk_1` FOREIGN KEY (`sample_id`) REFERENCES `samples` (`sample_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `samples`
--
ALTER TABLE `samples`
  ADD CONSTRAINT `samples_ibfk_1` FOREIGN KEY (`bacteria_id`) REFERENCES `bacteria` (`bacteria_id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
