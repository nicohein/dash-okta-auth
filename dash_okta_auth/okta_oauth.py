from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError
from config import OKTA_BASE_URL, OKTA_CLIENT_ID, OKTA_CLIENT_SECRET

from flask import redirect, url_for, Response, session

from flask_dance.consumer import OAuth2ConsumerBlueprint

from .auth import Auth


class OktaOAuth(Auth):
    def __init__(self, app, additional_scopes=None):
        super(OktaOAuth, self).__init__(app)
        self.okta_blueprint = OAuth2ConsumerBlueprint(
            name='okta',
            import_name=__name__,
            client_id=OKTA_CLIENT_ID,
            client_secret=OKTA_CLIENT_SECRET,
            base_url=OKTA_BASE_URL,
            token_url=f'{OKTA_BASE_URL}/token',
            authorization_url=f'{OKTA_BASE_URL}/authorize',
            scope=['openid', 'email', 'profile'] + (additional_scopes if additional_scopes else []),
            # by default a login redirects to the root page
        )
        app.server.register_blueprint(self.okta_blueprint, url_prefix="/login")

    def is_authorized(self):
        if not self.okta_blueprint.session.token:
            # send to okta login
            return False
        try:
            resp = self.okta_blueprint.session.get(f'{OKTA_BASE_URL}/userinfo')
            assert resp.ok, resp.text

            session['email'] = resp.json().get('email')
            return True
        except (InvalidGrantError, TokenExpiredError):
            # no clue how to test this
            # self.okta_blueprint.session.token = None
            return self.login_request()

    def login_request(self):
        # send to okta auth page
        return redirect(url_for("okta.login"))

    def auth_wrapper(self, f):
        def wrap(*args, **kwargs):
            if not self.is_authorized():
                return Response(status=403)

            response = f(*args, **kwargs)
            return response
        return wrap

    def index_auth_wrapper(self, original_index):
        def wrap(*args, **kwargs):
            if self.is_authorized():
                return original_index(*args, **kwargs)
            else:
                return self.login_request()
        return wrap
