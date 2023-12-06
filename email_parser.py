import re
from datetime import datetime

class Email:
  def __init__(self):
    self.sender : str = ""
    self.subject : str = ""
    self.date_str : str = ""
    self.body : str = ""
    self.transaction_price_str : str = ""
    self.transaction_description : str = ""
    self.transaction_date_str : str = ""
    self.category : str = ""
  
  @property
  def datetime(self):
      date_time = datetime.strptime(self.date_str, "%d %b %Y %H:%M:%S %z")
      return date_time.strftime("%Y-%m-%d_T%H-%M-%S")

  @property
  def date(self):
      date = datetime.strptime(self.date_str, "%d %b %Y %H:%M:%S %z")
      return date.strftime("%Y-%m-%d")

  def __repr__(self) -> str:
    text : str = ""
    text += "Sender:\t" + self.sender + "\n"
    text += "Subject:\t" + self.subject + "\n"
    text += "Date:\t" + self.date + "\n"
    text += "Description:\t" + self.transaction_description + "\n"
    text += "Price:\t" + self.transaction_price_str + "\n"
    text += "Category:\t" + self.category + "\n"
    return text

def set_category(email : Email) -> None:
  email.category = ""
  return

def parse_email(email : Email, bank : str)-> None:
  """
  Reads the email's body and sets its transaction's:
    description  : str
    date  : str
    price : str
    category : str
  """
  if bank == "scotiabank":
    parse_fn = parse_scotiabank
  else:
    raise Exception("Error bank not found")
  
  description, date, price = parse_fn(email.body)
  email.transaction_description = description
  email.transaction_date_str = date
  email.transaction_price_str = price
  set_category(email)
  return 

def parse_scotiabank(text : str) -> tuple[str, str, str]:
  text = text.replace("&nbsp", " ")

  DESCRIPTION_PATTERN = "Scotiabank le notifica que la transacción realizada en .*, el día"
  DATE_PATTERN = "el día .* a las"
  PRICE_PATTERN = "referencia \d* por .*, fue "
  description = ""
  date = ""
  price = ""
  
  description_match = re.findall(DESCRIPTION_PATTERN, text)
  if description_match:
    start = DESCRIPTION_PATTERN.index(".")
    finish = DESCRIPTION_PATTERN.index("*") - len(DESCRIPTION_PATTERN) + 1
    description = description_match[0][start:finish]
  
  date_match = re.findall(DATE_PATTERN, text)
  if date_match:
    start = DATE_PATTERN.index(".")
    finish = DATE_PATTERN.index("*") - len(DATE_PATTERN) + 1
    date = date_match[0][start:finish]

  price_match = re.findall(PRICE_PATTERN, text)
  if price_match:
    PRICE_PATTERN = " por .*, fue "
    price_match = re.findall(PRICE_PATTERN, price_match[0])
    start = PRICE_PATTERN.index(".")
    finish = PRICE_PATTERN.index("*") - len(PRICE_PATTERN) + 1
    price = price_match[0][start:finish]

  result = description, date, price
  return result


