from flask import render_template, request
from utils.config import COUNTRY_CAPACITY_CONFIG_OPTIONS, COUNTRY_CAPACITY_DEFAULT_PARAMS, COUNTRY_TERMINALS
from utils.create_capacity_map import create_country_capacity_map
import os

def register_country_capacity_routes(app):
    @app.route('/country-capacity', methods=['GET', 'POST'])
    def country_capacity():
        if request.method == 'POST':
            # Capture selected parameters from the form
            selected_params = {
                'Country': request.form.get('Country'),
                'Number of terminals': request.form.get('Number of terminals'),
                'User terminal distribution algorithm': request.form.get('User terminal distribution algorithm'),
                'Beam allocation': request.form.get('Beam allocation'),
            }

            # Map form inputs to filename components
            country_fn = selected_params['Country'].lower().replace(' ', '')
            terminals_fn = selected_params['Number of terminals']
            
            ut_algo_map = {
                'Population density': 'population',
                'GCB No Cap': 'waterfill',
                'GCB 1K': 'waterfill_variant_1000',
                'GCB 10K': 'waterfill_variant_10000',
                'GCB 100K': 'waterfill_variant_100000'
            }
            ut_algo_fn = ut_algo_map.get(selected_params['User terminal distribution algorithm'])

            beam_alloc_map = {
                'Priority': 'priority',
                'Population waterfill': 'popwaterfill'
            }
            beam_alloc_fn = beam_alloc_map.get(selected_params['Beam allocation'])

            # Construct the expected data filename
            filename = f"{country_fn}_0_{terminals_fn}_{ut_algo_fn}_{beam_alloc_fn}_cell_capacities.txt"
            data_path = os.path.join('static', 'country_capacity_data', filename)

            viz_path = None
            error = None

            if os.path.exists(data_path):
                # Read the capacity data from the file
                h3_data = []
                with open(data_path, 'r') as f:
                    for line in f:
                        parts = line.strip().split(',')
                        if len(parts) == 2:
                            h3_data.append(parts)
                
                # Generate the visualization
                viz_path = create_country_capacity_map(h3_data, selected_params['Country'], filename)
            else:
                error = f"Data file not found for the selected configuration: {filename}"

            # Re-render the page with the results
            return render_template('country_capacity.html',
                                   config_options=COUNTRY_CAPACITY_CONFIG_OPTIONS,
                                   current_params=selected_params,
                                   selected_params=selected_params,
                                   country_terminals=COUNTRY_TERMINALS,
                                   viz_path=viz_path,
                                   error=error)
        
        # For GET requests, render with defaults and all terminal data
        return render_template('country_capacity.html',
                               config_options=COUNTRY_CAPACITY_CONFIG_OPTIONS,
                               current_params=COUNTRY_CAPACITY_DEFAULT_PARAMS,
                               country_terminals=COUNTRY_TERMINALS)