import os
from fastapi import FastAPI
from supabase import create_client
from dotenv import load_dotenv

load_dotenv('/home/ubuntu/sovereign/.env')
app = FastAPI()
sb = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

@app.get("/sync/all")
async def sync_all(user_id: int):
    # Fetch Arena, Intel, and User Economy in one parallel hit
    matches = sb.table('live_arena').select('*').order('status').execute()
    intel = sb.table('market_intel').select('*').execute()
    economy = sb.table('user_economy').select('*').eq('user_id', user_id).maybe_single().execute()
    
    return {
        "arena": matches.data,
        "intel": intel.data,
        "economy": economy.data or {"aura_points": 1000.0, "stars": 0}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
