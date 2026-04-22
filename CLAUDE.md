# READ.AI Agent — CLAUDE.md

## Project Overview

**Goal:** An AI agent that understands user reading preferences and recommends books using semantic similarity, conversational refinement, and personalized taste profiles.

**One-sentence MVP:**
> A chatbot that recommends 5 books based on 3 favorite books and explains why each was chosen.

**Target users:** Avid readers, book club members, students, casual readers, niche genre fans.

---

## Problem & Solution

**Problem:** Readers struggle to find books that match their exact taste, mood, and reading preferences.

**Solution:** An AI agent that learns user preferences from favorite books, genres, moods, and feedback — then recommends books using semantic similarity and conversational refinement.

---

## MVP Features

- Favorite-book input (3–5 books to seed a taste profile)
- Semantic similarity recommendations (top 5–10 results)
- Recommendation explanations ("Recommended because you liked X")
- Basic feedback loop (thumbs up/down, "more like this")

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (MVP) → React (later) |
| Backend | Python + FastAPI |
| Data handling | Pandas |
| Embeddings | OpenAI Embeddings API |
| LLM reasoning/chat | OpenAI GPT (claude-sonnet-4-20250514 optional) |
| Vector DB | ChromaDB (MVP) → Pinecone (production) |
| Database | PostgreSQL / Supabase |
| Book data | Open Library API, Google Books API, Kaggle CSV |

---

## Architecture

```
Input Layer
  └── Favorite books, genre quiz, mood input, feedback ratings

Processing Layer
  └── Clean user input
  └── Fetch matching books from dataset
  └── Create user embedding (average of liked book vectors)
  └── Update preference profile

Recommendation Engine
  └── Vector similarity search (cosine similarity)
  └── Metadata filtering (genre, language, audience, exclusions)
  └── Ranking + reranking (diversity, novelty, rating boost)

LLM Layer
  └── Generate natural language explanations
  └── Ask follow-up clarification questions
  └── Refine recommendations conversationally

Output Layer
  └── Recommended books with match score
  └── Explanation per recommendation
  └── Feedback buttons
```

---

## Recommendation Approach

**Phase 1 (MVP):** Content-based filtering using embeddings + vector search.

**What to embed per book:**
- Summary / description
- Genre labels
- Themes and tone descriptors

**User taste vector:** Average the embeddings of the user's 3–5 favorite books. This becomes the "taste center" used for similarity search.

**Ranking formula:**
1. Retrieve top 50 semantically similar books
2. Filter out already-read books
3. Filter by language, audience level, disliked genres
4. Re-rank by: rating boost, author diversity, novelty score
5. Return top 10

**Phase 2+:** Add collaborative filtering ("people like you also enjoyed…") once sufficient user-rating history exists.

---

## Data

### Recommended Sources
- Kaggle book datasets (good for offline prototyping)
- Open Library API
- Google Books API
- ISBNdb API
- Manually curated CSV for early MVP

### Required Fields Per Book
```
title, author, ISBN, genre(s), description/summary,
tags/themes, publication_year, average_rating,
page_count, language, cover_image_url, audience_level
```

### Combined Text Field (for embedding)
Concatenate the following into a single string per book:
```
"{title} by {author}. {genres}. {themes}. {summary}"
```
Example: `"The Night Circus by Erin Morgenstern. Fantasy, magical realism, romance. A dreamy competition between illusionists inside a mysterious circus..."`

### Data Cleaning Checklist
- [ ] Remove duplicates
- [ ] Standardize author names
- [ ] Normalize genre labels
- [ ] Fill or remove missing descriptions
- [ ] Remove books with insufficient metadata

---

## User Onboarding Flow

**First-time user:**
1. Enter 3 favorite books
2. Select preferred genres and moods
3. Agent asks 2–3 follow-up questions
4. System returns recommendations with explanations

**Returning user:**
1. Sees updated recommendations
2. Rates previous suggestions
3. Asks for a specific mood or topic
4. Gets refined results

