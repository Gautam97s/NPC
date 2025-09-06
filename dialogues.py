# This module contains all logic related to storing and retrieving NPC dialogue,
# including a placeholder for a large language model (LLM) for special interactions.

import chromadb
import random
from chromadb.utils import embedding_functions

# --- Dialogue Data Storage ---
# This is a dictionary containing all pre-generated dialogue lines.
# The keys represent categories and subcategories for easy access.
DIALOGUE_DATA = {
    "core_interactions": {
        "greeting": [
            "Well met! Come on by and take a look around my farm.",
            "Hey, neighbor! What brings you to my doorstep today?",
            "Ah, hello there! How can I help you with your day?",
            "Welcome to my little corner of the village! Make yourself at home.",
            "Howdy! What do you need? I'm happy to lend a hand.",
            "Hiya! You're lookin' for something, ain't ya?",
            "Hey there! I reckon you're lookin' for some fresh produce?",
            "Ah, hi again! Didn't mean to leave you hanging earlier...",
            "Welcome back! What brings you by my farm today?",
            "Hey now! You're welcome back anytime!",
            "Well, look who it is! Good to see you, friend.",
            "G'day! Pull up a chair and let's have a chat.",
            "Top of the morning to you! A fine day for a walk, isn't it?",
            "I've been expecting you! Or, well, I hoped to see you.",
            "It's a bright day, and you've made it brighter just by showing up.",
            "Morning, adventurer! Out for another quest, are you?",
            "How's the world treating you? Anything I can help with?",
            "Feel free to wander. The chickens don't mind the company.",
            "Ah, a new face! I'm always happy to meet a fellow traveler.",
            "Just getting started with my chores. Glad you could drop by."
        ],
        "trade": [
            "What kind of crops are you lookin' for? I've got a fresh batch of wheat.",
            "How about some carrots? Worth your while, I reckon.",
            "You want some vegetables? I can give you a good deal on my tomatoes.",
            "I've got a few ears of corn left over from the harvest - you want 'em?",
            "What'll it take to get that sack of potatoes from me? A little trade maybe?",
            "I've got a nice batch of fresh eggs, if you're interested...",
            "What's your price for some of my finest herbs? I think we can come to an agreement.",
            "You want some seeds for next season? I've got some good ones to share.",
            "How about some fresh milk from my cows? It's the best in the village!",
            "I reckon you're lookin' for something a little more... unusual? Let me see what I can do.",
            "My produce is the freshest around. Take your pick!",
            "I'm willing to trade. What have you got?",
            "Got any rare goods? I'm always looking for something new for my collection.",
            "My chickens lay the best eggs. They're a steal at this price.",
            "I've got more apples than I know what to do with. Wanna trade?",
            "This old lantern? It's seen its share of adventures. Might be worth a bit.",
            "Looking to stock up? My stall is open for business.",
            "A fine item you have there. I might have something you'd like to trade for it.",
            "Let's see what you've got in that satchel. I'm always up for a good barter.",
            "My goods are fairly priced, friend. What'll it be?"
        ],
        "small_talk": [
            "Awful weather we've been having, ain't it? My crops are takin' a beating.",
            "Did you hear the news about old Tom's barn burnin' down?",
            "You know what they say: 'a farmer's work is never done'.",
            "I'm tellin' ya, this heat's been makin' my animals mighty cranky.",
            "The village elder asked me to remind you that the harvest festival is comin' up soon.",
            "I heard rumors of strange noises comin' from the old abandoned mine...",
            "You know what they say: 'a good farmer is always lookin' for ways to improve'!",
            "My wife's got a new recipe she's tryin' out - want me to bring some over?",
            "I heard some folks are talkin' about startin' up a new trade route through the village...",
            "You know what they say: 'a farmer's gotta be prepared for anything'!",
            "The chickens are behaving today, for once. A small victory.",
            "I saw a traveling merchant pass by just this morning. He had some strange wares.",
            "Heard the mayor's planning a new road. Hope it doesn't run through my fields.",
            "The seasons change, but the weeds in my garden always stay the same.",
            "Been thinking of getting a new scarecrow. The old one is starting to look a bit tired.",
            "My neighbor's been complaining about the wolves again. They're a persistent nuisance.",
            "You should see the size of the cabbages I'm growing this year. They're a sight to behold!",
            "Life on the farm is simple, but it's honest work.",
            "I'm just grateful for the sun and rain. Can't ask for much more than that.",
            "Been feeling a little ache in my back lately. Getting old, I suppose."
        ],
        "quests": [
            "You lookin' to help me with some pests eatin' away at my crops? I could use some extra hands.",
            "I heard there might be a new shipment of seeds comin' in - you should keep an eye out for it.",
            "The village elder asked me to remind you that the harvest festival is comin' up soon... better get started on your preparations!",
            "You want some information about the old abandoned mine? I've heard rumors myself...",
            "I reckon someone's been talkin' trash about my farm - you might wanna take a look around and see what's goin' on.",
            "The crops are doin' poorly this season... might be time to try out some new techniques, don't ya think?",
            "There's rumors of a hidden treasure somewhere in the village - I've heard it might be near my farm...",
            "You want some advice on how to keep your animals healthy? I've got some tricks up my sleeve.",
            "I reckon there's been some strange happenings around the village lately... you best keep an eye out for any trouble.",
            "There's a big harvest festival comin' up - we should start preparin' now! What do ya say?",
            "My prize-winning pig went missing. If you find him, there's a reward in it for you.",
            "The well's gone dry. I need someone to clear the rocks at the bottom. You up for it?",
            "I've got a delivery for the next town, but I can't leave my fields. Can you take it for me?",
            "There are some tricky critters digging up my carrots. I need a brave soul to deal with them.",
            "I lost my wedding ring somewhere in the fields. It's an old family heirloom. Please, can you help me find it?",
            "The village needs firewood for the winter. The forest is a bit dangerous, but the pay is good.",
            "I've heard whispers of a powerful artifact in the ruins. If you find it, the village would be grateful.",
            "Some of my livestock got spooked and ran off. Help me round them up, and I'll give you my finest cheese.",
            "The old mill is broken. I need someone with a strong arm to fix the main gear.",
            "A traveler passed through and mentioned a rare herb that grows on the mountain peak. I need it for a special potion."
        ],
        "farewell": [
            "Well, it was nice chattin' with ya! Come back anytime.",
            "Take care now! See you around the village.",
            "Alright then! Have a great day - and don't forget to bring some more seed for next season!",
            "Thanks for stoppin' by! I hope you found what you were lookin' for.",
            "See ya 'round, neighbor! Keep an eye out for any trouble in the village.",
            "Well, it was nice talkin' with ya - don't be a stranger now!",
            "Take care, friend! And remember: a good farmer always keeps his word.",
            "Thanks for helpin' me out today! You're a regular hero 'round these parts.",
            "It was great chattin' with ya - see you at the harvest festival next week!",
            "Alright then! Have a safe journey, and don't forget to bring some of those fine seeds back for me!",
            "Until next time! May the sun shine on your path.",
            "Farewell, adventurer! Good luck on your travels.",
            "The fields call to me, but I'm glad we had this talk. Until we meet again.",
            "Safe travels, friend. The road ahead is long.",
            "Don't be a stranger. My door is always open.",
            "It was a pleasure. Come back when you can.",
            "I've got more work to do. See you later!",
            "Take it easy out there. The world can be a bit rough.",
            "I wish you all the best on your journey.",
            "Goodbye for now. Stay out of trouble!"
        ]
    },
    "ambient": {
        "reward_greeting": [
            "Ah, friend! You're lookin' out for me again? Thanks!",
            "Hey there! I see you've been helpin' me out lately - how can I repay that?",
            "Well met, indeed! You're a regular hero 'round these parts.",
            "Hey now! You're a friend of mine, ain't ya?",
            "Ah, neighbor! It's always good to see someone as fine as you comin' by.",
            "That was mighty kind of you. My gratitude knows no bounds.",
            "I knew I could count on you!",
            "Your help is a true gift. Thank you.",
            "You saved me a lot of trouble. I won't forget this.",
            "You're an honorable person, I'm glad to have you on my side.",
            "This is a pleasant surprise! You're a good sort.",
            "I'm indebted to you for your kindness.",
            "Your assistance is greatly appreciated.",
            "You've proven yourself a true ally.",
            "Thank you kindly! You've made my day.",
            "You've earned my trust and respect.",
            "That's a weight off my shoulders. I thank you.",
            "You have my deepest thanks. I'll remember this.",
            "What a noble act! You're a credit to the village.",
            "I'm truly grateful for your generous spirit."
        ],
        "whistling_singing": [
            "(whistling) \"Oh, it's a beautiful day to be outside!\"",
            "(singing) \"The sun is shining bright, and my crops are lookin' just right!\"",
            "(whistling) \"Life is good when you're growin' your own food!\"",
            "(whistling) \"Ah, shucks! It's a lovely day today - ain't it?\"",
            "(singing) \"The wind is blowin' gentle, and my fields are thrivin' well!\"",
            "(humming a happy tune while tending to the chickens)",
            "(softly) \"A farmer's life is a happy life...\"",
            "(whistling a simple, cheerful melody)",
            "(singing) \"The corn grows tall, the pumpkins gleam, living out a simple dream.\"",
            "(humming) \"Hoo-hoo-hum, the day is long, but I'll sing a happy song.\"",
            "(singing) \"Oh, the simple life, it's the best of all, a sturdy roof and fields so tall.\"",
            "(whistling a complex tune with many trills)",
            "(singing to himself) \"The sun goes down, the moon shines bright, another day, another night.\"",
            "(humming) \"Mmm-mm-mm, gotta get this work done...\"",
            "(whistling) \"The old farm dog, he's a good old friend, stick with me 'til the very end.\"",
            "(singing) \"A farmer's hands are strong and true, always ready for something new.\"",
            "(humming a simple, repetitive melody)",
            "(whistling) \"The morning dew, a misty shroud, makes me feel proud.\"",
            "(singing) \"The seeds I plant, they grow so high, reaching for the endless sky.\"",
            "(humming) \"Hee-hee-hum, another day, another dollar, another farmer in the collar.\""
        ],
        "personal_routines": [
            "Alright, now let's get these chickens fed... Ah, yes, that's better.",
            "Water's lookin' a little low in the field... Gotta go give it a top-off.",
            "Now, where did I put that basket of fresh eggs? Ah, there we are!",
            "Time to check on my cows - they're gettin' a might restless.",
            "My plants are lookin' a little parched... Think it's time for some waterin'!",
            "Just gotta finish up this last patch of weeds. They never seem to stop growing.",
            "The fences need mending. Always something to fix around here.",
            "I'm just gathering some herbs for a special stew. Smells delicious already.",
            "Looks like the barn door is a bit loose. I'll get to that after my morning tea.",
            "I'm polishing my old boots. They've seen a lot of miles.",
            "Just counting the chickens. They always seem to be in a different number.",
            "I'm making a fresh batch of butter. The churn is a bit noisy.",
            "The morning air is crisp. A perfect day for work.",
            "I'm just sharpening my tools. A dull tool is no good to a farmer.",
            "Checking the weather. The sky is looking a bit grey.",
            "Just tending to my garden. The tomatoes are looking especially good this year.",
            "I'm just finished with my morning coffee. Time to get to work.",
            "Gotta get this wood chopped before the sun goes down.",
            "Just finished watering the fields. A long day's work, but it's worth it.",
            "I'm just taking a short break. It's important to rest, you know."
        ]
    },
    # The categories that will trigger the LLM placeholder in the main game.
    "special_interactions": {
        "damaged_crops": [], "stealing": [], "mocking": [], "helped": [], "lost_battle": []
    }
}

