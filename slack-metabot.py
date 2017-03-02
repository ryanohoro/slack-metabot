import os
import sys
import time
import requests
from urlparse import urlparse
from slackclient import SlackClient
from PIL import Image
from geocoder import google
import argparse

# metabot's ID as an environment variable
BOT_ID = os.environ.get("SLACK_BOT_ID")

# constants
AT_BOT = "<@metabot>"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


get_float = lambda x: float(x[0]) / float(x[1])


def convert_to_degrees(value):
    d = get_float(value[0])
    m = get_float(value[1])
    s = get_float(value[2])
    return d + (m / 60.0) + (s / 3600.0)


def get_lat_lon(info):
    try:
        gps_latitude = info[34853][2]
        gps_latitude_ref = info[34853][1]
        gps_longitude = info[34853][4]
        gps_longitude_ref = info[34853][3]
        lat = convert_to_degrees(gps_latitude)
        if gps_latitude_ref != "N":
            lat *= -1

        lon = convert_to_degrees(gps_longitude)
        if gps_longitude_ref != "E":
            lon *= -1
        return lat, lon
    except KeyError:
        return None


def parse_gps(url):
    """
        Extract available GPS coordinates data from image EXIF data and attempt to geocode them with the Google API,
        and return a message for the channel/user if found.

        :param url: URL to Slack-hosted image
        :return: String to be returned to chat
    """

    # We send a Bearer token to the URL we receive, so here we make sure it's Slack via HTTPS only #justsecuritythings
    try:
        parsedurl = urlparse(url)
        if not (parsedurl.hostname == 'files.slack.com' and parsedurl.scheme == 'https'):
            return None
    except Exception:
        raise

    try:
        # Fetch only the headers to check the file size and not waste time with large files
        response = requests.head(url, timeout=30,
                                headers={'Authorization': 'Bearer {}'.format(os.environ.get('SLACK_BOT_TOKEN'))})

        if int(response.headers.get('Content-Length')) > 16000000:
            if args.verbose: sys.stderr.write('Skipped large file\n')
            return None

        # Fetch the URL and use request's raw method to create a file object to give to Image
        response = requests.get(url, stream=True, timeout=10,
                                headers={'Authorization': 'Bearer {}'.format(os.environ.get('SLACK_BOT_TOKEN'))})

        if not response.status_code == 200:
            if args.verbose: sys.stderr.write('Status code {}\n'.format(response.status_code))
            return None

        # We don't make any assumptions about the file type from the URL in case there's no extension or it's inaccurate
        if response: img = Image.open(response.raw)

        # Attempt to get EXIF data from the image object
        if img: exif = img._getexif()

        # Attempt to find GPS coordinates and decode them to a tuple in degrees
        if exif: lat_lon = get_lat_lon(exif)

        # If we think we were successful, try to geocode the coordinates. If it fails, return only the coordinates
        if lat_lon and len(lat_lon) == 2:
            try:
                geocode = google(lat_lon, method='reverse')
                # Returns City, State and Country
                return '{}, {} ({}) - {:.4f}, {:.4f}'.format(geocode.city, geocode.state, geocode.country, lat_lon[0],
                                                             lat_lon[1])
            except:
                # Coordinates only
                return '{:.4f}, {:.4f}'.format(lat_lon[0], lat_lon[1])
        else:
            if args.verbose: sys.stderr.write('No GPS data in EXIF\n')
    except AttributeError:
        if args.verbose: sys.stderr.write('No EXIF data in file\n')
        pass
    except Exception:
        raise

    return None


# For future use
def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    slack_client.api_call('chat.postMessage', channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'file' in output and 'upload' in output and 'channel' in output:
                if 'url_private' in output['file'] and output['upload'] == True:
                    if args.verbose: print('URL: {}'.format(output['file']['url_private']))
                    try:
                        buffer = parse_gps(output['file']['url_private'])

                        if (buffer):
                            if args.verbose: print(buffer)
                            send_message(output['channel'], buffer)

                    except Exception as e:
                        sys.stderr.write('{}\n'.format(str(e)))

    return None, None

def send_message(channel_id, message):
    slack_client.api_call('chat.postMessage', channel=channel_id, text=message, username='metabot',
                          icon_emoji=':robot_face:')

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', dest='verbose', action='store_true',
                        help='Verbosity')
    args = parser.parse_args()


    if slack_client.rtm_connect():
        print('Metabot connected and running!')
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            #if command and channel:
            #    handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print('Connection failed. Invalid Slack token or bot ID?')