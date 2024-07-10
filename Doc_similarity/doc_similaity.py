"SE&IR Project "


import os
import re
import math
import time
start = time.time()


def create_tokens(file_content):
    dummy_text = file_content
    start = dummy_text.find('<TITLE>') + len("<TITLE>")
    end = dummy_text.find("</TITLE>")
    start_txt = dummy_text.find("<TEXT>") + len("<TEXT>")
    end_txt = dummy_text.find("</TEXT>")
    text = (dummy_text[start:end].lower()) + " " + (dummy_text[start_txt:end_txt].lower()).strip()
    return tokenize_text(text)

def tokenize_text(text):
    tokens = re.findall(r'\w+', text)
    return tokens

def tf_freq(tokens):
    tf_dict = {}
    total_tokens = len(tokens)

    for token in tokens:
        if token not in tf_dict:
            tf_dict[token] = 1
        else:
            tf_dict[token] += 1

    for key in tf_dict:
        tf_dict[key] /= total_tokens
    return tf_dict


df_freq = {}
def df_func(token_list):
    global df_freq
    for token in set(token_list):
        if token not in df_freq:
            df_freq[token] = 1
        else:
            df_freq[token] += 1
    return df_freq

def tf_idf_vec_cosine_vec(doc_tf_dict, idf_token_values):
    tf_idf_Vector = {}
    cosine_normalized_Vec = {}

    for doc_id, tokens in doc_tf_dict.items():
        tf_idf_Vector[doc_id] = {}
        cosine_normalized_Vec[doc_id] = {}
        
        sum_squares = sum((value * idf_token_values.get(token, 0)) ** 2 for token, value in tokens.items())
        sqrtsum = sum_squares ** 0.5
        
        for token, value in tokens.items():
            idf_value = idf_token_values.get(token, 0)
            tf_idf_Vector[doc_id][token] = value * idf_value
            cosine_normalized_Vec[doc_id][token] = value * idf_value / sqrtsum
            
    return tf_idf_Vector, cosine_normalized_Vec

def similarity(vec1, vec2):
    dot_prod = 0

    for token in vec1:
        if token in vec2:
            dot_prod += vec1[token] * vec2[token]
    return dot_prod


DOCNO_dict = {}
def DOCnum_dict(folder_files):
    global DOCNO_dict
    for i in range(len(folder_files)):
       DOCNO_dict[folder_files[i]] = i + 1

def get_id(vec1):
    for i in DOCNO_dict:
        if DOCNO_dict[i] == 1:
            return i
        
def doc_similarity_score(cosine_normalized_Vec):
    doc_similar_dict = []
    for doc_id1, vec1 in cosine_normalized_Vec.items():
        for doc_id2, vec2 in cosine_normalized_Vec.items():
            if doc_id1 != doc_id2:
                similarity_score = similarity(vec1, vec2)
                id1 = get_id(doc_id1)
                id2 = get_id(doc_id2)
                
                doc_similar_dict.append((doc_id1, doc_id2, similarity_score))
    return sorted(doc_similar_dict, key=lambda x: x[2], reverse=True)


def main():
    
    folder_path = input("Enter the directory path: ")

    folder_files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    DOCnum_dict(folder_files)

    folder_files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    doc_tf_dict = {}
    doc_id = {}
    for file_name in folder_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "r") as file:
            file_content = file.read()
            token_list = create_tokens(file_content)
            tf_freq_dict = tf_freq(token_list)
            df_func(token_list)
            doc_tf_dict[file_name] = tf_freq_dict

    def get_idf_token_values(df_freq):
        idf_token_values = {}
        total_documents = len(folder_files)

        for token, df in df_freq.items():
            idf_token_values[token] = math.log(total_documents / df)
        return idf_token_values    
    idf_token_values = get_idf_token_values(df_freq)
    tf_idf_Vector, cosine_normalized_Vec = tf_idf_vec_cosine_vec(doc_tf_dict, idf_token_values)
    doc_similarities = doc_similarity_score(cosine_normalized_Vec)

    print(doc_similarities[:50])

if __name__ == "__main__":
    main()
print("total time", time.time() - start)


