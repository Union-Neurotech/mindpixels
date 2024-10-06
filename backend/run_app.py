import sys
import streamlit
from streamlit.web import cli as stcli
from streamlit import runtime
import subprocess
import os

def run_streamlit_app(app_path):
    try:
        # Ensure all required packages are installed
        # subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        
        # Run the Streamlit app
        if runtime.exists():
            stcli.main()
        else:
            sys.argv = ["streamlit", "run", app_path]
            stcli.main()
    except Exception as e:
        print(f"An error occurred while running the Streamlit app: {str(e)}")

# Example usage
if __name__ == "__main__":
    full_app_path = os.path.join(os.path.dirname(__file__), 'app.py')
    run_streamlit_app(full_app_path)