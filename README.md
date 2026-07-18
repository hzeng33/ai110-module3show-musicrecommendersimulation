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

Below is a real run of the recommender for the default taste profile
`genre=pop, mood=happy, energy=0.8, likes_acoustic=False`, produced by
`python src/main.py`:

```
Top recommendations:

Sunrise City - Score: 4.47
Because: genre match (+2.0), mood match (+1.0), energy close to target (+1.47)

Gym Hero - Score: 3.30
Because: genre match (+2.0), energy close to target (+1.3)

Rooftop Lights - Score: 2.44
Because: mood match (+1.0), energy close to target (+1.44)

Night Drive Loop - Score: 1.42
Because: energy close to target (+1.42)

Storm Runner - Score: 1.33
Because: energy close to target (+1.33)
```

A quick read of this run: Sunrise City wins clearly because it is the only song
that matches the genre, the mood, and the target energy all at once. The more
interesting result is that Gym Hero lands above Rooftop Lights. Gym Hero is pop
but its mood is intense, while Rooftop Lights is genuinely happy with an almost
perfect energy match. Because a genre match is worth a full 2.0 and a mood match
is only worth 1.0, the pop label alone outweighs the better mood and energy fit.
This is the genre priority bias described above showing up in a real result.

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
