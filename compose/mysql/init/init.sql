# compose/mysql/init/init.sql
Alter user 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'patrick950207';
GRANT ALL PRIVILEGES ON myproject.* TO 'patrick950207'@'%';
FLUSH PRIVILEGES;