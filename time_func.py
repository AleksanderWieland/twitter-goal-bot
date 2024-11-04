import time
from datetime import datetime, timezone

def wait_until(target_time_str):
    """Function waits until it reaches the given date and time in ISO 8601 format."""
    
    # Convert the given string to a datetime object
    target_time = datetime.fromisoformat(target_time_str)
    
    # Current time
    now = datetime.now(timezone.utc)

    # Check if the current date and time are before the target time
    while now < target_time:
        time_left = (target_time - now).total_seconds()
        print(f"Waiting {int(time_left)} seconds to execute the code.")
        time.sleep(30)  # Check every 30 seconds if it’s time yet

        # Update the current time
        now = datetime.now(timezone.utc)

    print(f"Executing code at {target_time_str}!")

