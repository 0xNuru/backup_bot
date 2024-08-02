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
from tasks.process_letter import process_letter
from tasks.reply_email import reply_email


@task
def parse():
    """Parse the email and extract relevant information"""
    item = workitems.inputs.current
    email = item.email()
    text = parse_email(item)
    workitems.outputs.create(payload={"text": text, "to_email": email.from_.address, "subject": email.subject})
    return text

@task
def process():
    """Process the extracted information and return json"""
    item = workitems.inputs.current
    text = item.payload['text']
    to_email = item.payload["to_email"]
    subject  = item.payload["subject"]
    summary = process_letter(text)
    workitems.outputs.create(payload={"text": text, "summary": summary, "to_email": to_email, "subject": subject})
    return summary

@task
def reply():
    """Reply to the email thread with the processed information"""
    item = workitems.inputs.current
    text = item.payload["text"]
    summary = item.payload["summary"]
    to_email = item.payload["to_email"]
    subject = item.payload["subject"]
    reply_email(text, summary, to_email, subject)
    return



