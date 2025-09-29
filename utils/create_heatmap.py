import pandas as pd
import pydeck as pdk
import os
from utils.config import COUNTRY_CONFIGS

def create_heatmap(h3_data, country, config_name):
    # Convert data to DataFrame
    df = pd.DataFrame(h3_data)[['hex', 'value', 'is_nation']]
    
    # Round values for display
    df['value'] = df['value'].round(3)

    # Create layers for regular and nation cells
    regular_cells = df[~df['is_nation']]
    nation_cells = df[df['is_nation']]
    
    regular_layer = pdk.Layer(
        "H3HexagonLayer",
        regular_cells,
        pickable=True,
        stroked=True,
        filled=True,
        extruded=False,
        get_hexagon="hex",
        get_fill_color=["value <= 0.5 ? 255 : 255 * 2 * (1-value)", "value <= 0.5 ? 255 * 2 * value : 255", "0"],
        get_line_color=[255, 255, 255],
        line_width_min_pixels=2,
    )
    
    nation_layer = pdk.Layer(
        "H3HexagonLayer",
        nation_cells,
        pickable=True,
        stroked=True,
        filled=True,
        extruded=False,
        get_hexagon="hex",
        get_fill_color=[0, 0, 255],
        get_line_color=[255, 255, 255],
        line_width_min_pixels=2,
    )
    
    # Set the viewport location
    view_state = pdk.ViewState(
        latitude=COUNTRY_CONFIGS[country]['latitude'],
        longitude=COUNTRY_CONFIGS[country]['longitude'],
        zoom=COUNTRY_CONFIGS[country]['zoom'],
        bearing=0,
        pitch=0
    )
    
    # Create deck
    r = pdk.Deck(
        layers=[regular_layer, nation_layer],
        initial_view_state=view_state,
        tooltip={"text": "H3 cell: {hex}\nAvailable capacity: {value}"},
        map_style="light",
    )
    
    # Generate a unique filename based on parameters
    viz_dir = os.path.join('static', 'visualizations')
    os.makedirs(viz_dir, exist_ok=True)
    
    # Create HTML file with custom colorscale
    config_name = config_name.split('.')[0]  # Remove file extension
    html_path = os.path.join(viz_dir, f"{config_name}.html")
    
    # Get the base HTML from pydeck
    html_content = r.to_html(as_string=True)
    
    color_scale_path = os.path.join('static', 'color_scale.html')
    with open(color_scale_path, 'r') as f:
        color_scale_html = f.read()
    
    # Insert color scale before closing body tag
    html_content = html_content.replace('</body>', f'{color_scale_html}</body>')
    
    # Write the modified HTML to file
    with open(html_path, 'w') as f:
        f.write(html_content)
    
    return f"visualizations/{config_name.lower()}.html"