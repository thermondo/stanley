# Stanley

![Stanley](https://img.buzzfeed.com/buzzfeed-static/static/enhanced/webdr06/2013/4/28/19/anigif_enhanced-buzz-4627-1367192053-4.gif?downsize=715:*&output-format=auto&output-quality=auto)

A secret Santa Slack bot for positive feedback.

## Setting up the bot


Just click the button, duh!

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Thermondo/stanley)

## Setting up Slack

```https://api.slack.com/```
-> 'Start Building'

### 1. Add Bot

In the section 'Add features and functionality' select Bots and fill the form

### 2. Permissions

In the section 'Add features and functionality' select Permissions

In the Scope add

*   bot
*   chat:write:bot
*   team:read

### 3. Event Subscriptions

In the section 'Add features and functionality' select Event Subscriptions

you have to set the deployed app url into 'Requests URL' and verify

Next 'Subscribe to Bot Events' add 'message.im'

Now go to your app and have fun!
