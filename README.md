
Introduction:
-------------

This repository contains tools for managing options/stocks and crypto data using TradingView webhooks,
	and interacting with the Robinhood API.


Setup:
-------------
1. If you dont have a github account, create one now.
   
   You will need to make a new Repositorie, and name it whatever you want. 

3. After you have created a new Repo, you will need to create a folder for the project on your local PC.
  
   After creating a folder, you will need to open that up with a terminal. Once opened, and now direct yourself to the folder you just created. Once inside the folder you will need to initiate the folder for GitHub by typing this.  
		```git init```  
	Once intiated you will need to connect your account to github by typing this:

	```git remote add origin https://github.com/your-username/your-repository-name.git```
	That will be from your username from github and the new repo you just created.
	Keep the terminal open..

6. Go and create an account on DigitalOcean (If you use my referral link you will receive $200 
	of free credit to use) if you dont have one already [DigitalOcean](https://m.do.co/c/de7d99f5f217).
   
8. Go and create a new App under App Platform and name it whatever you want.



Installation:
-------------

1. Clone the repository into the new folder:
   
		```git clone https://github.com/MatthiasT91/Robinhood-Webhook-Bot.git```

2. Go into the folder to install Dependencies:
   
  	```cd options-bot```

3. Install dependencies:
   
		```pip install -r requirements.txt```

4. Run the application:
   	You will deploy the app on DigitalOcean and that will run the flask application waiting for new alerts to come in.
	
	To run the Webhook with Tradingview. You will need to have a paid TradingView account, and you will need to change the message for what you want to do.

5. Change the name of the example.ini fil to config.ini.


Tradingview Alert message:
-------------
Insert these messages into the TradingView alert message box, and then change the webhook URL in the notifications pannel.

Messages can be found in the alert_options_info.txt file.

Deployment to a New Server:
----------------------------
To deploy this application to a new server and set up webhooks from TradingView, follow these steps:

1. To Deploy the app onto the server, you first need to deploy it onto GitHub and that will 
	deploy it to DigitalOcean.
	```
	git add .
	git commit -m "Initial commit"
	git push -u origin master:main
 	```

2. Now you should have your new project in your github and now should be creating the app on
	DigitalOcean


Enjoy managing your options data with FCT's Options/Stock webhook Bot!
This README.txt file provides clear instructions for setting up the project, configuring environment variables, installing dependencies, and deploying the application to a new server. 
