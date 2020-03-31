import datetime
from .db import Logins
from .config import db


class SetUserMiddleware(object):
    def process_request(self, req, resp):
        """Process the request before routing it.

        Note:
            Because Falcon routes each request based on req.path, a
            request can be effectively re-routed by setting that
            attribute to a new value from within process_request().

        Args:
            req: Request object that will eventually be
                routed to an on_* responder method.
            resp: Response object that will be routed to
                the on_* responder.

        Adds: Sets req.user
        """

        token = req.get_header('Authorization')
        email = req.get_header('Account-ID')
        device = req.get_header('Device-ID')

        if token is None or email is None or device is None:
            req.user = None
        else:
            login = Logins.get_or_none(Logins.token == token)

            if login is not None:
                # check if token is still valid
                now = datetime.datetime.now()
                tdelta = now - login.ctime
                if tdelta.days >= 30:
                    req.user = None
                else:
                    if email == login.user.email and device == login.device_hash:
                        req.user = login.user
                    else:
                        req.user = None
            else:
                req.user = None


class CORSComponent(object):
    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin', '*')

        if (req_succeeded
            and req.method == 'OPTIONS'
            and req.get_header('Access-Control-Request-Method')
            ):
            # NOTE(kgriffs): This is a CORS preflight request. Patch the
            #   response accordingly.

            allow = resp.get_header('Allow')
            resp.delete_header('Allow')

            allow_headers = req.get_header(
                'Access-Control-Request-Headers',
                default='*'
            )

            resp.set_headers((
                ('Access-Control-Allow-Methods', allow),
                ('Access-Control-Allow-Headers', allow_headers),
                ('Access-Control-Max-Age', '86400'),  # 24 hours
            ))


class PeeweeConnectionMiddleware(object):
    def process_request(self, req, resp):
        try:
            db.connect()
        except Exception:
            pass

    def process_response(self, req, resp, resource, req_succeeded):
        if not db.is_closed():
            db.close()
