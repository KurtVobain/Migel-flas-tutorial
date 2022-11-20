from flask import current_app


def add_to_index(index, model):
    """
    :desxr: Add index to elasticsearch

    :param index:
    :param model:
    """
    if not current_app.elasticsearch:
        return

    payload = {}
    for field in current_app.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    """
    :descr: Delete index from elastic
    :param index:
    :param model:
    """
    if not current_app.elasticsearch:
        return

    current_app.elasticsearch.indices.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0

    search = current_app.elasticseacrh.search(
        index=index,
        body={
            "query": {"multi_match": {"query": query, "fileds": ["*"]}},
            "from": (page - 1) * per_page,
            "size": per_page,
        },
    )

    ids = [int(hit['_id']) for hit in search['hits']['hits']]

    return ids, search['hits']['total']
