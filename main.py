import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from email_parser import *
import base64
from bs4 import BeautifulSoup 

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]




def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    
    # request a list of all the messages 
    result = service.users().messages().list(maxResults=5, userId='me', q='label:Bancos').execute() 
    
    # We can also pass maxResults to get any number of emails. Like this: 
    # result = service.users().messages().list(maxResults=200, userId='me').execute() 
    messages = result.get('messages') 
    
    # messages is a list of dictionaries where each dictionary contains a message id. 
    # iterate through all the messages 
    for msg in messages:       
      # Get the message from its id 
      msg_data = service.users().messages().get(userId='me', id=msg['id']).execute() 

      headers = msg_data['payload']['headers'] 
      current_email = Email()
      # Look for Subject and Sender Email in the headers 
      for d in headers: 
        if d['name'] == 'Subject': 
          current_email.subject = d['value'] 
        if d['name'] == 'From': 
          current_email.sender = d['value'] 
        if d['name'] == "Date":
          current_email.date_str = d['value']

      current_email.body = "Not decripted"

      # Use try-except to avoid any Errors 
      try: 
        # The Body of the message is in Encrypted format. So, we have to decode it. 
        # Get the data and decode it with base 64 decoder. 

        encoded_body = msg_data['payload']['body']['data']
        decoded_body = base64.urlsafe_b64decode(encoded_body.encode('UTF-8'))
        current_email.body = BeautifulSoup(decoded_body, "lxml").text.replace("&nbsp","\n")
    
      except: 
        pass

      finally:
        # Printing the subject, sender's email and message 
        if ("scotiabank" in current_email.sender.lower()) and ("alerta transacción tarjeta" in current_email.subject.lower()):
          parse_email(current_email, "scotiabank")
          print(current_email)

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()
