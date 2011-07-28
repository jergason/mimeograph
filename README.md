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
   You may need some additional libraries for PIL to work. See its
   readme for more information.
3. Run `git clone git://github.com/jergason/mimeograph.git; cd mimeograph`
   to get the code and go into the mimeograph directory.
4. Run `python manage.py syncdb`, and do not create a superuser or the
   fixtures will not load. This should automatically load the
   fixtures with some seed data. The superuser is `jergason` with a
   password of `password`
5. Run it with `python manage.py runserver` and go to
   `http://localhost:8000` to check it out!
