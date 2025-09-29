from flask import render_template, request
import os
import json
from utils.create_heatmap import create_heatmap
from utils.config import CONFIG_OPTIONS, DISPLAY_MAPPING, DEFAULT_PARAMS

def register_heatmap_routes(app):    
    @app.route('/heatmap', methods=['GET', 'POST'])
    def heatmap():
        if request.method == 'POST':
            # Get user-selected parameters from the form
            country = request.form.get('Country').lower()
            if country == 'south africa':
                country = 'southafrica'
                
            num_terminals = request.form.get('Number of terminals')
            pop_cap = request.form.get('Population cap')
            beam_allocation = 'waterfill'  # Fixed value as per requirement
            routing_display = request.form.get('Routing policy')
            routing = DISPLAY_MAPPING['Routing policy'][routing_display]
            demand_display = request.form.get('Incumbent demand')
            demand = DISPLAY_MAPPING['Incumbent demand'][demand_display]
            
            json_name = f"{country}_{num_terminals}_{pop_cap}_{beam_allocation}_{routing}_{demand}.json"
            json_path = os.path.join('static', 'h3_data', json_name)
            print(f"Looking for JSON at: {json_path}")
            
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    h3_data = json.load(f)
                
                # Create visualization and get path to HTML file
                country_display = DISPLAY_MAPPING['Country'].get(country, country.capitalize())
                viz_path = create_heatmap(h3_data, country_display, json_name)
                
                return render_template('heatmap.html',
                                    viz_path=viz_path,
                                    config_options=CONFIG_OPTIONS,
                                    current_params=request.form)
            else:
                # For debugging purposes, list all files in the directory
                files = os.listdir(os.path.join('static', 'h3_data'))
                print(f"Available files: {files}")
                
                return render_template('heatmap.html',
                                    error=f"Configuration not found: {json_name}",
                                    config_options=CONFIG_OPTIONS,
                                    current_params=request.form)
        
        # For GET requests, use default parameters
        return render_template('heatmap.html',
                             config_options=CONFIG_OPTIONS,
                             current_params=DEFAULT_PARAMS)