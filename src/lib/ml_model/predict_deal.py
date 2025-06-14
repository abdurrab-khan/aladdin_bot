from pandas import DataFrame
from joblib import load
from ..types import Product
from os import path


def load_model(model_path='best_deal_model.pkl', feature_names_path='feature_names.pkl'):
    """Load the trained model and feature names"""

    # Get the directory where this script is located
    script_dir = path.dirname(path.abspath(__file__))

    # Create absolute paths to the model files
    model_path = path.join(script_dir, model_path)
    feature_names_path = path.join(script_dir, feature_names_path)

    model = load(model_path)
    feature_names = load(feature_names_path)
    return model, feature_names


def predict_deal(product_data: Product) -> dict['prediction': str, 'confidence': float]:
    """
    Predict if the product is a best deal or not.

    args:
        product_data (Product): The product data to predict on.

    return:
        dict: A dictionary containing the prediction and confidence score.
    """
    model, feature_names = load_model()
    if isinstance(product_data, dict):
        cp_product_data = DataFrame([product_data])

    if 'discount_percentage' not in cp_product_data.columns:
        cp_product_data['discount_percentage'] = (
            product_data['discount_price'] / product_data['price']) * 100

    if 'discount_amount' not in cp_product_data.columns:
        cp_product_data['discount_amount'] = product_data['price'] - \
            product_data['discount_price']

    X = product_data[feature_names]

    predictions = model.predict(X)
    probabilities = model.predict_proba(X)

    results = []
    for i, pred in enumerate(predictions):
        result = {
            'prediction': 'Best Deal' if pred == 1 else 'Not Best Deal',
            'confidence': probabilities[i][1]
        }
        results.append(result)

    return results[0]
