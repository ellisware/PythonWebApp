import os

from flask import Flask, send_file
app = Flask(__name__)

# Sample Dynamic Route
@app.route("/hello")
def hello():
    return "Hello World from Flask in a uWSGI Nginx Docker container with \
     Python 3.6 (from the example template)"

# Sample Chart as Image
@app.route("/")
def main():
    index_path = os.path.join(app.static_folder, 'index.html')
    return send_file(index_path)

@app.route("/sample_chart.png")
def simple():
    import datetime
    from io import BytesIO
    import random
    import numpy as np

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure

    r = np.arange(0, 2, 0.01)
    theta = 2 * np.pi * r

    fig=Figure()
    ax=fig.add_subplot(111, projection="polar")

    ax.plot(theta, r)
    ax.set_rmax(2)
    ax.set_rticks([0.5, 1, 1.5, 2])  # less radial ticks
    ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
    ax.grid(True)

    ax.set_title("A line plot on a polar axis", va='bottom')


    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


# Everything not declared before (not a Flask route / API endpoint)...
@app.route('/<path:path>')
def route_frontend(path):
    # ...could be a static file needed by the front end that
    # doesn't use the `static` path (like in `<script src="bundle.js">`)
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    # ...or should be handled by the SPA's "router" in front end
    else:
        index_path = os.path.join(app.static_folder, 'index.html')
        return send_file(index_path)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
