from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(req, **kwargs):

        if req.user:
            return func(req, **kwargs)
        else:
            return {'status':False, 'msg':'Login Required'}
    
    return wrapper


def user_required(levels):

    def inner(func):

        @wraps(func)
        def wrapper(req, **kwargs):

            if req.user.level in levels:
                return func(req, **kwargs)
            else:
                return {'status':False, 'msg':'Permission Required'}
        return wrapper
    return inner