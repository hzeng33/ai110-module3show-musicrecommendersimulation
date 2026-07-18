
# Support both `python -m src.main` (run from the project root) and
# `python src/main.py` (run from inside src/).
try:
    from src.recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# Profiles
#
# The first three are "clean" taste profiles: each states a genre, a mood, an
# energy target, and an acoustic preference that all point the same direction.
#
# The remaining profiles are deliberately adversarial / edge cases. They are
# built to stress the scoring logic: conflicting signals, impossible combos,
# and an empty profile. See the comment above each one for what it probes.
# ---------------------------------------------------------------------------
PROFILES = [
    # --- Three distinct, coherent profiles ---------------------------------
    (
        "High-Energy Pop",
        {"genre": "pop", "mood": "happy", "energy": 0.9, "likes_acoustic": False},
    ),
    (
        "Chill Lofi",
        {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    ),
    (
        "Deep Intense Rock",
        {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
    ),

    # --- Adversarial / edge-case profiles ----------------------------------
    # 1) Conflicting energy vs. mood: wants very high energy but a sad mood.
    #    Almost no real song is both loud AND sad, so which signal wins?
    (
        "Adversarial: High Energy but Sad",
        {"genre": "folk", "mood": "sad", "energy": 0.95, "likes_acoustic": False},
    ),
    # 2) Impossible combo: metal is angry and loud, yet this user asks for a
    #    calm, acoustic, chill metal track that does not exist in the catalog.
    (
        "Adversarial: Calm Acoustic Metal",
        {"genre": "metal", "mood": "chill", "energy": 0.1, "likes_acoustic": True},
    ),
    # 3) Acoustic lover chasing an electronic genre. Acousticness and edm pull
    #    in opposite directions, so the acoustic bonus fights the genre match.
    (
        "Adversarial: Acoustic Fan Wants EDM",
        {"genre": "edm", "mood": "energetic", "energy": 0.95, "likes_acoustic": True},
    ),
    # 4) Empty profile: no genre, no mood, no energy target, no acoustic pref.
    #    Every song scores 0, so this checks the tie-breaking / default order.
    (
        "Edge Case: Empty Profile",
        {"genre": "", "mood": "", "energy": None, "likes_acoustic": False},
    ),
]


HEADERS = ["#", "Song", "Artist", "Score", "Why it was picked"]


def _ascii_table(rows: list) -> str:
    """
    Fallback table used when `tabulate` is not installed. Builds a simple
    box-drawn table by hand so the app still runs with zero dependencies.
    """
    columns = [HEADERS] + [[str(cell) for cell in row] for row in rows]
    widths = [max(len(row[i]) for row in columns) for i in range(len(HEADERS))]

    def divider() -> str:
        return "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def line(cells: list) -> str:
        padded = [f" {cell:<{widths[i]}} " for i, cell in enumerate(cells)]
        return "|" + "|".join(padded) + "|"

    out = [divider(), line(HEADERS), divider()]
    out += [line([str(cell) for cell in row]) for row in rows]
    out.append(divider())
    return "\n".join(out)


def format_recommendations_table(recommendations: list) -> str:
    """
    Turn the (song, score, reasons) tuples into a readable table. Every row
    keeps the full 'reasons' string so you can see WHY each song scored.
    """
    rows = [
        [rank, song["title"], song["artist"], f"{score:.2f}", explanation]
        for rank, (song, score, explanation) in enumerate(recommendations, 1)
    ]

    try:
        from tabulate import tabulate

        return tabulate(
            rows,
            headers=HEADERS,
            tablefmt="grid",
            # Wrap the long reasons column instead of stretching the table.
            maxcolwidths=[None, 22, 16, None, 42],
        )
    except ModuleNotFoundError:
        return _ascii_table(rows)


def print_recommendations(name: str, user_prefs: dict, songs: list) -> None:
    """Run the recommender for one profile and print its top 5 results."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("=" * 70)
    print(f"PROFILE: {name}")
    print(f"Prefs: {user_prefs}")
    print("=" * 70)
    print(format_recommendations_table(recommendations))
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in PROFILES:
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
