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


class Gmail(object):
    def __init__(self):
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('gmail', 'v1', http=creds.authorize(Http()))
        self.ar_input_id = self.get_label_id('ar_input')

    def get_label_id(self, label_name):
        # Label
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        ar_input_id = None
        if not labels:
            print('No labels found.')
            raise KeyError
        else:
            for label in labels:
                if label['name'] == label_name:
                    ar_input_id = label['id']
                    break
            if not ar_input_id:
                raise KeyError
        return ar_input_id

    def read_messages(self):
        # Call the Gmail API
        info_form_list = []
        alpha_numeric_space = '(?P<value>[ a-zA-Z0-9]*)'
        numeric_plus = '(?P<value>[0-9+]*)'
        pattern_list = ['(?P<token>Name)[ :]*' + alpha_numeric_space,
                        '(?P<token>Phone)[ :]*' + numeric_plus,
                        '(?P<token>Mobile)[ :]*' + numeric_plus,
                        '(?P<token>Email)[ :]*(?P<value>[a-zA-Z0-9\.]*@[a-zA-Z0-9\.]*)',
                        ]
        messages_obj = self.service.users().messages().list(userId='me').execute()
        messages = messages_obj['messages']
        for message in messages[0:100]:
            message = self.service.users().messages().get(userId='me', id=message['id'], format='full').execute()

            if self.ar_input_id not in message['labelIds']:
                continue
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
        return info_form_list
