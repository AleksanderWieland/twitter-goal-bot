import os
from contextlib import redirect_stdout
from datetime import datetime
from time_func import wait_until
import time
from football import check_fixtures, get_match_data_by_team_id, get_match_time_from_fixture_data, send_tweet_with_new_events

# main function
def main():

    file_path = "events_log.json"

    # I want to store data in txt logs in order to track errors
    # Check if the file exists before deleting it
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"The file {file_path} has been deleted.")
    else:
        print(f"The file {file_path} does not exist.")

    # Fetch all today's fixtures
    response = check_fixtures()
    # Check if Arsenal (ID 42) is playing today
    team_id = 42  # Arsenal's ID

    match_data = get_match_data_by_team_id(response, team_id)
    if match_data is not None:
        print(match_data)
        match_time = get_match_time_from_fixture_data(match_data)
        fixture_id = match_data['id']
        wait_until(match_time)

        duration_in_minutes = 180
        total_iterations = duration_in_minutes // 2  # 180 minutes / 2 minutes = 90 iterations
        for _ in range(total_iterations):
            send_tweet_with_new_events(fixture_id)
            time.sleep(120)
    else:
        print('There is no data.')

# Redirect stdout to a file - in order to look for bugs
# main function
if __name__ == "__main__":
    # Create a log file name based on the current date and time
    log_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_app_log.txt"
    log_file_path = os.path.join(os.getcwd(), log_file_name)  # Full path to the log file
    
    with open(log_file_path, 'a') as log_file:  # Open the file in append mode
        with redirect_stdout(log_file):
            main()