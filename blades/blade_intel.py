import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv('/home/ubuntu/sovereign/.env')
sb = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

def generate_gists():
    # In production, this would call Gemini/GPT to summarize news.
    # For now, it formats market trends into 'AI Gists'.
    market_data = sb.table('market_intel').select('*').execute().data
    
    gists = []
    for item in market_data:
        trend_msg = "🔥 Price Spiking!" if item['trend'] == 'Up' else "📉 Cooling down."
        gists.append({
            "title": f"{item['item_name']} Update",
            "content": f"{item['item_name']} is currently ₦{item['price_naira']}. {trend_msg} Market sentiment is {item['trend']}.",
            "category": "MARKET"
        })
    
    # Push to a 'gists' table or return to frontend
    return gists

if __name__ == "__main__":
    print(generate_gists())
