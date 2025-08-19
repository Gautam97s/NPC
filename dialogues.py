import chromadb
from chromadb.utils import embedding_functions

# Initialize Chroma with embedding function
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./chromadb_npc")
collection = client.get_or_create_collection(name="npc_dialogues", embedding_function=embedding_func)

# Your dialogues dictionary (unchanged)
npc_dialogues = {
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
            "Hey now! You're welcome back anytime!"
        ],
        "trade": [
            "What kind of crops are you lookin' for? I've got a fresh batch of wheat.",
            "How about some carrots? Worth your while, I reckon.",
            "You want some vegetables? I can give you a good deal on my tomatoes.",
            "I've got a few ears of corn left over from the harvest – you want 'em?",
            "What'll it take to get that sack of potatoes from me? A little trade maybe?",
            "I've got a nice batch of fresh eggs, if you're interested...",
            "What's your price for some of my finest herbs? I think we can come to an agreement.",
            "You want some seeds for next season? I've got some good ones to share.",
            "How about some fresh milk from my cows? It's the best in the village!",
            "I reckon you're lookin' for something a little more... unusual? Let me see what I can do."
        ],
        "small_talk": [
            "Awful weather we've been having, ain't it? My crops are takin' a beating.",
            "Did you hear the news about old Tom's barn burnin' down?",
            "You know what they say: 'a farmer's work is never done'.",
            "I'm tellin' ya, this heat's been makin' my animals mighty cranky.",
            "The village elder asked me to remind you that the harvest festival is comin' up soon.",
            "I heard rumors of strange noises comin' from the old abandoned mine...",
            "You know what they say: 'a good farmer is always lookin' for ways to improve'!",
            "My wife's got a new recipe she's tryin' out – want me to bring some over?",
            "I heard some folks are talkin' about startin' up a new trade route through the village...",
            "You know what they say: 'a farmer's gotta be prepared for anything'!"
        ],
        "quests": [
            "You lookin' to help me with some pests eatin' away at my crops? I could use some extra hands.",
            "I heard there might be a new shipment of seeds comin' in – you should keep an eye out for it.",
            "The village elder asked me to remind you that the harvest festival is comin' up soon... better get started on your preparations!",
            "You want some information about the old abandoned mine? I've heard rumors myself...",
            "I reckon someone's been talkin' trash about my farm – you might wanna take a look around and see what's goin' on.",
            "The crops are doin' poorly this season... might be time to try out some new techniques, don't ya think?",
            "There's rumors of a hidden treasure somewhere in the village – I've heard it might be near my farm...",
            "You want some advice on how to keep your animals healthy? I've got some tricks up my sleeve.",
            "I reckon there's been some strange happenings around the village lately... you best keep an eye out for any trouble.",
            "There's a big harvest festival comin' up – we should start preparin' now! What do ya say?"
        ],
        "farewell": [
            "Well, it was nice chattin' with ya! Come back anytime.",
            "Take care now! See you around the village.",
            "Alright then! Have a great day – and don't forget to bring some more seed for next season!",
            "Thanks for stoppin' by! I hope you found what you were lookin' for.",
            "See ya 'round, neighbor! Keep an eye out for any trouble in the village.",
            "Well, it was nice talkin' with ya – don't be a stranger now!",
            "Take care, friend! And remember: a good farmer always keeps his word.",
            "Thanks for helpin' me out today! You're a regular hero 'round these parts.",
            "It was great chattin' with ya – see you at the harvest festival next week!",
            "Alright then! Have a safe journey, and don't forget to bring some of those fine seeds back for me!"
        ]
    },
    "ambient": {
        "reward_greeting": [
            "Ah, friend! You're lookin' out for me again? Thanks!",
            "Hey there! I see you've been helpin' me out lately – how can I repay that?",
            "Well met, indeed! You're a regular hero 'round these parts.",
            "Hey now! You're a friend of mine, ain't ya?",
            "Ah, neighbor! It's always good to see someone as fine as you comin' by."
        ],
        "whistling_singing": [
            "(whistling) \"Oh, it's a beautiful day to be outside!\"",
            "(singing) \"The sun is shining bright, and my crops are lookin' just right!\"",
            "(whistling) \"Life is good when you're growin' your own food!\"",
            "(whistling) \"Ah, shucks! It's a lovely day today – ain't it?\"",
            "(singing) \"The wind is blowin' gentle, and my fields are thrivin' well!\""
        ],
        "personal_routines": [
            "Alright, now let's get these chickens fed... Ah, yes, that's better.",
            "Water's lookin' a little low in the field... Gotta go give it a top-off.",
            "Now, where did I put that basket of fresh eggs? Ah, there we are!",
            "Time to check on my cows – they're gettin' a might restless.",
            "My plants are lookin' a little parched... Think it's time for some waterin'!"
        ]
    },
    "special_interactions": {
        "damaged_crops": [
            "What in tarnation have you done?! You've ruined my whole crop!",
            "How could you do this?! You know how hard I worked on those poor plants.",
            "This is just great! First, we get a drought, and then some fool comes along and destroys the rest.",
            "You're gonna regret this – mark my words!",
            "What's gotten into you? You used to be a decent person!"
        ],
        "stealing": [
            "You're stealing from me?! That's just not right!",
            "I don't know what kind of person you are, but I do know it ain't someone I want around here.",
            "Get your hands off my stuff! This ain't no place for thieves!",
            "You're as sneaky as a snake in the grass – I won't tolerate that kind of behavior!",
            "I'll have you know, I've worked hard to build this farm – don't go takin' it from me!"
        ],
        "mocking": [
            "You think you're funny, don't ya? Well, let me tell you somethin'...",
            "I may not be the most skilled farmer in the village, but at least I'm honest.",
            "You can mock all you want, but when it comes down to it, I've got skills and knowledge that'll always come out on top!",
            "You're just jealous of my success – don't try to bring me down!",
            "I've worked hard to get where I am – don't go thinkin' you can take that away from me!"
        ],
        "helped": [
            "Thanks for your help! You're a real lifesaver around here.",
            "I don't know what I'd do without someone like you lookin' out for me.",
            "You're a regular hero, friend! I owe you one.",
            "That's mighty kind of you – I appreciate it!",
            "You're as good as gold – thank you for your help!"
        ]
    }
}

# Insert dialogues into ChromaDB
for category, subcategories in npc_dialogues.items():
    for subcat, lines in subcategories.items():
        for i, line in enumerate(lines):
            collection.add(
                ids=[f"{category}_{subcat}_{i}"],
                documents=[line],
                metadatas=[{"category": category, "subcategory": subcat}]
            )

print("Dialogues stored in ChromaDB with embeddings by category and subcategory!")
