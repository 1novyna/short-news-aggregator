from sources.models import Message, Cluster


def create_clusters():
    left_messages = get_unclestered_messages()
    n_clusters = left_messages.get_approximate_clusters_number()
    df = left_messages.get_clusters()
    for i in range(n_clusters):
        cluster = Cluster.objects.create()
        messages_id = df[df.cluster == i]["id"].tolist()
        for id in messages_id:
            message = Message.objects.get(id=id)
            message.cluster = cluster
            message.save()


def get_unclestered_messages():
    return (
        Message.objects.filter(
            embedding__isnull=False,
            cluster__isnull=True,
        )
        .order_by("-datetime")
        .all()
    )
