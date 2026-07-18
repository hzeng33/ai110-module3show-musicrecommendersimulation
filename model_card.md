# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**
A small recommender that matches a song's vibe to the listener's taste.

---

## 2. Goal / Task

VibeMatch tries to guess which songs a person will like. The user tells it four things: a favorite genre, a mood, a target energy level, and whether they like an acoustic sound. The model checks every song in the catalog and returns the top five that fit best. It also gives a short reason for each pick, like "genre match" or "energy close to target."

---

## 3. How the Model Works

Every song starts at zero points and earns points for matching the user. A matching genre is the biggest reward at 2 points. A matching mood adds 1 point. Energy adds up to 1.5 points, and a song earns more the closer its energy is to what the user asked for. If the user likes acoustic music, a song can add up to 1 more point based on how acoustic it sounds. The model adds these up, sorts every song from highest to lowest, and returns the top five.

---

## 4. Data Used

The catalog has 18 songs stored in a CSV file. Each song lists a genre and a mood, plus number values for energy, tempo, valence, danceability, and how acoustic it is. Most genres have only one song, and many styles of music are missing.

---

## 5. Strengths

The model works best when a user's taste is clear and lines up with common genres like pop or lofi, since those have several songs to choose from. For a listener who wants upbeat pop, the top pick usually nails the genre, mood, and energy all at once, which matches my gut feeling. The short reasons are also a strength, because you can always see why a song was picked. The command-line output presents each result as a formatted table (via the `tabulate` library, with a plain-ASCII fallback) whose final column spells out the exact reasons behind every score, which makes the ranking easy to read and audit at a glance. Overall it does a good job when the request is simple and the catalog actually has matching songs.

---

## 6. Observed Behavior / Biases

The clearest weakness I found is that the model leans too hard on an exact genre match. Because a matching genre is worth a full 2.0 points and the match has to be spelled identically, the scorer treats "pop" and "indie pop" as complete strangers even though a listener would happily enjoy both. My adversarial "calm acoustic metal" profile showed this plainly: the one true metal song, _Iron Verdict_, still forced its way into the top results on its genre point alone, despite being loud and non-acoustic, which is the opposite of what that user asked for. The problem is worse for niche tastes, since most genres in my catalog have only a single song, so those users get one real hit and then four unrelated tracks pulled in just to fill the list. In short, the scoring over-prioritizes a narrow genre label and can trap a user in a small corner of the catalog instead of surfacing songs that actually fit their mood and energy.

---

## 7. Evaluation

### Profiles I tested

I ran seven made-up listeners through the recommender. Three were normal, everyday tastes: **High-Energy Pop** (upbeat pop, high energy), **Chill Lofi** (calm lofi, low energy, likes acoustic), and **Deep Intense Rock** (loud, intense rock). The other four were "trick" profiles meant to push on the scoring: **High Energy but Sad** (someone who wants loud music that is also sad), **Calm Acoustic Metal** (a quiet, acoustic, chill metal song that does not really exist), **Acoustic Fan Wants EDM** (loves acoustic sound but asks for electronic dance music), and an **Empty Profile** with no preferences at all. For each one I looked at the top five songs and asked a simple question: do these picks actually match what this person said they wanted?

### What surprised me

The biggest surprise was "Gym Hero" showing up near the top for the Happy Pop listener, even landing above songs that fit the mood better. The Happy Pop user asked for three things: pop, a happy mood, and high energy. "Gym Hero" is a pop song with very high energy, so it wins the big genre point (worth 2) and most of the energy points. But its mood is labeled "intense," not "happy," so it misses the mood point. It turns out that a genre match plus an energy match is already so many points that the song beats gentler options even though its mood is wrong. So the app keeps recommending an intense workout song to someone who just wanted something happy, simply because it carries the "pop" label and is loud. The other surprise was the Empty Profile: with no preferences, every song tied at zero and the app just handed back the first five rows of the file, which looks like a ranking but is really just the file's order.

### Comparing pairs of profiles

