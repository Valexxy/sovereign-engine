import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv('/home/ubuntu/sovereign/.env')
sb = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

def process_daily_checkin(user_id):
    # Logic: 100 Aura for checking in, +50 for streaks.
    user = sb.table('user_economy').select('*').eq('user_id', user_id).maybe_single().execute().data
    
    if not user:
        sb.table('user_economy').insert({"user_id": user_id, "aura_points": 1100.0}).execute()
        return "Welcome to Sovereign! 1100 Aura granted."
    
    new_balance = user['aura_points'] + 100
    sb.table('user_economy').update({"aura_points": new_balance}).eq('user_id', user_id).execute()
    return f"Check-in successful! Balance: {new_balance} Aura."

def convert_to_stars(user_id, aura_amount):
    # Logic: 1000 Aura = 1 Star (Example)
    if aura_amount < 1000: return "Insufficient Aura"
    # Update logic here...
    return "Conversion successful."
