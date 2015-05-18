from plone import api
from plone.browserlayer import utils
from zope.component.hooks import getSite

import logging


logger = logging.getLogger('collective.js.cycle2')


def remove_profile(context):
    """Profiles should not be mantained into JS packages"""

    utils.unregister_layer('collective.js.cycle2')
    logger.info('Remove browser layer')

    js_tool = api.portal.get_tool('portal_javascripts')
    ids_to_remove = [
        "++resource++collective.js.cycle2/jquery.cycle2.min.js",
        "++resource++collective.js.cycle2/jquery.cycle2.center.min.js",
        "++resource++collective.js.cycle2/jquery.cycle2.swipe.min.js"
    ]
    for js_id in ids_to_remove:
        js_tool.unregisterResource(js_id)
        logger.info('"{0}" resource was removed"'.format(js_id))
    js_tool.cookResources()
    logger.info('JS resources were cooked')
