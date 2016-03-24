"""Spawner for Nike

User work directories are mounted in /srv/jupyterhub/work/{name},
so that work is not lost when containers are rebuilt.

This makes /srv/jupyterhub/work/{name} directory prior to spawn,
because if a volume that doesn't exist is mounted, it is owned by root and not writable by users.
"""

import os

from dockerspawner import DockerSpawner

work = '/srv/jupyterhub/work'

class NikeSpawner(DockerSpawner):
    def start(self):
        user_dir = os.path.join(work, self.user.name)
        os.makedirs(user_dir, exist_ok=True)
        return super().start()
