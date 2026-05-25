from flask import Flask, render_template, request, jsonify, send_file
import io
import os
from datetime import datetime
from estimator import calculate_project_estimates, generate_report_text

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/estimate", methods=["POST"])
def estimate():
    data = request.get_json()
    try:
        result = calculate_project_estimates(data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/download-report", methods=["POST"])
def download_report():
    data = request.get_json()
    try:
        result = calculate_project_estimates(data)
        report_text = generate_report_text(data, result)
        buffer = io.BytesIO()
        buffer.write(report_text.encode("utf-8"))
        buffer.seek(0)
        filename = f"MTN_Uganda_Project_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype="text/plain"
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
