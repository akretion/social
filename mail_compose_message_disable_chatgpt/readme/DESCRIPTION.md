This module removes the "AI" button of the mail composer dialog and of the
scheduled message form. That button, provided by `mail`, opens a discussion
with Odoo's ChatGPT service even when the AI features of the HTML editor are
already disabled.

It only covers those two forms. To remove the editor AI features as well, use
it together with `web_editor_disable_chatgpt`.
