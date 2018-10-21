#!/usr/bin/env python
import json
import os
import sys

from clarifai.rest import ClarifaiApp, Image as ClImage

API_KEY = os.environ.get('CLARIFAI_API_KEY')
CLARIFAI_APP = ClarifaiApp(api_key=API_KEY)
CLARIFAI_MODEL = CLARIFAI_APP.public_models.face_detection_model
PREDICTION_CACHE = 'cache_predictions'

def predict(filename):
    image = ClImage(filename=filename)
    filename = os.path.basename(filename[:filename.find('.')])
    output = os.path.join(PREDICTION_CACHE, '{}_output.json'.format(filename))
    if os.path.exists(output):
        print('using cache: ' + output)
        with open(output) as f:
            return json.load(f)
    else:
        print('using clarifai to predict: ' + output)
        response = CLARIFAI_MODEL.predict([image])
        with open(output, 'w') as f:
            json.dump(response, f)
        return response

if __name__ == '__main__':
    print(json.loads(predict(sys.argv[1])))
