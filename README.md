
Introduction:
-------------

This repository contains scripts and tools for managing options/stock/crypto data using TradingView webhooks,
	and interacting with the Robinhood API.


Setup:
-------------
1. Go and create an account on DigitalOcean (If you uuse my referal linkk you will recieve $200 of free credit to use) if you dont have one already.
   	https://m.do.co/c/de7d99f5f217
   
2. Go and create a new App under App Platform and name it whatever you want.

3. 


Installation:
-------------

1. Clone the repository:
		git clone https://github.com/yourusername/options-bot.git

2. Go into the folder to install Dependencies:
  	cd options-bot

3. Install dependencies:
		pip install -r requirements.txt

4. Run the application:
   	You will deploy the app on DigitalOcean and that will run the flask application waiting for new alerts to come in.
		To run the Webhook with Tradingview. You will need to have a paid TradingView account, and you will need to change the message for what you want to do.


Tradingview Alert message:
-------------
Insert these messages into the TradingView alert message box, and then change the webhook URL in the notifications pannel.

1. Crypto Webhook Message:
	{
		"option":"crypto",
    "position":"market",
    "cord":"none",
  	"symbol": "{{ticker}}",
  	"qtity":"20",
  	"type":"buy",
  	"price": "{{close}}"
	{

2. Stocks Webhook Message:
	{
  	"option":"stocks",
  	"position":"open",
  	"cord":"debit",
  	"symbol": "{{ticker}}",
  	"qtity":"1",
  	"type":"none",
  	"price": "{{close}}"
	}

3. Options Webhook Message:
	{
  	"option":"options",
  	"position":"open",
  	"cord":"debit",
  	"symbol": "{{ticker}}",
  	"qtity":"1",
  	"type":"none",
  	"price": "{{close}}"
	}


Deployment to a New Server:
----------------------------
To deploy this application to a new server and set up webhooks from TradingView, follow these steps:

Enjoy managing your options data with FCT's Options/Stock webhook Bot!
This README.txt file provides clear instructions for setting up the project, configuring environment variables, installing dependencies, and deploying the application to a new server. 
