import chromadb
import random
from chromadb.utils import embedding_functions

# Embedding setup
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path="./chromadb_npc")
collection = client.get_collection(name="npc_dialogues", embedding_function=embedding_func)

# Map user input keywords to subcategories
keyword_map = {
    "hi": ("core_interactions", "greeting"),
    "hello": ("core_interactions", "greeting"),
    "hey": ("core_interactions", "greeting"),
    "trade": ("core_interactions", "trade"),
    "barter": ("core_interactions", "trade"),
    "craft": ("core_interactions", "trade"),
    "talk": ("core_interactions", "small_talk"),
    "gossip": ("core_interactions", "small_talk"),
    "quest": ("core_interactions", "quests"),
    "mission": ("core_interactions", "quests"),
    "bye": ("core_interactions", "farewell"),
    "farewell": ("core_interactions", "farewell"),
    "goodbye": ("core_interactions", "farewell"),
    "reward": ("ambient", "reward_greeting"),
    "whistle": ("ambient", "whistling_singing"),
    "sing": ("ambient", "whistling_singing"),
    "routine": ("ambient", "personal_routines"),
    "damage": ("special_interactions", "damaged_crops"),
    "steal": ("special_interactions", "stealing"),
    "mock": ("special_interactions", "mocking"),
    "help": ("special_interactions", "helped"),
}

print("🤖 NPC is ready! (type 'exit' to quit)\n")

while True:
    user_input = input("You: ").strip().lower()

    # Exit condition
    if user_input in ["exit", "quit"]:
        print("🤖 NPC says: Farewell, traveler!")
        break

    matched = None
    for keyword, (cat, subcat) in keyword_map.items():
        if keyword in user_input:
            matched = (cat, subcat)
            break

    if matched:
        cat, subcat = matched
        results = collection.query(
            query_texts=["npc line"],  # dummy query
            where={
                "$and": [
                    {"category": cat},
                    {"subcategory": subcat}
                ]
            },
            n_results=20
        )
        responses = results["documents"][0]
        if responses:
            print("🤖 NPC says:", random.choice(responses))
        else:
            print("🤖 NPC says: (no lines found in DB)")
    else:
        print("🤖 NPC says: I don’t understand that yet.")
