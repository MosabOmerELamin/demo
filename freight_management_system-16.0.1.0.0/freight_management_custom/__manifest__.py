# -*- coding: utf-8 -*-
###################################################################################
#    Freight Management
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2022-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Megha K (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
{
    'name': 'Freight Management Custom',
    'version': '16.0.1.0.0',
    'summary': 'Module for Managing All Frieght Operations',
    'description': 'Module for Managing All Frieght Operations',
    'author': 'NCTR',
    'maintainer': 'NCTR',
    'company': 'NCTR',
    'website': 'https://www.nctr.com',
    'depends': ['freight_management_system'],
    'data': [
        'views/api_tracking_inherit_views.xml',
        'views/track_web_template.xml'
   
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
