from flask import Flask, render_template, request, jsonify, flask_cors
import pymesh

app = Flask(__name__)
CORS(app)

def read_stl_file(stl_file):
    # Read the STL file
    mesh = pymesh.load_mesh(stl_file.read().decode("utf-8"))

    # Check for valid STL format
    if mesh.num_vertices == 0:
        raise ValueError("Invalid STL file format")

    return mesh

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if not request.files.get("stl_file"):
            raise ValueError("No file uploaded")

        stl_file = request.files["stl_file"]

        # Validate file size
        if stl_file.size > 10 * 1024 * 1024:  # 10 MB limit
            raise ValueError("File size exceeds 10MB")

        # Read and calculate size
        mesh = read_stl_file(stl_file)
        volume = pymesh.volume(mesh.vertices, mesh.faces)
        surface_area = pymesh.surface_area(mesh.vertices, mesh.faces)

        # Prepare JSON response
        result = {"volume": volume, "surfaceArea": surface_area}

        # Handle errors
        try:
            # Check network connectivity
            import requests
            r = requests.get("https://httpbin.org/get")
            if r.status_code == 200:
                return jsonify(result)
            else:
                raise ValueError("Network error")
        except:
            raise ValueError("Unknown error")
    else:
        return jsonify({"error": "Invalid request method"})

@app.route("/3d-model", methods=["GET"])
def display_3d_model():
    # Handle request and display 3D model here

    return render_template("3d-model.html")

@app.route("/error", methods=["GET", "POST"])
def handle_error():
    # Handle error scenarios and display error messages

    error_code = request.args.get("error")
    if error_code == "no_file":
        error_message = "No file uploaded"
    elif error_code == "invalid_format":
        error_message = "Invalid STL file format"
    elif error_code == "file_size":
        error_message = "File size exceeds 10MB"
    elif error_code == "network":
        error_message = "Network error"
    else:
        error_message = "Unknown error"

    return render_template("error.html", error_message=error_message)
