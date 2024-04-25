import requests
import configparser
import os
import platform
import sys
from datetime import datetime, timedelta

# good library page for endpoint searching: https://docs.microsoft.com/en-us/graph/query-parameters

if platform.system() == 'Windows':
    creds_file = 'C:/Users/JO008BU/OneDrive - Pitney Bowes/Data.Analytics/OTC_OR_VM/creds.ini'
else:
    path = '/home/ftpuser/'
    if os.path.exists(path):
        creds_file = '/home/ftpuser/creds.ini'
    else:
        creds_file = '/home/admin.eng/creds.ini'

config = configparser.ConfigParser()
config.read(creds_file)
JB_USERNAME = config['PB']['username']
JB_PASSWORD = config['PB']['password']
OTIS_USERNAME = config['OTIS']['username']
OTIS_PASSWORD = config['OTIS']['password']
CLIENT_ID = config['TEAMS-GRAPH']['client_id']
CLIENT_SECRET = config['TEAMS-GRAPH']['client_secret']
TENANT_ID = config['TEAMS-GRAPH']['tenant_id']

CONTENT_TYPE = "application/json"
OTIS_ID = '33be67ea-2dad-46db-a5d9-d365a28739b7'
JB_ID = 'e22a3495-fad7-42b2-aab6-9da7bd4c46ce'
FRANCE_E_DUNNING_ID = '72e40dbe-61d7-4066-ba05-8ed24d0cc8e4'

GRAPH_API_BASE_ENDPOINT = 'https://graph.microsoft.com/v1.0'
GRAPH_API_BETA_ENDPOINT = 'https://graph.microsoft.com/beta'

TEAMS_SITE_ID_OTC_ANALYTICS_REPORTING = 'teams.pb.com,fea90d6a-8b67-4d38-afb4-0bf2bdc6e044,dc5a06cc-d04c-4381-b885-a69d8796cba2'
TEAMS_SITE_ID_USACCENTURE = 'teams.pb.com,23eaa15b-0712-4571-be05-e3330b065836,1092ecb0-b5a6-40b5-a5ba-cb866aad6924'
CASH_BILLING_LIBRARY_ID = 'b!W6HqIxIHcUW-BeMzCwZYNrDskhCmtbVApbrLhmqtaSQRdo7iQDksRo8zeaVnBFTO'
OTC_ROOT_DRIVE_ID = 'b!ag2p_meLOE2vtAvyvcbgRMwGWtxM0IFDuIWmnYeWy6IM7eYExA_tQpiYeFaSCA2z'

OTIS_INBOX_ID = 'AQMkADY4OAE5ZGYxLTU3MGUtNDkwOS1hNjBlLTNiZDk1OTc0MmQyYwAuAAADlZFRa-BkaEGq6kq1zKfx2QEAzcHitISg302iNItCN9YoPwAAAgEMAAAA'

# probably not great to search for a site_id each and every time you want to do something when it won't change so creating a dictionary of site_id's
sharepoint_sites = {
    'USAccenture': 'teams.pb.com,23eaa15b-0712-4571-be05-e3330b065836,1092ecb0-b5a6-40b5-a5ba-cb866aad6924',
    'OTC Analytics & Reporting': 'teams.pb.com,fea90d6a-8b67-4d38-afb4-0bf2bdc6e044,dc5a06cc-d04c-4381-b885-a69d8796cba2',
    'OTC Analytics & Reporting-OTIS Codebase': 'teams.pb.com,ae7db8b5-d7fc-4fe7-af69-bee2f032234e,9d7382db-081f-4dde-8fb7-4b29e3a1cfea',
    'Funding Circle-PB Partnership - Pilot': 'teams.pb.com,449abb87-fa09-47df-92e5-231b13bc889e,476c104f-d48f-471a-b756-5c7b9c807a4f',
    'Multi Location (MLO) Collaborative Team Site': 'teams.pb.com,17956a9a-7613-4a68-936f-7fed3400fffc,e1c368a1-b2a7-4cf3-9e67-d0257d5ae1ae',
    'Multi Location (MLO) Collaborative Team Site - PB Bank Use - Email Notifications': 'teams.pb.com,2ae8c51d-039a-49ca-b211-8db481f8c453,ae12d5d4-f999-49c8-b036-57340176668e',
    'eBill/ePay Project': 'teams.pb.com,6df007b9-bb13-40a1-af0b-00585278f3a2,f806665e-0e7f-449e-ab8c-f72d72582de1',
    'QIS': 'teams.pb.com,b0552a90-00ba-46c2-9bb7-b499c3504d5e,8263939d-b4d6-4ab5-8d68-76912faa95ef',
    'Wheeler Financial': 'teams.pb.com,14469d3d-37b7-4def-8de9-973eeaca83fc,dccc1fff-0075-444e-9c72-c12ccdf76365',
    'SLA Fee Reporting': 'teams.pb.com,3001ed5a-38db-4e0d-b93d-c7a4b807c33d,b2192275-efd6-4af1-97bd-96e15badb7fe',
    'Global Inventory Reporting': 'teams.pb.com,f723fafc-6aa1-49d3-85a4-c4aa87988118,36ace248-bea6-468f-b8e7-c7eec3f9905b',
    'SendTech Open Return Orders': 'teams.pb.com,680ed457-31db-4007-bd0c-a7fe0e1873a9,ca5251b8-5f04-48b6-a299-0c2402872fb6',
    'Meter Lock/Unlock Automation': 'teams.pb.com,e8afa3ce-c17b-44f9-a061-f4908f3ca999,eadb3dca-7f62-4609-9ea9-9bb4c5ce96b3',
    'Billing Experience': 'teams.pb.com,a6564495-ee98-4d3b-b431-1acdf6c917ef,349c24ef-af2c-4e93-a284-db196967f22d',
    'Global Order Management': 'teams.pb.com,6c7316af-7d82-4e00-8081-c72f31f3624e,e85cad7a-ab9a-480a-bdd4-b88b30b8404b',
    'OTC Analytics & Reporting - Presort ACH': 'teams.pb.com,8db3aeb2-d863-4b48-a212-88b16df08f4b,af4bfbdc-dc6c-4fc9-996d-2d1983522761',
    'Cancel Supercede Tracker': 'teams.pb.com,9b3340e3-45ed-44f1-8b61-7a4d1d044469,fdf6c0ff-1169-404c-aa8d-a6cb9271a5b3',
    'GEC Finance Support - Shared': 'teams.pb.com,10d5b85d-0179-4ce8-8e95-30294fe1c9ab,22aadc08-da79-47ae-9d36-55f802c7453f',
    'GEC Finance Support': '4d2f9d93-b233-4aa3-9bf6-b12e45855906', # actually a group
    'US AR OTC Operations': 'teams.pb.com,36804fbc-7fa7-4e4a-8fd5-58c5e10af859,ab74fe7c-1f76-47f2-a651-0247f707111f',
    'USAROTCOperations-05LeasingACH': 'teams.pb.com,45947f5b-17ef-45c2-b0a1-16acacdd093f,5d4f9fbf-00b1-4bdf-9c65-add16e33e2ec',
    'OTC Controls': 'teams.pb.com,4b2f9461-551c-4d22-aac1-e455ded87b5e,c228ecf2-b9dd-41fe-895e-188fa4ebb473',
    'ANALYSE DATA COLLECTION': 'teams.pb.com,3d767e53-eb1e-45ec-9967-d182154375cc,d48753bc-a890-44cb-a1ce-23f4fce024bd',
    'NIDMaster': 'teams.pb.com,4115acc1-8287-4151-a111-105eff0f6b0f,c0343ead-6585-40c6-9c9b-ef5da502b8d3',
    'Global_ERP': 'teams.pb.com,b2383772-47d5-484e-b364-089b2f3cd941,8eabd0e7-b410-4f2e-971a-006de94ff2ca',
    'Supplies Price Group Info': 'ca122666-d092-4439-aa41-55c1566093b5',
    'Contingent Labor Program': 'teams.pb.com,fe5ca8d1-cb34-400f-99c6-e3707746cd71,119d01c5-f90c-48a8-8634-667d66a1b7db',
    'Global Talent Acquisition': '057cbea7-edf1-459e-b517-2b4d438e9a1c' # group
}


def now_utc():
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    formatted_datetime = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    return formatted_datetime


def generate_random_string(length):
    import random
    import string
    # Define the characters to choose from
    characters = string.ascii_letters  # Contains all uppercase and lowercase letters

    # Generate the random string
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string


def clean_folder_path(folder_path):
    # if you get '/folder/other_folder/' it will produce 'folder/other_folder'
    if folder_path[:1] == '/':
        folder_path = folder_path[1:]
    if folder_path[-1:] == '/':
        folder_path = folder_path[:-1]
    return folder_path


def get_headers(bearer_token, content_type=None):
    """This is the headers for the Microsoft Graph API calls"""
    # "Content-Type": "application/json; charset=utf-8"
    if content_type is not None:
        return {
            "Content-Type": content_type,
            "Authorization": f"Bearer {bearer_token}",
            # "ConsistencyLevel": "eventual",
        }
    return {
        "Accept": CONTENT_TYPE,
        "Authorization": f"Bearer {bearer_token}",
        #"ConsistencyLevel": "eventual",
    }


def get_token(user):
    if user.upper() == 'OTIS':
        username = OTIS_USERNAME
        password = OTIS_PASSWORD
    elif user.upper() == 'JORDAN':
        username = JB_USERNAME
        password = JB_PASSWORD
    else:
        print(f'user {user} is not currently configured so we cannot retrieve a token')
        return None

    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

    payload = (
        f"grant_type=password&client_id={CLIENT_ID}&username={username}&password={password}"
        "&scope=User.Read"
    )
    headers = {}

    resp = requests.request("POST", url, headers=headers, data=payload)
    # print(resp.json())
    if resp.status_code != 200:
        return None
    return resp.json()["access_token"]


# currently not a single use case for application level tokens, need to authenticate a user to get delegated permissions
# def get_token_for_client_application(client_id, client_secret, tenant_id):
def get_token_for_client_application():
    """
    Get Token on behalf of a client application using client_secret/client_id
    """
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

    payload = (
        f"grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
        "&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default"
    )

    headers = {}

    resp = requests.request("POST", url, headers=headers, data=payload)
    if resp.status_code != 200:
        return None
    return resp.json()["access_token"]


