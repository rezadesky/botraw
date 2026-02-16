import os
import glob
import subprocess
import sys
import time
import signal

def run_bots():
    # Helper to check if ENV_FILE is already set
    env_file_override = os.getenv("ENV_FILE")
    if env_file_override:
        print(f"[Launcher] ENV_FILE is explicitly set: {env_file_override}")
        subprocess.run([sys.executable, "-m", "core.bot"], env={**os.environ, "ENV_FILE": env_file_override})
        return

    # Find all .env files in instances/bot_*/.env
    # The pattern is recursive or specific
    # In Docker: /app/instances/bot_1/.env
    # Locally: instances/bot_1/.env
    env_files = glob.glob("instances/bot_*/.env")
    
    if not env_files:
        print("[Launcher] Error: No bot instances found in instances/ directory!")
        print(f"[Launcher] CWD: {os.getcwd()}")
        if os.path.exists("instances"):
            print(f"[Launcher] Instances content: {os.listdir('instances')}")
        else:
            print("[Launcher] 'instances' directory not found.")
        sys.exit(1)

    processes = []
    for env_path in env_files:
        print(f"[Launcher] Launching instance with config: {env_path}")
        # Create a copy of environment and inject ENV_FILE
        env = os.environ.copy()
        env["ENV_FILE"] = env_path
        
        # Start process in background
        p = subprocess.Popen([sys.executable, "-m", "core.bot"], env=env)
        processes.append(p)

    print(f"[Launcher] Started {len(processes)} bot instances.")
    
    # Wait for all processes
    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        print("[Launcher] Stopping all bots...")
        for p in processes:
            p.terminate()

if __name__ == "__main__":
    run_bots()
