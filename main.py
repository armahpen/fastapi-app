from flask import Flask, jsonify, request
import requests  # Import requests library

app = Flask(__name__)

@app.route('/extract_words', methods=['GET'])
def extract_words():
  text_to_query = request.args.get('text_query')
  json_url = request.args.get('json_url')

  if not text_to_query:
      return jsonify({"error": "Missing text_query parameter"}), 400
  if not json_url:
      return jsonify({"error": "Missing json_url parameter"}), 400

  # Download JSON data from provided URL
  response = requests.get(json_url)
  if response.status_code != 200:
      return jsonify({"error": f"Error downloading JSON: {response.status_code}"}), 500
  try:
      data = response.json()
  except:
      return jsonify({"error": "Invalid JSON format"}), 400

  # Find the first occurrence
  found = False
  for segment in data['segments']:
    words = segment['words']
    for word in words:
      if word['text'] == text_to_query and not found:
        result = {"start": word['start'], "end": word['end']}
        found = True
        break  # Exit inner loop after finding the first occurrence

  # Handle not found or multiple occurrences
  if not found:
      return jsonify({"message": f"Text '{text_to_query}' not found"}), 404
  elif found and len(data['segments']) > 1:
      return jsonify({"message": f"Text '{text_to_query}' found multiple times. Returning only the first occurrence."}), 200, result

  return jsonify(result)

if __name__ == '__main__':
  app.run(debug=True)
