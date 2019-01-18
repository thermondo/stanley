# Stanley

![Stanley](https://camo.githubusercontent.com/10a960a0a1f2b2373d970140ed26749330ab67d8/687474703a2f2f69312e7974696d672e636f6d2f76692f394548394b4f744e4c35452f6d617872657364656661756c742e6a7067)

A secret Santa Slack bot for positive feedback.

## Setting up the bot

Just click the button, duh!

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Thermondo/stanley)

You must configure on [Heroku Scheduler](https://devcenter.heroku.com/articles/scheduler)
how often Stanley will ask for feedback. Our team is asking feedback on Mondays,
Wednesdays, and Fridays. It doesn't mean that all team members will be asked three
times a week. Instead, Stanley will choose a sender and a receiver each day randomly.

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

### 4. Install your app to your workspace

Until this moment you have a bot configure but not installed in your workspace yet.
To do it and have access to Slack API credentials, click on _Install your app to your workspace_.

### 5. Set environment variables on Stanley

* `SLACK_VERIFICATION_TOKEN`: Still on Slack, click on _Basic Information_ and
in the section _App Credentials_ copy **Verification Token**.

* `SLACK_API_TOKEN`: in the section _Install App_, copy it from _Bot User OAuth Access Token_.

The variables `SLACK_API_TOKEN` and `SLACK_VERIFICATION_TOKEN` are required.
Other environment variables that are optional:

* `FEEDBACK_MEMBERS`: Stanley will use all members if you don't fill it in.
You can get the users and their ids using [Request team members](#request-team-members) command

* `REDIS_URL`: default is `redis://127.0.0.1:6379/0`

* `SENTRY_DSN`: for Sentry integration purposes

## Helpful management commands

### Request team members

To be able to see team members internal usernames (used in `FEEDBACK_MEMBERS` variable), you can run

```bash
FLASK_APP=stanley/app.py flask team-command
```

It will give you the list of Slack team members with their IDs.

### Request a feedback

To ask for a feedback, just run

```bash
FLASK_APP=stanley/app.py flask request-feedback-command
```

This will ask a random person to provide a feedback to another random person.

Example of our command (that will run on Mondays, Wednesdays, and Fridays):

```bash
if [ "$(date +%u)" = 1 ] || [ "$(date +%u)" = 3 ] || [ "$(date +%u)" = 5 ];
then FLASK_APP=stanley/app.py flask request-feedback-command;
fi
```
