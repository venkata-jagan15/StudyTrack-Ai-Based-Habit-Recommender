CREATE DATABASE IF NOT EXISTS ai_study_insight;
USE ai_study_insight;

-- 1. Create the Django auth_user table first (Required for Foreign Keys)
CREATE TABLE IF NOT EXISTS `auth_user` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `password` varchar(128) NOT NULL,
    `last_login` datetime(6) NULL,
    `is_superuser` bool NOT NULL,
    `username` varchar(150) NOT NULL UNIQUE,
    `first_name` varchar(150) NOT NULL,
    `last_name` varchar(150) NOT NULL,
    `email` varchar(254) NOT NULL,
    `is_staff` bool NOT NULL,
    `is_active` bool NOT NULL,
    `date_joined` datetime(6) NOT NULL
);

-- 2. Create Dashboard Tables
CREATE TABLE IF NOT EXISTS `dashboard_userprofile` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `role` varchar(10) NOT NULL,
    `grade_level` varchar(10) NULL,
    `attendance_rate` double NOT NULL,
    `predicted_score` double NOT NULL,
    `risk_level` varchar(20) NOT NULL,
    `user_id` integer NOT NULL UNIQUE,
    -- Constraint to link to Django's auth_user table
    CONSTRAINT `dashboard_userprofile_user_id_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
);

CREATE TABLE IF NOT EXISTS `dashboard_habitlog` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `date` date NOT NULL,
    `sleep_hours` double NOT NULL,
    `study_hours` double NOT NULL,
    `social_media_hours` double NOT NULL,
    `student_id` integer NOT NULL,
    CONSTRAINT `dashboard_habitlog_student_id_fk_auth_user_id` FOREIGN KEY (`student_id`) REFERENCES `auth_user` (`id`)
);

CREATE TABLE IF NOT EXISTS `dashboard_subjectgrade` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `subject_name` varchar(50) NOT NULL,
    `score` double NOT NULL,
    `student_id` integer NOT NULL,
    CONSTRAINT `dashboard_subjectgrade_student_id_fk_auth_user_id` FOREIGN KEY (`student_id`) REFERENCES `auth_user` (`id`)
);

CREATE TABLE IF NOT EXISTS `dashboard_weeklytestscore` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `week_number` integer NOT NULL,
    `avg_score` double NOT NULL,
    `student_id` integer NOT NULL,
    CONSTRAINT `dashboard_weeklytestscore_student_id_fk_auth_user_id` FOREIGN KEY (`student_id`) REFERENCES `auth_user` (`id`)
);

CREATE TABLE IF NOT EXISTS `dashboard_teacherfeedback` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `message` longtext NOT NULL,
    `created_at` datetime(6) NOT NULL,
    `student_id` integer NOT NULL,
    `teacher_id` integer NULL,
    CONSTRAINT `dashboard_teacherfeedback_student_id_fk_auth_user_id` FOREIGN KEY (`student_id`) REFERENCES `auth_user` (`id`),
    CONSTRAINT `dashboard_teacherfeedback_teacher_id_fk_auth_user_id` FOREIGN KEY (`teacher_id`) REFERENCES `auth_user` (`id`)
);

CREATE TABLE IF NOT EXISTS `dashboard_airecommendation` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `category` varchar(20) NOT NULL,
    `message` longtext NOT NULL,
    `is_alert` bool NOT NULL,
    `created_at` datetime(6) NOT NULL,
    `student_id` integer NOT NULL,
    CONSTRAINT `dashboard_airecommendation_student_id_fk_auth_user_id` FOREIGN KEY (`student_id`) REFERENCES `auth_user` (`id`)
);
