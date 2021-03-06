# -*- coding: utf-8 -*-
import base64
import csv

from odoo import fields, models, api, exceptions


class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    instructor = fields.Boolean("Instructor", default=False)
    session_ids = fields.Many2many('academy.session', string="Attended Sessions", readonly=True)
    biography = fields.Html()
    session_ins = fields.One2many('academy.session', 'instructor_id', string="Sessions")
    num_ses = fields.Integer(string="Number of sessions", compute='sessions')
    invoice_count = fields.Integer(string="count invoice", compute="_compute_invoice_count")
    input_file = fields.Binary('/ma_facture.xlsx')

    def sessions(self):
        self.num_ses = len(self.session_ins)

    def _compute_invoice_count(self):
        self.invoice_count = self.env['account.move'].search_count([('partner_id', '=', self.id)])

    def facturer(self):
        id_product_template = self.env['product.template'].search([('name', 'ilike', 'Session')]).id
        price_session = self.env['product.template'].search([('name', 'ilike', 'Session')]).list_price
        id_product_product = self.env['product.product'].search([('product_tmpl_id', '=', id_product_template)]).id
        # self.button_clicked = True
        # data= les donnes envoyes au facturaion
        data = {
            'partner_id': self.id,
            'type': 'out_invoice',
            # 'partner_shipping_id': self.instructor_id.address,
            # 'invoice_date': self.date,
            "invoice_line_ids": [],
        }
        list = []
        quantity = 0
        is_validated = 0
        is_invoiced = 0
        for line in self.session_ids:
            if line.state == "validate":
                is_validated = is_validated + 1
                quantity = quantity + line.duration
                line.state = 'fact'

        if len(self.session_ids) == 0:
            raise exceptions.ValidationError("This customer has no session to invoice")
        if is_validated == 0:
            raise exceptions.ValidationError("This customer has no validated session ")

        line1 = {
            "product_id": id_product_product,
            "quantity": quantity,
            "price_unit": price_session,
        }
        list.append(line1)
        for element in list:
            data["invoice_line_ids"].append((0, 0, element))
        invoice = self.env['account.move'].create(data)
        invoices = self.mapped('invoice_ids')
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        form_view = [(self.env.ref('account.view_move_form').id, 'form')]
        if 'views' in action:
            action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
        else:
            action['views'] = form_view
        action['res_id'] = invoice.id

        context = {
            'default_type': 'out_invoice',
        }

        action['context'] = context
        return action

    def facturer1(self):
        invoices = self.mapped('invoice_ids')
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            'default_type': 'out_invoice',
        }

        action['context'] = context
        return action

    def print_invoices(self):
        listes = []
        invoices = self.mapped('invoice_ids.id')
        for inv in invoices:
            listes.append(inv)
        invoice_id = max(listes)
        invoice = self.env['account.move'].search([('id', '=', invoice_id)])
        return self.env.ref('account.account_invoices').report_action(invoice)
