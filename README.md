
# Download Manager

Download manager for Linux written in c

<br>

### Prerequisites
You need to have MySQL server installed (local or remote)

<br>

### Install
Clone repository by running
```bash
git clone https://github.com/Lasithih/downloader.git
```

Or download the latest release from
https://github.com/Lasithih/downloader/releases

<br>

Go to base directory and execute
```bash
./install.sh
```

This will
- Install downloader as a systemd service
- Update the config file of the downloader with the configurations of your database
- Update the config file of the frontend app with the configurations of your database
<br>

### Frontend app
To manage download jobs use the frontend app located in downloader-fe directory. **after running install.sh**
Copy downloader-fe directory to a server
<br>
  
### Configurations
You can find the configurations file at
```bash
$HOME/LIHApps/Downloader/config.cfg
```
<br>

### Troubleshooting
Log files location
```bash
/var/log/downloader
```
<br>

#### Check status of downloader
```bash
sudo systemctl status downloader.service
```