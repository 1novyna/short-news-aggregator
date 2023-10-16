from openai.embeddings_utils import get_embedding
from openai.error import RateLimitError
from tenacity import RetryError

from sources.models import Message


def populate_embedding():
    left_messages = Message.objects.filter(embedding__isnull=True).all()
    for message in left_messages:
        try:
            message.embedding = get_embedding(message.text, "text-embedding-ada-002")
            message.save()
        except (RateLimitError, RetryError) as error:
            print("Embedding's rate limit is exceeded.", error)
            break
