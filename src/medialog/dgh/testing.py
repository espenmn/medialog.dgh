# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import medialog.dgh


class MedialogDghLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=medialog.dgh)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'medialog.dgh:default')


MEDIALOG_DGH_FIXTURE = MedialogDghLayer()


MEDIALOG_DGH_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEDIALOG_DGH_FIXTURE,),
    name='MedialogDghLayer:IntegrationTesting'
)


MEDIALOG_DGH_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MEDIALOG_DGH_FIXTURE,),
    name='MedialogDghLayer:FunctionalTesting'
)


MEDIALOG_DGH_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        MEDIALOG_DGH_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='MedialogDghLayer:AcceptanceTesting'
)
