#Mimeograph

This is the readme for Mimeograph, a Twitter clone that fulfills the
underserved market of people that want to share ASCII images with each
other.

##Installation

Mimeograph was developed with Django 1.3, PIL 1.1.7 and Python 2.7. It
was not tested on any other configurations, but it would probably work
fine with other versions of Python.


1. Get Django 1.3. See https://docs.djangoproject.com/en/1.3/intro/install/ 
   for instructions on how to install.
2. Get and install the Python Image Library 1.1.7 from
   http://www.pythonware.com/products/pil/index.htm.
3. `git clone git://github.com/jergason/mimeograph.git; cd mimeograph`
4. Run `python manage.py syncdb`. This should automatically load the
   fixtures with some seed data.
5. Run it with `python manage.py runserver` and go to
   `http://localhost:8000` to check it out!
