import re
from datetime import datetime

classification_list = {}

def read_classification():
  global classification_list
  with open("classification.txt","r") as f:
    lines = f.readlines()

  current_class = ""
  for line in lines:
    line = line.strip().lower().replace("\n","")
    if len(line) == 0:
      pass
    elif line[0] == "#":
      pass
    elif line.startswith("class:"):
      current_class = f"temp{len(classification_list)+1}"
      if len(line) > 6:
        line = line[6:].strip()
        if (len(line) != 0) and (line not in classification_list):
          current_class = line.title()

      classification_list[current_class] = [[],[]]

    elif line.startswith("include:"):
      include_list = []
      if len(line) > 8:
        line = line[8:].strip()
        if len(line) != 0:
          include_list = line.split(",")
          include_list = [i.strip() for i in include_list]

      classification_list[current_class][0].extend(include_list)

    elif line.startswith("exclude:"):
      exclude_list = []
      if len(line) > 8:
        line = line[8:].strip()
        if len(line) != 0:
          exclude_list = line.split(",")
          exclude_list = [i.strip() for i in exclude_list]

      classification_list[current_class][1].extend(exclude_list)
    else:
      pass

  return

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

  def set_category(self) -> None:
    description = " " + self.transaction_description.lower() + " "

    for category, (include_words, exclude_words) in classification_list.items():
      excluded = False
      for word in exclude_words:
        word = " " + word + " "
        if excluded:
          break
        if word in description:
          excluded = True
          break
      if not excluded:
        for word in include_words:
          word = " " + word + " "
          if word in description:
            self.category = category
            return
    self.category = ""
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
  email.set_category()
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


