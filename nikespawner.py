import os

from dockerspawner import DockerSpawner

root='/srv/jupyterhub'

class NikeSpawner(DockerSpawner):
    def start(self):
        self.log.warn("Starting %s" % self.user)
        home_dir = os.path.join('/srv/jupyterhub/home/%s' % self.user.name)
        self.log.warn("Making %r" % home_dir)
        os.makedirs(home_dir, exist_ok=True)
        os.chmod(home_dir, 0o777)
        self.log.warn("Made %s" % home_dir)
        self.log.warn("stat: %s" % (os.stat(home_dir), ))
        return super().start()