**MVP onboarding questions:**
1. What are 3 books you loved?
2. What genres do you enjoy?
3. What kind of vibe do you want right now?
4. Any books or topics you want to avoid?

---

## Taste Profile

The user profile should track multiple signals:

| Signal | Description |
|---|---|
| `liked_vector` | Average embedding of liked books |
| `disliked_vector` | Average embedding of disliked/DNF books |
| `genre_preferences` | Explicit genre likes/dislikes |
| `mood_keywords` | Free-text mood descriptors |
| `exclusions` | Themes, topics, or content to avoid |
| `pace_preference` | Fast-paced / slow literary |
| `length_preference` | Short / medium / long |

Rank candidates by: closeness to `liked_vector` + distance from `disliked_vector` + genre/mood match + penalties for exclusions.

---

## Explanation Generation

Every recommendation must include a natural language explanation. Prompt the LLM with the user profile and the candidate book metadata, and ask it to explain the match. Examples:

- "Recommended because you loved *The Night Circus* — similarly lyrical prose with a magical atmosphere."
- "Matches your preference for fast-paced plot over literary description."
- "Less romance than your usual reads, but shares the dark academia vibe you enjoy."

---

## Feedback Loop

Collect feedback signals:
- Thumbs up / down
- Star rating (1–5)
- "More like this"
- "Less romance / more fast-paced / not interested"

Use feedback to:
- Strengthen vectors from liked recommendations
- Weaken disliked themes in the taste profile
- Track preference drift over time

---

## Conversational Intelligence

The agent should handle natural language refinement, not just static queries:

- "Do you want something darker or lighter than your usual reads?"
- "Are you okay with long fantasy series?"
- "Would you prefer literary prose or fast-paced plot?"
- "Find me something like *Project Hail Mary* but less science-heavy."

Keep agent logic simple for MVP — a clean Python backend with LLM prompt logic is sufficient. Avoid heavy frameworks (LangChain, CrewAI) until complexity justifies them.

---

## Build Phases

### Phase 1 — Prototype
- Small dataset (1,000–10,000 books)
- Embeddings + ChromaDB or FAISS
- Top 5 recommendations from 3 favorite books

### Phase 2 — Personalization
- Onboarding quiz
- Full taste profile (liked/disliked vectors, filters)
- Explanation generation per recommendation

### Phase 3 — Conversation
- Chatbot interface
- Follow-up questions
- Prompt-based refinement

### Phase 4 — Learning System
- Rating collection
- Feedback memory
- Recommendation tuning over time

### Phase 5 — Production
- User accounts and dashboards
- Scalable database
- Analytics and monitoring

---

## Common Problems & Solutions

| Problem | Solution |
|---|---|
| **Cold start** (new user, no history) | Ask for 3 favorite books + genre/mood quiz |
| **Weak metadata** (bad summaries = bad recs) | Enrich metadata; combine title + author + summary + genre + tags |
| **Over-recommending popular books** | Add novelty score; include hidden gems |
| **Too much similarity** (repetitive results) | Diversity re-ranking; limit same-author results; mix "safe" and "explore" |
| **Explainability** (black-box distrust) | Always generate a natural language reason per recommendation |

---

## Success Metrics

- Click-through rate on recommendations
- Wishlist / save rate
- User star ratings on recommendations
- Repeat usage rate
- Recommendation acceptance rate

---

## First 7 Steps to Start Now

1. **Define MVP in one sentence** — write it at the top of your project README.
2. **Choose one dataset** — start with a clean CSV of 1,000–10,000 books.
3. **Clean the data** — keep `title`, `author`, `genre`, `summary` at minimum.
4. **Generate embeddings** for each book's combined text field.
5. **Store embeddings** in ChromaDB or FAISS.
6. **Build a taste vector function** — accepts 3 favorite book titles, returns averaged embedding.
7. **Retrieve top similar books** and pass them to an LLM to generate explanations in natural language.

That alone is a working, demonstrable prototype.
