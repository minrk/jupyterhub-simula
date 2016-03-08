# Configuration file for Jupyter Hub

c = get_config()

c.JupyterHub.proxy_cmd = ['configurable-http-proxy', '--redirect-port', '80']


# OAuth with GitHub
c.JupyterHub.authenticator_class = 'oauthenticator.LocalGitHubOAuthenticator'
c.LocalGitHubOAuthenticator.create_system_users = True

c.Authenticator.admin_users = admin = set()
c.JupyterHub.admin_access = True

import os

join = os.path.join
here = os.path.dirname(__file__)
with open(join(here, 'userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)

c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

# ssl config
ssl = join(here, 'ssl')
keyfile = join(ssl, 'ssl.key')
certfile = join(ssl, 'ssl.crt')
if os.path.exists(keyfile):
    c.JupyterHub.ssl_key = keyfile
if os.path.exists(certfile):
    c.JupyterHub.ssl_cert = certfile
    c.JupyterHub.port = 443
