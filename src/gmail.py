# https://developers.google.com/gmail/api/quickstart/python

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import re


class InfoForm(object):
    def __init__(self):
        self.name = None
        self.phone = None
        self.email = None

    def is_valid(self):
        if not self.name:
            return False
        if not self.phone and not self.email:
            return False
        return True

    def __str__(self):
        result = '{0}  : {1}'.format('Name', self.name)
        if self.phone:
            result += '\n{0} : {1}'.format('Phone', self.phone)
        if self.email:
            result += '\n{0} : {1}'.format('Email', self.email)
        return result

    def correct_phone(self):
        if not self.phone:
            return
        match = re.match('(?P<isd>\+91)?(?P<number>[0-9]{10})', self.phone)
        if match:
            if not match.group('isd'):
                self.phone = '+91' + self.phone


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

alpha_numeric_space = '(?P<value>[ a-zA-Z0-9]*)'
numeric_plus = '(?P<value>[0-9+]*)'

pattern_list = ['(?P<token>Name)[ :]*' + alpha_numeric_space,
                '(?P<token>Phone)[ :]*' + numeric_plus,
                '(?P<token>Mobile)[ :]*' + numeric_plus,
                '(?P<token>Email)[ :]*(?P<value>[a-zA-Z0-9\.]*@[a-zA-Z0-9\.]*)',
                ]


def extract_info():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    info_form_list = []
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API
    messages_obj = service.users().messages().list(userId='me').execute()
    messages = messages_obj['messages']
    for message in messages[0:50]:
        message = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        try:
            # for header in message['payload']['headers']:
            #     print('{0} : {1}'.format(header['name'], header['value']))
            for part in message['payload']['parts']:
                msg_str = base64.urlsafe_b64decode(part['body']['data'].encode('UTF8'))
                info_form = InfoForm()
                for pattern in pattern_list:
                    match = re.search(pattern, msg_str)
                    if match:
                        if match.group('value') == '':
                            continue
                        # print '{0} : {1}'.format(match.group('token'), match.group('value'))
                        if match.group('token') == 'Name':
                            info_form.name = match.group('value')
                        if match.group('token') in ('Phone', 'Mobile'):
                            info_form.phone = match.group('value')
                        if match.group('token') == 'Email':
                            info_form.email = match.group('value')
                if info_form.is_valid():
                    info_form_list.append(info_form)

        except TypeError as e:
            print '****TypeError****'
            print e.message

    return info_form_list
