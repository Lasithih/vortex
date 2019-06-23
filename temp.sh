echo "Enter mysql server address (eg: localhost):  "
read db_server

read -p "Enter mysql server port (Leave blank to use default port):  " port
port=${port:-3306}

echo "Enter mysql user (eg: root):  "
read db_user

echo "Enter mysql password: "
read -s password


sed -i "/private \$servername =/c\private \$servername = \"$db_server\"" downloader-fe/db_access.php
sed -i "/private \$username =/c\private \$username = \"$db_user\"" downloader-fe/db_access.php
sed -i "/private \$password =/c\private \$password = \"$password\"" downloader-fe/db_access.php