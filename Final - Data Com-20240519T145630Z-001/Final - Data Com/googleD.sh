#!/bin/bash

# Set variables
FOLDER_TO_BACKUP="/home/vm1/Desktop/dir"
BUCKET_NAME="backupstest2345678987654"
BACKUP_NAME="backup-$(date +'%Y-%m-%d_%H-%M-%S').tar.gz"

# Create a tar archive of the folder
tar czf "$BACKUP_NAME" "$FOLDER_TO_BACKUP"

# Upload the backup to Google Cloud Storage
gsutil cp "$BACKUP_NAME" "gs://$BUCKET_NAME/"

# Remove the local backup file
rm "$BACKUP_NAME"