def graph_get(user, endpoint, value_level=True):
    bearer_token = get_token(user)
    url = f'{GRAPH_API_BASE_ENDPOINT}{endpoint}'
    # if search_terms is not None:
    #     url = f'{url}'
    # print(url)
    resp = requests.get(url, headers=get_headers(bearer_token))
    if resp.status_code in [200, 201]:
        resp_json = resp.json()
        if value_level:
            values = resp_json['value']
        else:
            values = resp_json
        return values
    else:
        print(f'{endpoint} returned a status code of {resp.status_code}')
        print(f'json payload was:\n{resp.json()}')
        return False


def get_teams_user_data(email):
    bearer_token = get_token_for_client_application()
    url = f'{GRAPH_API_BASE_ENDPOINT}/users?$filter=mail eq \'{email}\''
    resp = requests.get(url, headers=get_headers(bearer_token))
    if resp.status_code == 200:
        resp_json = resp.json()
        # {
        #     "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#users",
        #     "value": [
        #         {
        #             "businessPhones": [
        #                 "+1 (203) 4507433"
        #             ],
        #             "displayName": "Paul Frese",
        #             "givenName": "Paul",
        #             "jobTitle": "Mgr_web Design & Software Program",
        #             "mail": "paul.frese@pb.com",
        #             "mobilePhone": "+1 203-450-7433",
        #             "officeLocation": "US CT Shelton",
        #             "preferredLanguage": "None",
        #             "surname": "Frese",
        #             "userPrincipalName": "paul.frese@pb.com",
        #             "id": "40664edc-5b06-4da0-aebe-9e5591c59348"
        #         }
        #     ]
        # }
        if len(resp_json['value']) > 0:
            return resp_json['value'][0]
        else:
            print(f'API call successful but {email} could not be found to retrieve an ID\nmy call returned a response of:\n{resp_json}')
            return False
    print(f'api returned status code of {resp.status_code}')
    return False


def extract_to_email(headers_string):
    # maybe enhance later to feed headers string and then return specific components but for now, this will be required to determine which smtp email address a message was sent to
    import re
    # pattern = r'To: (.+?@.+?\.\w{2,})'
    pattern = r'To: .*<(.+?@.+?\.\w{2,})>'
    match = re.search(pattern, headers_string, re.IGNORECASE)

    if match:
        to_email = match.group(1)
        return to_email.lower()
    else:
        return None



def get_given_name(email):
    user_data = get_teams_user_data(email)
    # print(f'user_data is {user_data}')
    if not user_data:
        return None
    # {'businessPhones': [], 'displayName': 'NationalSalesSupport', 'givenName': None, 'jobTitle': None, 'mail': 'nss@pb.com', 'mobilePhone': None, 'officeLocation': None, 'preferredLanguage': None, 'surname': None, 'userPrincipalName': 'nss@pb.com', 'id': 'f2ab2462-e464-488c-aba6-0dcea44e7d70'}
    if 'givenName' in user_data:
        given_name = user_data['givenName']
        if given_name is not None:
            return given_name
        else:
            return user_data['displayName']
    return None


def get_teams_user_id(email):
    user_data = get_teams_user_data(email)
    if user_data:
        user_id = user_data['id']
        return user_id
    else:
        return False


def get_signedin_user_data(user):
    if user.upper() == 'OTIS':
        user_id = OTIS_ID
    elif user.upper() == 'JORDAN':
        user_id = JB_ID
    else:
        print(f'user {user} is not currently configured so we cannot get signed in user data')
        return None
    bearer_token = get_token(user)
    # resp = requests.get(f"https://graph.microsoft.com/v1.0/me", headers=get_headers(bearer_token))
    resp = requests.get(f"https://graph.microsoft.com/v1.0/users/{user_id}", headers=get_headers(bearer_token))

    json_resp = resp.json()
    return json_resp


def build_recipients(recipients):
    list = []
    for recipient in recipients:
        list.append({"emailAddress": {"address": recipient}})
    return list


def handle_attachment(file, add_id=False):
    if not os.path.exists(file):
        print(f'file {file} was not found')
        return False
    import base64
    with open(file, 'rb') as upload:
        file_content = base64.b64encode(upload.read())
    data_body = {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": os.path.basename(file),
        "contentBytes": file_content.decode('utf-8')
    }
    if add_id:
        data_body["contentId"] = generate_random_string(16)
    return data_body


def prep_file_for_upload(file):
    if not os.path.exists(file):
        print(f'file {file} was not found')
        return False
    with open(file, 'rb') as upload:
        file_content = upload.read()
    file_name = os.path.basename(file)
    data_body = {
        'item': {
            'name': file_name
        }
    }
    return file_content, data_body


def send_email(user, to_recipients, subject, message, cc_recipients=None, bcc_recipients=None, attachments=None, content_type=None):
    if user.upper() == 'OTIS':
        user_id = OTIS_ID
    elif user.upper() == 'JORDAN':
        user_id = JB_ID
    else:
        print(f'user {user} is not currently configured so we cannot get signed in user data')
        return None
    bearer_token = get_token(user)
    post_url = f'https://graph.microsoft.com/v1.0/users/{user_id}/sendMail'

    to_list = build_recipients(to_recipients)
    message = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": message
            },
            "toRecipients": to_list
        }
    }
    if cc_recipients is not None:
        cc_list = build_recipients(cc_recipients)
        message['message']['ccRecipients'] = cc_list
    if bcc_recipients is not None:
        bcc_list = build_recipients(bcc_recipients)
        message['message']['bccRecipients'] = bcc_list
    if attachments is not None:
        attachments_payload = []
        for attachment in attachments:
            attachment_json = handle_attachment(attachment)
            attachments_payload.append(attachment_json)
        message['message']['attachments'] = attachments_payload

    resp = requests.post(post_url, headers=get_headers(bearer_token, content_type=content_type), json=message)
    if resp.status_code not in [200, 201, 202]:
        return resp.status_code
    if resp.status_code in [202]:
        return f'Email has been sent to {to_recipients}'
    return resp


def send_email_with_inline_images(user, to_recipients, subject, message, inline_images, cc_recipients=None, bcc_recipients=None, attachments=None, content_type=None):
    if user.upper() == 'OTIS':
        user_id = OTIS_ID
    elif user.upper() == 'JORDAN':
        user_id = JB_ID
    else:
        print(f'user {user} is not currently configured so we cannot get signed in user data')
        return None
    bearer_token = get_token(user)
    post_url = f'https://graph.microsoft.com/v1.0/users/{user_id}/sendMail'

    to_list = build_recipients(to_recipients)
    message = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": message
            },
            "toRecipients": to_list
        }
    }
    # this works...
    # message_body = {
    #    "message": {
    #       "subject": "test subject",
    #       "body": {
    #          "contentType": "HTML",
    #          "content": "<html><body><p>here is an image:</p></br><img src='cid:pb_logo_image' /></body></html>"
    #       },
    #       "toRecipients": [
    #          {
    #             "emailAddress": {
    #                "address": "jordan.buser@pb.com"
    #             }
    #          }
    #       ],
    #       "attachments": [
    #          {
    #             "@odata.type": "#microsoft.graph.fileAttachment",
    #             "name": "pb-logo.png",
    #             "contentBytes": "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",
    #             "contentId": "pb_logo_image"
    #          }
    #       ]
    #    }
    # }

    if cc_recipients is not None:
        cc_list = build_recipients(cc_recipients)
        message['message']['ccRecipients'] = cc_list
    if bcc_recipients is not None:
        bcc_list = build_recipients(bcc_recipients)
        message['message']['bccRecipients'] = bcc_list

    attachments_payload = []
    inline_images_dict = {}
    for inline_image in inline_images:
        attachment_json = handle_attachment(inline_image, add_id=True)
        # builds the dictionary because the image src needs to be replaced in the message body
        inline_images_dict[inline_image] = attachment_json['contentId']
        attachments_payload.append(attachment_json)
    # print(inline_images_dict)
    # {'/home/admin.eng/python/dump/pb-logo.png': 'OcKfsIHGyOvrpood'}
    for find, replace in inline_images_dict.items():
        # print(f'find {find} replace with {replace}')
        message['message']['body']['content'] = message['message']['body']['content'].replace(find, replace)
    message['message']['attachments'] = attachments_payload
    # print(message)

    resp = requests.post(post_url, headers=get_headers(bearer_token, content_type=content_type), json=message)
    if resp.status_code not in [200, 201, 202]:
        return resp.status_code
    if resp.status_code in [202]:
        return f'Email has been sent to {to_recipients}'
    return resp


def reply_or_forward_email(user, email_id, comment, action, to_recipients=None, cc_recipients=None, bcc_recipients=None, attachments=None):
    bearer_token = get_token(user)
    acceptable_actions = ['reply', 'replyAll', 'forward']
    if action not in acceptable_actions:
        print(f'action of {action} not configured, acceptable values are {acceptable_actions}')
        return False
    url = f'{GRAPH_API_BASE_ENDPOINT}/me/messages/{email_id}/{action}'

    post_body = {
            "comment": comment
    }
    if action.lower() in ['reply', 'replyall']:
        post_body['message'] = {}
    if to_recipients is not None:
        to_list = build_recipients(to_recipients)
        if action.lower() == 'reply':
            post_body['message']['toRecipients'] = to_list
        else:
            post_body['toRecipients'] = to_list
    if cc_recipients is not None:
        cc_list = build_recipients(cc_recipients)
        if action.lower() in ['reply', 'replyall']:
            post_body['message']['ccRecipients'] = cc_list
        # else:
        #     post_body['toRecipients'] = cc_list
    if bcc_recipients is not None:
        bcc_list = build_recipients(bcc_recipients)
        if action.lower() == 'reply':
            post_body['message']['bccRecipients'] = bcc_list
        # else:
        #     post_body['toRecipients'] = to_list
    if attachments is not None:
        attachments_payload = []
        for attachment in attachments:
            attachment_json = handle_attachment(attachment)
            attachments_payload.append(attachment_json)
        if action in ['forward', 'replyAll']:
            post_body['message'] = {}
        post_body['message']['attachments'] = attachments_payload
    resp = requests.post(url, headers=get_headers(bearer_token), json=post_body)
    if resp.status_code in [202]:
        return True
    else:
        print(resp.json())
        return False


