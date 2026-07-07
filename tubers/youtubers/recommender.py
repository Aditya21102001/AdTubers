"""Lightweight, dependency-free creator recommender.

Ranks YouTubers against a free-text event brief using TF-IDF cosine similarity,
implemented in pure Python (stdlib only). This keeps the feature fully
open-source and safe within Render's 512 MB free tier — no numpy/scikit-learn.

To upgrade on a larger instance, swap `rank_youtubers` for scikit-learn's
TfidfVectorizer or sentence-transformer embeddings; the interface can stay the
same.
"""

import math
import re
from collections import Counter

_TOKEN_RE = re.compile(r"[a-z0-9]+")
_TAG_RE = re.compile(r"<[^>]+>")

# Small stopword list so common filler words in an event brief don't skew ranking.
_STOPWORDS = {
    "the", "a", "an", "and", "or", "for", "to", "of", "in", "on", "with", "is",
    "are", "i", "need", "want", "looking", "my", "our", "event", "who", "that",
    "this", "at", "be", "by", "it", "as", "from", "can", "you", "your", "me",
    "we", "some", "someone", "creator", "creators", "youtuber", "youtubers",
}


def _tokenize(text):
    text = _TAG_RE.sub(" ", text or "")  # strip HTML from RichText descriptions
    return [
        tok for tok in _TOKEN_RE.findall(text.lower())
        if len(tok) > 1 and tok not in _STOPWORDS
    ]


def _profile_text(youtuber):
    """The searchable text profile for one creator."""
    category = youtuber.category or ""
    return " ".join(str(part) for part in (
        youtuber.name,
        category,
        category.replace("_", " "),
        youtuber.city,
        youtuber.camera_type,
        youtuber.crew,
        youtuber.description,
    ))


def rank_youtubers(query, youtubers, top_n=6):
    """Return [{'tuber': Youtuber, 'score': 0-100}, ...] ranked by relevance."""
    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    docs = [(y, _tokenize(_profile_text(y))) for y in youtubers]
    docs = [(y, toks) for y, toks in docs if toks]
    if not docs:
        return []

    # Inverse document frequency across the creator corpus.
    doc_freq = Counter()
    for _, toks in docs:
        doc_freq.update(set(toks))
    n_docs = len(docs)
    idf = {t: math.log((1 + n_docs) / (1 + f)) + 1 for t, f in doc_freq.items()}

    def tfidf(tokens):
        n = len(tokens)
        return {t: (c / n) * idf.get(t, 0.0) for t, c in Counter(tokens).items()}

    q_vec = {t: (c / len(query_tokens)) * idf.get(t, 0.0)
             for t, c in Counter(query_tokens).items()}
    q_norm = math.sqrt(sum(w * w for w in q_vec.values()))
    if q_norm == 0:  # none of the query terms appear in any creator profile
        return []

    ranked = []
    for youtuber, tokens in docs:
        d_vec = tfidf(tokens)
        d_norm = math.sqrt(sum(w * w for w in d_vec.values()))
        if not d_norm:
            continue
        dot = sum(w * d_vec.get(t, 0.0) for t, w in q_vec.items())
        score = dot / (q_norm * d_norm)
        if score > 0:
            # The query terms that contributed most to this match, for display.
            contrib = {t: w * d_vec.get(t, 0.0) for t, w in q_vec.items() if d_vec.get(t, 0.0) > 0}
            matched = sorted(contrib, key=contrib.get, reverse=True)[:3]
            ranked.append({
                "tuber": youtuber,
                "score": round(score * 100),
                "matched": matched,
            })

    ranked.sort(key=lambda r: r["score"], reverse=True)
    return ranked[:top_n]
