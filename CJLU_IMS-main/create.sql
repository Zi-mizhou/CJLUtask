CREATE TABLE `user` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `role` VARCHAR(10) NOT NULL,
    `username` VARCHAR(100) NOT NULL UNIQUE,
    `password` VARCHAR(128) NOT NULL,
    `name` VARCHAR(100),
    `gender` VARCHAR(10),
    `avatar_url` VARCHAR(255),
    `email` VARCHAR(100) UNIQUE,
    `is_active` BOOLEAN DEFAULT TRUE,
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `department` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `path` VARCHAR(255) NOT NULL UNIQUE,
    `name` VARCHAR(100) NOT NULL,
    `parent_id` INT,
    `description` VARCHAR(255),
    `is_active` INT DEFAULT 1,  -- 1表示激活，0表示禁用
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `ck_department_path_format` CHECK (`path` REGEXP '^[0-9]+(/[0-9]+)*$')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX `ix_department_parent_id` ON `department` (`parent_id`);

CREATE TABLE `application` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(100) NOT NULL,
    `content` VARCHAR(1000) NOT NULL,
    `category` VARCHAR(50),
    `has_file` BOOLEAN DEFAULT FALSE,
    `status` VARCHAR(20) DEFAULT 'pending',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `ck_application_status_valid` CHECK (`status` IN ('pending', 'approved', 'rejected'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `file` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `size` INT,  -- 文件大小，单位字节
    `url` VARCHAR(255),
    `type` VARCHAR(255),  -- 文件类型，例如 'pdf', 'docx'
    `parent` INT,  -- 仅保留字段，无外键
    `is_dir` INT DEFAULT 0,  -- 1表示目录，0表示文件
    `active` INT DEFAULT 1,
    `public` INT DEFAULT 0,  -- 1表示公开，0表示私有
    `key` VARCHAR(255),  -- OSS存储的key
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `log` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `event_type` VARCHAR(50) NOT NULL,
    `description` VARCHAR(255),
    `user_id` INT,
    `referer` VARCHAR(255),
    `ip` VARCHAR(45),
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `student` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `student_no` VARCHAR(50) NOT NULL UNIQUE,
    `class_name` VARCHAR(100),
    `major` VARCHAR(100),
    `college` VARCHAR(100),
    `grade` VARCHAR(20),
    `enrollment_year` INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX `ix_student_user_id` ON `student` (`user_id`);

CREATE TABLE `teacher` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `staff_no` VARCHAR(50) NOT NULL UNIQUE,
    `title` VARCHAR(50),
    `office_location` VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX `ix_teacher_user_id` ON `teacher` (`user_id`);

CREATE TABLE `user_application` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `sender_id` INT NOT NULL,
    `receive_id` INT NOT NULL,
    `application_id` INT NOT NULL,
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `uq_user_app` (`sender_id`, `receive_id`, `application_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `user_department` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `department_id` INT NOT NULL,
    `position` VARCHAR(100),
    `is_active` BOOLEAN DEFAULT TRUE,
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `user_file` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `file_id` INT NOT NULL,
    `permission` VARCHAR(20) NOT NULL,
    UNIQUE KEY `uq_user_file` (`user_id`, `file_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
