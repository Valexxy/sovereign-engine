import os
import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv('/home/ubuntu/sovereign/.env')
sb = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

def update_market():
    # Mock data for Onitsha Market Intelligence (can be replaced with scrapers)
    intel = [
        {"item_name": "US Dollar (P2P)", "price_naira": "1,620", "category": "FX", "trend": "Up"},
        {"item_name": "Chinese Yuan (Bank)", "price_naira": "225", "category": "FX", "trend": "Stable"},
        {"item_name": "PMS (Fuel) - Onitsha", "price_naira": "1,150", "category": "Fuel", "trend": "Down"}
    ]
    
    for item in intel:
        sb.table('market_intel').upsert(item, on_conflict='item_name').execute()
    print("🛰️ Anambra Oracle: Market Intel Updated.")

if __name__ == "__main__":
    update_market()
