# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class Invoice(models.Model):
    _inherit = 'account.move'

    session_id = fields.Many2one("academy.session", string="session")
