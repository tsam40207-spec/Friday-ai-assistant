import os
from dotenv import load_dotenv
from livekit import api

load_dotenv()

token = api.AccessToken(os.getenv("LIVEKIT_API_KEY"), os.getenv("LIVEKIT_API_SECRET")) \
    .with_identity("boss") \
    .with_name("Boss") \
    .with_grants(api.VideoGrants(
        room_join=True,
        room="friday-room",
    ))

print("URL:", os.getenv("LIVEKIT_URL"))
print("TOKEN:", token.to_jwt())
