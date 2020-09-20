import os
from jinja2 import Template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

email_template = Template(
    """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "https://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="https://www.w3.org/1999/xhtml">
<head>
<title>Test Email Sample</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<meta name="viewport" content="width=device-width, initial-scale=1.0 " />
    <style>
        img {
            width: 200px;
        }
    </style>
</head>
<body>
{% for dog in dogs %}
    <div>
        {{dog.name}}
    </div>
    <div>
        {{dog.breed}}
    </div>
    <div>
        {{dog.age}}
    </div>
    
    <div>
        <a href="{{dog.profile_url}}">
            <img src="{{dog.photo}}">
        </a>
    </div>
    <hr/>
{% endfor %}
</body>
"""
)


def email_dogs(dogs):
    if not dogs:
        print("No new dogs!")
        return
    message = Mail(
        from_email=os.environ.get("SENDER"),
        to_emails=os.environ.get("RECEIVER").split(","),
        subject="New Dogs!",
        html_content=email_template.render(dogs=dogs),
    )
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        return sg.send(message)
    except Exception as e:
        print(e.message)
