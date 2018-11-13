import sendgrid
from sendgrid.helpers.mail import *
from random import randint

from datetime import timedelta, datetime

def gen_OTP():
    otp = randint(1000, 9999)
    return otp


def send_mail(list):
    sg = sendgrid.SendGridAPIClient('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')
    mail = Mail(list[0], list[1], list[2], list[3])
    response = sg.client.mail.send.post(request_body = mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

def this_is_signup(t):
    otp = str(gen_OTP())
    subject = "Welcome to Flask Assignment"
    content = Content("text/plain", otp
                      + " this is for confirmation of your email."
                      + " go to /confirm in postman and send your username and otp in json format")
    t[1] = subject
    t[3] = content
    send_mail(t)
    return otp


def this_is_forgot(t):
    otp = str(gen_OTP())
    subject = "OTP for resetting your password"
    content = Content("text/plain", otp
                      + "  this is for confirmation of your email."
                      + "  Go to /reset in postman and send your username , otp and the new password in json format")
    t[1] = subject
    t[3] = content
    send_mail(t)
    return otp


def gen_send_otp(user, confirm):
    from_mail = Email("glanis.monteiro@robosoftin.com")
    to_mail = Email(user.email)
    t = [from_mail, " ", to_mail, ""]
    if confirm  == True:
        otp = this_is_signup(t)
    else:
        otp  = this_is_forgot(t)
    return otp

def otp_check(otp, user):
    print(str(user.otp_sent))
    print(str(datetime.now()))

    if user.otp == otp:
        if (user.otp_sent + timedelta(minutes = 30)) >= datetime.now():
            return [True, True]
        return [True, False]
    return [False, False]