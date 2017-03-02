# slack-metabot

Captures content metadata from Slack channels, such as photo EXIF data.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
virtualenv starterbot

source starterbot/bin/activate

pip install -r requirements.txt
```

### Installing

To set up your bot in your team's slack, you'll need to add it to your team first as bot integration.

"Add bot integration"

https://my.slack.com/services/new/bot

Read more: https://api.slack.com/bot-users

Set the bot's id and token in your script environment:

```
set SLACK_BOT_TOKEN xoxb-148375225045-zpDMaKWm6gRaS5tm8EyUohMe
set SLACK_BOT_ID 
```

To find out your bot's id value, use the following code:

https://github.com/mattmakai/slack-starterbot/blob/master/print_bot_id.py

For more information check out Matt's full tutorial on StarterBot:

https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

```
Give the example
```

And repeat

```
python slack-metabot.py &


```

End with an example of getting some data out of the system or using it for a little demo

```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds


## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Code based on Matt Makai's [slack-starterbot](https://github.com/mattmakai/slack-starterbot)
* GPS EXIF code based on maxbellec's [get_lat_lon_exif_pil.py](https://gist.github.com/maxbellec/dbb60d136565e3c4b805931f5aad2c6d)