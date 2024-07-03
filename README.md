Introduction
---------------
This repository contains tools for managing options/stocks and crypto data using TradingView webhooks, and interacting with the Robinhood API.

Setup
--------------
Create a GitHub Account:

If you don't have a GitHub account, create one now.
You will need to create a new repository and name it whatever you want.
Set Up the Local Project Folder:

Create a folder for the project on your local PC.
Open the terminal and navigate to the newly created folder.
Initialize the folder for GitHub:
sh
Copy code
git init
Connect your account to GitHub:
sh
Copy code
git remote add origin https://github.com/your-username/your-repository-name.git
Replace your-username and your-repository-name with your GitHub username and the new repository name.
Create a DigitalOcean Account:

If you don't have one already, create an account on DigitalOcean. You can use my referral link to receive $200 of free credit: DigitalOcean.
Create a New App on DigitalOcean:

Create a new app under the App Platform and name it whatever you want.
Installation
Clone the Repository:

Clone the repository into the new folder:
sh
Copy code
git clone https://github.com/MatthiasT91/Robinhood-Webhook-Bot.git
Navigate to the Project Folder:

Go into the folder to install dependencies:
sh
Copy code
cd options-bot
Install Dependencies:

Install the required dependencies:
sh
Copy code
pip install -r requirements.txt
Run the Application:

Deploy the app on DigitalOcean. This will run the Flask application, waiting for new alerts to come in.
To run the webhook with TradingView, you will need a paid TradingView account. Change the alert message to suit your requirements.
Configure the Application:

Rename the example.ini file to config.ini.
TradingView Alert Message
Insert these messages into the TradingView alert message box, and then change the webhook URL in the notifications panel. Messages can be found in the alert_options_info.txt file.

Deployment to a New Server
To deploy this application to a new server and set up webhooks from TradingView, follow these steps:

Deploy the App:

First, deploy it to GitHub, which will then deploy it to DigitalOcean:
sh
Copy code
git add .
git commit -m "Initial commit"
git push -u origin master:main
Create the App on DigitalOcean:

Now you should have your new project on GitHub and can proceed to create the app on DigitalOcean.
Enjoy managing your options data with FCT's Options/Stock Webhook Bot! This README.md file provides clear instructions for setting up the project, configuring environment variables, installing dependencies, and deploying the application to a new server.
