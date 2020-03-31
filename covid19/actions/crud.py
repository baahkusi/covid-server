import covid19.db as db


def read(resource, id):
    """
    :kwargs: resource, id
    """
    try:

        resource = getattr(db, resource)
        data = resource.get_by_id(id)

    except Exception as e:
        return {'status': False, 'data': repr(e)}

    return {'status': True, 'data': data}


def read_many(resource, filters):
    """
    :params: resource, filters
    """
    try:

        resource = getattr(db, resource)
        filters = filters  # query filters
        data = resource.get(**filters)

    except Exception as e:
        return {'status': False, 'data': repr(e)}

    return {'status': True, 'data': data}


def create(resource, data):
    """
    :params: resource, data
    """
    try:

        resource = getattr(db, resource)
        resource.create(**data)

    except Exception as e:
        return {'status': False, 'data': repr(e)}

    return {'status': True, 'data': ''}


def update(resource, id, data):
    """
    :params: resource, id, data
    """
    try:

        resource = getattr(db, resource)
        data = resource.update(data).execute()

    except Exception as e:
        return {'status': False, 'data': repr(e)}

    return {'status': True, 'data': data}


def delete(resource, id):
    """
    :params: resource, id
    """
    try:

        resource = getattr(db, resource)
        data = resource.delete().where(id=id).execute()

    except Exception as e:
        return {'status': False, 'data': repr(e)}

    return {'status': True, 'data': data}
