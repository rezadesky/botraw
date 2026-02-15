#!/bin/bash

# Function to run a single bot instance
run_bot() {
    local env_file=$1
    echo "Starting bot with config: $env_file"
    export ENV_FILE="$env_file"
    python -m core.bot
}

# If ENV_FILE is explicitly set (e.g. via Railway Variables), run only that bot
if [ -n "$ENV_FILE" ]; then
    echo "ENV_FILE is set to $ENV_FILE. Running single instance..."
    run_bot "$ENV_FILE"
    exit 0
fi

# Otherwise, run ALL instances found in the instances directory
echo "No ENV_FILE set. Auto-detecting and running all bot instances..."

# Find all .env files in instances directory
# We look for instances/bot_*/.env
instances=(instances/bot_*/.env)

if [ ${#instances[@]} -eq 0 ]; then
    echo "Error: No bot instances found in instances/ directory!"
    exit 1
fi

# Loop through each instance and start it in the background
for env in "${instances[@]}"; do
    echo "Launching instance: $env"
    # Run in background with inline env var to avoid scope issues
    ENV_FILE="$env" python -m core.bot &
done

# Wait for all background processes to finish (runs forever basically)
wait