def get_email_ids(user, sender, subject, has_attachments=True, subject_contains=True, date_time_start='2022-01-01T00:00:00Z', date_time_end=None, sort_order='DESC', folder_name=None, user_id=None, client_app=False, top=10, multiple_senders=False, check_inline=False):
    if user.upper() == 'OTIS' and user_id is None:
        user_id = OTIS_ID
    elif user.upper() == 'JORDAN' and user_id is None:
        user_id = JB_ID
    elif user_id is None:
        print(f'user {user} is not currently configured so we cannot get signed in user data')
        return None
    if has_attachments and not check_inline:
        has_attachments_insert = ' and hasAttachments eq true'
    else:
        has_attachments_insert = ''
    if subject_contains:
        subject_insert = f" and contains(subject, '{subject}')"
    else:
        subject_insert = f" and subject eq '{subject}'"
    if len(subject) == 0:
        subject_insert = ''
    if client_app:
        bearer_token = get_token_for_client_application()
    else:
        bearer_token = get_token(user)
    if date_time_end is None:
        date_time_end = now_utc()
    if multiple_senders:
        filter_conditions = [f"from/emailAddress/address eq '{email}'" for email in sender]
        filter_query = ' or '.join(filter_conditions)
        sender_insert = f"({filter_query})"
    else:
        sender_insert = f"contains(from/emailAddress/address, '{sender}')"

    if folder_name is not None:
        folder_id = __get_mail_folder_id(user, folder_name) # ?$top=50&
        get_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/mailFolders/{folder_id}/messages?$top={top}&$orderby=receivedDateTime {sort_order}&$filter=receivedDateTime ge {date_time_start} and receivedDateTime lt {date_time_end} and {sender_insert}{subject_insert}{has_attachments_insert}&$select=receivedDateTime,from,subject,bodyPreview,id"
    else:
        get_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/mailFolders/inbox/messages?$top={top}&$orderby=receivedDateTime {sort_order}&$filter=receivedDateTime ge {date_time_start} and receivedDateTime lt {date_time_end} and {sender_insert}{subject_insert}{has_attachments_insert}&$select=receivedDateTime,from,subject,bodyPreview,id"
    # print(get_url)
    resp = requests.get(get_url, headers=get_headers(bearer_token))
    json_resp = resp.json()
    # print(json_resp)
    # BEGIN ADDED CODE #
    if "@odata.nextLink" in json_resp:
        next_link = json_resp['@odata.nextLink']
        iter_list = []
        iter_list = iter_list + json_resp['value']
        while next_link:
            resp = requests.get(next_link, headers=get_headers(bearer_token))
            this_json = resp.json()
            iter_list = iter_list + this_json['value']
            if "@odata.nextLink" in this_json:
                next_link = this_json['@odata.nextLink']
            else:
                next_link = None
    elif 'value' in json_resp:
        iter_list = json_resp['value']
    else:
        iter_list = []
    if len(iter_list) > 0:
        print(f"i found {len(iter_list)} email(s)!")
        return_list = []
        for email in iter_list:
            id = email['id']
            return_list.append(id)
        return return_list
    else:
        return False
    # END ADDED CODE #
    # if 'value' in json_resp:
    #     if len(json_resp['value']) > 0:
    #         print(f"i found {len(json_resp['value'])} email(s)!")
    #         return_list = []
    #         for email in json_resp['value']:
    #             id = email['id']
    #             return_list.append(id)
    #         return return_list
    #     else:
    #         # print(f'i found no emails from {sender} with a subject {subject} where subject_contains was {subject_contains} has_attachments was {has_attachments}')
    #         return False
    # else:
    #     return False


#     if "@odata.nextLink" in json_resp:
#         next_link = json_resp['@odata.nextLink']
#         iter_list = []
#         iter_list = iter_list + json_resp['value']
#         while next_link:
#             resp = requests.get(next_link, headers=get_headers(bearer_token))
#             this_json = resp.json()
#             iter_list = iter_list + this_json['value']
#             if "@odata.nextLink" in this_json:
#                 next_link = this_json['@odata.nextLink']
#             else:
#                 next_link = None
#     else:
#         iter_list = json_resp['value']
#
#     if len(iter_list) > 0:
#         for folder in iter_list:
#             if folder['displayName'] == folder_name:
#                 return folder['id']
#     print(f'folder {folder_name} could not be found underneath parent folder {parent_folder}')
#     return False



def get_emails_by_conversation_id(user, conversation_id, date_time_start='2022-01-01T00:00:00Z', fields=None):
    bearer_token = get_token(user)
    url = f'{GRAPH_API_BASE_ENDPOINT}/me/mailFolders/inbox/messages?$orderby=receivedDateTime DESC&$filter=receivedDateTime ge {date_time_start} and conversationId eq \'{conversation_id}\''
    resp = requests.get(url, headers=get_headers(bearer_token))
    try:
        json_resp = resp.json()
        if len(json_resp["value"]) > 0:
            if fields is not None:
                need_separate_call = False
                for field in fields:
                    if field not in json_resp["value"][0]: #caller requested specific fields and the field they requested is not in the standard payload for at least the first email
                        need_separate_call = True
                if need_separate_call:
                    return_list = []
                    for email in json_resp["value"]:
                        email_id = email['id']
                        email_details = get_email_details(user, email_id, fields=fields)
                        return_list.append(email_details)
                    return return_list

            return json_resp["value"]
        else:
            return False
    except:
        return False


def get_email_unique_body(user, email_id):
    # /me/messages/AAMkAGQ0ZGZhM2ZiLWE1YzgtNDlmNC04OGI3LTc2NTg0NWM1YjYyMQBGAAAAAAAPrRJzocsHSY1ZRDVORFfnBwAO4-wZenpjSZiG66J7I39lAFz9EGygAAAN6Lhf5n4-TJpKEiRfCBUxAATiH-_iAAA=?$select=uniqueBody
    bearer_token = get_token(user)
    url = f'{GRAPH_API_BASE_ENDPOINT}/me/messages/{email_id}?$select=uniqueBody'
    resp = requests.get(url, headers=get_headers(bearer_token))
    try:
        json_resp = resp.json()
        # print(json_resp)
        if 'uniqueBody' in json_resp:
            # print(json_resp["value"])
            return json_resp["uniqueBody"]["content"]
        else:
            return False
    except:
        return False


def get_mail_folder_id(user, folder_name, parent_folder='Inbox'):
    bearer_token = get_token(user)
    url = f'{GRAPH_API_BASE_ENDPOINT}/me/mailFolders/{parent_folder}/childFolders'
    resp = requests.get(url, headers=get_headers(bearer_token))
    json_resp = resp.json()

    if "@odata.nextLink" in json_resp:
        next_link = json_resp['@odata.nextLink']
        iter_list = []
        iter_list = iter_list + json_resp['value']
        while next_link:
            resp = requests.get(next_link, headers=get_headers(bearer_token))
            this_json = resp.json()
            iter_list = iter_list + this_json['value']
            if "@odata.nextLink" in this_json:
                next_link = this_json['@odata.nextLink']
            else:
                next_link = None
    else:
        iter_list = json_resp['value']

    if len(iter_list) > 0:
        for folder in iter_list:
            if folder['displayName'] == folder_name:
                return folder['id']
    print(f'folder {folder_name} could not be found underneath parent folder {parent_folder}')
    return False


def move_emails_to_folder(user, email_ids, folder):
    bearer_token = get_token(user)
    responses = []
    new_ids = {}
    if email_ids is None:
        return False
    for email_id in email_ids:
        url = f'{GRAPH_API_BASE_ENDPOINT}/me/messages/{email_id}/move'
        # print(f'trying url {url}')
        payload = {
            "destinationId": folder
        }
        resp = requests.post(url, headers=get_headers(bearer_token), json=payload)
        resp_json = resp.json()
        if 'id' not in resp_json:
            print(f'id not in response, which was:\n{resp_json}')
            return False
        new_ids[email_id] = resp_json['id']
        responses.append(resp.status_code)
    if all(response == 201 for response in responses):
        print(f'all {len(email_ids)} emails were moved')
        return new_ids
    else:
        return False


def mark_emails_read(user, email_ids):
    bearer_token = get_token(user)
    #headers = get_headers(bearer_token)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {bearer_token}'
        }
    #print(headers)
    if not email_ids:
        return False
    for email_id in email_ids:
        url = f'{GRAPH_API_BASE_ENDPOINT}/me/messages/{email_id}'
        payload = {
            "isRead": True
        }
        resp = requests.patch(url, json=payload, headers=headers)
        if resp.status_code == 201:
            return True
        else:
            return False


def delete_emails(user, email_ids):
    bearer_token = get_token(user)
    response_codes = []
    if email_ids:
        for email_id in email_ids:
            url = f'{GRAPH_API_BASE_ENDPOINT}/me/messages/{email_id}'
            resp = requests.delete(url, headers=get_headers(bearer_token))
            if resp.status_code == 204:
                print('email deleted!')
                response_codes.append(resp.status_code)
        if all(response == 204 for response in response_codes):
            print(f'all {len(email_ids)} emails were deleted')
            return True
        else:
            print(f'at least one of the {len(email_ids)} could not be deleted')
            return False
    return False


def check_sent_mail(user, subject, subject_contains=True, date_time_start='2022-01-01T00:00:00Z'):
    if user.upper() == 'OTIS':
        user_id = OTIS_ID
    elif user.upper() == 'JORDAN':
        user_id = JB_ID
    else:
        print(f'user {user} is not currently configured so we cannot get signed in user data')
        return None
    if subject_contains:
        subject_insert = f"contains(subject, '{subject}')"
    else:
        subject_insert = f"subject eq '{subject}'"
    bearer_token = get_token(user)
    get_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/mailFolders/SentItems/messages?$orderby=receivedDateTime DESC&$filter=receivedDateTime ge {date_time_start} and {subject_insert}&$select=receivedDateTime,from,subject,bodyPreview,id"
    # print(get_url)
    resp = requests.get(get_url, headers=get_headers(bearer_token))
    json_resp = resp.json()
    if len(json_resp['value']) > 0:
        print(f"i found {len(json_resp['value'])} email(s)!")
        return_list = []
        for email in json_resp['value']:
            id = email['id']
            return_list.append(id)
        return return_list
    else:
        print(f'i found no sent emails with a subject {subject} where subject_contains was {subject_contains}')
        return False


