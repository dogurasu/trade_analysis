import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

AV_KEY = os.environ.get("AVKEY1")
print(AV_KEY)