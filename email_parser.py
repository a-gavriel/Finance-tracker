import re
class Email:
  sender : str
  subject : str
  date_str : str
  body : str
  transaction_price_str : str
  transaction_description : str
  transaction_date_str : str

  def __init__(self):
    self.sender : str = ""
    self.subject : str = ""
    self.date_str : str = ""
    self.body : str = ""
    self.transaction_price_str : str = ""
    self.transaction_description : str = ""
    self.transaction_date_str : str = ""

  def __repr__(self) -> str:
    text : str = ""
    text += "Sender:\t" + self.sender + "\n"
    text += "Subject:\t" + self.subject + "\n"
    text += "Email date:\t" + self.date_str + "\n"
    text += "Description:\t" + self.transaction_description + "\n"
    text += "Price:\t" + self.transaction_price_str + "\n"
    text += "Date:\t" + self.transaction_date_str + "\n"
    
    return text


def parse_email(email : Email, bank : str)-> None:
  """
  Reads the email and extracts a tuple with format:
    description  : str
    date  : str
    price : str

  body : can be enconded or plain text, depends on the bank
  """
  parse_fn = bank_specs_dict.get(bank, None)
  if not parse_email:
    raise("Error bank not found")
  
  description, date, price = parse_fn(email.body)

  email.transaction_description = description
  email.transaction_date_str = date
  email.transaction_price_str = price

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



bank_specs_dict = {
  "scotiabank" : parse_scotiabank
}