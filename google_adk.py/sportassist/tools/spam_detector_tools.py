import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# In a real-world scenario, the model and vectorizer would be saved and loaded.
# For this example, we'll keep them in memory.
_model = None
_vectorizer = None

def load_dataset(file_path: str) -> str:
    """
    Loads a dataset from a CSV or JSON file.

    Args:
        file_path: The path to the dataset file.

    Returns:
        A JSON string of the dataframe head and column info.
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            df = pd.read_json(file_path, lines=True)
        else:
            return json.dumps({"error": "Unsupported file format. Please use CSV or JSON."})

        if 'text' not in df.columns or 'label' not in df.columns:
            return json.dumps({"error": "Dataset must contain 'text' and 'label' columns."})

        result = {
            "message": "Dataset loaded successfully.",
            "columns": df.columns.tolist(),
            "sample_data": df.head().to_dict(orient='records')
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

def preprocess_data(text_data: str) -> str:
    """
    Performs basic text cleaning and feature extraction.
    For simplicity, this example assumes text_data is a list of strings.

    Args:
        text_data: A JSON string representing a list of email texts.

    Returns:
        A JSON string with preprocessing status.
    """
    # TODO: Implement more advanced preprocessing like stopword removal, stemming, etc.
    global _vectorizer
    _vectorizer = TfidfVectorizer(max_features=5000)
    try:
        data_list = json.loads(text_data)
        features = _vectorizer.fit_transform(data_list)
        return json.dumps({
            "status": "Preprocessing complete.",
            "features_shape": features.shape,
            "num_features": len(_vectorizer.get_feature_names_out())
        })
    except Exception as e:
        return json.dumps({"error": f"Failed to preprocess data: {str(e)}"})


def train_model(training_data_json: str) -> str:
    """
    Trains a simple spam classification model.

    Args:
        training_data_json: A JSON string containing 'features' and 'labels'.
                           Example: '{"features": ["email text 1", ...], "labels": ["spam", "not spam", ...]}'

    Returns:
        A JSON string with the training results and evaluation metrics.
    """
    global _model, _vectorizer
    try:
        data = json.loads(training_data_json)
        texts = data['features']
        labels = data['labels']

        # Preprocess the text data
        _vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        X = _vectorizer.fit_transform(texts)
        
        X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

        _model = LogisticRegression()
        _model.fit(X_train, y_train)

        y_pred = _model.predict(X_test)

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, pos_label="spam"),
            "recall": recall_score(y_test, y_pred, pos_label="spam"),
            "f1_score": f1_score(y_test, y_pred, pos_label="spam")
        }
        return json.dumps({"status": "Model training complete.", "metrics": metrics}, indent=2)

    except Exception as e:
        return json.dumps({"error": f"Model training failed: {str(e)}"})

def predict_spam(email_text: str) -> str:
    """
    Predicts if a single email is spam or not.

    Args:
        email_text: The text content of the email.

    Returns:
        A structured JSON string with the prediction and probability.
    """
    global _model, _vectorizer
    if not _model or not _vectorizer:
        return json.dumps({"error": "Model is not trained yet. Please train the model first."})

    try:
        # Transform the input email text using the same vectorizer
        features = _vectorizer.transform([email_text])
        prediction = _model.predict(features)[0]
        probability = _model.predict_proba(features).max()

        # Get top features
        feature_names = _vectorizer.get_feature_names_out()
        # TODO: A more robust way to explain features is needed for a real model.
        top_features = sorted(zip(_model.coef_[0], feature_names), reverse=True)[:5]

        result = {
            "prediction": prediction,
            "probability": f"{probability:.2f}",
            "top_features_explaining_decision": [feature for _, feature in top_features]
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Prediction failed: {str(e)}"})
