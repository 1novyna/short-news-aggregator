from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from transformers import AutoTokenizer
import torch


def group_by_keywords(articles):
    tokenizer = AutoTokenizer.from_pretrained(
        "MaxVortman/bert-base-ukr-eng-rus-uncased"
    )
    preprocessed_articles = [preprocess(article, tokenizer) for article in articles]
    tfidf_vectorizer = TfidfVectorizer(max_df=0.85, min_df=2, max_features=10)
    tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_articles)
    keywords = extract_keywords(articles, tfidf_vectorizer, tfidf_matrix)
    return group(articles, keywords)


def preprocess(text, tokenizer):
    from .stop_words import STOP_WORDS

    tokens = tokenizer.tokenize(text)
    tokens_without_stopwords = [
        token
        for token in tokens
        if token not in STOP_WORDS + tokenizer.all_special_tokens
    ]
    return " ".join(tokens_without_stopwords)


def extract_keywords(articles, tfidf_vectorizer, tfidf_matrix):
    keywords = []
    for i, article in enumerate(articles):
        tfidf_scores = [
            (word, score)
            for word, score in zip(
                tfidf_vectorizer.get_feature_names_out(), tfidf_matrix[i].toarray()[0]
            )
        ]
        sorted_keywords = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)[
            :3
        ]  # Get the top 3 keywords
        keywords.append([kw for kw, _ in sorted_keywords])
    return keywords


def group(articles, keywords):
    keyword_articles = defaultdict(list)
    for i, article in enumerate(articles):
        for keyword in keywords[i]:
            keyword_articles[keyword].append(article)
    return keyword_articles
