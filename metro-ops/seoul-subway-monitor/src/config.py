import os
from dotenv import load_dotenv

# Load environment variables from .env file
# Assuming .env is in the project root (seoul-subway-monitor/.env)
load_dotenv()

class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SEOUL_API_KEY = os.getenv("SEOUL_API_KEY", "sample")
    
    # Target subway lines
    TARGET_LINES = [
        "1호선", "2호선", "3호선", "4호선", "5호선", 
        "6호선", "7호선", "8호선", "9호선"
    ]

    @classmethod
    def validate(cls):
        """Validate that essential environment variables are set."""
        if not cls.SUPABASE_URL or not cls.SUPABASE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file.")
        if not cls.SEOUL_API_KEY:
            print("Warning: SEOUL_API_KEY is not set. Using 'sample' key.")