# --- ChromaDB Initialization and Population ---
def initialize_chromadb():
    """Initializes ChromaDB and populates the database with dialogue data."""
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    client = chromadb.PersistentClient(path="./chromadb_npc")
    collection = client.get_or_create_collection(
        name="npc_dialogues",
        embedding_function=embedding_func
    )

    # Clear and re-populate the collection for a clean start
    all_ids = collection.get()["ids"]
    if all_ids:
        collection.delete(ids=all_ids)
    doc_id = 0
    for group, subcats in DIALOGUE_DATA.items():
        for subcat, lines in subcats.items():
            if lines:
                collection.add(
                    documents=lines,
                    metadatas=[{"category": subcat, "group": group}] * len(lines),
                    ids=[f"doc_{doc_id + i}" for i in range(len(lines))]
                )
                doc_id += len(lines)
    return collection

# --- LLM Placeholder Function ---
def get_llm_response(response_type):
    """
    Simulates a call to an LLM to get a dynamic dialogue response.
    This function will be replaced with an actual API request later.
    """
    mock_responses = {
        "damaged_crops": [
            "What in tarnation?! Look what you've done to my prize-winning pumpkins!",
            "My entire crop is ruined! You'll pay for this!",
            "How could you be so careless? I worked all season on those!"
        ],
        "stealing": [
            "I knew it! You've got the look of a thief in your eyes, get outta here!",
            "My goods are not for the taking! Leave my property at once!",
            "You think you can just take what's mine? Not on my watch!"
        ],
        "mocking": [
            "Hah! I heard you got beat by a goblin... again? Might want to stick to taming chickens, adventurer.",
            "Is that the best you can do? I've seen scarecrows with more fighting spirit.",
            "Don't worry, I won't tell anyone about your little 'defeat'. Our secret."
        ],
        "helped": [
            "Ah, you're a true friend. My farm is safe thanks to you. I owe you one!",
            "That's mighty kind of you. You've earned a special place in my heart.",
            "I don't know what I'd do without someone like you looking out for me."
        ],
        "lost_battle": [
            "Another one bites the dust, eh? Looks like you're not as tough as you thought you were! (chuckles)",
            "Don't worry, even the greatest heroes have off days. Just... not that many.",
            "Maybe you should try a different strategy next time. Or a different career path."
        ]
    }
    return random.choice(mock_responses.get(response_type, ["I don't know how to respond to that."]))

# --- Dialogue Retrieval Function ---
def get_dialogue(collection, choice):
    """
    Fetches a dialogue line based on the player's choice.
    Uses LLM for special interactions, otherwise queries the ChromaDB.
    """
    # The logic to decide between pre-generated and LLM dialogue
    if choice in DIALOGUE_DATA["special_interactions"]:
        return get_llm_response(choice)
    else:
        results = collection.query(
            query_texts=["dummy"], # A dummy query text since we are filtering by metadata
            where={"category": choice},
            n_results=1
        )
        if results["documents"] and results["documents"][0]:
            return random.choice(results["documents"][0])
        else:
            return "I'm not sure what to say about that."


if __name__ == "__main__":
    collection = initialize_chromadb()
    print("Dialogue collection initialized with", collection.count(), "entries.")