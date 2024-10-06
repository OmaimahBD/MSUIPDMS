import json
import logging
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import numpy as np
from pypdf import PdfReader
from core.models import IPSimilarityScore, IntellectualProperty


nltk.download('punkt')
nltk.download('stopwords')


def parse_doc_text(pdf_file_path):
    reader = PdfReader(pdf_file_path)
    page_texts = ''
    for page in reader.pages:
        page_texts += page.extract_text()
    return page_texts


def preprocess_doc_tokens(pdf_file_path):
    texts = parse_doc_text(pdf_file_path)
    texts = texts.lower()
    
    # Remove punctuation
    texts = texts.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize
    tokens = word_tokenize(texts)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    return tokens


def json_tokens_to_list(json_str):
    if json_str:
        try:
            return json.loads(json_str)
        except Exception as err:
            logging.error(err, exc_info=True)
    return []


def calc_doc_similarity(doc_source):
    other_docs = IntellectualProperty.objects.filter(is_approved=True).exclude(pk=doc_source.pk,is_approved=False)
    doc_source_tokens = json_tokens_to_list(doc_source.doc_text_tokens)
    
    highest_score = 0
    highest_score_target = None
    
    if doc_source_tokens:
        for doc_target in other_docs:
            doc_target_tokens = json_tokens_to_list(doc_target.doc_text_tokens)
            score = -1
            remarks = ''
            if doc_target_tokens:
                score = cosine_similarity_nltk(doc_source_tokens, doc_target_tokens)
                if score > highest_score:
                    highest_score = score
                    highest_score_target = doc_target
            else:
                remarks = f'Target document with pk [{doc_target.pk}] has no tokens'
                
            IPSimilarityScore.objects.create(
                doc_source=doc_source,
                doc_target=doc_target,
                score=score,
                remarks=remarks
            )
        
        if highest_score_target:
            logging.info(f'Highest similarity score: {highest_score} with document pk: {highest_score_target.pk}')
    else:
        logging.error(f'Source document with pk [{doc_source.pk}] has no tokens')
    
    return highest_score, highest_score_target


def cosine_similarity_nltk(doc_source_tokens, doc_target_tokens):
    """
    Compute cosine similarity between two texts using NLTK for preprocessing.

    Parameters:
    text1 (str): First text.
    text2 (str): Second text.

    Returns:
    float: Cosine similarity between text1 and text2.
    """
    # Create set of unique tokens
    unique_tokens = set(doc_source_tokens).union(set(doc_target_tokens))
    
    # Create vectors
    vector1 = [doc_source_tokens.count(token) for token in unique_tokens]
    vector2 = [doc_target_tokens.count(token) for token in unique_tokens]
    
    # Compute cosine similarity
    dot_product = np.dot(vector1, vector2)
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    similarity = dot_product / (norm1 * norm2)
    
    return similarity
