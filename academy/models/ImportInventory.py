# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import models, fields, api, _
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)
import io

try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')

try:
    import pandas
except ImportError:
    _logger.debug('Cannot `import pandas`.')

try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class import_inventory(models.TransientModel):
    _name = "import.inventory"

    File_select = fields.Binary(string="Select File", required=True)
    inventory_reference = fields.Char(string="Inventory Reference", required=True)
    location_id = fields.Many2one('stock.location', 'Inventoried Location', required=False)

    def import_file(self):
        inventory = self.env['stock.inventory'].create(
            {'name': self.inventory_reference,  'state': 'confirm'})
        keys = ['default_code', 'product_name', 'location_name', 'real_product_qty', 'product_uom_name']
        try:
            csv_data = base64.b64decode(self.File_select)
            data_file = io.StringIO(csv_data.decode("utf-8"))
            data_file.seek(0)
            file_reader = []
            values = {}
            csv_reader = csv.reader(data_file, delimiter=',')
            file_reader.extend(csv_reader)
            lines = []
            result = {}


        except:
            raise Warning(_("Invalid file!"))
        loan_lines = []
        for i in range(1, len(file_reader)):
            field = list(map(str, file_reader[i]))
            values = dict(zip(keys, field))
            values['real_product_qty'] = float(values['real_product_qty'])
            lines.append(values)

        df = pandas.DataFrame(lines)
        lines = df.groupby(['location_name', 'product_name', 'default_code', 'product_uom_name']).sum().to_dict()
        print(lines)
        for k, v in lines['real_product_qty'].items():
            if k[0] == "":
                raise Warning(_('location_name field cannot be empty.'))
            elif k[1] == "":
                raise Warning(_('product_name field cannot be empty.'))
            elif k[2] == "":
                raise Warning(_('default_code field cannot be empty.'))
            elif k[3] == "":
                raise Warning(_('product_uom_name field cannot be empty.'))
            elif v == "":
                raise Warning(_('real_product_qty field cannot be empty.'))
            else:
                location = self.env['stock.location'].search([('name', '=', k[0])])
                product = self.env['product.product'].search([('name', '=', k[1]), ('default_code', '=', k[2])])
                #unit = self.env['product.uom'].search([('name', '=', k[3])])

                if not location:
                    temp = self.env['stock.location'].create({'name': k[0]})
                    location_id = temp.id
                    temp.location_id = self.location_id
                else:
                    location_id = location.id
                    location.location_id = self.location_id

                if not product:
                    temp = self.env['product.product'].create({'name': k[1], 'type': 'product', 'default_code': k[2]})
                    product_id = temp.id

                else:
                    product_id = product.id
                loan_lines.append((0, _, {'location_id': location_id, 'product_id': product_id,
                                          'product_qty': v}))
        print(inventory.write({'line_ids': loan_lines}))
        return True
