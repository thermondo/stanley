# Stanley

![Stanley](https://camo.githubusercontent.com/10a960a0a1f2b2373d970140ed26749330ab67d8/687474703a2f2f69312e7974696d672e636f6d2f76692f394548394b4f744e4c35452f6d617872657364656661756c742e6a7067)

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
