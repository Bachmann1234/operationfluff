# Operation Fluff
Monitor for the latest puppy listings
 
Weekend project to email/text my wife and I when a new puppy is
listed in our area that we may be interested in

This was written to be deployed to a service
like heroku with the main method ran periodically via cron

Basically it runs and if it finds any dogs posted in the 
last X minutes (based on config, but you should set this to be similar
to the time between runs in the cron config) it will text/email the listings
based on the config.

## I wanna deploy this myself! 

Sure! I would suggest forking it and taking a look
at `dog_finder.py`. That is one place where I hardcode
some stuff you may wanna customize yourself.

Dog finder is also the thing most likely to break as its using 
a undocumented api. So if I have stopped using this expect that to get 
stale. It's fairly simple

## I want you do deploy it for me

no!

## Can you add my email/number to yours?

No, sorry. This was for me and my wife. If you want it for some reason
just fork the code and deploy it yourself. If you know me personally reach out
and we can figure something out.

# Heroku setup

This is a basic heroku on the free hobby tier. 
I have it hooked to github to deploy whenever master updates.

The app has the Heroku Scheduler addon (free tier) set to run
```
python operation_fluff/main.py
```

every 10 minutes

The configuration is a set of environment variables (look at `main.py` to see them)