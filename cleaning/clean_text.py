import nltk
import re
import spacy
from nltk.corpus import stopwords
from unidecode import unidecode
import string
import pandas as pd

nltk.download('stopwords')


# Stopwords combinés
stopwords_fr = set(stopwords.words("french"))
stopwords_en = set(stopwords.words("english"))
stopwords_combined = stopwords_fr.union(stopwords_en)

# Chargement des modèles français et anglais
nlp_fr = spacy.load("fr_core_news_sm")
nlp_en = spacy.load("en_core_web_sm")

RISK_KEYWORDS = {
    'financial_distress': [
        'deficit', 'perte', 'endettement', 'liquidite', 'insolvabilite', 
        'faillite', 'restructuration', 'difficulte', 'crise', 'loss', 
        'debt', 'bankruptcy', 'liquidity', 'distress', 'default',
        'impairment', 'write-down', 'provision', 'deterioration',
        'decline', 'decrease', 'negative', 'shortfall'
    ],
    'operational_issues': [
        'retard', 'probleme', 'suspension', 'arret', 'fermeture',
        'reduction', 'licenciement', 'restructuration', 'delay',
        'problem', 'closure', 'layoff', 'downsizing', 'interruption',
        'shutdown', 'suspension', 'difficulties', 'issues'
    ],
    'regulatory_concerns': [
        'sanction', 'amende', 'violation', 'non-conformite',
        'penalite', 'enquete', 'penalty', 'fine', 'investigation',
        'compliance', 'violation', 'audit', 'litigation',
        'lawsuit', 'legal', 'court', 'dispute'
    ],
    'market_risks': [
        'volatilite', 'incertitude', 'risque', 'exposition',
        'volatility', 'uncertainty', 'risk', 'exposure',
        'fluctuation', 'instability', 'vulnerable'
    ]
}


ALL_RISK_KEYWORDS = []
for category in RISK_KEYWORDS.values():
    ALL_RISK_KEYWORDS.extend(category)

def clean_text(text):
    # Normalisation : minuscules, sans accents
    text = text.lower()
    text = unidecode(text)
    
    # Suppression des caractères spéciaux
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r'\s+', ' ', text)
    
    # Remove short words (less than 3 characters)
    text = re.sub(r'\b\w{1,2}\b', '', text)
    # Suppression des mots trop courts
    text = re.sub(r'http\S+|www\S+', ' ', text)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'\d+', ' NUM ', text)  # Replace numbers with token
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # Tokenisation + lemmatisation avec spaCy
    doc_fr = nlp_fr(text)
    doc_en = nlp_en(text)

    tokens = []
    for token in doc_fr:
        if token.lemma_ not in stopwords_combined:
            tokens.append(token.lemma_)
    for token in doc_en:
        if token.lemma_ not in stopwords_combined:
            tokens.append(token.lemma_)

    return " ".join(tokens)


def extract_risk_features(documents):
    """Extract various risk-related features from documents"""
    features = []
    
    for doc in documents:
        doc_features = {}
        
        # Basic statistics
        doc_features['doc_length'] = len(doc)
        doc_features['word_count'] = len(doc.split())
        
        # Risk keyword counts by category
        for category, keywords in RISK_KEYWORDS.items():
            count = sum(1 for keyword in keywords if keyword.lower() in doc.lower())
            doc_features[f'{category}_count'] = count
            doc_features[f'{category}_density'] = count / max(len(doc.split()), 1)
        
        # Overall risk score
        doc_features['total_risk_score'] = calculate_risk_score(doc)
        
        # Sentiment-related features (simple approach)
        negative_words = ['not', 'no', 'never', 'without', 'lack', 'failed', 'unable']
        doc_features['negative_sentiment'] = sum(1 for word in negative_words if word in doc.lower())
        
        features.append(doc_features)
    
    return pd.DataFrame(features)



def calculate_risk_score(text, risk_keywords=ALL_RISK_KEYWORDS):
    """Calculate risk score based on keyword presence"""
    text_lower = text.lower()
    risk_count = sum(1 for keyword in risk_keywords if keyword in text_lower)
    total_words = len(text_lower.split())
    
    if total_words == 0:
        return 0
    
    risk_score = (risk_count / total_words) * 100
    return risk_score



