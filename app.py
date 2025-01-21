from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
from collections import Counter

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# -------------------------------------------------
# 1. DICTIONARY LOADING
# -------------------------------------------------
def load_spanish_dictionary(filepath="spanish_words.txt"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return {line.strip().upper() for line in f if line.strip()}
    except FileNotFoundError:
        return set()

dictionary = load_spanish_dictionary()

# -------------------------------------------------
# 2. WORD GENERATION LOGIC
# -------------------------------------------------
def can_form_word_only_tiles(word, tiles):
    tile_counter = Counter(tiles)
    word_counter = Counter(word)

    for letter, count in word_counter.items():
        if tile_counter[letter] < count:
            return False
    return True

def generate_words(tiles, dictionary, limit=10):
    tile_counter = Counter(tiles)
    valid_words = [word for word in dictionary if can_form_word_only_tiles(word, tiles)]
    valid_words.sort(key=lambda x: (-len(x), x))
    return valid_words[:limit]

# -------------------------------------------------
# 3. FLASK ENDPOINTS
# -------------------------------------------------
@app.route('/')
def home():
    return "Welcome to the Spanish Bananagrams Solver API!"

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    tiles = data.get("tiles", "").upper().replace(" ", "").split(",")
    words = generate_words(tiles, dictionary)
    return jsonify({"words": words})

# -------------------------------------------------
# RUN APP
# -------------------------------------------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
