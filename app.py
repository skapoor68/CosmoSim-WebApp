from flask import Flask, render_template

app = Flask(__name__)

from routes.heatmap import register_heatmap_routes
from routes.gs_utilization import register_gs_routes
from routes.country_capacity import register_country_capacity_routes

register_heatmap_routes(app)
register_gs_routes(app)
register_country_capacity_routes(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)