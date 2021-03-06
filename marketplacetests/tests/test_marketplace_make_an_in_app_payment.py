# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import Wait

from marketplacetests.in_app_payments.in_app import InAppPayment
from marketplacetests.payment.app import Payment
from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase


class TestMakeInAppPayment(MarketplaceGaiaTestCase):

    APP_NAME = 'Testing In-App-Payments'
    APP_TITLE = 'In-App-Payments'
    PIN = '1234'

    def setUp(self):
        MarketplaceGaiaTestCase.setUp(self)

        self.create_account_and_change_its_region()
        self.install_in_app_payments_test_app()

    def test_make_an_in_app_payment(self):

        # Verify that the app icon is visible on one of the homescreen pages
        self.assertTrue(
            self.homescreen.is_app_installed(self.APP_NAME),
            'App %s not found on homescreen' % self.APP_NAME)

        # Click icon and wait for h1 element displayed
        self.homescreen.installed_app(self.APP_NAME).tap_icon()
        Wait(self.marionette).until(lambda m: m.title == self.APP_TITLE)

        tester_app = InAppPayment(self.marionette)
        fxa = tester_app.tap_buy_product()
        fxa.login(self.acct.email, self.acct.password)

        payment = Payment(self.marionette)
        payment.create_pin(self.PIN)

        self.assertEqual('Confirm Payment', payment.confirm_payment_header_text)
        self.assertEqual('test 0.10USD', payment.in_app_product_name)

        payment.tap_buy_button()
        tester_app.wait_for_bought_products_displayed()
        self.assertEqual('test 0.10USD', tester_app.bought_product_text)
