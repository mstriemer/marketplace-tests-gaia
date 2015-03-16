# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from marionette.by import By

from marketplacetests.marketplace.app import Marketplace


class Debug(Marketplace):

    _back_button_locator = (By.ID, 'nav-back')
    _region_select_locator = (By.NAME, 'region')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_element_displayed(*self._region_select_locator)

    def tap_back(self):
        self.marionette.find_element(*self._back_button_locator).tap()

    def select_region(self, region):
        self.marionette.find_element(*self._region_select_locator).tap()
        self.select(region)
        self.switch_to_marketplace_frame()
