# -*- coding: utf-8 -*-
from collective.js.cycle2 import _
from plone.app.registry.browser import controlpanel
from plone.directives import form
from zope import schema
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

fx = ['fade', 'fadeout', 'none', 'scrollHorz']
fx = SimpleVocabulary([SimpleTerm(f) for f in fx])

# TODO: get this from portal_properties/imaging_properties
scales = ['large', 'preview', 'mini', 'thumb', 'tile', 'icon', 'listing']
scales = SimpleVocabulary([SimpleTerm(s) for s in scales])


class ICycle2Settings(form.Schema):

    """Interface for the control panel form."""

    paused = schema.Bool(
        title=_(u'Paused'),
        description=_(u'If selected the slideshow will begin in a paused state.'),
        default=True,
    )

    allow_wrap = schema.Bool(
        title=_(u'Allow wrap'),
        description=_(u'Determines whether or not a slideshow can advance from the last slide to the first (or vice versa).'),
        default=True,
    )

    caption_template = schema.TextLine(
        title=_(u'Caption Template'),
        description=_(
            u'A template string which defines how the slideshow caption should be formatted. '
            u'',
        ),
        default=u'{{slideNum}} / {{slideCount}}',
    )

    pager_template = schema.TextLine(
        title=_(u'Pager Template'),
        description=_(
            u'A template string which defines how the pager links should be formatted. '
            u'',
        ),
        default=u'<span>&bull;</span>',
    )

    speed = schema.Int(
        title=_(u'Speed'),
        description=_(u'The speed of the transition effect in milliseconds.'),
        default=500,
    )

    timeout = schema.Int(
        title=_(u'Timeout'),
        description=_(u'The time between slide transitions in milliseconds.'),
        default=4000,
    )

    transition_effect = schema.Choice(
        title=_(u'Transition effect'),
        description=_(u'The name of the slideshow transition to use.'),
        required=True,
        vocabulary=fx,
        default='fade',
    )

    default_image_size = schema.Choice(
        title=_(u'Default Image Size'),
        description=_(u''),
        required=True,
        vocabulary=scales,
        default='preview',
    )


class Cycle2SettingsEditForm(controlpanel.RegistryEditForm):
    schema = ICycle2Settings
    label = _(u'Cycle2')
    description = _(
        u'Here you can define global configuration options for the Cycle2 slideshow plugin.')


class Cycle2SettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = Cycle2SettingsEditForm
