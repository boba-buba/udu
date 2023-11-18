from wikibaseintegrator import wbi_login

#OAuth 2
login_instance = wbi_login.Login(client_id='<your_client_app_key>', client_secret='<your_client_app_secret>')

#Oauth 1.0

login_instance = wbi_login.Login(consumer_key='<your_consumer_key>', consumer_secret='<your_consumer_secret>',
                                 access_token='<your_access_token>', access_secret='<your_access_secret>')