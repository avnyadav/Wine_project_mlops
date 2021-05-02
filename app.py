from flask import Flask, render_template, request, jsonify
import os
import yaml
import joblib
import numpy as np
import json


params_path = "params.yaml"
webapp_root = "webapp"
static_dir = os.path.join(webapp_root, "static")
templates_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=templates_dir)

webapp = Flask(__name__)

def read_params(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)
    return config
def predict(data):
    config=read_params(params_path)
    model_dir_path=config['webapp_model_dir']
    model=joblib.load(model_dir_path)
    prediction=model.predict(data)
    print(prediction)
    return prediction[0]

def api_response(request):
    try:
        data=np.array([list(request.json.values())])
        config = read_params(params_path)
        model_dir_path = config['webapp_model_dir']
        model = joblib.load(model_dir_path)
        prediction = model.predict(data)
        print(prediction)
        return {"prediction":prediction[0]}
    except Exception as e:
        raise e


@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        if request.method == "POST":
            if request.form:
                data=dict(request.form).values()
                print(dict(request.form))
                print(data)
                data=[list(map(lambda x:float(x[0]),data))]
                reponse=predict(data)
                return render_template("index.html",response=reponse)
            elif request.json:
                try:
                    response=api_response(request)
                    return jsonify(response)
                except Exception as e:
                    return jsonify({"error":str(e)})
        else:
            return render_template("index.html")
    except Exception as e:
        print(e)
        error = {"error": str(e)}
        return render_template("404.html", error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)
