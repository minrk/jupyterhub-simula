FROM quay.io/fenicsproject/dev-py3
ENV PYTHON=python3
ENV PREFIX=$HOME/build
ENV DEBIAN_FRONTEND=noninteractive

USER root
# base packages
RUN apt-get -y update && apt-get -y install libzmq3-dev libfreetype6-dev libpng-dev python3-scipy
# set UTF8 locale (see https://bitbucket.org/fenics-project/docker/pull-requests/3)
RUN echo "C.UTF-8 UTF-8" > /etc/locale.gen && locale-gen
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8

RUN $PYTHON -m pip install --upgrade setuptools pip

# Python dependencies for the notebook
ADD requirements.txt /tmp/requirements.txt
RUN $PYTHON -m pip install -r /tmp/requirements.txt

# update dolfin, checking that it works because the build commands don't check for success
# See https://bitbucket.org/fenics-project/docker/pull-requests/4
RUN rm -rf build/src/dolfin/build
USER fenics
RUN bash -l -c 'source ~/fenics.conf && build_dolfin && python -c "import dolfin"'
USER root

# setup singleuser (copied from dockerspawner/singleuser)
EXPOSE 8888
RUN wget -q https://raw.githubusercontent.com/jupyter/jupyterhub/master/scripts/jupyterhub-singleuser -O /usr/local/bin/jupyterhub-singleuser && \
    chmod 755 /usr/local/bin/jupyterhub-singleuser
RUN wget -q https://raw.githubusercontent.com/jupyter/dockerspawner/master/singleuser/singleuser.sh -O /srv/singleuser.sh

# tini entrypoint
RUN wget --quiet https://github.com/krallin/tini/releases/download/v0.9.0/tini && \
    echo "faafbfb5b079303691a939a747d7f60591f2143164093727e870b289a44d9872 *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

ENTRYPOINT ["tini", "--"]
CMD ["bash", "-l", "/srv/singleuser.sh", "--notebook-dir=work"]

ARG UID
ARG GID
RUN usermod -u $UID fenics \
 && groupmod -g $GID fenics \
 && chown -R fenics:fenics /home/fenics

# switch back to fenics user
USER fenics
ENV SHELL /bin/bash

# fix broken 'ipython' symlink in fenics.conf
RUN rm -f $PREFIX/bin/ipython && ln -s $(which ipython) $PREFIX/bin/ipython
