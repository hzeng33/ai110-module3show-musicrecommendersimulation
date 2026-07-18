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

### Data Flow

The whole program moves in one direction, from what the user tells us to a short list of songs we hand back:

```
Input (User Prefs)  →  Process (The Loop: judge every song in the CSV)  →  Output (The Ranking: Top K songs)
```

I like to think of it in three stages:

1. **Input.** We load all the songs from `data/songs.csv` into memory and we read the user's taste profile, which is their favorite genre, their mood, the energy level they are aiming for, and whether they enjoy an acoustic sound.
2. **Process, the loop.** We walk through the catalog one song at a time and run each song through the scoring recipe below. At this stage the song is judged completely on its own. It knows nothing about the other songs. The output of this stage is a score and a short list of reasons for every song.
3. **Output, the ranking.** Once every song has a score, we sort the whole catalog from the highest score to the lowest and keep only the top K, for example the top five. This is the one and only place where songs are compared against each other.

Keeping scoring and ranking separate is the core idea. Scoring answers "how well does this one song fit the user," and ranking answers "which of these songs win."

### My Finalized Algorithm Recipe

Every song starts at zero points and earns points for matching the user. Here is the exact recipe I settled on:

| Rule             | Points     | Reasoning                                                          |
| ---------------- | ---------- | ------------------------------------------------------------------ |
| Genre match      | +2.0       | Genre is the strongest taste signal, so it carries the most weight |
| Mood match       | +1.0       | Mood matters but it blurs across genres, so it counts for less     |
| Energy closeness | up to +1.5 | Reward for sitting near the target energy, not for being loud      |
| Acoustic bonus   | up to +1.0 | Only added when the user says they like an acoustic sound          |

Explanation for couple of rules:

- Energy closeness - rewards nearness, not size. I take the distance between the song's energy and the user's target energy, subtract that distance from one, and multiply the result by 1.5. A song that sits right on the target earns the full 1.5, and the points fade toward zero as the gap grows. Both energy values live on a scale from 0 to 1.
- Acoustic bonus - scales with the song's own acousticness value times 1.0, so a very acoustic track earns more than a barely acoustic one, but only when the user asked for that sound.

The most any single song can earn is 2.0 plus 1.0 plus 1.5 plus 1.0, which comes to a ceiling of **5.5 points**. The ordering of the weights, genre above energy above mood and acoustic, is a deliberate claim about taste: genre is close to a deal breaker, energy sets the vibe, and mood and acousticness act as tie breakers.

### Biases I Expect

Because I chose these weights by hand, the system carries some biases I already anticipate:

- **It may over prioritize genre.** With genre worth a full 2.0, a song in the exact right genre can beat a wonderful song that nails the user's mood and energy but happens to sit in a neighboring genre. Great matches can get buried simply for wearing the wrong label.
- **It treats genres as all or nothing.** The match is exact, so "pop" and "indie pop" earn zero shared credit even though a listener would probably enjoy both. There is no idea of genres being close cousins.
- **It leans toward the average middle of the catalog.** Since energy rewards closeness to the target, songs with a very high or very low energy rarely score well unless the user aims for an extreme, so unusual or adventurous tracks tend to lose out.
- **It can echo a single preference too loudly.** A user who states a strong genre will keep seeing that same genre, which narrows discovery and can trap them in a small corner of the catalog.

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

