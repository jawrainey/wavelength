## Wavelength

Wavelength is a web application built during the [self-harmony hackathon, 2016](http://self-harmony.co.uk/).

The project provides a chat service for those with depression or anxiety to anonymously
and openly chat about their concerns or current life circumstances.

This application's novelty is through the speakers selection and association of
images to represent how they feel at a given point in time, which is used by
the `listener` as the focus, context and start of the conversation.

![Demo of application use](http://g.recordit.co/GraJTP3QM7.gif?1 "Demo of application use")


### Installing dependencies

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

### Viewing the web application.

To run the flask application server:

    python app.py

View the webpages at `http://0.0.0.0:5000/` or use your IP address to access the application externally.
