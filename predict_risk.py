import os
import joblib
import pandas as pd
from data.pdftotext import pdftotxt
from cleaning.clean_text import clean_text, extract_risk_features

def predict_risk(file_path):
    ext = os.path.splitext(file_path)[-1].lower()

    # Load file content
    if ext == ".pdf":
        text = pdftotxt(file_path)
    elif ext == ".txt":
        with open(file_path, encoding='utf-8') as f:
            text = f.read()
    else:
        raise ValueError("Format non supporté. Veuillez fournir un fichier PDF ou TXT.")

    # Clean and extract features
    cleaned = clean_text(text)
    features = extract_risk_features([text])
    features["clean_text"] = [cleaned]

    # Load models
    svm_model = joblib.load("svm_model.pkl")
    tfidf_vectorizer = joblib.load("tfidf_vectorizer.pkl")
    expected_columns = joblib.load("feature_columns.pkl")  # Must match training

    # Vectorize cleaned text
    tfidf_input = tfidf_vectorizer.transform([cleaned])
    tfidf_df = pd.DataFrame(tfidf_input.toarray(), columns=tfidf_vectorizer.get_feature_names_out())

    # Manual features
    manual_features = features[[
        'word_count',
        'financial_distress_count',
        'operational_issues_count',
        'regulatory_concerns_count',
        'negative_sentiment'
    ]].reset_index(drop=True)

    # Combine features
    X_input = pd.concat([tfidf_df, manual_features], axis=1)

    # Align features to expected set
    missing_cols = set(expected_columns) - set(X_input.columns)
    for col in missing_cols:
        X_input[col] = 0
    X_input = X_input[expected_columns]

    # Predict
    prediction = svm_model.predict(X_input)[0]
    probability = svm_model.predict_proba(X_input)[0][1]

    return {
        "is_risky": bool(prediction),
        "probability": round(probability, 4),
        "missing_features": list(missing_cols)  # Optional for debugging
    }


predict_risk("data\pdfs\FCMKW113796_20230413.pdf")