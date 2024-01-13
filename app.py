from flask import Flask, render_template, request, jsonify
import pymesh

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
                    return jsonify({"volume": volume, "surfaceArea": surfaceArea})
                else:
                    # Error handling for invalid STL file
                    return jsonify({"error": "Invalid STL file format"})
            else:
                # Error handling for no file uploaded
                return jsonify({"error": "No file uploaded"})
    else:
        return jsonify({"error": "Invalid request method"})
