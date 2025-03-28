from flask import Flask, request, jsonify
import requests
from io import BytesIO
import prepare_text as pt
import text_generate as tg
from flask_cors import CORS
from prepare_text import TypeNotSupportError

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

@app.route('/visualization', methods=['POST'])
def process_image():
    try:
        data = request.get_json()
        image_url = data.get('image_url')

        age = data.get('age')
        gender = data.get('gender')

        if not age or not (int(age) > 0 and int(age) < 110):
            return jsonify({"error": "Age field is not available or invalid"}), 400     

        if gender not in ['male', 'female']:
            return jsonify({"error": "Gender field is not available or invalid"}), 400
        
        if not image_url:
            return jsonify({"error": "No lab report image URL provided"}), 400

        response = requests.get(image_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch image from URL"}), 400

        image_data = BytesIO(response.content)
        extracted_text = pt.extract_text(image_data)

        processed_data = pt.process_report_data(extracted_text, age, gender)
        final_data = pt.add_reference_data(processed_data)

        explanation = tg.generate_explanation(final_data)
        cleaned_explanation = tg.clean_response(explanation)

        tg.save_to_file(explanation, "explanations/explanation_before_cleaning.md")
        tg.save_to_file(cleaned_explanation, "explanations/explanation_after_cleaning.md")


        return jsonify({
            "status": "success",
            "explanation": cleaned_explanation
        }), 200

    except TypeNotSupportError as e:
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def health():
    return jsonify({
            "message": "Curasync Visualization Backend is alive."
        }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)