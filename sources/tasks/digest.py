from openai import Completion
from openai.error import RateLimitError
from tenacity import RetryError

from sources.models import Cluster


def populate_digests():
    left_clusters = Cluster.objects.exclude(digest__gt=0).all()
    for cluster in left_clusters:
        try:
            messages = cluster.messages.all()[:3]
            texts = [message.text for message in messages]
            content = "\n".join(texts)
            response = Completion.create(
                engine="text-davinci-003",
                prompt=f'Напиши короткий зміст наступних повідомлень.\n\Повідомлення:\n"""\n{content}\n"""\n\nЗміст:',
                temperature=0,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            digest = response["choices"][0]["text"]
            cluster.digest = digest.replace("\n", "")
            cluster.save()
        except (RateLimitError, RetryError) as error:
            print("Completion's rate limit is exceeded.", error)
            break
