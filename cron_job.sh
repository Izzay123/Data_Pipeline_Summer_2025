#!/bin/bash

# Cron job script for Data Pipeline
# Add this to your crontab using: crontab -e
# Example cron schedule: 0 2 * * * /path/to/this/script/cron_job.sh

# Set the working directory
cd "$(dirname "$0")/trail-trekker"

# Log file for cron job output
LOG_FILE="cron_job.log"

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "$(date): Activated virtual environment" >> "$LOG_FILE"
else
    echo "$(date): No virtual environment found, proceeding without activation" >> "$LOG_FILE"
fi

# Function to log messages with timestamp
log_message() {
    echo "$(date): Starting sqlmesh job" >> "$LOG_FILE"
    sqlmesh run prod >> "$LOG_FILE" 2>&1
    echo "$(date): Finished sqlmesh job" >> "$LOG_FILE"
}

# Run the sqlmesh job
log_message

# Exit with success status
exit 0