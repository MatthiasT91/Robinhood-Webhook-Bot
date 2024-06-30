from robinhood.authentication import login

def rh_login():
    """
    Robinhood Login:
    username: "Your Username" - Most likely your email
    password: "Your Robinhood password to login"

    """
    logins = login(username='matthias91.mt@gmail.com', password='Mjt42391!!', expiresIn=None, scope='internal', by_sms=True, store_session=True, mfa_code=None, pickle_name='')
    
    if logins.get('access_token'):
        print("Good to go! Logged into Robinhood")
        pass

if __name__ == '__main__':
    rh_login()