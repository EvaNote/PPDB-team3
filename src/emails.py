import smtplib
import imaplib

global sender


def send_email_signedup(email):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    send_from = 'campus.carpool.ua@gmail.com'
    password = 'campuscarpool2020'
    subject = 'Welcome to campus carpool!'

    recipient = email

    headers = ["From: " + send_from,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/plain"]
    # "Content-Type: text/html"]
    # to use html in body
    headers = "\r\n".join(headers)
    body = "Your account on Campus Carpool was successfully created! You can now log in, find rides, create rides,"
    body += " and edit your account at team3.ppdb.me!\n"
    body += "If you no longer want to receive these emails, you can turn it off in 'Edit account'.\n"
    body += "Thank you for using Campus Carpool!"

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(send_from, password)

    session.sendmail(send_from, recipient, headers + "\r\n\r\n" + body)
    session.quit()


def send_email_newpassenger(email, passenger_name, depart_time, destination):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    send_from = 'campus.carpool.ua@gmail.com'
    password = 'campuscarpool2020'
    subject = 'A passenger has joined your ride!'

    recipient = email

    headers = ["From: " + send_from,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/plain"]
    # "Content-Type: text/html"]
    # to use html in body
    headers = "\r\n".join(headers)
    body = "A new passenger, " + passenger_name + ", has joined your ride on " + depart_time + " to " + destination + "!\n"
    body += "To view this passenger's profile, go to 'My rides' and click on their profile picture. \n"
    body += "To delete your ride, go to 'My rides' and click 'Delete ride'.\n"
    body += "Thank you for using Campus Carpool!"

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(send_from, password)

    session.sendmail(send_from, recipient, headers + "\r\n\r\n" + body)
    session.quit()


def send_email_deletedride(email, depart_time, destination):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    send_from = 'campus.carpool.ua@gmail.com'
    password = 'campuscarpool2020'
    subject = 'A ride you joined has been deleted.'

    recipient = email

    headers = ["From: " + send_from,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/plain"]
    # "Content-Type: text/html"]
    # to use html in body
    headers = "\r\n".join(headers)
    body = "A ride you recently joined to " + destination + " on " + depart_time + " has been deleted by the driver.\n"
    body += "If you still need a ride, we suggest joining a new one.\n"
    body += "Thank you for using Campus Carpool!"

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(send_from, password)

    session.sendmail(send_from, recipient, headers + "\r\n\r\n" + body)
    session.quit()


def send_email_passengercancelled(email, passenger_name, depart_time, destination):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    send_from = 'campus.carpool.ua@gmail.com'
    password = 'campuscarpool2020'
    subject = 'A passenger has cancelled their involvement in your ride.'

    recipient = email

    headers = ["From: " + send_from,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/plain"]
    # "Content-Type: text/html"]
    # to use html in body
    headers = "\r\n".join(headers)
    body = "Your passenger, " + passenger_name + ", has cancelled your ride on " + depart_time + " to " + destination + ".\n"
    body += "Thank you for using Campus Carpool!"

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(send_from, password)

    session.sendmail(send_from, recipient, headers + "\r\n\r\n" + body)
    session.quit()

def send_email_review(email, review_writer):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    send_from = 'campus.carpool.ua@gmail.com'
    password = 'campuscarpool2020'
    subject = 'Someone wrote a review about you!'

    recipient = email

    headers = ["From: " + send_from,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/plain"]
    # "Content-Type: text/html"]
    # to use html in body
    headers = "\r\n".join(headers)
    body = "User " + review_writer + " has written a review about you. You can see your reviews and rating on your account page.\n"
    body += "Thank you for using Campus Carpool!"

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(send_from, password)

    session.sendmail(send_from, recipient, headers + "\r\n\r\n" + body)
    session.quit()
