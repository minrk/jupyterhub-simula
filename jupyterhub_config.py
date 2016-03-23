# Configuration file for Jupyter Hub

c = get_config()

c.JupyterHub.proxy_cmd = ['configurable-http-proxy', '--redirect-port', '80']


from oauthenticator.github import GitHubOAuthenticator

# OAuth with GitHub
c.JupyterHub.authenticator_class = GitHubOAuthenticator

c.Authenticator.admin_users = admin = set()
c.JupyterHub.admin_access = True

import os, sys

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

# spawn with Docker:

import netifaces
docker_ip = netifaces.ifaddresses('docker0')[netifaces.AF_INET][0]['addr']
c.JupyterHub.hub_ip = docker_ip

sys.path.insert(0, os.path.dirname(__file__))
from nikespawner import NikeSpawner
c.JupyterHub.spawner_class = NikeSpawner
c.DockerSpawner.container_image = 'singleuser'
c.DockerSpawner.volumes = {
    '/srv/jupyterhub/home/{username}': '/home/fenics/work',
}

# ssl config
ssl = join(here, 'ssl')
keyfile = join(ssl, 'ssl.key')
certfile = join(ssl, 'ssl.cert')
if os.path.exists(keyfile):
    c.JupyterHub.ssl_key = keyfile
if os.path.exists(certfile):
    c.JupyterHub.ssl_cert = certfile
    c.JupyterHub.port = 443
