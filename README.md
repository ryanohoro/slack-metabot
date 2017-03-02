# slack-metabot

Captures content metadata from Slack channels, at this point only photo EXIF data.


### Prerequisites

Slack-metabot targets Python 2.7 and requires slackclient, requests, geocoder and Pillow.

Configure the script environment.

```
virtualenv starterbot

source starterbot/bin/activate

git clone https://github.com/ryanohoro/slack-metabot.git

cd slack-metabot

pip install -r requirements.txt
```

### Installing

To set up your bot in your team's slack, you'll need to add it to your team first using "Add bot integration".

https://my.slack.com/services/new/bot

Capture the API token and customize your bot.

Set the bot's token in your script environment:

```
set SLACK_BOT_TOKEN xoxb-148375115045-zoDMcKWN6gRVS5tm7EyUphNo
```

You'll need your bot's ID value. Run the following code, then set the bot ID in your script environment.

https://github.com/mattmakai/slack-starterbot/blob/master/print_bot_id.py

```
set SLACK_BOT_ID U1CA99M5C
```

Then spin up the bot.

```
python slack-metabot.py

```


For more information check out Matt's full tutorial on StarterBot:

https://www.fullstackpython.com/blog/build-first-slack-bot-python.html


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Code based on Matt Makai's [slack-starterbot](https://github.com/mattmakai/slack-starterbot)
* GPS EXIF code based on maxbellec's [get_lat_lon_exif_pil.py](https://gist.github.com/maxbellec/dbb60d136565e3c4b805931f5aad2c6d)