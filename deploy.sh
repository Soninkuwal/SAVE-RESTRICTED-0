    #!/bin/bash
    # Create a virtual environment
    python3 -m venv venv

    # Activate the virtual environment
    source venv/bin/activate

    # Install requirements
    pip install -r requirements.txt

    # Run the bot (Adjust bot/main.py if needed)
    python bot/main.py
