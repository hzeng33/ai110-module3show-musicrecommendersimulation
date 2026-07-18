import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dictionaries.
    Required by src/main.py

    Numeric columns are converted so later math works:
      - id and tempo_bpm become ints
      - energy, valence, danceability, acousticness become floats
    Everything else (title, artist, genre, mood) stays a string.
    """
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs


# --- Algorithm Recipe weights (see README "My Finalized Algorithm Recipe") ---
GENRE_WEIGHT = 2.0      # +2.0 for a genre match
MOOD_WEIGHT = 1.0       # +1.0 for a mood match
ENERGY_WEIGHT = 1.5     # up to +1.5 for energy closeness
ACOUSTIC_WEIGHT = 1.0   # up to +1.0 acoustic bonus, only if the user likes acoustic

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the Algorithm Recipe.

    user_prefs keys: "genre", "mood", "energy", and "likes_acoustic".
    Returns (score, reasons), where reasons is a list of short strings such as
    "genre match (+2.0)" so the user can see whya song was recommended.
    """
    score = 0.0
    reasons: List[str] = []

    # Genre match: +2.0. Compared case-insensitively so "Pop" == "pop".
    favorite_genre = user_prefs.get("genre", "")
    if favorite_genre and song["genre"].lower() == favorite_genre.lower():
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT})")

    # Mood match: +1.0.
    favorite_mood = user_prefs.get("mood", "")
    if favorite_mood and song["mood"].lower() == favorite_mood.lower():
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT})")

    # Energy closeness: reward being NEAR the target, not being loud.
    # distance is 0 when identical and grows to 1 at the far end of the 0..1
    # scale, so (1 - distance) is 1 for a perfect match and fades to 0.
    target_energy = user_prefs.get("energy", None)
    if target_energy is not None:
        distance = abs(song["energy"] - target_energy)
        energy_points = round((1 - distance) * ENERGY_WEIGHT, 2)
        if energy_points > 0:
            score += energy_points
            reasons.append(f"energy close to target (+{energy_points})")

    # Acoustic bonus: only when the user asked for an acoustic sound. Scales
    # with the song's own acousticness, so more acoustic tracks earn more.
    if user_prefs.get("likes_acoustic", False):
        acoustic_points = round(song["acousticness"] * ACOUSTIC_WEIGHT, 2)
        if acoustic_points > 0:
            score += acoustic_points
            reasons.append(f"acoustic sound (+{acoustic_points})")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Judge every song with score_song. A list comprehension is the Pythonic
    # way to turn one list (songs) into another (song + its score + reasons).
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    # Rank: sort the whole catalog by score, highest first. sorted() returns a
    # new list and leaves the caller's `songs` untouched.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    # Keep the top k and turn each reasons list into a readable sentence.
    return [
        (song, score, ", ".join(reasons) if reasons else "no strong matches")
        for song, score, reasons in ranked[:k]
    ]
