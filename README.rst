=========
Trame App
=========

An example Trame application


* Free software: BSD License


Getting data
----------

.. code-block:: console
    wget -O trame_app/data/skull.vti https://github.com/Kitware/vtk-js-datasets/blob/master/data/vti/skull.vti?raw=true


Installing
----------
Build and install the Vue components

.. code-block:: console

    cd vue-components
    npm i
    npm run build
    cd -

Install the application

.. code-block:: console

    pip install -e .


Run the application

.. code-block:: console

    trame-app
