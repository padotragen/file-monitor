# file-monitor
.
|-- ./checkFolderSize.py
|-- ./file-monitor
|   |-- ./file-monitor/Dockerfile
|   |-- ./file-monitor/requirements.txt
|   |-- ./file-monitor/docker-compose.yml
|   `-- ./file-monitor/monitor.py
|-- ./filemonitoring.py
|-- ./folder-cleanup
|   |-- ./folder-cleanup/Dockerfile
|   |-- ./folder-cleanup/docker-compose.yml
|   `-- ./folder-cleanup/folderCleanup.py
|-- ./docker-compose.yml
`-- ./README.md

# Running the docker-compose.yml file from the root requires and .env file
# Template for the file below

# File Monitoring Configuration
SOURCE_DIR="/app/MonitoredFolder"
DEST_DIR="/app/SecondFolder"

# Folder Cleanup Configuration
MAXFOLDERSIZE="100"  # Specify in MB
TARGETFOLDERSIZE="10"  # Specify in MB
CLEANUPTIMEOUT="15"  # Specify in Seconds

# Redis Configuration
REDIS_HOST="redis"
REDIS_PORT="6379"

# Docker Volume Mount Paths
MONITORED_FOLDER=<LOCAL MONITORED FOLDER>
SECOND_FOLDER=<LOCAL DESINATION FOLDER>