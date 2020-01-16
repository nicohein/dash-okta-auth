# Plotly Okta Auth

The goal of this little project is to greate a plotly dashboard that authenticates 
users with Okta.

This project is almost a copy of https://github.com/fspijkerman/dash-okta-auth
with the difference that it uses OAuth2ConsumerBlueprint because the okta blueprint 
was removed in flask_dance.

All required environment variables can be set in a .env file. Use .env.example as 
a blueprint.

Start the app using flask: 

```
flask run -h localhost -p 8080
```

