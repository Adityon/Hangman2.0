from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Dictionary to store user credentials
user_credentials = {
    "admin": "password123",
    "user1": "pass456",
    # Add more users if needed
}

# Dictionary to store game data
game_data = {
    "word": "",
    "guessed_letters": [],
    "attempts": 6,
    "result": ""
}

def authenticate(username, password):
    # Check if the username exists in the dictionary and the provided password is correct
    return username in user_credentials and user_credentials[username] == password

def create_account(username, password):
    # Create a new user account
    user_credentials[username] = password
    print(f"New user '{username}' created successfully!")

def choose_word():
    word_list = [
        "abandon", "ability", "absence", "academy", "account", "accuse", "achieve", "acoustic", "activate", "addict",
        "address", "adequate", "adjust", "admit", "adventure", "aerospace", "affair", "against", "agile", "aircraft",
        "alcohol", "alien", "allege", "alliance", "allocate", "alongside", "alphabet", "ambiguous", "ambulance", "amendment",
        "amplitude", "ancestor", "angel", "anger", "anguish", "animal", "announce", "antenna", "anxiety", "apology",
        "apparel", "appetite", "applause", "appoint", "aquarium", "architect", "ardent", "arise", "armor", "arrest",
        "artifact", "ashamed", "aspect", "assault", "assemble", "athlete", "atmosphere", "auction", "audience", "austere",
        "authentic", "average", "awesome", "balance", "barrier", "battery", "beacon", "beautiful", "believe", "benefit",
        "besiege", "between", "beyond", "biology", "birthday", "bishop", "blanket", "blessing", "blitz", "bodyguard",
        "boldness", "boundary", "bracelet", "breakfast", "breeze", "bridge", "brochure", "bruise", "budge", "builder",
        "burden", "business", "butterfly", "cabinet", "calculate", "calendar", "campaign", "capacity", "captain", "capture",
        "carbon", "cascade", "catalog", "celebrate", "century", "ceremony", "champion", "chance", "change", "charcoal",
        "charity", "charm", "checkpoint", "cherish", "childhood", "choice", "chronicle", "cinnamon", "circulate", "citizen",
        "clarity", "classic", "clay", "climate", "clockwork", "closet", "cluster", "coastal", "collapse", "colony",
        "combination", "comfort", "commander", "commence", "commerce", "compass", "compete", "comply", "concert", "concrete",
        "condemn", "confess", "conflict", "congress", "connect", "conquer", "consent", "consult", "consume", "contend",
        "context", "contour", "contrive", "control", "convoy", "cookie", "corner", "corridor", "cosmic", "counter",
        "courage", "cover", "craft", "crash", "create", "creature", "crimson", "crisis", "criterion", "crossing",
        "crown", "cruiser", "crystal", "cucumber", "culminate", "culture", "curiosity", "cylinder", "dainty", "daredevil",
        "debut", "decide", "decorate", "defend", "deliver", "demand", "denial", "depict", "deploy", "describe",
        "desire", "destroy", "devotion", "dictionary", "different", "diligent", "dimension", "discover", "disease", "display",
        "diversity", "doctrine", "document", "dominant", "dread", "dream", "dynamic", "earnest", "earthquake", "eclipse",
        "education", "effective", "effort", "elastic", "elegant", "element", "elephant", "eloquent", "embark", "embrace",
        "emotion", "empire", "employee", "enchant", "encounter", "endure", "energy", "enforce", "engagement", "enhance",
        "enjoy", "enlighten", "enrich", "ensemble", "enthusiasm", "entrance", "envelope", "epic", "equator", "erosion",
        "essential", "establish", "ethereal", "evaluate", "evoke", "examine", "exceed", "exchange", "execute", "exert",
        "exhaust", "expand", "experience", "expertise", "explore", "exquisite", "extend", "extraordinary", "exuberant", "fabric",
        "factor", "familiar", "fantasy", "fascinate", "favorite", "fearless", "feast", "feminine", "festival", "fidelity",
        "fiction", "filter", "flame", "flourish", "fluid", "focus", "fondness", "forever", "formulate", "fragile",
        "framework", "freedom", "frequent", "friendship", "frustrate", "fundamental", "fusion", "gallant", "gather", "gemstone",
        "generate", "genesis", "gentle", "genuine", "geology", "gesture", "gigantic", "glisten", "glorious", "graceful",
        "grandeur", "graphic", "gravity", "guitar", "habitat", "harbor", "harmony", "hazard", "health", "heavenly",
        "heritage", "heroic", "hibernate", "hidden", "highway", "hologram", "homage", "horizon", "humble", "hunger",
        "huntress", "hurricane", "hybrid", "identity", "ignite", "illuminate", "illustrate", "imagine", "imbue", "imitate",
        "immense", "immerse", "impact", "imprint", "incite", "infinite", "influence", "infuse", "inhale", "inherent",
        "innocent", "inquire", "inscribe", "insert", "inspire", "integral", "integrity", "intense", "interact", "intrigue",
        "intuition", "invincible", "invoke", "isolate", "jazz", "jubilee", "junction", "justify", "keen", "kinetic",
        "knockout", "landscape", "laughter", "legacy", "legend", "leisure", "liberate", "lifetime", "lightning", "limb",
        "limitless", "listen", "litigate", "lively", "longitude", "lovely", "lucid", "luminous", "luxury", "machine",
        "magical", "magnitude", "majestic", "mankind", "manifest", "manipulate", "marathon", "mascot", "mastery", "maverick",
        "meadow", "meander", "meditate", "megabyte", "melody", "memorable", "merge", "mesmerize", "metaphor", "meticulous",
        "midnight", "migrate", "milestone", "military", "mineral", "miracle", "mission", "mobile", "momentum", "monarch",
        "monument", "morning", "mystery", "navigate", "nebula", "nectar", "negotiate", "neutron", "noble", "nomad",
        "nostalgia", "novelty", "nurture", "observe", "obstacle", "oceanic", "opulent", "orbit", "organic", "outcome",
        "outdoor", "overture", "pacific", "pageant", "pandemonium", "parade", "paragon", "paramount", "passionate", "patience",
        "patriot", "pedestrian", "pendulum", "perceive", "perfect", "perpetual", "persist", "persona", "petition", "phenomenon",
        "pioneer", "planet", "plaque", "pleasure", "plunge", "poetic", "polar", "polygon", "portfolio", "possess",
        "potential", "praise", "precarious", "precise", "prelude", "preserve", "press", "pretend", "pretty", "prevail",
        "primal", "pristine", "proclaim", "prodigy", "profound", "progress", "prologue", "prominent", "propel", "prosper",
        "protect", "proud", "provoke", "pulsar", "pyramid", "quasar", "quest", "quick", "quicken", "quiet",
        "radiant", "rainbow", "random", "rapture", "rascal", "ravishing", "readiness", "reality", "rebel", "recipe",
        "reclaim", "reflect", "rejoice", "relax", "relinquish", "remarkable", "renegade", "renew", "renowned", "replenish",
        "replica", "request", "rescue", "research", "reside", "resilient", "resolve", "resource", "respect", "resplendent",
        "restrain", "revive", "rhapsody", "rifle", "rivulet", "roam", "romance", "ruminate", "sabotage", "sacrifice",
        "safeguard", "salvage", "sapphire", "satellite", "savor", "scandal", "scenic", "scheme", "scope", "scrutiny",
        "sculpture", "seamless", "search", "season", "secret", "seduction", "seedling", "segment", "seismic", "semicolon",
        "sensation", "serene", "shadow", "shimmer", "shipwreck", "sibling", "simplify", "simulate", "singular", "sketch",
        "sleep", "slumber", "soothe", "spark", "spectacle", "speed", "sphere", "spirit", "spontaneous", "sprout",
        "stargaze", "status", "stellar", "stimulate", "storyteller", "strategy", "streamline", "sublime", "subtle", "success",
        "suffice", "sugar", "suggestion", "summit", "sunrise", "supreme", "surge", "surrender", "survival", "synergy",
        "tangible", "telescope", "tempest", "tender", "tension", "terminate", "terrain", "testimonial", "texture", "thrive",
        "timeless", "tradition", "tranquil", "transform", "transition", "transparent", "treasure", "treaty", "tribute", "triumph",
        "trouble", "twilight", "typical", "ultimate", "universe", "unveil", "uplift", "validate", "valor", "vanish",
        "variable", "variation", "velocity", "venture", "verdict", "verify", "vibrant", "victory", "vigilant", "vintage",
        "virtue", "visionary", "vitality", "vivid", "vocation", "volcano", "vortex", "vow", "voyage", "vulnerable",
        "warrior", "weaver", "whisper", "wilderness", "willow", "witness", "wondrous", "world", "yearn", "yield"
    ]
    return random.choice(word_list) if word_list else "default"

