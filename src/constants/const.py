from os import getenv
from dotenv import load_dotenv

load_dotenv()

# SUPABASE STUFF
ASSOCIATED_APP = getenv("ASSOCIATED_APP")
USER_ID = getenv("USER_ID")

# AMAZON URL BASE FORMAT
INDEX = "&i={index}"
CATEGORY_ID = "&rh=n%3A{category_id}"


# FLIPKART URL BASE FORMAT
FLIPKART_CATEGORY = "{category_name}/pr?sid={category_id}"
FLIPKART_QUERY_WITH_CAT = "&q={query}"
FLIPKART_QUERY_WITHOUT_CAT = "search?q={query}"