def get_email_attachments(user, email_ids, local_folder, return_ids=False, allowed_extensions=None):
    import time
    if allowed_extensions is not None:
        from pathlib import Path
        allowed_extensions = [item.lower() for item in allowed_extensions]
    bearer_token = get_token(user)
    return_list = []
    return_dict = {}
    if not email_ids:
        # print('no email_ids provided')
        return False
    for email_id in email_ids:
        get_url = f"{GRAPH_API_BASE_ENDPOINT}/me/messages/{email_id}/attachments"
        resp = requests.get(get_url, headers=get_headers(bearer_token))
        json_resp = resp.json()
        # print(json_resp)
        #
        if len(json_resp['value']) > 0:
            return_dict_list = []
            print('message has at least one attachment')
            for attachment in json_resp['value']:
                file_name = attachment['name']
                if allowed_extensions is not None:
                    file_extension = Path(file_name).suffix
                    if file_extension.lower() not in allowed_extensions:
                        continue
                if file_name == 'ATP Scan In Progress':
                    print('attachment is in ATP scan, returning false')
                    return False
                id = attachment['id']
                attachment_url = f'{GRAPH_API_BASE_ENDPOINT}/me/messages/{email_id}/attachments/{id}/$value'
                attachment_content = requests.get(attachment_url, headers=get_headers(bearer_token))
                now = round(time.time() * 1000)
                file_name = f'{now}_{file_name}'
                print(f'saving file {file_name} to {local_folder}')
                with open(os.path.join(local_folder, file_name), 'wb') as _f:
                    _f.write(attachment_content.content)
                saved_file = local_folder + file_name
                return_list.append(saved_file)
                return_dict_list.append(saved_file)
            if len(return_dict_list) > 0:
                return_dict[email_id] = return_dict_list

    if len(return_list) > 0:
        if(return_ids):
            return return_dict
        else:
            return return_list
    return False


def find_email_attachments_that_are_emails(user, sender, subject, subject_contains=True, date_time_start='2022-01-01T00:00:00Z', sort_order='DESC'):
    bearer_token = get_token(user)
    email_ids = get_email_ids(user, sender, subject, subject_contains=subject_contains, date_time_start=date_time_start, sort_order=sort_order)
    if email_ids:
        return_dict = {}
        for email_id in email_ids:
            url = f'{GRAPH_API_BASE_ENDPOINT}/me/messages/{email_id}/attachments'
            resp = requests.get(url, headers=get_headers(bearer_token))
            resp_json = resp.json()
            attachments = resp_json['value']
            if len(attachments) > 0:
                for attachment in attachments:
                    if attachment['@odata.type'] == '#microsoft.graph.itemAttachment':
                        attachment_id = attachment['id']
                        return_dict[email_id] = attachment_id
        return return_dict
    else:
        return False


def __get_email_attachments_from_attached_emails(user, email_id_attachment_id_dict, local_folder):
    import base64
    bearer_token = get_token(user)
    if local_folder[-1:] == '/':
        local_folder = local_folder[:-1]
    return_list =[]
    for email_id_attachment_id in email_id_attachment_id_dict:
        email_id = email_id_attachment_id
        attachment_id = email_id_attachment_id_dict[email_id_attachment_id]
        url = f'{GRAPH_API_BASE_ENDPOINT}/me/messages/{email_id}/attachments/{attachment_id}/?$expand=microsoft.graph.itemattachment/item'
        resp = requests.get(url, headers=get_headers(bearer_token))
        resp_json = resp.json()
        attachments = resp_json['item']['attachments']
        for attachment in attachments:
            file_name = attachment['name']
            file_bytes = attachment['contentBytes']
            print(f'saving {file_name} to {local_folder}')
            with open(os.path.join(local_folder, file_name), 'wb') as _f:
                _f.write(base64.b64decode(file_bytes))
            return_list.append(f'{local_folder}/{file_name}')
    return return_list


def get_email_attachments_from_attached_emails(user, sender, subject, local_folder, subject_contains=True, date_time_start='2022-01-01T00:00:00Z', sort_order='DESC', archive_folder=None):
    dictionary = find_email_attachments_that_are_emails(user, sender, subject, subject_contains=subject_contains, date_time_start=date_time_start, sort_order=sort_order)
    email_ids = []
    for email_id in dictionary:
        email_ids.append(email_id)
    return_list = __get_email_attachments_from_attached_emails(user, dictionary, local_folder)
    mark_emails_read(user, email_ids)
    if archive_folder is not None:
        folder_id = get_mail_folder_id(user, archive_folder)
        move_emails_to_folder(user, email_ids, folder_id)
    return return_list


def get_email_attachments_search(user, sender, subject, local_folder, subject_contains=True, archive_folder=None, mark_read=True, return_ids=False, multiple_senders=False, top=10, allowed_extensions=None, date_time_start='2022-01-01T00:00:00Z', check_inline=False):
    email_ids = get_email_ids(user, sender, subject, subject_contains=subject_contains, multiple_senders=multiple_senders, top=top, date_time_start=date_time_start, check_inline=check_inline)
    email_attachments = get_email_attachments(user, email_ids, local_folder, return_ids=return_ids, allowed_extensions=allowed_extensions)
    if not email_attachments:
        return False
    if mark_read:
        mark_emails_read(user, email_ids)
    if archive_folder is not None:
        archive_folder_id = get_mail_folder_id(user, archive_folder, parent_folder='Inbox')
        # {'ORIGINAL_ID': 'ARCHIVED_ID', 'ORIGINAL_ID': 'ARCHIVED_ID'}
        new_ids_dict = move_emails_to_folder(user, email_ids, archive_folder_id)
        if return_ids:
            archive_return_dict = {}
            for old_id, new_id in new_ids_dict.items():
                archive_return_dict[new_id] = email_attachments[old_id]
            return archive_return_dict

    return email_attachments


def archive_emails(user, message_ids, archive_folder):
    mark_emails_read(user, message_ids)
    archive_folder_id = get_mail_folder_id(user, archive_folder, parent_folder='Inbox')
    return_dict = move_emails_to_folder(user, message_ids, archive_folder_id)
    return return_dict


def get_email_details(user, email_id, fields=None, return_alias=False): #uniqueBody,from
    bearer_token = get_token(user)
    if fields is not None:
        # $expand=singleValueExtendedProperties($filter=id eq 'String 0x007D')
        fields_str = ','.join(fields)
        url = f'{GRAPH_API_BASE_ENDPOINT}/me/messages/{email_id}?$select={fields_str}'
    else:
        url = f'{GRAPH_API_BASE_ENDPOINT}/me/messages/{email_id}'
    if return_alias:
        url = f"{GRAPH_API_BASE_ENDPOINT}/me/messages/{email_id}?$expand=singleValueExtendedProperties($filter=id eq 'String 0x007D')"
    resp = requests.get(url, headers=get_headers(bearer_token))
    resp_json = resp.json()
    if return_alias:
        message_headers = resp_json["singleValueExtendedProperties"][0]["value"]
        sent_to_alias = extract_to_email(message_headers)
        resp_json["sent_to_alias"] = sent_to_alias
    returnable = resp_json

    return returnable


def get_email_body(user, email_ids):
    return_dict = {}
    if email_ids:
        for email_id in email_ids:
            resp_json = get_email_details(user, email_id)
            email_body = resp_json['body']['content']
            return_dict[email_id] = email_body
    return return_dict


def get_email_body_search(user, sender, subject, subject_contains=True, archive_folder=None, mark_read=False, date_time_start='2022-01-01T00:00:00Z', date_time_end=None, sort_order='DESC', multiple_senders=False):
    if date_time_end is None:
        date_time_end = now_utc()
    email_ids = get_email_ids(user, sender, subject, has_attachments=False, subject_contains=subject_contains, date_time_start=date_time_start, date_time_end=date_time_end, sort_order=sort_order, multiple_senders=multiple_senders)
    email_bodies = get_email_body(user, email_ids)
    return email_bodies


def get_mime_content(user, email_id):
    bearer_token = get_token(user)
    url = f'{GRAPH_API_BASE_ENDPOINT}/me/messages/{email_id}/$value'
    resp = requests.get(url, headers=get_headers(bearer_token))
    resp_mime = resp.content
    #resp_json = resp.json()
    return resp_mime


def __get_mail_folder_id(user, folder_name, parent_folder='Inbox'):
    bearer_token = get_token(user)
    if parent_folder=='Inbox':
        parent_folder_id = OTIS_INBOX_ID
    else:
        print(f'parent folder of {parent_folder} not configured')
        return False
    url = f'{GRAPH_API_BASE_ENDPOINT}/me/mailFolders/{parent_folder_id}/childFolders' #/me/mailFolders/{id}/childFolders
    resp = requests.get(url, headers=get_headers(bearer_token))
    resp_json = resp.json()
    if 'value' in resp_json:
        for folder in resp_json['value']:
            if folder['displayName'].upper() == folder_name.upper():
                return folder['id']
    print(f'Folder {folder_name} not found under parent folder {parent_folder}')
    return False


def get_calendar_invites(user, sort_order='ASC'): # (user, calendar_user):
    # print('*******************************************************WARNING*******************************************************')
    # print('THIS FUNCTION CANNOT BE MEANINGFULLY FILTERED ON DATE/TIME AND THERE IS NO NEXTLINK FROM GRAPH, PROCEED WITH CAUTION!')
    # if calendar_user.upper() == 'OTIS':
    #     user_id = OTIS_ID
    # elif calendar_user.upper() == 'JORDAN':
    #     user_id = JB_ID
    # else:
    #     raise Exception(f'user {user} is not currently configured so we cannot get signed in user data')  # &$orderby=receivedDateTime {sort_order}
    bearer_token = get_token(user)
    url = f'{GRAPH_API_BASE_ENDPOINT}/me/mailFolders/inbox/messages?$filter=microsoft.graph.eventMessage/jMessageType eq \'meetingRequest\''
    # end_point = f'/users/{user_id}/mailFolders/inbox/messages?$filter=microsoft.graph.eventMessage/meetingMessageType eq \'meetingRequest\''
    resp = requests.get(url, headers=get_headers(bearer_token))
    json_resp = resp.json()
    # print(json_resp)
    if '@odata.nextLink' in json_resp:
        next_link = json_resp['@odata.nextLink']
        iter_list = []
        iter_list = iter_list + json_resp['value']
        while next_link:
            resp = requests.get(next_link, headers=get_headers(bearer_token))
            this_json = resp.json()
            iter_list = iter_list + this_json['value']
            if '@odata.nextLink' in this_json:
                next_link = this_json['@odata.nextLink']
            else:
                next_link = None
    elif 'value' in json_resp:
        iter_list = json_resp['value']
    else:
        iter_list = []
    print(f'api call returned {len(iter_list)} results')
    return iter_list


def get_online_meeting_ids(meeting_url, user='OTIS'):
    url = f"/me/onlineMeetings?$filter=JoinWebUrl%20eq%20'{meeting_url}'"
    online_meetings = graph_get(user, url, value_level=True)
    return_list = []
    for online_meeting in online_meetings:
        online_meeting_id = online_meeting["id"]
        return_list.append(online_meeting_id)
    return return_list


#def get_email_body_search
# get mime content -> GET /users/{id}/messages/{id}/$value (documentation https://docs.microsoft.com/en-us/graph/outlook-get-mime-message)

# -------------SHAREPOINT FUNCTIONS BELOW------------- #

