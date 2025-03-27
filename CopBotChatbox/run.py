import subprocess

if __name__ == '__main__':
    # Run the backend app on port 5000
    backend_process = subprocess.Popen(['python', 'backend/app.py'])

    # Run the frontend app on port 5001
    frontend_process = subprocess.Popen(['python', 'frontend/app.py'])

    # Wait for the processes to finish
    backend_process.wait()
    frontend_process.wait()

