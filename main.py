import base64
import functions_framework
import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG)


# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def handle_slack_event(cloud_event):
    # Print out the data from Pub/Sub, to prove that it worked
    logging.debug('this is handle_slack_event')
    # convert the data from Slack, sent via pub/sub, into a python dict
    # see https://cloud.google.com/pubsub/docs/reference/rest/v1/PubsubMessage
    data = json.loads(base64.b64decode(cloud_event.data["message"]["data"]).decode())
   
    # get the intended name for the puzzle. To be used to create a spreadsheet and a new channel in slack
    # add puz- if it doesn't start with puz
    puzzle_name = str(data["text"])
    if not puzzle_name.startswith("puz-"):
        puzzle_name = "puz-" + puzzle_name
    
    respond_to_slack(data["response_url"], puzzle_name)

def respond_to_slack(response_url, puzzle_name):
    logging.debug('responding to slack')
    logging.debug(response_url)
    payload = {
        'text': f"Setting up new puzzle: {puzzle_name}"
    }
    try:
        res = requests.request(method='POST',url=response_url, json=payload)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http Error:", e)
    