The recommender prints each result as a formatted table (using the
[`tabulate`](https://pypi.org/project/tabulate/) library, with a plain-ASCII
fallback if it is not installed). The last column always carries the full list
of reasons behind the score, so you can see *why* every song was picked, not
just where it ranked.

Below is a real run for the default taste profile
`genre=pop, mood=happy, energy=0.8, likes_acoustic=False`, produced by
`python -m src.main`:

```
+-----+------------------+---------------+---------+--------------------------------------------+
|   # | Song             | Artist        |   Score | Why it was picked                          |
+=====+==================+===============+=========+============================================+
|   1 | Sunrise City     | Neon Echo     |    4.47 | genre match (+2.0), mood match (+1.0),     |
|     |                  |               |         | energy close to target (+1.47)             |
+-----+------------------+---------------+---------+--------------------------------------------+
|   2 | Gym Hero         | Max Pulse     |    3.3  | genre match (+2.0), energy close to target |
|     |                  |               |         | (+1.3)                                     |
+-----+------------------+---------------+---------+--------------------------------------------+
|   3 | Rooftop Lights   | Indigo Parade |    2.44 | mood match (+1.0), energy close to target  |
|     |                  |               |         | (+1.44)                                    |
+-----+------------------+---------------+---------+--------------------------------------------+
|   4 | Night Drive Loop | Neon Echo     |    1.42 | energy close to target (+1.42)             |
+-----+------------------+---------------+---------+--------------------------------------------+
|   5 | Storm Runner     | Voltline      |    1.33 | energy close to target (+1.33)             |
+-----+------------------+---------------+---------+--------------------------------------------+
```

A quick read of this run: Sunrise City wins clearly because it is the only song
that matches the genre, the mood, and the target energy all at once. The more
interesting result is that Gym Hero lands above Rooftop Lights. Gym Hero is pop
but its mood is intense, while Rooftop Lights is genuinely happy with an almost
perfect energy match. Because a genre match is worth a full 2.0 and a mood match
is only worth 1.0, the pop label alone outweighs the better mood and energy fit.
This is the genre priority bias described above showing up in a real result.

---

### Multiple User Profiles & Adversarial Edge Cases

`src/main.py` runs the recommender against seven profiles: three normal taste
profiles and four edge cases meant to stress the scorer. Each block below is the
top 5 from a real `python src/main.py` run.

#### Three Distinct Profiles

**High-Energy Pop** — `genre=pop, mood=happy, energy=0.9, likes_acoustic=False`

```
======================================================================
PROFILE: High-Energy Pop
Prefs: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9, 'likes_acoustic': False}
======================================================================
+-----+------------------+---------------+---------+--------------------------------------------+
|   # | Song             | Artist        |   Score | Why it was picked                          |
+=====+==================+===============+=========+============================================+
|   1 | Sunrise City     | Neon Echo     |    4.38 | genre match (+2.0), mood match (+1.0),     |
|     |                  |               |         | energy close to target (+1.38)             |
+-----+------------------+---------------+---------+--------------------------------------------+
|   2 | Gym Hero         | Max Pulse     |    3.46 | genre match (+2.0), energy close to target |
|     |                  |               |         | (+1.46)                                    |
+-----+------------------+---------------+---------+--------------------------------------------+
|   3 | Rooftop Lights   | Indigo Parade |    2.29 | mood match (+1.0), energy close to target  |
|     |                  |               |         | (+1.29)                                    |
+-----+------------------+---------------+---------+--------------------------------------------+
|   4 | Storm Runner     | Voltline      |    1.48 | energy close to target (+1.48)             |
+-----+------------------+---------------+---------+--------------------------------------------+
|   5 | Neon Pulse Arena | Byte Surge    |    1.43 | energy close to target (+1.43)             |
+-----+------------------+---------------+---------+--------------------------------------------+
```

**Chill Lofi** — `genre=lofi, mood=chill, energy=0.35, likes_acoustic=True`

```
======================================================================
PROFILE: Chill Lofi
Prefs: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}
======================================================================
+-----+--------------------+-----------------+---------+--------------------------------------------+
|   # | Song               | Artist          |   Score | Why it was picked                          |
+=====+====================+=================+=========+============================================+
|   1 | Library Rain       | Paper Lanterns  |    5.36 | genre match (+2.0), mood match (+1.0),     |
|     |                    |                 |         | energy close to target (+1.5), acoustic    |
|     |                    |                 |         | sound (+0.86)                              |
+-----+--------------------+-----------------+---------+--------------------------------------------+
|   2 | Midnight Coding    | LoRoom          |    5.11 | genre match (+2.0), mood match (+1.0),     |
|     |                    |                 |         | energy close to target (+1.4), acoustic    |
|     |                    |                 |         | sound (+0.71)                              |
+-----+--------------------+-----------------+---------+--------------------------------------------+
|   3 | Focus Flow         | LoRoom          |    4.2  | genre match (+2.0), energy close to target |
|     |                    |                 |         | (+1.42), acoustic sound (+0.78)            |
+-----+--------------------+-----------------+---------+--------------------------------------------+
|   4 | Spacewalk Thoughts | Orbit Bloom     |    3.32 | mood match (+1.0), energy close to target  |
|     |                    |                 |         | (+1.4), acoustic sound (+0.92)             |
+-----+--------------------+-----------------+---------+--------------------------------------------+
|   5 | Moonlit Drift      | Amelie Rousseau |    2.37 | energy close to target (+1.42), acoustic   |
|     |                    |                 |         | sound (+0.95)                              |
+-----+--------------------+-----------------+---------+--------------------------------------------+
```

**Deep Intense Rock** — `genre=rock, mood=intense, energy=0.9, likes_acoustic=False`

```
======================================================================
PROFILE: Deep Intense Rock
Prefs: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False}
======================================================================
+-----+------------------+------------+---------+-------------------------------------------+
|   # | Song             | Artist     |   Score | Why it was picked                         |
+=====+==================+============+=========+===========================================+
|   1 | Storm Runner     | Voltline   |    4.48 | genre match (+2.0), mood match (+1.0),    |
|     |                  |            |         | energy close to target (+1.48)            |
+-----+------------------+------------+---------+-------------------------------------------+
|   2 | Gym Hero         | Max Pulse  |    2.46 | mood match (+1.0), energy close to target |
|     |                  |            |         | (+1.46)                                   |
+-----+------------------+------------+---------+-------------------------------------------+
|   3 | Neon Pulse Arena | Byte Surge |    1.43 | energy close to target (+1.43)            |
+-----+------------------+------------+---------+-------------------------------------------+
|   4 | Iron Verdict     | Ashfall    |    1.4  | energy close to target (+1.4)             |
+-----+------------------+------------+---------+-------------------------------------------+
|   5 | Sunrise City     | Neon Echo  |    1.38 | energy close to target (+1.38)            |
+-----+------------------+------------+---------+-------------------------------------------+
```

All three behave as expected: the song matching genre, mood, and energy wins
clearly, and the acoustic bonus pushes two Chill Lofi tracks past 5.0.

#### Adversarial & Edge-Case Profiles

**Conflicting energy vs. mood** — `genre=folk, mood=sad, energy=0.95, likes_acoustic=False`

```
======================================================================
PROFILE: Adversarial: High Energy but Sad
Prefs: {'genre': 'folk', 'mood': 'sad', 'energy': 0.95, 'likes_acoustic': False}
======================================================================
+-----+------------------+-----------------+---------+----------------------------------------+
|   # | Song             | Artist          |   Score | Why it was picked                      |
+=====+==================+=================+=========+========================================+
|   1 | Paper Boats      | Wren and Hollow |    3.57 | genre match (+2.0), mood match (+1.0), |
|     |                  |                 |         | energy close to target (+0.57)         |
+-----+------------------+-----------------+---------+----------------------------------------+
|   2 | Neon Pulse Arena | Byte Surge      |    1.5  | energy close to target (+1.5)          |
+-----+------------------+-----------------+---------+----------------------------------------+
|   3 | Gym Hero         | Max Pulse       |    1.47 | energy close to target (+1.47)         |
+-----+------------------+-----------------+---------+----------------------------------------+
|   4 | Iron Verdict     | Ashfall         |    1.47 | energy close to target (+1.47)         |
+-----+------------------+-----------------+---------+----------------------------------------+
|   5 | Storm Runner     | Voltline        |    1.44 | energy close to target (+1.44)         |
+-----+------------------+-----------------+---------+----------------------------------------+
```

Genre and mood together (3.0) beat the energy signal, so a calm sad folk song
wins even though its energy is the opposite of what was asked. The loud tracks
the user really wanted sit far below at ~1.5, with the wrong mood.

**Impossible combo: calm, acoustic metal** — `genre=metal, mood=chill, energy=0.1, likes_acoustic=True`

```
======================================================================
PROFILE: Adversarial: Calm Acoustic Metal
Prefs: {'genre': 'metal', 'mood': 'chill', 'energy': 0.1, 'likes_acoustic': True}
======================================================================
+-----+--------------------+-----------------+---------+--------------------------------------------+
|   # | Song               | Artist          |   Score | Why it was picked                          |
+=====+====================+=================+=========+============================================+
|   1 | Spacewalk Thoughts | Orbit Bloom     |    3.15 | mood match (+1.0), energy close to target  |
|     |                    |                 |         | (+1.23), acoustic sound (+0.92)            |
+-----+--------------------+-----------------+---------+--------------------------------------------+
|   2 | Library Rain       | Paper Lanterns  |    2.98 | mood match (+1.0), energy close to target  |
|     |                    |                 |         | (+1.12), acoustic sound (+0.86)            |
+-----+--------------------+-----------------+---------+--------------------------------------------+
|   3 | Midnight Coding    | LoRoom          |    2.73 | mood match (+1.0), energy close to target  |
|     |                    |                 |         | (+1.02), acoustic sound (+0.71)            |
+-----+--------------------+-----------------+---------+--------------------------------------------+
|   4 | Iron Verdict       | Ashfall         |    2.24 | genre match (+2.0), energy close to target |
|     |                    |                 |         | (+0.2), acoustic sound (+0.04)             |
+-----+--------------------+-----------------+---------+--------------------------------------------+
|   5 | Moonlit Drift      | Amelie Rousseau |    2.15 | energy close to target (+1.2), acoustic    |
|     |                    |                 |         | sound (+0.95)                              |
+-----+--------------------+-----------------+---------+--------------------------------------------+
```

No song fits the genre and the vibe, so the top picks drop metal entirely and
serve calm acoustic tracks. Yet the one real metal song still lands 4th on its
genre match alone, despite being loud and non-acoustic — the exact-label match
outweighs missing every other preference.

**Acoustic fan chasing EDM** — `genre=edm, mood=energetic, energy=0.95, likes_acoustic=True`

```
======================================================================
PROFILE: Adversarial: Acoustic Fan Wants EDM
Prefs: {'genre': 'edm', 'mood': 'energetic', 'energy': 0.95, 'likes_acoustic': True}
======================================================================
+-----+------------------+---------------+---------+------------------------------------------+
|   # | Song             | Artist        |   Score | Why it was picked                        |
+=====+==================+===============+=========+==========================================+
|   1 | Neon Pulse Arena | Byte Surge    |    4.53 | genre match (+2.0), mood match (+1.0),   |
|     |                  |               |         | energy close to target (+1.5), acoustic  |
|     |                  |               |         | sound (+0.03)                            |
+-----+------------------+---------------+---------+------------------------------------------+
|   2 | Rooftop Lights   | Indigo Parade |    1.57 | energy close to target (+1.22), acoustic |
|     |                  |               |         | sound (+0.35)                            |
+-----+------------------+---------------+---------+------------------------------------------+
|   3 | Canyon Dust      | Sawyer Wells  |    1.56 | energy close to target (+0.9), acoustic  |
|     |                  |               |         | sound (+0.66)                            |
+-----+------------------+---------------+---------+------------------------------------------+
|   4 | Storm Runner     | Voltline      |    1.54 | energy close to target (+1.44), acoustic |
|     |                  |               |         | sound (+0.1)                             |
+-----+------------------+---------------+---------+------------------------------------------+
|   5 | Gym Hero         | Max Pulse     |    1.52 | energy close to target (+1.47), acoustic |
|     |                  |               |         | sound (+0.05)                            |
+-----+------------------+---------------+---------+------------------------------------------+
```

The acoustic preference barely registers: the EDM winner earns only a +0.03
acoustic bonus because electronic tracks are near-zero acoustic. So
`likes_acoustic` is effectively ignored here and only nudges the low-scoring tail.

**Empty profile** — `genre="", mood="", energy=None, likes_acoustic=False`

```
======================================================================
PROFILE: Edge Case: Empty Profile
Prefs: {'genre': '', 'mood': '', 'energy': None, 'likes_acoustic': False}
======================================================================
+-----+-----------------+----------------+---------+---------------------+
|   # | Song            | Artist         |   Score | Why it was picked   |
+=====+=================+================+=========+=====================+
|   1 | Sunrise City    | Neon Echo      |       0 | no strong matches   |
+-----+-----------------+----------------+---------+---------------------+
|   2 | Midnight Coding | LoRoom         |       0 | no strong matches   |
+-----+-----------------+----------------+---------+---------------------+
|   3 | Storm Runner    | Voltline       |       0 | no strong matches   |
+-----+-----------------+----------------+---------+---------------------+
|   4 | Library Rain    | Paper Lanterns |       0 | no strong matches   |
+-----+-----------------+----------------+---------+---------------------+
|   5 | Gym Hero        | Max Pulse      |       0 | no strong matches   |
+-----+-----------------+----------------+---------+---------------------+
```

Nothing crashes on the empty strings or `None` energy, and every song ties at
0.00. But a stable sort then just returns the first five rows of the CSV, so an
empty profile gets file order dressed up as a ranking — a real system would need
a fallback here.

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

Building this taught me that a recommender turns data into predictions by scoring each song against what the user says they want and then sorting those scores, so a "prediction" is really just simple math deciding which song fits best. It also showed me that bias sneaks in through my own design choices, like making genre worth the most points or using a small uneven catalog, which can quietly push some users toward the same narrow set of songs while ignoring tastes the data never covers.
