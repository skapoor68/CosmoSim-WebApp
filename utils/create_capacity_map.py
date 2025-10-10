import pandas as pd
import pydeck as pdk
import os
from utils.config import COUNTRY_CONFIGS

def create_country_capacity_map(h3_data, country, config_name):
    """
    Generates and saves a pydeck map visualization for per-cell capacity.
    """
    # Convert input data to a DataFrame
    df = pd.DataFrame(h3_data, columns=['hex', 'capacity'])
    df['capacity'] = pd.to_numeric(df['capacity'])

    # Normalize capacity to a 0-1 range for coloring
    min_cap = df['capacity'].min()
    max_cap = df['capacity'].max()
    if max_cap > min_cap:
        df['normalized_capacity'] = (df['capacity'] - min_cap) / (max_cap - min_cap)
    else:
        # Avoid division by zero if all capacities are the same
        df['normalized_capacity'] = 0.5

    # Define the H3 hexagon layer for the map
    layer = pdk.Layer(
        "H3HexagonLayer",
        df,
        pickable=True,
        stroked=True,
        filled=True,
        extruded=False,
        get_hexagon="hex",
        # Color scale: green (low) -> yellow (mid) -> red (high)
        get_fill_color="[normalized_capacity <= 0.5 ? 255 : 255 * 2 * (1 - normalized_capacity), normalized_capacity <= 0.5 ? 255 * 2 * normalized_capacity : 255, 0, 185]",
        get_line_color=[255, 255, 255],
        line_width_min_pixels=2,
    )

    # Set the initial viewport based on the selected country
    view_state = pdk.ViewState(
        latitude=COUNTRY_CONFIGS[country]['latitude'],
        longitude=COUNTRY_CONFIGS[country]['longitude'],
        zoom=COUNTRY_CONFIGS[country]['zoom'],
        bearing=0,
        pitch=0
    )

    # Create the pydeck map object
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Capacity: {capacity} Mb"},
        map_style="light",
    )

    # Ensure the visualization directory exists
    viz_dir = os.path.join('static', 'visualizations', 'country_capacity')
    os.makedirs(viz_dir, exist_ok=True)

    # Save the map to an HTML file
    config_name = config_name.split('.')[0]
    html_path = os.path.join(viz_dir, f"{config_name}.html")
    
    # Get the base HTML from pydeck
    html_content = r.to_html(as_string=True)
    
    # Read the color scale HTML
    color_scale_path = os.path.join('static', 'country_capacity_color_scale.html')
    with open(color_scale_path, 'r') as f:
        color_scale_html = f.read()
        
    # Insert color scale before closing body tag
    html_content = html_content.replace('</body>', f'{color_scale_html}</body>')
    
    # Write the modified HTML to file
    with open(html_path, 'w') as f:
        f.write(html_content)

    # Return the relative path for use in the template
    return f"visualizations/country_capacity/{config_name.lower()}.html"