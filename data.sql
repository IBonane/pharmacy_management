-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 06, 2023 at 12:31 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pharmacie`
--

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `stock`, `description`, `price`) VALUES
(1, 'Aspirine', 100, 'Médicament contre la douleur et la fièvre', 600),
(2, 'Paracétamol', 150, 'Antipyrétique et analgésique', 400),
(3, 'Ibuprofène', 120, 'Anti-inflammatoire non stéroïdien', 700),
(4, 'Amoxicilline', 80, 'Antibiotique', 1300),
(5, 'Loratadine', 200, 'Antihistaminique', 900),
(6, 'Omeprazole', 90, 'Inhibiteur de la pompe à protons', 1500),
(7, 'Simvastatine', 60, 'Statine pour abaisser le cholestérol', 1900),
(8, 'Amlodipine', 75, 'Inhibiteur calcique pour la pression artérielle', 1000),
(9, 'Metformine', 110, 'Traitement du diabète de type 2', 800),
(10, 'Atorvastatine', 50, 'Statine pour abaisser le cholestérol', 2300),
(11, 'Levothyroxine', 95, 'Hormone thyroïdienne synthétique', 1600),
(12, 'Salbutamol', 30, 'Bronchodilatateur pour l\'asthme', 1100),
(13, 'Warfarine', 40, 'Anticoagulant', 1800),
(14, 'Insuline', 25, 'Hormone pour le contrôle du diabète', 260),
(15, 'Méthotrexate', 35, 'Antimétabolite pour le traitement du cancer', 300),
(16, 'Furosémide', 70, 'Diurétique pour l\'insuffisance cardiaque', 800),
(17, 'Diazépam', 55, 'Anxiolytique et anticonvulsivant', 145),
(18, 'Citalopram', 65, 'Antidépresseur sélectif du recaptage de la sérotonine', 200),
(19, 'Tramadol', 45, 'Analgésique opioïde', 165),
(20, 'Ranitidine', 85, 'Antagoniste des récepteurs H2', 1100);

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `first_name`, `last_name`, `user_name`, `password`, `is_admin`) VALUES
(1, 'bonane', 'djimbala', 'bonane@pharma.fr', 'd9647cfdf1864ac491ae14b31abfcc680aeee1772b4a28cc9ff286fad20967af', 0),
(3, 'Admin', 'Admin', 'admin@pharma.fr', '7ae12d486dc1faf51e631283f2bf7c9f88c1b7cc5487df7a339119943405263d', 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
