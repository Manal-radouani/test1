# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Academy(http.Controller):
    @http.route(['/my/', '/my/home'], website=True, auth='user')
    def index(self, **kw):
        Partners = http.request.env['res.partner']
        id_user = http.request.env.user.partner_id.id
        return http.request.render('academy.portal_my_home', {
            'partners': Partners.search([('id', '=', id_user)])
        })

    @http.route('/my/<model("res.partner"):partner>/', auth='public', website=True)
    def partner(self, partner):
        sessions = list(partner.session_ins)
        return http.request.render('academy.portal_session', {
            'session': sessions
        })

    @http.route(['/my/session/<model("academy.session"):session>/'], auth='user', website=True)
    def session(self, session):
        return http.request.render('academy.session_details', {
            'session': session
        })

    @http.route(['/my/session/edit/<model("academy.session"):session>/'], auth='user', website=True)
    def edit(self, session):
        return http.request.render('academy.portal_my_details', {
            'session': session
        })

    @http.route(['/my/session/edit/done/'], auth='user', website=True)
    def confirm(self, ses_id, **kw):
        session = http.request.env['academy.session'].search([('id', '=', ses_id)])

        session.name = kw['name']
        session.duration = kw['duration']
        session.start_date = kw['start_date']
        session.seats = kw['seats']

        return http.request.redirect('/my/home')
