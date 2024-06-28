Options Bot

Introduction:
-------------
This repository contains scripts and tools for managing options/stock data using TradingView webhooks,
  and interacting with the Robinhood API.

Setup:
------
Environment Variables:

1. Rename the `example.ini` to `config.ini` file:
    USERNAME=your_robinhood_username
    PASSWORD=your_robinhood_password
    ACCOUNTID=your_robinhood_account_number
    WEBHOOK=discord_webhook # If none then type: None

Replace `USERNAME`, `PASSWORD`, `ACCOUNTID`, `WEBHOOK` with your Robinhood credentials. Ensure you keep this file secure and do not share it publicly.

Installation:
-------------

1. Clone the repository:
  git clone https://github.com/yourusername/options-bot.git
  cd options-bot

2. Install dependencies:
  pip install -r requirements.txt

3. Run the application:
To run the Webhook with Tradingview. You will need to have a paid account, and you will need to change the message for what you want to do.

{
  "option":"stocks",
  "position":"open",
  "cord":"debit",
  "symbol": "{{ticker}}",
  "qtity":".22",
  "type":"none",
  "price": "{{close}}"
}

Deployment to a New Server:
----------------------------

To deploy this application to a new server and set up webhooks from TradingView, follow these steps:

Enjoy managing your options data with FCT's Options/Stock webhook Bot!
This README.txt file provides clear instructions for setting up the project, configuring environment variables, installing dependencies, and deploying the application to a new server. 
