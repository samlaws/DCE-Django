import os
from sklearn.externals import joblib
from django.core.cache import cache
from pathlib import Path
from newspaper.settings import BASE_DIR

def classify_defect(phrase):

    model_cache_key = 'mlp_model'

    path = os.path.join(BASE_DIR,'articles\\dce_model.pkl')

    model = cache.get(model_cache_key)

    if model is None:
        model_path = os.path.join(path)
        model = joblib.load(model_path)
        #save in django memory cache
        cache.set(model_cache_key, model, None)

    prediction = model.predict([phrase])

    if prediction == [1]:
	    return 'Functional'
    elif prediction == [2]:
        return 'Performance'
    elif prediction == [3]:
	    return 'Reliability and Scalability Issues'
    elif prediction == [4]:
	    return 'Security'
    elif prediction == [5]:
	    return 'Usability'
    elif prediction == [0]:
        return 'Compliance'
