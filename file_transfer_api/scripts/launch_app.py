import subprocess
import sys
import signal


def launch_app(port: int = 8000):
    """Script to launch the API.

    Args:
        port: Port to run the API on. Defaults to 8000.
    """
    print(f"Launching API on port {port}...")
    cmd = ["uvicorn", "src.api.api:app", f"--port={port}", "--reload"]

    def signal_handler(sig, frame):
        print("\nThe API has been terminated...")
        sys.exit(0)

    # Launch the API
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run the API
    process = subprocess.Popen(cmd)
    process.wait()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Launch the API.")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the API on.")
    args = parser.parse_args()

    launch_app(port=args.port)
