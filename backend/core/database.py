# core/database.py
from supabase import create_client, Client
from core.config import settings

def init_supabase() -> Client:
    """
    Initializes the Supabase client using the Service Role Key for backend operations.
    """
    url: str = settings.SUPABASE_URL
    key: str = settings.SUPABASE_KEY
    return create_client(url, key)

# Singleton client to be imported across the application
supabase: Client = init_supabase()