# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from email.utils import COMMASPACE

from odoo import api, models

from odoo.addons.base.models.ir_mail_server import extract_rfc2822_addresses


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    @api.model
    def send_email(self, message, *args, **kwargs):
        do_not_send_copy = self.env.context.get("do_not_send_copy", False)
        sender = message["From"]
        if do_not_send_copy or not sender:
            return super().send_email(message, *args, **kwargs)
        # Get existing Bcc recipients (if any)
        bcc = message["Bcc"]
        # Combine existing Bcc with From address
        all_bcc = COMMASPACE.join(filter(None, [bcc, sender]))
        # Set the combined Bcc
        del message["Bcc"]
        message["Bcc"] = all_bcc
        mail_server = self
        validated_to = self.env.context.get("send_validated_to")
        if validated_to:
            mail_server = self.with_context(
                send_validated_to=validated_to + extract_rfc2822_addresses(sender)
            )
        return super(IrMailServer, mail_server).send_email(message, *args, **kwargs)
