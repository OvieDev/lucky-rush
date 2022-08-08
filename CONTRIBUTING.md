# Contributing to the project
You want to contribute to this teeny tiny project? If you do, you're in right place, since this entire document is about contributing to the project.
## 1. General rules
First, remember to follow [code of conduct](https://github.com/OvieDev/lucky-rush/blob/master/CODE_OF_CONDUCT.md). It's a set of basic rules about community health etc.
Another important thing is to be as descriptive as you can in your issues or pull requests. This allows us for better dialog with contributors and makes project development faster
Don't forget about properly tagging your issues/pull requests. It's not difficult to do, and it makes filtering through all of them faster.
## 2. Unsignificant changes (markdown files editing etc.)
If you're about to do anything without touching the actual code of the bot, you create pull requests as you would do in any other project. However, if you're here for the first time, let me say how to do this.
1. Create a fork of the project
2. Do some stuff with any, non-python file
3. Create pull request and tag it properly (as mentioned in paragraph 1)
4. Wait for your PR to be merged

It's simple and it works.
## 3. Code changes
But what if you want to do some stuff with an actual code? Don't worry too much because the process is pretty much the same. Fork the project, edit code, create a PR and wait for merge.
And that works, but you may want to test your code. Well in that case, you need to host the bot on your own. So, to do this follow these steps.
### 3.1 Install discord.py (2.0)
If you're on windows use this in cmd:
`py -3 -m pip install -U discord.py`\
If you're running linux use this in your terminal:
`py -3 -m pip install -U discord.py`\
[Full article how to download it](https://discordpy.readthedocs.io/en/latest/intro.html)
### 3.2 Install python-dotenv
You can install it with this command: `pip install python-dotenv`
### 3.3 Fork the project
You can also clone it on your device to use your favorite IDE.
### 3.4 Go to Discord Developer Portal and create an app
Head to the bot tab\
![The bot tab](https://i.imgur.com/CesWcMR.png)\
...and create a bot.
To give it an invite link go to Oauth2 tab and to the URL generator subtab
![URL generator tab](https://i.imgur.com/pn6yHTe.png)\
Select **bot** and **application.commands** box as shown on the picture
![What to select](https://i.imgur.com/12qwcAP.png)\
Copy the url, go to genral tab in Oauth2 section, add redirect and paste your URL in the textbox as shown in the picture\
![Where to put an url](https://i.imgur.com/8Zu2dWN.jpg)
And finally get bot's token from the bot tab and copy it. Also don't forget to invite the bot to your server with the invite link
### 3.5 Create .env file and paste there your token
Your .env file should look like this:\
`TOKEN=<your token>`\
**AND CONGRATULATIONS! Your bot fork is up and running now**

If you're happy with the changes you made, push the code to your fork, create a pull request and wait for the merge.
