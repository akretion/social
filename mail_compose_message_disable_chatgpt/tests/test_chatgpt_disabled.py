# Copyright 2026 Akretion
# @author Benoît Guillot <benoit.guillot@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestChatgptDisabled(TransactionCase):
    """The AI button of the mail composer must be removed."""

    def test_no_chatgpt_widget_in_views(self):
        for xmlid in (
            "mail.email_compose_message_wizard_form",
            "mail.mail_scheduled_message_view_form",
        ):
            view = self.env.ref(xmlid)
            self.assertNotIn(
                "mail_composer_chatgpt",
                view.get_combined_arch(),
                f"The AI button should be removed from {xmlid}",
            )
