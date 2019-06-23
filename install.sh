#!/usr/bin/env bash

sudo apt-get -y update

echo "Installing build tools"
sudo apt-get install -y cmake build-essential


echo "Installing youtube-dl"
sudo wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl


echo "Installing log4c"
sudo apt-get install -y liblog4c-dev


echo "Installing mysql client"
sudo apt-get install -y libmysqlclient-dev


echo "Installing libConfig"
sudo apt-get install -y libconfig-dev


echo "Enter mysql server address (eg: localhost):  "
read db_server

read -p "Enter mysql server address (Leave blank to use default port):  " port
port=${port:-3306}

echo "Enter mysql user (eg: root):  "
read db_user

echo "Enter mysql password"
mysql -u $db_user -h $db_server -P port -p << EOF
source support/database.sql
EOF


sed -i "/server =/c\server = \"$db_server\"" support/config.cfg
sed -i "/user =/c\user = \"$db_user\"" support/config.cfg


echo "Building downloader"
sudo mkdir build
cd build
cmake ..
make

echo "Installing..."
mkdir -p $HOME/LIHApps/Downloader
cp Downloader $HOME/LIHApps/Downloader
cd ..
cp support/config.cfg $HOME/LIHApps/Downloader
cp support/log4crc $HOME/LIHApps/Downloader

echo "Enabling service"
sed -i "/WorkingDirectory=/c\WorkingDirectory=$HOME/LIHApps/Downloader" support/downloader.service
sed -i "/ExecStart=/c\ExecStart=$HOME/LIHApps/Downloader/Downloader" support/downloader.service
sudo cp support/downloader.service /lib/systemd/system

sudo systemctl enable downloader.service
sudo systemctl start downloader.service


