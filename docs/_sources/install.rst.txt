Install Guide
=============

This guide is a resource for using the AT EM Imaging Workflow package.
It is maintained by the `Allen Institute for Brain Science <http://www.alleninstitute.org/>`_.

The AT EM Imaging Workflow was developed and tested with Python 3.6, installed.
We do not guarantee consistent behavior with other Python versions.

Quick Start Using Pip
---------------------

First ensure you have `pip <http://pypi.python.org/pypi/pip>`_ installed.
It is included with the Anaconda distribution.

::

    pip install at_em_imaging_workflow


To uninstall::

    pip uninstall at_em_imaging_workflow

Other Distribution Formats
--------------------------

The AT EM Imaging Workflow is also available from the Stash source repository.

Required Dependencies
---------------------

 * Django
 * Celery
 * Pika

Optional Dependencies
---------------------

 * `pytest <http://pytest.org/latest>`_
 * `coverage <http://nedbatchelder.com/code/coverage>`_

Installation with Docker (Optional)
-----------------------------------

`Docker <http://www.docker.com/>`_ is an open-source technology
for building and deploying applications with a consistent environment
including required dependencies.

 #. Use Docker to build one of the images.
 
     Anaconda::

         docker pull docker.aibs-artifactory.corp.alleninstitute.org/at_em_image_processing
 
     Other docker configurations are also available.
 
 #. Run the docker image::
 
     docker tag docker.aibs-artifactory.corp.alleninstitute.org/at_em_image_processing alleninstitute/at_em_image_processing
     docker run -i -t alleninstitute/at_em_image_processing /bin/bash
