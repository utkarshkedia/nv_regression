from django.shortcuts import render,redirect,HttpResponse
#from django.core.mail import send_mail
from django.contrib.auth.models import Group,User
import smtplib
from email.message import EmailMessage

# Create your views here.
def send_mail(recepient_list,current_user,is_critical):
    msg = EmailMessage()
    msg['Subject'] = 'Changes made by {} in the POR Page'.format(current_user)
    msg['From'] = 'ukedia@nvidia.com'
    msg['To'] = recepient_list
    #msg.set_content('The changed database name can be attached in the body')

    if is_critical:
        msg.__setitem__("Importance","High")

    f = open("D:\\POR_Automation\\POR\\templates\\mail_template.html",'r')
    mail_content = f.read()
    f.close()
    msg.add_alternative(mail_content.format(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),subtype='html')

    with smtplib.SMTP('outlook.office365.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        #EMAIL_PWD = os.environ.get('EMAIL_PWD')
        smtp.login('ukedia@nvidia.com', '')
        smtp.send_message(msg)

def track_modifications(response):
    if response.user.is_authenticated:
        user_email = []
        current_user = response.user.username
        if response.user.is_superuser:
            pass
        else:
            user_email.append(response.user.email)

        admin_group = Group.objects.get(name='admin')
        admin_users = admin_group.user_set.all()
        admin_emails = []
        for admin_user in admin_users:
            admin_emails.append(admin_user.email)

        recepient_emails = user_email + admin_emails
        print(recepient_emails)
        send_mail(recepient_emails,current_user,True)
        return redirect('/')
    else:
        return ('/')
