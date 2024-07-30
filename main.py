#!/usr/bin/env python3
"""This bot is going to be used to simulate the processing of discharge letters
in GPs via email

The workflow will be as follows:
- GP worker recieves email with their discharge letter
- the email is fowarded to their WA Health email (e.g minetpurple@wahealth.co.uk)
- processing is done and a reply is sent to the email thread
"""
from robocorp import workitems
from robocorp.tasks import task

from tasks.parse_email import parse_email
from tasks.process_email import process_letter
from tasks.reply_email import reply_email


@task
def parse():
    """Parse the email and extract relevant information"""
    text = parse_email()
    workitems.outputs.create(payload={"text": text})
    return text

@task
def process():
    """Process the extracted information and return json"""
    return process_letter()

@task
def reply():
    """Reply to the email thread with the processed information"""
    return reply_email()



