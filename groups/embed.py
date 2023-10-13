from openai.embeddings_utils import get_embedding
from tiktoken import get_encoding


def add_embedding(
    df,
    column_name="Text",
    model="text-embedding-ada-002",
    encoding="cl100k_base",
    max_tokens=8000,
):
    column = getattr(df, column_name)

    encoding = get_encoding(encoding)
    df["TokensNumber"] = column.apply(lambda x: len(encoding.encode(x)))

    limit = 1000
    df = df[df.TokensNumber <= max_tokens].tail(limit)

    df["Embedding"] = column.apply(lambda x: get_embedding(x, engine=model))
    return df