def get_sharepoint_site_id(user, site_name):
    # SHOULD NOT BE USING THIS IN A PROGRAM AS GENERATING A TOKEN AND GETTING A SITE_ID EACH TIME SEEMS WASTEFUL, SHOULD ONLY USE MANUALLY TO POPULATE STATIC DICTIONARY OF SITE_ID'S
    bearer_token = get_token(user)
    url = f'{GRAPH_API_BASE_ENDPOINT}/sites?search={site_name}'
    resp = requests.get(url, headers=get_headers(bearer_token))
    json_resp = resp.json()
    print(json_resp)
    values = json_resp['value']
    list = []
    if len(values) > 0:
        # if len(values) > 1:
        #     raise ValueError(
        #         f'Site name search of {site_name} returned {len(values)} results and this function is only meant to return one site_id')
        # else:
        return json_resp
        for value in values:
            list.append(value['id'])
        return list
    else:
        return None


def get_sharepoint_drive_id(user, site_id, root_folder='Documents', endpoint_type='sites'):
    bearer_token = get_token(user)
    # added endpoint_type to enable downloading from groups, the process is the same you just have to get the drive_id associated with the group using the /groups/ endpoint so defaulting to sites (99% of jobs) but enabling specifying groups
    url = f'{GRAPH_API_BASE_ENDPOINT}/{endpoint_type}/{site_id}/drives'
    # print(url)
    resp = requests.get(url, headers=get_headers(bearer_token))
    json_resp = resp.json()
    # print(f'\n\ntrying for site_id {site_id}\n\n')
    # print(json_resp)
    # print('\n\n')
    values = json_resp['value']
    for value in values:
        if value['name'] == root_folder:
            documents_folder_id = value['id']
            return documents_folder_id
    return None


def get_sharepoint_root_item_ids(user, site_id, drive_id):
    bearer_token = get_token(user)
    url = f'{GRAPH_API_BASE_ENDPOINT}/sites/{site_id}/drives/{drive_id}/root/children'
    resp = requests.get(url, headers=get_headers(bearer_token))
    json_resp = resp.json()
    values = json_resp['value']
    return_dict = {}
    for value in values:
        folder_name = value['name']
        folder_id = value['id']
        return_dict[folder_name] = folder_id
    return return_dict


def _get_sharepoint_folder_contents(user, drive_id, path):
    bearer_token = get_token(user)
    url = f'{GRAPH_API_BASE_ENDPOINT}/drives/{drive_id}/root:/{path}:/children'
    resp = requests.get(url, headers=get_headers(bearer_token))
    if resp.status_code not in [200, 201, 202]:
        print(resp.json())
        return None
    json_resp = resp.json()
    # print(json_resp)
    values = json_resp['value']
    return_dict = {}
    rd = []
    for value in values:
        name = value['name']
        id = value['id']
        web_uri = value['webUrl']
        rd_d = {}
        rd_d['file_name'] = name
        rd_d['id'] = id
        rd_d['web_uri'] = web_uri
        if 'folder' in value:
            rd_d['is_folder'] = True
        else:
            rd_d['is_folder'] = False
        rd.append(rd_d)
        return_dict[name] = id
    # print(rd)
    return rd


def get_sharepoint_folder_contents(user, site, path, root_folder = 'Documents'):
    drive_id = get_sharepoint_drive_id(user, sharepoint_sites[site], root_folder=root_folder)
    rd = _get_sharepoint_folder_contents(user, drive_id, path)
    return rd


def get_sharepoint_file_id(user, drive_id, path, file_name):
    # print(f'trying {user}|{drive_id}|{path}')
    files = _get_sharepoint_folder_contents(user, drive_id, path)
    # print(files)
    if files is not None:
        for file in files:
            if file['file_name'] == file_name:
                return file['id'], file['web_uri']
    else:
        return None


def get_sharepoint_file_ids(user, drive_id, path):
    files = _get_sharepoint_folder_contents(user, drive_id, path)
    if files is not None:
        return_files = {}
        for file in files:
            if not file['is_folder']:
                return_files[file['file_name']] = file['id']
        return return_files
    else:
        return None


def get_sharepoint_file_uri(user, sharepoint_site, sharepoint_path, file_name, root_folder='Documents'):
    drive_id = get_sharepoint_drive_id(user, sharepoint_sites[sharepoint_site], root_folder)
    file_id, web_uri = get_sharepoint_file_id(user, drive_id, sharepoint_path, file_name)
    return web_uri


def download_sharepoint_file_int(user, drive_id, file_id, file_name, local_path, local_file_name=None):
    if local_file_name is None:
        local_file_name = file_name
    bearer_token = get_token(user)
    url = f'{GRAPH_API_BASE_ENDPOINT}/drives/{drive_id}/items/{file_id}/content'
    response_file_content = requests.get(url, headers=get_headers(bearer_token))
    with open(os.path.join(local_path, local_file_name), 'wb') as _f:
        _f.write(response_file_content.content)


def download_sharepoint_file(user, sharepoint_site, file_name, sharepoint_folder_path, local_path, root_folder='Documents', local_file_name=None, endpoint_type='sites'):
    if local_file_name is None:
        local_file_name = file_name
    sharepoint_folder_path = clean_folder_path(sharepoint_folder_path)
    drive_id = get_sharepoint_drive_id(user, sharepoint_sites[sharepoint_site], root_folder, endpoint_type=endpoint_type)
    # print(f'drive id is {drive_id} path is {sharepoint_folder_path} and file name is {file_name}')
    file_id, web_uri = get_sharepoint_file_id(user, drive_id, sharepoint_folder_path, file_name)
    if file_id is not None:
        try:
            download_sharepoint_file_int(user, drive_id, file_id, file_name, local_path, local_file_name=local_file_name)
            return True
        except:
            errorCode = str(sys.exc_info()[0]).replace("<class '", "").replace("'>", "")
            errorCode = errorCode.replace("'", r"\'")
            errorDesc = str(sys.exc_info()[1]).replace("<class '", "").replace("'>", "")
            errorDesc = errorDesc.replace("'", r"\'")
            print(f"local file could not be saved with error code of {errorCode} and description {errorDesc}")
            return f'download failed for {file_name} to {local_path}'
    else:
        return f'File {file_name} not found in path {sharepoint_folder_path} on site {sharepoint_site}'


def download_sharepoint_files(user, sharepoint_site, sharepoint_folder_path, local_path, root_folder='Documents', endpoint_type='sites'):
    """
    used if you want to download all files in a directory
    """
    sharepoint_folder_path = clean_folder_path(sharepoint_folder_path)
    drive_id = get_sharepoint_drive_id(user, sharepoint_sites[sharepoint_site], root_folder, endpoint_type=endpoint_type)
    # print(f'drive id is {drive_id}')
    # print(f'drive id is {drive_id} path is {sharepoint_folder_path} and file name is {file_name}')
    # file_id, web_uri = get_sharepoint_file_id(user, drive_id, sharepoint_folder_path, file_name)
    file_dict = get_sharepoint_file_ids(user, drive_id, sharepoint_folder_path)
    # print(f'file dict is {file_dict}')
    if file_dict is not None:
        files = []
        for key, value in file_dict.items():
            file_name = key
            file_id = value
            download_sharepoint_file_int(user, drive_id, file_id, file_name, local_path)
            files.append(file_name)
        return files
    else:
        return []


def get_file_session_info(user, site, site_path, file_name, root_folder='Documents'):
    bearer_token = get_token(user)
    site_path = clean_folder_path(site_path)
    site_id = sharepoint_sites[site]
    drive_id = get_sharepoint_drive_id(user, site_id, root_folder)
    file_id, web_uri = get_sharepoint_file_id(user, drive_id, site_path, file_name)
    #url = f'{GRAPH_API_BASE_ENDPOINT}/drives/{drive_id}/items/{file_id}/workbook/sessions'
    url = f'{GRAPH_API_BASE_ENDPOINT}/drives/{drive_id}/root:/{site_path}:/workbook/worksheets'
    response = requests.get(url, headers=get_headers(bearer_token))
    print(f'url is {url}')
    if response:
        print(response)
        resp_json = response.json()
        return resp_json
    else:
        print(f'call to {url} failed and response was as follows\n')
        print(response)
        return response


def does_file_exist(user, file_name, sharepoint_folder_path, sharepoint_site, root_folder='Documents', drive_id=None):
    sharepoint_folder_path = clean_folder_path(sharepoint_folder_path)
    if drive_id is None:
        drive_id = get_sharepoint_drive_id(user, sharepoint_sites[sharepoint_site], root_folder)
    if get_sharepoint_file_id(user, drive_id, sharepoint_folder_path, file_name):
        file_id, web_uri = get_sharepoint_file_id(user, drive_id, sharepoint_folder_path, file_name)
        return file_id
    return False


def get_drive_item_id(user, site_name, drive_item_path):
    site_id = sharepoint_sites[site_name]
    bearer_token = get_token(user)
    url = f"{GRAPH_API_BASE_ENDPOINT}/sites/{site_id}/drive/root:/{drive_item_path}"
    # /sites/{site-id}/drive/root:/{item-path}
    resp = requests.get(url, headers=get_headers(bearer_token))
    return resp.json()["id"]


def check_file_in_out(user, site_name, path, file_name, action, file_id=None):
    # site_id = get_site_id(site_name)
    site_id = sharepoint_sites[site_name]
    bearer_token = get_token(user)
    # drive_id = get_sharepoint_drive_id(user, site_id)
    # drive_item_id = get_sharepoint_file_id(user, drive_id, path, file_name)
    file_path = f'{path}/{file_name}'
    if file_id is None:
        drive_item_id = get_drive_item_id(user, site_name, file_path)
    else:
        drive_item_id = file_id
    if action.lower() not in ['checkin', 'checkout']:
        raise ValueError(f'action of {action} not configured')
    url = f"{GRAPH_API_BASE_ENDPOINT}/sites/{site_id}/drive/items/{drive_item_id}/{action.lower()}"
    # /sites/{siteId}/drive/items/{itemId}/checkout
    resp = requests.post(url, headers=get_headers(bearer_token))
    if action.lower() == 'checkout':
        return resp.status_code == 204
    else:
        return resp


# def check_in_file(user, site_name, file_path):
#     # site_id = get_site_id(site_name)
#     site_id = sharepoint_sites[site_name]
#     bearer_token = get_token(user)
#
#     drive_item_id = get_drive_item_id(site_name, file_path)
#
#     url = (
#         f"{GRAPH_API_BASE_ENDPOINT}/sites/{site_id}/drive/items/{drive_item_id}/checkin"
#     )
#     resp = requests.post(url, headers=get_headers(bearer_token))
#     return resp


