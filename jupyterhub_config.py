# Configuration file for Jupyter Hub

c = get_config()

c.JupyterHub.proxy_cmd = ['configurable-http-proxy', '--redirect-port', '80']


from oauthenticator.github import GitHubOAuthenticator

# OAuth with GitHub
c.JupyterHub.authenticator_class = GitHubOAuthenticator

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

# spawn with Docker:

from tornado.gen import coroutine
from dockerspawner import DockerSpawner
import netifaces
docker_ip = netifaces.ifaddresses('docker0')[netifaces.AF_INET][0]['addr']
c.JupyterHub.hub_ip = docker_ip

class MySpawner(DockerSpawner):
    def start(self):
        self.log.warn("Starting %s" % self.user)
        home_dir = os.path.join('/srv/jupyterhub/home/%s' % self.user.name)
        self.log.warn("Making %r" % home_dir)
        os.makedirs(home_dir, exist_ok=True)
        os.chmod('/srv/jupyterhub', 0o777)
        os.chmod(home_dir, 0o777)
        self.log.warn("Made %s" % home_dir)
        self.log.warn("stat: %s" % (os.stat(home_dir), ))
        return super().start()

c.JupyterHub.spawner_class = MySpawner
c.DockerSpawner.container_image = 'singleuser'
c.DockerSpawner.volumes = {
    '/srv/jupyterhub/home/{username}': '/home/jovyan',
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
