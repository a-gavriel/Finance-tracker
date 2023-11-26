import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from bs4 import BeautifulSoup 
import lxml.html as lh
import base64 
import html

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
    result = service.users().messages().list(maxResults=50, userId='me', q='label:Bancos').execute() 
    
    # We can also pass maxResults to get any number of emails. Like this: 
    # result = service.users().messages().list(maxResults=200, userId='me').execute() 
    messages = result.get('messages') 
    
    # messages is a list of dictionaries where each dictionary contains a message id. 
    i = 0
    # iterate through all the messages 
    for msg in messages:       
      

      # Get the message from its id 
      txt = service.users().messages().get(userId='me', id=msg['id']).execute() 
    
      
      # Get value of 'payload' from dictionary 'txt' 
      payload = txt['payload'] 
      headers = payload['headers'] 
  
      # Look for Subject and Sender Email in the headers 
      for d in headers: 
        if d['name'] == 'Subject': 
          subject = d['value'] 
        if d['name'] == 'From': 
          sender = d['value'] 
        if d['name'] == "Date":
          date_text = d['value']

      body = "Not decripted"

      # Use try-except to avoid any Errors 
      try: 
        # The Body of the message is in Encrypted format. So, we have to decode it. 
        # Get the data and decode it with base 64 decoder. 

        data = txt['payload']['body']['data']
        #data = data.replace("-","+").replace("_","/") 
        decoded_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
    
        body = decoded_data 
        body = BeautifulSoup(body, "lxml").text.replace("&nbsp","\n")
    
      except: 
        pass

      finally:
        # Printing the subject, sender's email and message 
        if "scotiabank" in sender.lower():
          i = i + 1
          print(i)
          print("Subject: ", subject) 
          print("From: ", sender) 
          print('Date:', date_text)
          print("Body:" , body)
          print('\n') 

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()
