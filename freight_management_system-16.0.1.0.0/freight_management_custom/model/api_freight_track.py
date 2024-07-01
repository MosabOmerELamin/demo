from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import requests
from datetime import datetime, timedelta


class FreightTrack(models.Model):
    _inherit = 'freight.track'


    move = fields.Char(string='Move')
    location = fields.Char(string='Location')
    vessel = fields.Char(string='Vessel')