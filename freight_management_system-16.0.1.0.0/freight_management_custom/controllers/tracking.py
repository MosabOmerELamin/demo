from odoo import http
from odoo.http import request

class BillOfLadingController(http.Controller):
    @http.route('/tracking', type='http', auth='public', website=True)
    def index(self, **kw):
        return request.render('freight_management_custom.tracking_form', {})

    @http.route('/tracking/search', type='http', auth='public', methods=['POST'], website=True)
    def search(self, **post):
        bill_of_lading = post.get('bill_of_lading')
        user_id = request.env.user
        partner_id = user_id.partner_id.id

        print('User:', user_id)
        print('Partner ID:', partner_id)
        record = request.env['freight.order'].sudo().search([
            ('bill_of_lading', '=', bill_of_lading),
            ('consignee_id','=',partner_id)
            ], limit=1)
        if record :
            values = {
                'record': record,
            }
            return request.render('freight_management_custom.tracking_result', values)
        else:
            values = {
                'error': 'You do not have permission to view this shipment or it does not exist.',
            }
            return request.render('freight_management_custom.tracking_form', values)

