import json
import requests
from datetime import datetime
from twitter import send_tweet
import constants

def check_fixtures():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        "x-rapidapi-key": str(constants.X_RAPIDAPI_KEY),
    }
    today = datetime.today().strftime('%Y-%m-%d')
    querystring = {"date": today}

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return data

def get_match_data_by_team_id(response, teamid):
    """Zwraca dane meczu drużyny o danym ID, jeśli gra dzisiaj"""
    for match in response['response']:
        home_team_id = match['teams']['home']['id']
        away_team_id = match['teams']['away']['id']
        if home_team_id == teamid or away_team_id == teamid:
            return match['fixture']
    return None  # Return None if the team is not playing


def get_match_time_from_fixture_data(response):
    """Returns the match time from the fixture data"""
    if response != None:
        return response['date']
    else:
        return None # Return None if the team is not playing
    
def save_date_to_file(date_time):
    with open('date_match.txt', 'w') as file:
        file.write(date_time)


def check_fixture_events(fixture_id):
    url = "https://v3.football.api-sports.io/fixtures/events"
    headers = {
        "x-rapidapi-key": str(constants.X_RAPIDAPI_KEY),
    }
    today = datetime.today().strftime('%Y-%m-%d')
    querystring = {"fixture": fixture_id}

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return data


def load_previous_events(file_path):
    """Load previous events from file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Jeśli plik nie istnieje, zwróć pustą listę

def save_current_events(file_path, events):
    """Save current events to file."""
    with open(file_path, 'w') as file:
        json.dump(events, file)

def send_tweet_with_new_events(fixture_id, file_path="events_log.json"):
    """Monitors events and reports new ones."""
    data = check_fixture_events(fixture_id)

    if 'response' in data and data['response']:
        current_events = data['response']
        
        # Load previous events from file
        previous_events = load_previous_events(file_path)
        
        # Find new events
        new_events = [event for event in current_events if event not in previous_events]

        if new_events:
            print(f'New events detected at {datetime.now()}: {len(new_events)} new events')
            for event in new_events:
                tweet_text = format_event_tweet(event)
                print(tweet_text)
                send_tweet(tweet_text)
            # Save current events to file to monitor further changes
            save_current_events(file_path, current_events)
        else:
            print(f'No new events detected at {datetime.now()}.')
    else:
        print(f'No events found for fixture {fixture_id} at {datetime.now()}.')

def format_event_tweet(event):
    event_type = event['type']
    player_name = event['player']['name']
    team_name = event['team']['name']
    elapsed_time = event['time']['elapsed']
    elapsed_extra_time = event['time']['extra']
    card_detail = event['detail']
    
    extra_time_text = ''
    if elapsed_extra_time != None:
        extra_time_text=f"+{elapsed_extra_time}'"

    if player_name != None or event_type == 'Var':
        match event_type:
            case "Card":
                print()
                return f"📋 {player_name} from {team_name} received a {card_detail} at {elapsed_time}'{extra_time_text}!"

            case "subst":
                assist_name = event.get('assist', {}).get('name', 'No assist') #player that is being substituted is considered in API as an assist
                return f"🔄 Substitution! {player_name} replaced {assist_name} for {team_name} at {elapsed_time}'{extra_time_text}!"

            case "Var":
                if card_detail != None:
                    return f"📺 VAR check at {elapsed_time}'{extra_time_text} for {team_name}. Decision: {card_detail}."
                else:
                    return f"📺 VAR check at {elapsed_time}'{extra_time_text} for {team_name}. Decision pending..."
                

            case "Goal":
                assist_name = event.get('assist', {}).get('name', 'No assist')
                return f"⚽ {player_name} scored a goal for {team_name} at {elapsed_time}'{extra_time_text}! Assist by {assist_name}."

            case _:
                return f"⏱ Event of type {event_type} at {elapsed_time}'{extra_time_text}"




