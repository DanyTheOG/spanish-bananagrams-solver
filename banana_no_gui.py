import sys
from collections import Counter

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
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading dictionary: {e}")
        sys.exit(1)

# -------------------------------------------------
# 2. WORD GENERATION LOGIC
# -------------------------------------------------

def can_form_word_exactly_one_free_tile(word, tiles, free_tiles):
    """
    Checks if 'word' can be formed from 'tiles' + 'free_tiles'.
    Ensures that exactly one free tile is used.
    """
    tile_counter = Counter(tiles)
    free_tile_counter = Counter(free_tiles)
    word_counter = Counter(word)

    total_available = tile_counter + free_tile_counter
    for letter, count in word_counter.items():
        if total_available[letter] < count:
            return False

    overlap_letters = word_counter & free_tile_counter
    total_possible_free_usages = sum(overlap_letters.values())

    if total_possible_free_usages >= 1:
        for free_tile in free_tile_counter:
            if word_counter[free_tile] >= 1 and free_tile_counter[free_tile] >= 1:
                temp_tile_counter = tile_counter.copy()
                temp_tile_counter[free_tile] -= 1

                can_cover = True
                for letter, cnt in word_counter.items():
                    required = cnt
                    if letter == free_tile:
                        required -= 1
                    if required > temp_tile_counter.get(letter, 0):
                        can_cover = False
                        break
                if can_cover:
                    return True
        return False
    else:
        return False

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

def generate_words(tiles, dictionary, free_tiles=None, limit=10):
    """
    Generates up to 'limit' longest words from the dictionary using 'tiles' and 'free_tiles'.
    If 'free_tiles' is provided, ensures that exactly one free tile is used.
    """
    if free_tiles:
        valid_words = [word for word in dictionary if can_form_word_exactly_one_free_tile(word, tiles, free_tiles)]
    else:
        valid_words = [word for word in dictionary if can_form_word_only_tiles(word, tiles)]

    valid_words.sort(key=lambda x: (-len(x), x))  # Sort by length descending, then alphabetically
    return valid_words[:limit]

# -------------------------------------------------
# 3. TILE MANAGEMENT
# -------------------------------------------------

def split_tiles(tiles):
    """
    Splits a string of tiles into individual letters, considering special Spanish tiles (CH, LL, RR).
    """
    special_tiles = {"CH", "LL", "RR"}
    result = []
    i = 0
    tiles = tiles.upper().replace(" ", "")  # Remove spaces and uppercase

    while i < len(tiles):
        if i + 1 < len(tiles):
            pair = tiles[i:i+2]
            if pair in special_tiles:
                result.append(pair)
                i += 2
                continue
        result.append(tiles[i])
        i += 1

    return result

# -------------------------------------------------
# 4. MAIN FUNCTION
# -------------------------------------------------

def main():
    print("Welcome to the Spanish Bananagrams Solver!")
    print("This program helps you find words using your tiles.")
    print()

    # Load dictionary
    dictionary = load_spanish_dictionary()

    # Get initial tiles from user
    tiles_input = input("Enter the tiles in your hand (e.g., afretstegs,ch,heroef,rr): ")
    tiles_in_hand = split_tiles(tiles_input)
    print(f"Tiles in hand: {', '.join(tiles_in_hand)}")

    # Main loop
    while True:
        print("\nOptions:")
        print("1. Generate words")
        print("2. Add tiles")
        print("3. Reset tiles")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")

        if choice == "1":
            # Generate words
            free_tiles_input = input("Enter free tiles (e.g., O,U) or type 'no' if none: ").strip()
            if free_tiles_input.upper() == "NO":
                free_tiles = []
            else:
                free_tiles = split_tiles(free_tiles_input)

            words = generate_words(tiles_in_hand, dictionary, free_tiles=free_tiles, limit=10)
            if words:
                print("\nTop 10 words you can form:")
                for idx, word in enumerate(words, 1):
                    print(f"{idx}. {word}")
            else:
                print("\nNo words can be formed with the current tiles.")

        elif choice == "2":
            # Add tiles
            add_tiles_input = input("Enter tiles to add (e.g., A,B,CH): ")
            added_tiles = split_tiles(add_tiles_input)
            tiles_in_hand.extend(added_tiles)
            print(f"Tiles in hand updated: {', '.join(tiles_in_hand)}")

        elif choice == "3":
            # Reset tiles
            tiles_input = input("Enter the new tiles in your hand (e.g., afretstegs,ch,heroef,rr): ")
            tiles_in_hand = split_tiles(tiles_input)
            print(f"Tiles in hand reset to: {', '.join(tiles_in_hand)}")

        elif choice == "4":
            # Exit
            print("Thank you for using the Spanish Bananagrams Solver! Goodbye!")
            break

        else:
            print("Invalid choice. Please choose a valid option.")

# -------------------------------------------------
# RUN PROGRAM
# -------------------------------------------------

if __name__ == "__main__":
    main()
