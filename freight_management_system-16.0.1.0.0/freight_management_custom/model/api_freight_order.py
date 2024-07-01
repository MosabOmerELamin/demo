from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import requests
from datetime import datetime, timedelta



class FreightOrderCustom(models.Model):
    _inherit = 'freight.order'

    bill_of_lading = fields.Char(string='Bill Of Lading')
    shipment_status = fields.Char(string='Shipment Status')
    # test = fields.Char(string='test')
    loading_port_id = fields.Many2one(
        'freight.port', 
        string="Loading Port",
        required=False,
        help="Loading port of the freight order",
    )
    discharging_port_id = fields.Many2one(
        'freight.port',
        string="Discharging Port",
        required=False,
        help="Discharging port of freight order",
    )
    port_of_loading = fields.Char(string='Loading Port')
    port_of_discharge = fields.Char(string='Discharging Port')

    def parse_datetime(self,date_str):
        for fmt in ('%Y-%m-%dT%H:%M:%S.%f%z', '%Y-%m-%dT%H:%M:%S%z'):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Time data '{date_str}' does not match any expected format.")



  
    def track_order(self):
        for record in self:
            if record.bill_of_lading:
                url = "https://api.sinay.ai/container-tracking/api/v2/shipment?&route=true&ais=true"
                headers = {
                    'API_KEY': '52cbbdd4-9e80-4582-9e34-3343c41b1fe5',
                }
                params = {
                    'shipmentNumber': record.bill_of_lading
                }
                try:
                    response = requests.get(url, headers=headers, params=params)
                    response.raise_for_status() 
                    data = response.json()
                except requests.exceptions.RequestException as e:
                    print("Error during request:", e)
                    return None
                except ValueError as e:
                    print("Error parsing JSON response:", e)
                    return None
                
                shipment_status = data.get('metadata', {}).get('shippingStatus')
                port_of_loading = data.get('route', {}).get('pol', {}).get('location', {}).get('name', '')
                print('ssssssssss',port_of_loading)
                port_of_discharge = data.get('route', {}).get('pod', {}).get('location', {}).get('name', '')
                print('wwwwwwwwww',port_of_discharge)


                container_moves = []
                for container in data.get('containers', []):
                    for event in container.get('events', []):
                        location_name = event['location']['name']
                        vessel_data = event.get('vessel')
                        vessel_name = vessel_data['name'] if vessel_data else ''   
                        move_description = event.get('description', '')
                        try:
                            move_date = self.parse_datetime(event['date'])
                        except ValueError as e:
                            print("Error parsing date:", e)
                            continue
                        
                        container_moves.append({
                            'location': location_name,
                            'vessel': vessel_name,
                            'move': move_description,
                            'date': move_date,
                        })
                    break    

                shipment_info = {
                    'shipment_status': shipment_status,
                    'port_of_loading': port_of_loading,
                    'port_of_discharge': port_of_discharge,
                    'track_ids': [(0, 0, {
                        'location': move['location'],
                        'vessel': move['vessel'],
                        'move': move['move'],
                        'date': move['date'].strftime('%Y-%m-%d %H:%M:%S.%fZ')
                    }) for move in container_moves],
                }        

                record.update({
                    'shipment_status': shipment_info.get('shipment_status', ''),
                    'port_of_loading': shipment_info.get('port_of_loading', ''),
                    'port_of_discharge': shipment_info.get('port_of_discharge', ''),
                    'track_ids': shipment_info.get('track_ids', [])
                })
        return True  
