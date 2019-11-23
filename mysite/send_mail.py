import os, sys
from django.core.mail import EmailMultiAlternatives,send_mail

sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == "__main__":
    # send_mail(
    #     'Django的邮件来了',
    #     'Django正文',
    #     'victor4321@163.com',
    #     ['victor321@163.com']
    # )
    subject, from_email, to = 'Django的邮件来了', 'victor4321@163.com', '583813345@qq.com'
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()