import re




def parse_email(body : str, bank : str)-> tuple[str, str, str]:
  """
  Reads the email and extracts a tuple with format:
    description  : str
    date  : str
    price : str

  body : can be enconded or plain text, depends on the bank
  """
  parse_fn = bank_specs_dict.get(bank, None)
  parse_result = parse_fn(body)

  return parse_result

def parse_scotiabank(text : str) -> tuple[str, str, str]:
  text = text.replace("&nbsp", " ")

  DESCRIPTION_PATTERN = "Scotiabank le notifica que la transacción realizada en .*, el día"
  DATE_PATTERN = "el día .* a las"
  PRICE_PATTERN = "referencia \d* por .*, fue aprobada"
  description = ""
  date = ""
  price = ""
  
  description_match = re.findall(DESCRIPTION_PATTERN, text)
  if description_match:
    start = DESCRIPTION_PATTERN.index(".")
    finish = DESCRIPTION_PATTERN.index("*") - len(DESCRIPTION_PATTERN)+1
    description = description_match[0][start:finish]
  
  date_match = re.findall(DATE_PATTERN, text)
  if date_match:
    start = DATE_PATTERN.index(".")
    finish = DATE_PATTERN.index("*") - len(DATE_PATTERN)+1
    date = date_match[0][start:finish]

  price_match = re.findall(PRICE_PATTERN, text)
  if price_match:
    PRICE_PATTERN = " por .*, fue aprobada"
    price_match = re.findall(PRICE_PATTERN, price_match[0])
    start = PRICE_PATTERN.index(".")
    finish = PRICE_PATTERN.index("*") - len(PRICE_PATTERN)+1
    price = price_match[0][start:finish]

  result = description, date, price
  return result



bank_specs_dict = {
  "scotiabank" : parse_scotiabank
}