- **High-Energy Pop vs. Chill Lofi:** These are near opposites, and the outputs reflect that. Pop pulled loud, upbeat songs like _Sunrise City_ and _Gym Hero_; Lofi pulled quiet, mellow songs like _Library Rain_ and _Midnight Coding_. This makes sense because the two users asked for opposite energy levels and different genres, so almost no songs overlap.
- **High-Energy Pop vs. Deep Intense Rock:** Both want high energy, so a few loud songs (_Storm Runner_, _Neon Pulse Arena_, _Gym Hero_) appear on both lists. The difference is the top pick: Pop crowns _Sunrise City_ and Rock crowns _Storm Runner_, because the genre point breaks the tie between two otherwise similar high-energy songs. This is valid — same energy taste, different genre, so the lists share a bottom but split at the top.
- **Chill Lofi vs. Deep Intense Rock:** This pair shows energy doing its job. Lofi's list sits at the calm end (energy around 0.35) while Rock's sits at the loud end (energy around 0.9), and there is basically no overlap. It makes sense because energy is the one preference where these two users disagree the most.
- **Chill Lofi vs. Acoustic Fan Wants EDM:** Both users say they like acoustic, but the results look very different, and that is the point. For Lofi, the acoustic bonus adds real weight to soft guitar-and-piano tracks. For the EDM fan, the acoustic bonus barely matters, because electronic songs have almost no acoustic quality to reward — so the winning EDM song gets only a tiny acoustic boost. This shows the acoustic preference only helps when the songs in that genre are actually acoustic.
- **High Energy but Sad vs. Deep Intense Rock:** Both asked for high energy, but the "sad" user ends up with _Paper Boats_, a quiet, sad folk song, at the top. Rock, by contrast, gets a genuinely loud winner. The reason is that genre and mood together outweigh energy, so the sad label pulled a calm song to the top even though the user also asked for loud music. It is a good example of the scorer trusting the category labels over the energy number.
- **Calm Acoustic Metal vs. Chill Lofi:** These lists look almost the same at the top — both are full of calm, acoustic tracks — because the metal user's real request (quiet and acoustic) matches lofi songs better than it matches metal. The only sign of the metal request is _Iron Verdict_ sneaking into the list on its genre point alone, despite being loud and harsh. This makes sense given how heavy the genre point is, and it is not really a valid recommendation for someone who wanted calm music.
- **Empty Profile vs. any other profile:** Every other profile produces a clearly personalized list, but the Empty Profile produces the same generic top five no matter what, because nothing scores any points. Comparing them shows how much the app depends on the user actually stating a preference — with none, it has nothing to sort by and falls back on file order.

---

## 8. Future Work

- **Give partial genre credit.** Let close genres like "pop" and "indie pop" share some points, so the model stops treating them as strangers.
- **Let the user choose what matters most.** Right now genre almost always wins. I would lower its weight or let people say whether genre, mood, or energy matters most to them.
- **Use more of the data and handle empty cases.** I would score tempo and danceability too, and add a real fallback for a user who gives no preferences, instead of returning file order.

---

## 9. Personal Reflection

My biggest learning moment was seeing how one heavy rule, the genre point, quietly shaped almost every result, even when it gave the user the wrong vibe. That is when bias stopped being an abstract idea and became something I could point to in my own code.

AI tools helped me move faster. They helped me set up the test profiles, spot the "Gym Hero" pattern, and put my thoughts into clear sentences. But I still had to double-check them. A few times the explanations sounded confident but did not fully match my actual output, so I ran the code myself and compared the real numbers before trusting them.

What surprised me most was how something this simple can still "feel" like a real recommendation. There is no learning or magic here, just points being added and sorted, yet the results look personal and the short reasons make them feel smart. It made me realize a lot of everyday apps might be simpler under the hood than they seem.

If I extended this project, I would give close genres partial credit, let the user choose which feature matters most, and use more of the song data like tempo and danceability. I would also add a real fallback for users who give no preferences, so the app does not just hand back the order of the file.