def display_word(word, guessed_letters):
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter
        else:
            display += "_"
    return display

def draw_hangman(attempts):
    hangman_figures = [
        "  -----\n  |   |\n      |\n      |\n      |\n      |\n------",
        "  -----\n  |   |\n  O   |\n      |\n      |\n      |\n------",
        "  -----\n  |   |\n  O   |\n  |   |\n      |\n      |\n------",
        "  -----\n  |   |\n  O   |\n /|   |\n      |\n      |\n------",
        "  -----\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n------",
        "  -----\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n------",
        "  -----\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n------"
    ]
    return hangman_figures[6 - attempts]

def start_new_game():
    game_data["word"] = choose_word()
    game_data["guessed_letters"] = []
    game_data["attempts"] = 6
    game_data["result"] = ""

# ...

@app.route('/')
def index():
    display = display_word(game_data["word"], game_data["guessed_letters"])
    result = game_data["result"]
    attempts = game_data["attempts"]
    hangman_figure = draw_hangman(attempts)
    
    return (
        f"<div style='text-align: center; margin: auto; width: 80%; height: 80%; font-size: 24px; font-family: Brandon Grotesque, sans-serif; background-color: #f0f0f0;'>"
        f"<div style='font-size: 40px;'>Hangman Game</div>"
        f"<pre>{hangman_figure}</pre>"
        f"<p>{result}</p>"
        f"<p>Attempts remaining: {attempts}</p>"
        f"<p>Word: {display}</p>"
        f"<form action='{url_for('make_guess')}' method='post'>"
        f"<label for='guess'>Enter a letter:</label>"
        f"<input type='text' id='guess' name='guess' maxlength='1' required pattern='[a-zA-Z]'>"
        f"<button type='submit'>Guess</button>"
        f"</form>"
        f"</div>"
    )

# ...

@app.route('/make_guess', methods=['POST'])
def make_guess():
    if request.method == 'POST':
        guess = request.form['guess'].lower()

        if guess.isalpha() and len(guess) == 1:
            if guess in game_data["guessed_letters"]:
                game_data["result"] = "You already guessed that letter. Try again."
            elif guess in game_data["word"]:
                game_data["result"] = "Good guess!"
                game_data["guessed_letters"].append(guess)
            else:
                game_data["result"] = "Incorrect guess. Try again."
                game_data["attempts"] -= 1
        else:
            game_data["result"] = "Invalid input. Please enter a single letter."

        if set(game_data["guessed_letters"]) == set(game_data["word"]):
            game_data["result"] = f"Congratulations! You guessed the word: {game_data['word']}"
            start_new_game()

        if game_data["attempts"] == 0:
            game_data["result"] = f"Out of attempts. The word was: {game_data['word']}"
            start_new_game()

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
