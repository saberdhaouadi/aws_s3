import boto3
client = boto3.client('ses', region_name='us-east-1')


from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
message = MIMEMultipart()
message['Subject'] = 'Weekly Cost Report in all aws managed accounts'
message['From'] = 'dhaouadis@gmail.com'
message['To'] = ', '.join(['dhaouadis@gmail.Com'])
# message body

# attachment
#else:    # if file provided
part = MIMEApplication(open('October_weekly_cost.html', 'rb').read())
part.add_header('Content-Disposition', 'attachment', filename='October_weekly_cost.html')
message.attach(part)
response = client.send_raw_email(
Source=message['From'],
Destinations=['dhaouadis@gmail.com'],
RawMessage={
    'Data': message.as_string()
    }
)

