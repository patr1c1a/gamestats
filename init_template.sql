-- replace <mysql_database>, <mysql_user> and <mysql_password> with the same values you used in secrets.py and docker-compose.yml

CREATE DATABASE IF NOT EXISTS `<mysql_database>` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '<mysql_user>'@'%' IDENTIFIED BY '<mysql_password>';
GRANT ALL PRIVILEGES ON `<mysql_database>`.* TO '<mysql_user>'@'%';
GRANT CREATE, ALTER, DROP, INDEX, CREATE TEMPORARY TABLES, LOCK TABLES, INSERT ON *.* TO '<mysql_user>'@'%';
GRANT ALL PRIVILEGES ON test_<mysql_database>.* TO '<mysql_user>'@'%';
GRANT INSERT ON test_<mysql_database>.django_migrations TO '<mysql_user>'@'%';
FLUSH PRIVILEGES;