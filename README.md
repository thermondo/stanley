# Setting up Slack
```https://api.slack.com/```
-> 'Start Building'
## 1. Add Bot
In the section 'Add features and functionality' select Bots and fill the form
## 2. Permissions
In the section 'Add features and functionality' select Permissions

In the Scope add 
- bot
- chat:write:bot
- team:read

## 3. Event Subscriptions
In the section 'Add features and functionality' select Event Subscriptions

you have to set the deployed app url into 'Requests URL' and verify

Next 'Subscribe to Bot Events' add 'message.im'

now go to your app and have fun!