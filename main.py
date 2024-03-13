from fastapi import FastAPI, HTTPException
import requests
app = FastAPI()
@app.get('/extract_words')
async def extract_words(text_query: str = None, json_url: str = None):
  if not text_query:
    raise HTTPException(status_code=400, detail="Missing text_query parameter")
  if not json_url:
    raise HTTPException(status_code=400, detail="Missing json_url parameter")
  response = requests.get(json_url)
  if response.status_code != 200:
    raise HTTPException(status_code=500, detail=f"Error downloading JSON: {response.status_code}")
  try:
    data = response.json()
  except:
    raise HTTPException(status_code=400, detail="Invalid JSON format")
  found = False
  for segment in data['segments']:
    words = segment['words']
    for word in words:
      if word['text'] == text_query and not found:
        result = {"start": word['start'], "end": word['end']}
        found = True
        break
  if not found:
    raise HTTPException(status_code=404, detail=f"Text '{text_query}' not found")
  elif found and len(data['segments']) > 1:
    return {"message": f"Text '{text_query}' found multiple times. Returning only the first occurrence.", "data": result}
  return result
