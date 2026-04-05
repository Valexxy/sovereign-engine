import os
import requests
import time
from dotenv import load_dotenv
from supabase import create_client

load_dotenv('/home/ubuntu/sovereign/.env')
sb = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
ODDS_KEY = os.getenv('ODDS_API_KEY')

def fetch_all():
    # 1. Update Market Intel (FX & Fuel)
    intel = [
        {"item_name": "USD/NGN P2P", "price_naira": "1,625", "category": "FX", "trend": "Up"},
        {"item_name": "CNY/NGN Bank", "price_naira": "228", "category": "FX", "trend": "Stable"},
        {"item_name": "Fuel (Onitsha)", "price_naira": "1,150", "category": "Fuel", "trend": "Down"}
    ]
    for i in intel: sb.table('market_intel').upsert(i, on_conflict='item_name').execute()

    # 2. Update Live Arena
    url = f"https://api.the-odds-api.com/v4/sports/soccer/scores/?apiKey={ODDS_KEY}&daysFrom=1"
    try:
        res = requests.get(url).json()
        for m in res:
            h, a = 0, 0
            if m.get('scores'):
                for s in m['scores']:
                    val = int(s['score']) if s['score'] else 0
                    if s['name'] == m['home_team']: h = val
                    else: a = val
            
            sb.table('live_arena').upsert({
                "match_id": m['id'], "teams": f"{m['home_team']} vs {m['away_team']}",
                "score": f"{h} - {a}", "match_time": "LIVE" if not m.get('completed') else "FT",
                "last_event": "🔥 High Tension" if not m.get('completed') else "Match Ended"
            }).execute()
    except: pass
    print("🛰️ Omni-Worker: Pulse Sync Complete.")

if __name__ == "__main__":
    while True:
        fetch_all()
        time.sleep(60)
