# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real world recommenders like the ones on Spotify or YouTube learn from huge amounts of behavior. They watch what millions of people play, skip, save, and replay, and they use those patterns to guess what someone will enjoy next. They also mix in the qualities of the songs themselves, such as genre and energy, and they keep updating as tastes change. My version is much smaller and simpler. It does not learn from crowds or history. Instead it focuses on content, meaning it compares the qualities of each song to a taste profile the user describes up front. My version prioritizes matching a user's stated genre and mood, keeping the song's energy close to what the user wants, and honoring whether the user prefers an acoustic sound.

- What each `Song` uses
  Every song stores its identity plus a set of qualities the recommender can compare against:
  - `id`, `title`, `artist` for identity and display
  - `genre` (for example pop, lofi, rock, jazz)
  - `mood` (for example happy, chill, intense, focused)
  - `energy` (0 to 1, how calm or intense the song feels)
  - `tempo_bpm` (speed in beats per minute)
  - `valence` (0 to 1, how positive or upbeat the song sounds)
  - `danceability` (0 to 1, how easy it is to move to)
  - `acousticness` (0 to 1, how acoustic versus produced it sounds)

- What the `UserProfile` stores
  The profile holds what the user tells us about their taste:
  - `favorite_genre` the genre they want to hear
  - `favorite_mood` the mood they are in
  - `target_energy` the energy level they are aiming for (0 to 1)
  - `likes_acoustic` whether they prefer an acoustic sound

- How the `Recommender` computes a score
  The recommender scores one song at a time. It gives points when the song's genre matches the favorite genre and fewer points when the mood matches, since genre is a stronger taste signal. For energy it rewards closeness rather than size, so a song whose energy sits near the target scores higher than one that is far away in either direction. If the user likes acoustic music, songs with higher acousticness earn extra points. Each quality is weighted so that the strongest signals count for more.

- How songs are chosen
  After every song has a score, the recommender sorts the whole list from highest score to lowest and returns the top few. Scoring judges one song on its own, and ranking then compares all of those scores to decide the final order.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
