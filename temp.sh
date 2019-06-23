#!/bin/bash
echo "Enter mysql server address (eg: localhost):  "
read db_server

read -p "Enter mysql server address (Leave blank to use default port):  " port
port=${port:-3306}

echo "Enter mysql user (eg: root):  "
read db_user

echo "Enter mysql password: "
read -s password

echo "server: $db_server"
echo "port: $port"
echo "user: $db_user"
echo "password: $password"

mysql -u $db_user -h $db_server -P $port -p$password<< EOF
select * from downloads.jobs;
EOF