# Copyright from 2024: Alwinen GmbH (https://www.alwinen.de)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from email.message import EmailMessage
from unittest.mock import patch

from odoo import Command

from odoo.addons.mail.tests.test_mail_composer import TestMailComposer


class TestMailSendCopyCommon(TestMailComposer):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context={"testing": True})
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "email": "test@example.com",
            }
        )

    def _create_composer(self, **context):
        return (
            self.env["mail.compose.message"]
            .with_context(**context)
            .create(
                {
                    "model": "res.partner",
                    "res_ids": [self.partner.id],
                    "partner_ids": [Command.set(self.partner.ids)],
                    "subject": "Test Subject",
                    "body": "<p>Test Body</p>",
                    "email_from": "sender@example.com",
                    "composition_mode": "comment",
                }
            )
        )


class TestMailSendCopy(TestMailSendCopyCommon):
    def test_send_email_with_copy(self):
        """The sender is added to Bcc when sending an email."""
        composer = self._create_composer()
        with patch(
            "odoo.addons.base.models.ir_mail_server.IrMailServer.send_email"
        ) as mock_send_email:
            composer._action_send_mail()
        self.assertTrue(mock_send_email.called)
        message = mock_send_email.call_args[0][0]
        self.assertIn("sender@example.com", message["Bcc"])

    def test_send_email_without_copy(self):
        """The sender is not added to Bcc when ``do_not_send_copy`` is set."""
        composer = self._create_composer(do_not_send_copy=True)
        with patch(
            "odoo.addons.base.models.ir_mail_server.IrMailServer.send_email"
        ) as mock_send_email:
            composer._action_send_mail()
        self.assertTrue(mock_send_email.called)
        message = mock_send_email.call_args[0][0]
        self.assertNotIn("Bcc", message)

    def test_send_email_with_existing_bcc(self):
        """The sender is appended to an existing Bcc header."""
        message = EmailMessage()
        message["From"] = "sender@example.com"
        message["Bcc"] = "existing@example.com"
        with patch(
            "odoo.addons.base.models.ir_mail_server.IrMailServer.send_email"
        ) as mock_send_email:
            self.env["ir.mail_server"].send_email(message)
        self.assertTrue(mock_send_email.called)
        sent = mock_send_email.call_args[0][0]
        self.assertEqual(sent["Bcc"], "existing@example.com, sender@example.com")
