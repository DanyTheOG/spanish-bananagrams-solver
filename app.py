from flask import Flask, request, jsonify
from collections import Counter

app = Flask(__name__)

# -------------------------------------------------
# 1. DICTIONARY LOADING
# -------------------------------------------------

def load_spanish_dictionary(filepath="spanish_words.txt"):
    """
    Loads Spanish words from a text file into a set of uppercase words.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            words = {line.strip().upper() for line in f if line.strip()}
        print(f"Dictionary loaded with {len(words):,} words.")
        return words
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found. Returning an empty dictionary.")
        return set()

dictionary = load_spanish_dictionary()

# -------------------------------------------------
# 2. WORD GENERATION LOGIC
# -------------------------------------------------

def can_form_word_only_tiles(word, tiles):
    """
    Checks if 'word' can be formed using only 'tiles'.
    """
    tile_counter = Counter(tiles)
    word_counter = Counter(word)

    for letter, count in word_counter.items():
        if tile_counter[letter] < count:
            return False
    return True

def generate_words(tiles, dictionary, limit=10):
    """
    Generates up to 'limit' longest words from the dictionary using 'tiles'.
    """
    tile_counter = Counter(tiles)
    valid_words = [word for word in dictionary if can_form_word_only_tiles(word, tiles)]
    valid_words.sort(key=lambda x: (-len(x), x))  # Sort by length descending, then alphabetically
    return valid_words[:limit]

# -------------------------------------------------
# 3. FLASK ENDPOINTS
# -------------------------------------------------

@app.route('/')
def home():
    return "Welcome to the Spanish Bananagrams Solver API!"

@app.route('/generate', methods=['POST'])
def generate():
    """
    Endpoint to generate words based on provided tiles.
    Expects JSON with a 'tiles' key.
    """
    data = request.json
    tiles = data.get("tiles", "").upper().replace(" ", "").split(",")
    words = generate_words(tiles, dictionary)
    return jsonify({"words": words})

# -------------------------------------------------
# RUN APP
# -------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
