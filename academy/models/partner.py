# -*- coding: utf-8 -*-

from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    instructor = fields.Boolean("Instructor", default=False)
    session_ids = fields.Many2many('academy.session', string="Attended Sessions", readonly=True)
    biography = fields.Html()
    session_ins = fields.One2many('academy.session', 'instructor_id', string="Sessions")
    num_ses = fields.Integer(string="Number of sessions", compute='sessions')

    def sessions(self):
        self.num_ses = len(self.session_ins)