def __upload_small_file(user, local_path, sharepoint_path, drive_id, remote_file_name):
    bearer_token = get_token(user)
    if remote_file_name is None:
        file_name = os.path.basename(local_path)
    else:
        file_name = remote_file_name
    with open(local_path, 'rb') as upload:
        media_content = upload.read()
    url = f'{GRAPH_API_BASE_ENDPOINT}/drives/{drive_id}/root:/{sharepoint_path}/{file_name}:/content'
    upload_response = requests.put(url, data=media_content, headers=get_headers(bearer_token))
    response = upload_response.json()
    return response


def __upload_large_file(user, local_path, sharepoint_path, drive_id, print_progress, remote_file_name):
    sharepoint_path = clean_folder_path(sharepoint_path)
    bearer_token = get_token(user)
    if remote_file_name is None:
        file_name = os.path.basename(local_path)
    else:
        file_name = remote_file_name
    request_body = {
        "@microsoft.graph.conflictBehavior": "replace",
        "name": file_name
    }
    url = f'{GRAPH_API_BASE_ENDPOINT}/drives/{drive_id}/root:/{sharepoint_path}/{file_name}:/createUploadSession'
    resp = requests.post(url, headers=get_headers(bearer_token), json=request_body)
    resp_json = resp.json()
    response_payload = None
    try:
        upload_url = resp_json['uploadUrl']
        with open(local_path, 'rb') as f:
            total_file_size = os.path.getsize(local_path)
            chunk_size = 2376640
            chunk_number = total_file_size // chunk_size
            chunk_leftover = total_file_size - chunk_size * chunk_number
            i = 0
            while True:
                chunk_data = f.read(chunk_size)
                start_index = i * chunk_size
                end_index = start_index + chunk_size
                if not chunk_data:
                    break
                if i == chunk_number:
                    end_index = start_index + chunk_leftover
                headers = {'Content-Length': '{}'.format(chunk_size),
                           'Content-Range': 'bytes {}-{}/{}'.format(start_index, end_index - 1, total_file_size)}
                chunk_data_upload = requests.put(upload_url, data=chunk_data, headers=headers)
                if chunk_data_upload.status_code in [200, 201]:
                    response_payload = chunk_data_upload.json()
                if print_progress:
                    progress = round((end_index / total_file_size) * 100)
                    print(f'upload is {progress}% complete')
                i = i + 1
        if response_payload is not None:
            return response_payload
        else:
            return None
    except Exception as e:
        print(e)
        return None


def upload_sharepoint_file(user, local_path, sharepoint_path, sharepoint_site, root_folder='Documents', print_progress=False, remote_file_name=None, drive_id=None):
    # added this because drive_id needs to be specified when uploading to a private channel
    if drive_id is None:
        drive_id = get_sharepoint_drive_id(user, sharepoint_sites[sharepoint_site], root_folder)
    file_size = os.path.getsize(local_path)
    four_megs = 4 * 1024 * 1024
    if file_size < four_megs:
        print('uploading small file')
        response = __upload_small_file(user, local_path, sharepoint_path, drive_id, remote_file_name)
    else:
        print(f'uploading large file of {file_size}')
        response = __upload_large_file(user, local_path, sharepoint_path, drive_id, print_progress, remote_file_name)
    try:
        web_url = response['webUrl']
        return web_url
    except:
        return False


def delete_sharepoint_file(user, file_name, sharepoint_site, sharepoint_path, root_folder='Documents', drive_id=None):
    sharepoint_path = clean_folder_path(sharepoint_path)
    if drive_id is None:
        drive_id = get_sharepoint_drive_id(user, sharepoint_sites[sharepoint_site], root_folder)
    site_id = sharepoint_sites[sharepoint_site]
    bearer_token = get_token(user)
    # file_id = '01H746ITGD2XHHQRRHPBCKXVM2CL5CYQWZ' # temporarily - the ID of the SFDC List file in sandbox/Processed
    # print(f'{user} {drive_id} {sharepoint_path} {file_name}')
    file_id, file_uri = get_sharepoint_file_id(user, drive_id, sharepoint_path, file_name)
    url = f'{GRAPH_API_BASE_ENDPOINT}/sites/{site_id}/drive/items/{file_id}'
    resp = requests.delete(url, headers=get_headers(bearer_token))
    if resp.status_code == 204:
        return True
    else:
        return False


def get_groups(user):
    bearer_token = get_token(user)
    url = f'{GRAPH_API_BASE_ENDPOINT}/me/joinedTeams'
    resp = requests.get(url, headers=get_headers(bearer_token))
    return resp.json()


def get_group_drive_id(user, group):
    bearer_token = get_token(user)
    group_id = sharepoint_sites[group]
    url = f'{GRAPH_API_BASE_ENDPOINT}/groups/{group_id}/drive' #
    resp = requests.get(url, headers=get_headers(bearer_token))
    return resp.json()


def get_group_drive_item_id(user, group, path):
    bearer_token = get_token(user)
    group_id = sharepoint_sites[group]
    url = f'{GRAPH_API_BASE_ENDPOINT}/groups/{group_id}/drive/root:/{path}'
    resp = requests.get(url, headers=get_headers(bearer_token))
    return resp.json()


def create_group_folder(user, group, parent_item_id, folder_name):
    bearer_token = get_token(user)
    group_id = sharepoint_sites[group]
    url = f'{GRAPH_API_BASE_ENDPOINT}/groups/{group_id}/drive/items/{parent_item_id}/children'
    post_body = {
      "name": folder_name,
      "folder": { },
      "@microsoft.graph.conflictBehavior": "replace"
    }
    resp = requests.post(url, headers=get_headers(bearer_token), json=post_body)
    # if resp.status_code not in [200, 201, 202]:
    #     return resp.status_code
    return resp

#--------------CHAT FUNCTIONS BELOW------------------


def get_ms_teams_users(bearer_token, filters=""):
    """
    Get/Search MS Teams users
    """
    if filters:
        filters = f"$filter={filters}"

    url = f"https://graph.microsoft.com/beta/users?{filters}"
    resp = requests.get(url, headers=get_headers(bearer_token))
    if resp.status_code != 200:
        print(resp.json())
        return None

    json_resp = resp.json()
    try:
        return json_resp["value"]
    except KeyError as err:
        return []


def create_chat_id(bearer_token, sender_ms_team_id, user_ms_teams_id):
    creat_chat_url = "https://graph.microsoft.com/v1.0/chats"
    data = {
        "chatType": "oneOnOne",
        "members": [
            {
                "@odata.type": "#microsoft.graph.aadUserConversationMember",
                "roles": ["owner"],
                "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{user_ms_teams_id}')",
            },
            {
                "@odata.type": "#microsoft.graph.aadUserConversationMember",
                "roles": ["owner"],
                "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{sender_ms_team_id}')",
            },
        ],
    }

    resp = requests.post(creat_chat_url, headers=get_headers(bearer_token), json=data)
    json_resp = resp.json()
    if resp.status_code not in [200, 201]:
        return False
    chat_id = json_resp["id"]
    return chat_id


def send_chat_message(user, recipient_id, message, chat_id=None):
    bearer_token = get_token(user)
    if user.upper() == 'OTIS':
        user_id = OTIS_ID
    elif user.upper() == 'JORDAN':
        user_id = JB_ID
    else:
        print(f'user {user} is not currently configured so we cannot get signed in user data')
        return False
    if chat_id is None:
        chat_id = create_chat_id(bearer_token, user_id, recipient_id)
    url = f'{GRAPH_API_BASE_ENDPOINT}/chats/{chat_id}/messages'
    json_payload = {"body": {"contentType": "html", "content": message}}
    resp = requests.post(url, headers=get_headers(bearer_token), json=json_payload)
    if resp.status_code in [200, 201]:
        print(f'successfully sent chat message: \'{message}\'')
        return_dict = {}
        resp_json = resp.json()
        return_dict['message_id'] = resp_json['id']
        return_dict['message_date'] = resp_json['createdDateTime']
        return_dict['message_last_modified_date'] = resp_json['lastModifiedDateTime']
        return_dict['chat_id'] = chat_id
        return_dict['message'] = message
        return_dict['sent_by_id'] = user_id
        return return_dict
    else:
        print(f'api rejected message with status code of {resp.status_code}')
        return False



def send_chat_message_by_chat_id(user, chat_id, message):
    bearer_token = get_token(user)
    url = f'{GRAPH_API_BASE_ENDPOINT}/chats/{chat_id}/messages'
    json_payload = {"body": {"contentType": "html", "content": message}}
    resp = requests.post(url, headers=get_headers(bearer_token), json=json_payload)
    if resp.status_code in [200, 201]:
        print(f'successfully sent chat message: \'{message}\' to chat {chat_id}')
        resp_json = resp.json()
        print(resp_json)
        return chat_id
    else:
        print(f'api rejected message with status code of {resp.status_code}')
        return False


def get_messages_in_chat(user, chat_id, summarized=False, date_time_start='2023-01-01T00:00:00Z'):
    bearer_token = get_token(user)
    #not expecting to ever have more than 50 messages for surveying, even if this happens assume we will have handled and stored messages beyond 50 and API returns newest first
    url = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages?$top=50&$filter=lastModifiedDateTime gt {date_time_start}"
    # get_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/mailFolders/{folder_id}/messages?$orderby=receivedDateTime {sort_order}&$filter=receivedDateTime ge {date_time_start} and contains(from/emailAddress/address, '{sender}') and {subject_insert}{has_attachments_insert}&$select=receivedDateTime,from,subject,bodyPreview,id"
    #data = {"body": {"contentType": "html", "content": message}}
    resp = requests.get(url, headers=get_headers(bearer_token))
    # print(url)
    # https://graph.microsoft.com/v1.0/chats/19:33be67ea-2dad-46db-a5d9-d365a28739b7_e22a3495-fad7-42b2-aab6-9da7bd4c46ce@unq.gbl.spaces/messages?$filter=createdDateTime gt 2023-01-01T00:00:00Z
    # https://graph.microsoft.com/v1.0/chats/19:2da4c29f6d7041eca70b638b43d45437@thread.v2/messages?$top=2&$orderBy=lastModifiedDateTime desc&$filter=lastModifiedDateTime gt 2022-09-22T00:00:00.000Z and lastModifiedDateTime lt 2022-09-24T00:00:00.000Z
    if resp.status_code == 200:
        json_resp = resp.json()
        return json_resp
    else:
        print(f'api returned status code {resp.status_code}')
        print(f'json payload is {resp.json()}')
        return False

    # if resp.status_code not in [200, 201]:
    #     return False
    # messages = json_resp['value']
    # if summarized:
    #     messages = format_messages(messages)
    #
    # return messages

