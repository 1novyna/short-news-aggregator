import openai


def add_titles(df, max_per_cluster=5, n_clusters=4):
    result = {}
    per_cluster = min(max_per_cluster, len(df.size) // n_clusters)
    sample_params = {
        "n": per_cluster,
        "random_state": 42,
        "replace": True,
    }
    for i in range(n_clusters):
        texts = df[df.Cluster == i].Text.sample(**sample_params).values
        content = "\n".join(texts)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f'What do the following texts have in common?\n\Texts:\n"""\n{content}\n"""\n\nTheme:',
            temperature=0,
            max_tokens=64,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        title = response["choices"][0]["text"]
        result[title.replace("\n", "")] = texts
    return result
