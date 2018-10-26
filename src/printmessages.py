# https://developers.google.com/gmail/api/quickstart/python

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import re

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'=' * (4 - missing_padding)
    return base64.decodestring(data)


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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
        id = message['id']
        print('<<<-------------->>>')
        message = service.users().messages().get(userId='me', id=id, format='full').execute()
        # print(pprint.pprint(message))
        try:
            # for header in message['payload']['headers']:
            #     print('{0} : {1}'.format(header['name'], header['value']))
            for part in message['payload']['parts']:
                msg_str = base64.urlsafe_b64decode(part['body']['data'].encode('UTF8'))
                # print(msg_str)
                match = re.search('Caller Name:([ a-zA-Z0-9]*)', msg_str)
                if match:
                    print(match.groups())
        except TypeError as e:
            print('****TypeError****')
            print(e.message)


if __name__ == '__main__':
    main()
