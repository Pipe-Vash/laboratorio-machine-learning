# Inicializamos las librerias necesarias 
import pickle
import json
from flask import Flask, request
import pandas as pd
from keras import models


# Cargamos el modelo y los objetos necesarios para la transformacion de los datos
model= models.load_model('churn/models/best_model.hdf5')
categorical_transformer = pickle.load(open("churn/models/cat_trans.pk", "rb"))
scaler = pickle.load(open("churn/models/scaler.pk", "rb"))
df_features = pickle.load(open("churn/models/df_features.pk", "rb"))

# create the Flask app
app = Flask(__name__)


# Hacemos la predicción y definimos la ruta para la API
@app.route('/query')
def query_example():
    feats = request.args.get('feats').split(',')
    feats_df= pd.DataFrame([feats], columns= df_features)
    final_df= scaler.transform(categorical_transformer.transform(feats_df))
    test_pred = model.predict(final_df)
    test_pred_labels = (test_pred > 0.5).astype(int).flatten()


    response = {
        'response': test_pred_labels.tolist()
    }
    return json.dumps(response)

# Corremos el programa.
if __name__ == '__main__':
    # run app in debug mode on port 3001
    app.run(debug=True, port=3001)