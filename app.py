from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pymesh

app = Flask(__name__)
CORS(app)
app = Flask(__name__)

def read_stl_file(stl_file):
    # Read the STL file
    mesh = pymesh.load_mesh(stl_file.read().decode("utf-8"))
    return mesh

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Get the uploaded file
        if request.files.get("stl_file"):
            stl_file = request.files["stl_file"]

            # Check if file exists
            if stl_file.filename:
                # Check if file is a valid STL format
                valid_stl_format = False
                try:
                    pymesh.load_mesh(stl_file.read().decode("utf-8"))
                    valid_stl_format = True
                except:
                    pass

                if valid_stl_format:
                    # Read the STL file and extract relevant data
                    mesh = read_stl_file(stl_file)
                    vertices = mesh.vertices
                    triangles = mesh.faces

                    # Calculate size
                    volume = pymesh.volume(vertices, triangles)
                    surfaceArea = pymesh.surface_area(vertices, triangles)

                    # Return the calculated size as JSON
                    response = jsonify({"volume": volume, "surfaceArea": surfaceArea})

                    # Set CORS headers
                    response.headers["Access-Control-Allow-Origin"] = "*"
                    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
                    response.headers["Access-Control-Allow-Headers"] = "Content-Type"


                    
return response
                else:
                    # Error handling for invalid STL file
                    response = jsonify({"error": "Invalid STL file format"})
                    # Set CORS headers
                    response.headers["Access-Control-Allow-Origin"] = "*"
                    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
                    response.headers["Access-Control-Allow-Headers"] = "Content-Type"


                    
return response
            else:
                # Error handling for no file uploaded
                return jsonify({"error": "No file uploaded"})
    else:
        # Return 405 Not Allowed error for invalid HTTP methods
        return jsonify({"error": "Invalid request method"})
