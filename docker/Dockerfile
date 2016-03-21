FROM jupyter/singleuser
ENV CHANNEL minrk
USER root
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install build-essential gfortran libglu-dev wget bzip2 gcc git pkg-config ruby less
RUN jupyter kernelspec remove python2 || echo 'already gone'
RUN gem install a2km commander
RUN a2km env-kernel python2
RUN a2km set python2 display_name "Python 2 (fenics)"
USER jovyan
RUN conda install -y -n python2 -c $CHANNEL fenics==1.7.0dev ipykernel matplotlib scipy pandas cmake seaborn pytest nose
WORKDIR /home/jovyan
