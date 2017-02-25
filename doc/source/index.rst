.. Supreme Rotary Phone documentation master file, created by
   sphinx-quickstart on Thu Jan 12 17:08:16 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Supreme Rotary Phone
====================

Overview of the file structure:

 * :doc:`files/cgi`

    * Contains cgi scripts for displaying a rudimentary web interface
    * supposed to be set as the webroot of a cgi-webserver such as apache
 
 * :doc:`files/check_access`

    * Contains scripts that get called to check if a device/user is authorized to access the network
 
 * :doc:`files/dynamic`
    
    * Contains the script that write the config files on update
    * scripts that should get called on update are to be symlinked in dynamic/enabled

 * :doc:`files/generateconfig`

    * Contains scripts that generate various config files
    * not to be called manually, used by the scripts in dynamic

 * :doc:`files/helpers`
    
    * various helper scripts to make the admins life easier
 
 * :doc:`files/helpers.py`
    
    * main "library" of this project
    * contains all functions used for DB calls

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :glob:

   database
   files/*


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
