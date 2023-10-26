import joblib
import pickle
import os
import json
import sklearn
import pandas as pd
import subprocess
import sys
subprocess.check_call([sys.executable,'-m', 'pip', 'install',  "autoai-libs==1.13.6","--no-deps"])


"""
Deserialize fitted model
"""
def model_fn(model_dir):
    model = pickle.load(os.path.join(model_dir, "scikit_model.pkl"))
    return model

"""
input_fn
    request_body: The body of the request sent to the model.
    request_content_type: (string) specifies the format/variable type of the request
"""
def input_fn(request_body, request_content_type):
    if request_content_type == 'application/json':
        request_body = json.loads(request_body)
        inpVar = request_body['Input']
        return inpVar
    else:
        raise ValueError("This model only supports application/json input")

"""
predict_fn
    input_data: returned array from input_fn above
    model (sklearn model) returned model loaded from model_fn above
"""
def predict_fn(input_data, model):
    df=pd.DataFrame(input_data)
    
    probs=model.predict_proba(df.values).tolist()
    preds=model.predict(df.values).tolist()
    
    return [{'prediction':preds[i], 'probability':probs[i]} for i in range(len(preds))]
    


"""
output_fn
    prediction: the returned value from predict_fn above
    content_type: the content type the endpoint expects to be returned. Ex: JSON, string

"""

def output_fn(prediction, content_type):
    res = prediction
    respJSON = {'predictions': res}
    return respJSON