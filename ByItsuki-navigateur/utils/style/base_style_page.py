
import os
from dotenv import load_dotenv
load_dotenv()


def base_style():
    theme_color = os.getenv('THEME')
    return f"<html><body style='background-color:{theme_color}; margin:0; border:0;'></body></html>"