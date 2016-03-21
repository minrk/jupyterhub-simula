# JupyterHub setup for Nike (Simula)

These are the setup scripts for a  deployment of JupyterHub at Simula,
using GitHub OAuth and Docker spawning.
It is currently running internally at Simula on the Nike machine.

The images are currently installing fenics 1.7.0dev from [these conda recipes](https://github.com/minrk/fenics-recipes/tree/dev).


## Clone and install JupyterHub and dependencies

    git clone https://github.com/minrk/jupyterhub-simula /srv/jupyterhub
    cd /srv/jupyterhub
    sudo bash install.sh

## Configure your deployment

1. write admins to `userlist`, in the form:

        mal admin
        zoe admin
        inara admin

   Admin users will have admin access to the JupyterHub instance. 
   See `userlist.example` for an example.
   Since Nike is only accessible on the private Simula network,
   any GitHub account will be able to login as a user.

2. set up [GitHub OAuth][] and put the variables in `env`. See `env.example` for an example.
   The `OAUTH_CALLBACK_URL` will want to be of the form `https://nike.simula.no/hub/oauth_callback`

3. add your ssl cert and key in `ssl/ssl.crt` and `ssl/ssl.key`, respectively.

4. edit `jupyterhub_config.py` as appropriate


## Start and stop JupyterHub

This sets up JupyterHub with supervisor, so you use `supervisorctl` to stop and start the service:

    supervisorctl start jupyterhub

See supervisor docs for details on managing services.

[GitHub OAuth]: https://github.com/settings/applications/new