def get_chats(user):
    bearer_token = get_token(user)
    url = f"https://graph.microsoft.com/v1.0/chats/"
    resp = requests.get(url, headers=get_headers(bearer_token))
    print(resp)
    json_resp = resp.json()
    if resp.status_code not in [200, 201]:
        return False
    return json_resp


def send_message_to_ms_teams_user(user, sender_ms_team_id, user_ms_teams_id, message):
    """
    Send Message to MS Teams user is done in 2 steps:
        1: Create chat
        2: Use chat-id created in 1st step and send message to the user.
    """
    # 1st step: Create chat
    # creat_chat_url = "https://graph.microsoft.com/v1.0/chats"
    # data = {
    #     "chatType": "oneOnOne",
    #     "members": [
    #         {
    #             "@odata.type": "#microsoft.graph.aadUserConversationMember",
    #             "roles": ["owner"],
    #             "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{user_ms_teams_id}')",
    #         },
    #         {
    #             "@odata.type": "#microsoft.graph.aadUserConversationMember",
    #             "roles": ["owner"],
    #             "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{sender_ms_team_id}')",
    #         },
    #     ],
    # }
    #
    # resp = requests.post(
    #     creat_chat_url, headers=get_headers(bearer_token), json=data)
    # json_resp = resp.json()
    # if resp.status_code not in [200, 201]:
    #     return False
    #
    # # 2nd step: Use created chat-id and send message to it.
    # chat_id = json_resp["id"]
    bearer_token = get_token(user)
    chat_id = create_chat_id(bearer_token, sender_ms_team_id, user_ms_teams_id)
    print(f'chat_id is {chat_id}')
    send_message_url = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages"

    message_data = {"body": {"contentType": "html", "content": message}}
    resp = requests.post(send_message_url, headers=get_headers(
        bearer_token), json=message_data)
    json_resp = resp.json()
    if resp.status_code not in [200, 201]:
        return False

    return chat_id


def send_question_to_ms_teams_user(bearer_token, sender_ms_team_id, user_ms_teams_id, message):
    chat_id = create_chat_id(bearer_token, sender_ms_team_id, user_ms_teams_id)
    print(f'chat_id is {chat_id}')
    send_message_url = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages"

    message_data = {"body": {"contentType": "html", "content": message}}

    question_data = {
        "subject": None,
        "body": {
            "contentType": "html",
            "content": "<attachment id=\"74d20c7f34aa4a7fb74e2b30004247c5\"></attachment>"
        },
        "attachments": [
            {
                "id": "74d20c7f34aa4a7fb74e2b30004247c5",
                "contentType": "application/vnd.microsoft.card.thumbnail",
                "contentUrl": None,
                "content": "{"
                           "\"title\": \"Please rate your experience\","
                           "\"subtitle\": \"<h3>Onboarding - ordering a new hire PC</h3>\","
                           "\"text\": \"Please select your rating\","
                           "\"buttons\": "
                           "   ["
                           "       {"
                           "           \"type\": \"messageBack\","
                           "           \"title\": \"0 - it's really bad\","
                           "           \"text\": \"0\","
                           "           \"displayText\": \"0\","
                           "           \"value\": \"0\""
                           "       }"
                           "   ]"
                           "}",
                "name": None,
                "thumbnailUrl": None
            }
        ]
    }
    #                         "       {"
    #                         "           \"type\": \"messageBack\","
    #                         "           \"title\": \"0 - it's so bad I wish I could rate you negative\","
    #                         "           \"text\": \"0\","
    #                         "           \"displayText\": \"0\","
    #                         "           \"value\": \"0\""
    #                         "       }"
    #                        "type": 'Action.Submit',
    #                     "title": '0 - it is so bad I wish I could rate you negative',
    #                     "data": {
    #                         "msteams": {
    #                             "type": "imBack",
    #                             "value": "0 - yuck!"
    #                         }
    #                     }

    resp = requests.post(send_message_url, headers=get_headers(bearer_token), json=question_data)
    json_resp = resp.json()
    print(json_resp)
    if resp.status_code not in [200, 201]:
        return False
    return chat_id


def get_ms_teams_users_using_emails(bearer_token, emails=[]):
    filters = [f"mail eq '{email}'" for email in emails]
    filters = " OR ".join(filters)
    users = get_ms_teams_users(bearer_token, filters=filters)

    return users


def format_messages(message_list):
    return_list = []
    for message in message_list:
        message_dict = {}
        message_dict['message_id'] = message['id']
        message_dict['sent_by_id'] = message['from']['user']['id']
        message_dict['message'] = message['body']['content']
        return_list.append(message_dict)
    return return_list


# def get_chats(bearer_token):
#     url = f"https://graph.microsoft.com/v1.0/chats/"
#     resp = requests.get(url, headers=get_headers(bearer_token))
#     json_resp = resp.json()
#     if resp.status_code not in [200, 201]:
#         return False
#     return json_resp


# def get_messages_in_chat(bearer_token, chat_id, summarized=False):
#     url = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages"
#     # data = {"body": {"contentType": "html", "content": message}}
#     resp = requests.get(url, headers=get_headers(bearer_token))
#     json_resp = resp.json()
#     if resp.status_code not in [200, 201]:
#         return False
#     messages = json_resp['value']
#     if summarized:
#         messages = format_messages(messages)
#
#     return messages


def get_calendar_entries(user, start_datetime, end_datetime, filters=None, selects=None, unresponded=False, tease_boundaries=False):
    bearer_token = get_token(user)
    if filters is not None:
        # filters_insert = f' and {filters}'
        filters_insert = filters
    else:
        filters_insert = ''
    if selects is not None:
        selects_insert = f'&$select={selects}'
    else:
        selects_insert = ''
    # datetime format is 2023-08-09T12:00:00Z
    if tease_boundaries:
        def offset_seconds(timestamp, offset):
            input_datetime = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
            time_offset = timedelta(seconds=offset)
            new_datetime = input_datetime + time_offset
            new_timestamp = new_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
            return new_timestamp


        start_datetime = offset_seconds(start_datetime, 1)
        end_datetime = offset_seconds(end_datetime, -1)
        # print(f'start started at {start_datetime} but is now {new_start} after the offset')
        # print(f'end_ms started at {end_datetime} but is now {new_end} after the offset')

    url = f'{GRAPH_API_BASE_ENDPOINT}/me/calendarview?startdatetime={start_datetime}&enddatetime={end_datetime}&$filter={filters_insert}' #&$select=id,subject,isReminderOn,isCancelled
    # https://graph.microsoft.com/v1.0/me/events?$filter=start/DateTime lt 2023-08-09T13:30:00.000Z
    #date/time format is for some unknowable reason 2023-08-07T09:00:00Z vs. standard
    # url = f'{GRAPH_API_BASE_ENDPOINT}/me/events?$filter=start/DateTime le \'{end_datetime}\' and end/DateTime ge \'{start_datetime}\'{filters_insert}{selects_insert}' #&$select=id,subject,isReminderOn,isCancelled
    # print(url)
    resp = requests.get(url, headers=get_headers(bearer_token))
    # print(resp.json())
    if resp.status_code == 200:
        resp_json = resp.json()

        if '@odata.nextLink' in resp_json:
            next_link = resp_json['@odata.nextLink']
            iter_list = []
            iter_list = iter_list + resp_json['value']
            while next_link:
                resp = requests.get(next_link, headers=get_headers(bearer_token))
                this_json = resp.json()
                iter_list = iter_list + this_json['value']
                if '@odata.nextLink' in this_json:
                    next_link = this_json['@odata.nextLink']
                else:
                    next_link = None
        elif 'value' in resp_json:
            iter_list = resp_json['value']
        else:
            iter_list = []
        if unresponded:
            print('unresponded is on and unfortunately there is no way to filter the graph call on notResponded')
            iter_list = [item for item in iter_list if item['responseStatus']['response'] == 'notResponded']
            # for item in iter_list:
            #     if item['responseStatus']['response'] != 'none' or item['responseStatus']['response'] is not None:
            #

        print(f'api call returned {len(iter_list)} results')
        return iter_list
    else:
        print(f'api returned status code of {resp.status_code} and payload was:\n{resp.json()}')
        print('remember date/time format is for some unknowable reason 2023-08-07T09:00:00Z')
        return False


def respond_to_invite(user, calendar_user, action, event_id, comment='', send_response=True, proposed_start=None, proposed_end=None, proposed_time_zone='UTC'):
    bearer_token = get_token(user)
    if calendar_user.upper() == 'OTIS':
        calendar_user_id = OTIS_ID
    elif calendar_user.upper() == 'JORDAN':
        calendar_user_id = JB_ID
    else:
        raise Exception(f'calendar user {calendar_user} not currently configured')
    configured_actions = ['tentativelyAccept', 'accept', 'decline']
    if action not in configured_actions:
        raise Exception(f'action of {action} not configured')
    # url = f'{GRAPH_API_BASE_ENDPOINT}/users/{calendar_user_id}/events/{event_id}/{action}'
    url = f'{GRAPH_API_BASE_ENDPOINT}/me/events/{event_id}/{action}'
    json_payload = {
        "comment": comment,
        "sendResponse": send_response
    }
    if proposed_start is not None and proposed_end is not None:
        json_payload['proposedNewTime'] = {
            "start": {
                "dateTime": proposed_start,
                "timeZone": proposed_time_zone
            },
            "end": {
                "dateTime": proposed_end,
                "timeZone": proposed_time_zone
            }
        }
    resp = requests.post(url, headers=get_headers(bearer_token), json=json_payload)
    if resp.status_code in [202]:
        print(f'meeting invite successfully {action}ed')
        return True
    print(resp)
    return None
    # {
    #   "comment": "I won't be able to make this week. How about next week?",
    #   "sendResponse": true,
    #   "proposedNewTime": {
    #       "start": {
    #           "dateTime": "2019-12-02T18:00:00",
    #           "timeZone": "Pacific Standard Time"
    #       },
    #       "end": {
    #           "dateTime": "2019-12-02T19:00:00",
    #           "timeZone": "Pacific Standard Time"
    #       }
    #   }
    # }


def add_calendar_reminder(user, event_ids):
    bearer_token = get_token(user)
    for event_id in event_ids:
        url = f'{GRAPH_API_BASE_ENDPOINT}/me/events/{event_id}'
        json_payload = {
            "reminderMinutesBeforeStart": 15,
            "isReminderOn": True
        }
        resp = requests.patch(url, json=json_payload, headers=get_headers(bearer_token))
        if resp.status_code == 200:
            print(f'calendar entry {event_id} updated')
        else:
            print(f'calendar entry {event_id} was not updated, api returned status code of {resp.status_code}')


