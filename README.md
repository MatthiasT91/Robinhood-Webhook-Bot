Introduction:
-------------

**This repository contains tools for managing options/stocks and crypto data using TradingView webhooks,
and interacting with the Robinhood API.**

Setup:
------

1. **Create a GitHub Account:**
    - If you don't have a GitHub account, create one now.
    - You will need to create a new repository and name it whatever you want.

2. **Set Up the Local Project Folder:**
    - Create a folder for the project on your local PC.
    - Open the terminal and navigate to the newly created folder.
    - Initialize the folder for GitHub:
        ```sh
        git init
        ```
    - Connect your account to GitHub:
        ```sh
        git remote add origin https://github.com/your-username/your-repository-name.git
        ```
        Replace `your-username` and `your-repository-name` with your GitHub username and the new repository name.

3. **Create a DigitalOcean Account:**
    - If you don't have one already, create an account on DigitalOcean. You can use my referral link to receive $200 of free credit: [DigitalOcean](https://m.do.co/c/de7d99f5f217).

4. **Create a New App on DigitalOcean:**
    - Create a new app under the App Platform and name it whatever you want.
    - Cost is around $10/mon to run the aop on the server

Installation:
-------------

1. **Clone the Repository:**
    - Clone the repository into the new folder:
        ```sh
        git clone https://github.com/MatthiasT91/Robinhood-Webhook-Bot.git
        ```

2. **Navigate to the Project Folder:**
    - Go into the folder to install dependencies:
        ```sh
        cd options-bot
        ```

3. **Install Dependencies:**
    - Install the required dependencies:
        ```sh
        pip install -r requirements.txt
        ```
4. **Configure the Application:**
    - Rename the `example.ini` file to `config.ini`.
    - Fill in the fields in the file to your settings
      

5. **Run the Application:**
    - Deploy the app on DigitalOcean. This will run the Flask application, waiting for new alerts to come in.
    - To run the webhook with TradingView, you will need a paid TradingView account. Change the alert message to suit your requirements.
      

TradingView Alert Message:
--------------------------

Insert these messages into the TradingView alert message box, and then change the webhook URL in the notifications panel. Messages can be found in the **alert_options_info.txt** file.

Deployment to a New Server:
---------------------------

To deploy this application to a new server and set up webhooks from TradingView, follow these steps:

1. **Deploy the App:**
    - First, deploy it to GitHub, which will then deploy it to DigitalOcean:
        ```sh
        git add .
        git commit -m "Initial commit"
        git push -u origin master:main
        ```

2. **App created on DigitalOcean:**
    - Now you should have your new project on GitHub and on DigitalOcean.

---

**Enjoy managing your trading data with FCT's Robinhoods Options/Stock/Crypto Webhook Bot! This `README.txt` file provides clear instructions for setting up the project, configuring environment variables, installing dependencies, and deploying the application to a new server.**

**If you would like to buy me a coffee here is a few ways:**

    - PayPal - @MatthiasTovar
    - Solana (Crypto) -  E2VUz9PzabS547pxBJnFZCCDT3VtqdhnrMgyKc7ksPE7
    - ETH (Crypto) - 0xeCcDF3B9fD507bf3a7B196e093Dc7FC0114CfDb3
    -BTC (Crypto) - bc1qu06sj3z4dkllkup2ew42gh523u3usvw0p2wpk2**
