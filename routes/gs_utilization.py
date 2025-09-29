from flask import render_template, request
import os
import json
from utils.config import CONFIG_OPTIONS, DISPLAY_MAPPING, DEFAULT_PARAMS

def register_gs_routes(app):    
    @app.route('/gs-utilization', methods=['GET', 'POST'])
    def gs_utilization():
        """Route for ground station utilization visualization"""
        # Create a modified config options dictionary without Incumbent demand
        gs_config_options = {
            'Country': CONFIG_OPTIONS['Country'],
            'Number of terminals': CONFIG_OPTIONS['Number of terminals'],
            'Population cap': CONFIG_OPTIONS['Population cap'],
            'Routing policy': CONFIG_OPTIONS['Routing policy'],
            'Scenario': ['Emergency', 'Incumbent']
        }
        
        # Read ground station location data
        gs_locations = []
        try:
            with open(os.path.join('static', 'data', 'ground_stations_starlink.csv'), 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) >= 4:
                        gs_id = int(parts[0])
                        name = parts[1]
                        lat = float(parts[2])
                        lng = float(parts[3])
                        gs_locations.append({
                            'id': gs_id,
                            'name': name,
                            'lat': lat,
                            'lng': lng
                        })
        except Exception as e:
            print(f"Error reading ground station locations: {e}")
        
        if request.method == 'POST':
            # Get user-selected parameters
            country = request.form.get('Country').lower()
            if country == 'south africa':
                country = 'southafrica'
                
            num_terminals = request.form.get('Number of terminals')
            pop_cap = request.form.get('Population cap')
            routing_display = request.form.get('Routing policy')
            routing = DISPLAY_MAPPING['Routing policy'][routing_display]
            scenario = request.form.get('Scenario').lower()
            
            # Construct the path to the utilization data file
            utilization_file = f"starlink_current_5shells_isls_three_ground_stations_starlink_cells_{country}_0_{num_terminals}_waterfill_variant_{pop_cap}_waterfill/{scenario}/{routing}/gs_utilization.txt"
            utilization_path = os.path.join('static', 'utilization_data', utilization_file)
            
            # Check if the file exists
            if os.path.exists(utilization_path):
                # Read the utilization data
                utilizations = {}
                with open(utilization_path, 'r') as f:
                    for line in f:
                        parts = line.strip().split(',')
                        if len(parts) >= 2:
                            gs_id = int(parts[0]) - 6364
                            util = float(parts[1])
                            utilizations[gs_id] = util
                
                # Combine the location and utilization data
                gs_data = []
                for gs in gs_locations:
                    gs_id = gs['id']
                    util = utilizations.get(gs_id, 0)
                    gs_data.append({
                        'id': gs_id,
                        'name': gs['name'],
                        'lat': gs['lat'],
                        'lng': gs['lng'],
                        'utilization': util
                    })
                
                return render_template('gs_utilization.html',
                                    gs_data=json.dumps(gs_data),
                                    config_options=gs_config_options,
                                    current_params=request.form)
            else:
                return render_template('gs_utilization.html',
                                    error=f"Utilization data not found: {utilization_file}",
                                    config_options=gs_config_options,
                                    current_params=request.form)
        
        # For GET requests, use default parameters with Emergency scenario
        default_params = {
            'Country': DEFAULT_PARAMS['Country'],
            'Number of terminals': DEFAULT_PARAMS['Number of terminals'],
            'Population cap': DEFAULT_PARAMS['Population cap'],
            'Routing policy': DEFAULT_PARAMS['Routing policy'],
            'Scenario': 'Emergency'
        }
        
        return render_template('gs_utilization.html',
                             config_options=gs_config_options,
                             current_params=default_params)