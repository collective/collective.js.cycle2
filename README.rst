********************
collective.js.cycle2
********************

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

`Cycle2 <http://jquery.malsup.com/cycle2/>`_ is a versatile slideshow plugin for jQuery built around ease-of-use.
It supports a declarative initialization style that allows full customization without any scripting.
Simply include the plugin, declare your markup, and Cycle2 does the rest.

This package adds a browser resource to use Cycle2 and its plugins on a Plone site.

Mostly Harmless
===============

.. image:: http://img.shields.io/pypi/v/collective.js.cycle2.svg
    :target: https://pypi.python.org/pypi/collective.js.cycle2

.. image:: https://img.shields.io/travis/collective/collective.js.cycle2/master.svg
    :target: http://travis-ci.org/collective/collective.js.cycle2

.. image:: https://img.shields.io/coveralls/collective/collective.js.cycle2/master.svg
    :target: https://coveralls.io/r/collective/collective.js.cycle2

Got an idea? Found a bug? Let us know by `opening a support ticket <https://github.com/collective/collective.js.cycle2/issues>`_.

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add add the following to it:

.. code-block:: ini

    [buildout]
    ...
    eggs =
        collective.js.cycle2

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.js.cycle2`` and click the 'Activate' button.

Usage
-----

If your page template inherits from ``main_template``,
just include the resources on it by usign the following syntax:

.. code-block:: xml

    <metal:block fill-slot="javascript_head_slot">
      <script tal:attributes="src string:$portal_url/++resource++collective.js.cycle2/jquery.cycle2.min.js"></script>
    </metal:block>

Alternatively you can add them into your site's JavaScript Registry directly or by using GenericSetup:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_javascripts">
      <javascript
          cacheable="True" compression="none" cookable="True" enabled="True"
          id="++resource++collective.js.cycle2/jquery.cycle2.min.js" />
    </object>

Plugins
-------

The package also includes the code for the following plugins:

* Transition
    * Carousel
    * Flip
    * IE-Fade
    * ScrollVert
    * Shuffle
    * Tile
* Functional
    * Caption2
    * Center
    * Swipe
    * YouTube

Check Cycle2 `download page <http://jquery.malsup.com/cycle2/download/>`_ for more information.

Utility
=======

The ``utils.js`` script has an utility that:

* fix the player size according with the width of the container and the aspect ratio
* vertically center images
* sync the player, description and thumbnails when click in other picture or next/prev buttons

Usage
-----

To use the utility, you need to add the script in the same way you add Cycle2 resources:

If your page template inherits from ``main_template``,
just include the script on it by usign the following syntax:

.. code-block:: xml

    <metal:block fill-slot="javascript_head_slot">
      <script tal:attributes="src string:$portal_url/++resource++collective.js.cycle2/utils.min.js"></script>
    </metal:block>

Alternatively you can add it directly into your site's JavaScript Registry or by using GenericSetup:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_javascripts">
      <javascript
          cacheable="True" compression="none" cookable="True" enabled="True"
          id="++resource++collective.js.cycle2/utils.min.js" />
    </object>

And in your script you should call the utility object passing the gallery element:

.. code-block:: javascript

    $(window).load(function() {
      var i, len, ref, slideshow;
      ref = $('.slideshow-container');
      for (i = 0, len = ref.length; i < len; i++) {
        slideshow = ref[i];
        new cycle2SlideShow(slideshow);
      }
    });

The script is currently used in `sc.photogallery <https://github.com/simplesconsultoria/sc.photogallery>`_ and  `collective.nitf <https://github.com/collective/collective.nitf>`_.

Not entirely unlike
===================

`collective.js.galleria <https://pypi.python.org/pypi/collective.js.galleria>`_
    Galleria is a JavaScript image gallery framework built on top of the jQuery library.
    The aim is to simplify the process of creating professional image galleries for the web and mobile devices.