def get_transcripts(meeting_id, user='OTIS', save_to_local=None):
    def transcript_to_json(transcript, keep_time_stamps=False):
        import re
        # transcript = """
        # WEBVTT\r\n\r\n00:00:02.374 --> 00:00:02.774\r\n<v Jordan Buser>Scribing.</v>\r\n\r\n00:00:07.404 --> 00:00:09.954\r\n<v Jordan Buser>So as I talk, do you see the transcription window?</v>\r\n\r\n00:00:11.344 --> 00:00:12.844\r\n<v Kacper Borowiecki>And now I will.</v>\r\n\r\n
        # """
        ts_pattern = r'\d{2}:\d{2}:\d{2}\.\d{3}'
        all_timestamps = re.findall(ts_pattern, transcript)
        if all_timestamps:
            last_timestamp = all_timestamps[-1]
        else:
            last_timestamp = None
        transcript = transcript[13:]
        if not keep_time_stamps:
            timestamp_pattern = r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\r\n'
            transcript = re.sub(timestamp_pattern, '', transcript)
        else:
            raise ValueError('transcript_to_json in library_utils has not been configured to handle timestamps yet')
        transcript = transcript.replace('\r\n\r\n', '\r\n')
        line_pattern = r'<v (.*?)>(.*?)</v>'
        transcript_list = []
        for line in transcript.split('\r\n'):
            result_dict = {}
            match = re.search(line_pattern, line)
            if match:
                name = match.group(1)
                text = match.group(2)
                result_dict["person"] = name
                result_dict["text"] = text
                transcript_list.append(result_dict)
        return transcript_list, last_timestamp


    def calculate_total_timestamp(timestamps):
        # print(f'calculating for {timestamps}')
        import datetime
        total_duration = datetime.timedelta()
        for timestamp in timestamps:
            # Split the timestamp into hours, minutes, seconds
            timestamp = timestamp[:8]
            h, m, s = map(int, timestamp.split(':'))

            # Create a timedelta for each timestamp
            timestamp_duration = datetime.timedelta(hours=h, minutes=m, seconds=s)
            # Add the timedelta to the total duration
            total_duration += timestamp_duration
        # Convert the total duration back to a string in the desired format
        total_timestamp = str(total_duration)

        return total_timestamp


    bearer_token = get_token(user)
    url = f'{GRAPH_API_BETA_ENDPOINT}/me/onlineMeetings/{meeting_id}/transcripts'
    resp = requests.get(url, headers=get_headers(bearer_token))
    if resp.status_code == 200:
        resp_json = resp.json()
        if len(resp_json['value']) > 0:
            import io
            from docx import Document
            content_list = []
            transcripts = resp_json['value']
            for transcript in transcripts:
                transcript_id = transcript["id"]
                transcript_url = f'{GRAPH_API_BETA_ENDPOINT}/me/onlineMeetings/{meeting_id}/transcripts/{transcript_id}/content?$format=text/vtt'
                transcript_call_header = get_headers(bearer_token, content_type='text/vtt')
                del transcript_call_header['Content-Type']
                transcript_resp = requests.get(transcript_url, headers=transcript_call_header)
                transcript_content = transcript_resp.content.decode('utf-8')
                content_list.append(transcript_content)
                print(f'transcript content is {transcript_content}')
            return_list = []
            timestamps = []
            file_buffer = io.BytesIO()
            doc = Document()
            # print(f'content list is {content_list}')
            for content in content_list:
                content_dict, last_timestamp = transcript_to_json(content)
                return_list = return_list + content_dict
                timestamps.append(last_timestamp)
                doc.add_paragraph(content)
            doc.save(file_buffer)
            file_buffer.seek(0)
            if save_to_local is not None:
                with open(save_to_local, 'wb') as f:
                    f.write(file_buffer.read())
            # if len(timestamps) > 1:
                # there were multiple transcripts in the meeting
            return_ts = calculate_total_timestamp(timestamps)
            return return_list, return_ts
        else:
            print('no transcripts found')
            return None, 'NO TRANSCRIPTS'
    else:
        print(f'api returned status code of {resp.status_code}')
        return None, None


def get_presence(user, person, sending_id=False):
    if sending_id:
        person_id = person
    else:
        person_id = get_teams_user_id(person)
    if person_id:
        endpoint = f'/users/{person_id}/presence'
        presence_payload = graph_get(user, endpoint, value_level=False)
        # print(presence_payload)
        if presence_payload:
            return presence_payload['availability']
        else:
            return False
    else:
        print(f'could not get an id for {person}')
        return False

def set_presence(user, presence, duration_hours=1):
    bearer_token = get_token(user)
    if user.upper() == 'OTIS':
        user_id = OTIS_ID
    elif user.upper() == 'JORDAN':
        user_id = JB_ID
    else:
        print(f'user {user} is not currently configured so we cannot get signed in user data')
        return None
    url = f'{GRAPH_API_BASE_ENDPOINT}/users/{user_id}/presence/setPresence'
    availability_dict = {
        'Available': 'Available',
        'Busy': 'InACall',
        'Away': 'Away'
    }
    if not presence in availability_dict:
        print(f'presence of {presence} not supported')
        return False
    # duration...
    # The value is represented in ISO 8601 format for durations. If not provided, a default expiration of 5 minutes will be applied. The valid duration range is 5-240 minutes (PT5M to PT4H)
    if not duration_hours in [1, 2, 3, 4]:
        print(f'duration hours of {duration_hours} not supported. Microsoft limits presence duration expiration of 4 hours')
        return False
    elif duration_hours < 4:
        duration_insert = '1M'
    else:
        duration_insert = ''
    json_payload = {
        "sessionId": CLIENT_ID,
        "availability": presence,
        "activity": availability_dict[presence],
        "expirationDuration": f"PT{duration_hours}H{duration_insert}"
    }
    resp = requests.post(url, headers=get_headers(bearer_token), json=json_payload)
    if resp.status_code == 200:
        print('status successfully updated')
        return True
    else:
        resp_json = resp.json()
        print(resp_json)
        return False


# ---------------------------------------------------------------------------------------------------------------------
# Sharepoint List Functions
# ---------------------------------------------------------------------------------------------------------------------
def get_column_translation(user, site_name, list_name, mode="name_to_displayName"):
    bearer_token = get_token(user)
    # site_id = get_site_id(site_name)
    url = f"{GRAPH_API_BASE_ENDPOINT}/sites/{sharepoint_sites[site_name]}/lists/{list_name}/columns"
    resp = requests.get(url, headers=get_headers(bearer_token))
    resp = resp.json()["value"]

    # column_translation = [x for x in resp if x["name"].startswith("field_")]
    column_translation = [
        x
        for x in resp
        if not x["readOnly"]
    ]

    if mode == "name_to_displayName":
        column_translation = {x["name"]: x["displayName"] for x in column_translation}
    if mode == "displayName_to_name":
        column_translation = {x["displayName"]: x["name"] for x in column_translation}
    return column_translation


def get_list_items(user, site_name, list_name, fields, as_data_frame=False):
    import pandas as pd
    bearer_token = get_token(user)
    url = f"{GRAPH_API_BASE_ENDPOINT}/sites/{sharepoint_sites[site_name]}/lists/{list_name}/items?expand=fields"
    resp = requests.get(url, headers=get_headers(bearer_token))
    json = resp.json()

    if "@odata.nextLink" in json:
        next_link = json['@odata.nextLink']
        iter_list = []
        iter_list = iter_list + json['value']
        while next_link:
            resp = requests.get(next_link, headers=get_headers(bearer_token))
            this_json = resp.json()
            iter_list = iter_list + this_json['value']
            if "@odata.nextLink" in this_json:
                next_link = this_json['@odata.nextLink']
            else:
                next_link = None
    else:
        iter_list = json['value']

    column_translation = get_column_translation(
        user, site_name, list_name, mode="name_to_displayName"
    )

    items = []
    for item in iter_list:
        new_item = {}
        for field in fields:
            new_item[field] = item["fields"][field]
        items.append(new_item)

    if as_data_frame:
        if len(items) > 0:
            items = pd.DataFrame(items)
        else:
            items = pd.DataFrame(columns=list(column_translation.values()) + ["id"])

    return items


def get_list_items_two(user, site_name, list_name, fields, as_data_frame=False):
    import pandas as pd
    bearer_token = get_token(user)
    url = f"{GRAPH_API_BASE_ENDPOINT}/sites/{sharepoint_sites[site_name]}/lists/{list_name}/items?expand=fields"
    resp = requests.get(url, headers=get_headers(bearer_token))
    json = resp.json()

    if "@odata.nextLink" in json:
        is_nextlink_available = json['@odata.nextLink']
        iter_list = []
        while is_nextlink_available:
            resp = requests.get(is_nextlink_available, headers=get_headers(bearer_token))
            this_json = resp.json()
            # iter_list.append(this_json['value'])
            iter_list = iter_list + this_json['value']
            if "@odata.nextLink" in this_json:
                is_nextlink_available = this_json['@odata.nextLink']
            else:
                is_nextlink_available = None
    else:
        iter_list = json['value']

    column_translation = get_column_translation(
        user, site_name, list_name, mode="name_to_displayName"
    )

    items = []
    for item in iter_list:
        new_item = {}
        for field in fields:
            new_item[field] = item["fields"][field]
        items.append(new_item)

    if as_data_frame:
        if len(items) > 0:
            items = pd.DataFrame(items)
        else:
            items = pd.DataFrame(columns=list(column_translation.values()) + ["id"])

    return items


def delete_items(user, site_name, list_name, item_ids):
    # site_id = get_site_id(site_name)
    # user_id = OTIS_ID
    resp = None
    bearer_token = get_token(user)
    for item_id in item_ids:
        url = f"{GRAPH_API_BASE_ENDPOINT}/sites/{sharepoint_sites[site_name]}/lists/{list_name}/items/{item_id}"
        resp = requests.delete(url, headers=get_headers(bearer_token))
    return resp


def create_item(user, site_name, list_name, items):
    resp = None
    bearer_token = get_token(user)

    for item in items:

        column_translation = get_column_translation(user, site_name, list_name, mode="displayName_to_name")
        item = {
            column_translation[k]: v
            for k, v in item.items()
            if k in column_translation.keys()
        }
        item = {"fields": item}

        url = f"{GRAPH_API_BASE_ENDPOINT}/sites/{sharepoint_sites[site_name]}/lists/{list_name}/items"
        resp = requests.post(url, headers=get_headers(bearer_token), json=item)

    return resp.json()


