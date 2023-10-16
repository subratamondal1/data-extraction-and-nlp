from pathlib import Path
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import cmudict
import string
from article_extractor import extracted_files, output_df
from custom_inputs import custom_stopwords, positive_words, negative_words

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('cmudict')
cumdict = cmudict.dict()

articles = extracted_files

for article_file in articles:
  with open(file = article_file, mode = 'r') as f:
    article = f.read()
    result_dict = {}
    url_id = str(article_file).split("/")[-1]

    # Tokenize the text
    tokens = word_tokenize(article)
    tokens = [token.lower() for token in tokens]

    english_stop_words = set(stopwords.words('english'))
    english_stop_words = set(word.lower() for word in english_stop_words)

    # Define a set of punctuation characters to remove
    punctuation = set(string.punctuation)
    punctuation = set(word.lower() for word in punctuation)

    # Clean the tokens by removing stop words
    filtered_tokens = list()
    for word in tokens:
        if (word not in english_stop_words) and (word not in custom_stopwords) and (word not in punctuation):
            filtered_tokens.append(word)

    # Positive and Negative Score
    positive_score = 0
    negative_score = 0

    # Calculate the positive and negative scores
    for word in filtered_tokens:
        if word in positive_words:
            positive_score += 1
        if word in negative_words:
            negative_score += 1
    output_df.loc[url_id,"POSITIVE SCORE"] = positive_score
    output_df.loc[url_id,"NEGATIVE SCORE"] = negative_score

    # Sentiment, Polarity and Subjectivity score
    polarity_score = (positive_score - negative_score) / (positive_score + negative_score + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(filtered_tokens) + 0.000001)

    output_df.loc[url_id,"POLARITY SCORE"] = polarity_score
    output_df.loc[url_id,"SUBJECTIVITY SCORE"] = subjectivity_score

    # Determine the sentiment
    if polarity_score > 0:
        sentiment = "Positive"
    elif polarity_score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    ### Average Sentence Length
    sentences = nltk.sent_tokenize(article)
    words = filtered_tokens
    average_sentence_length = len(words) / len(sentences)

    output_df.loc[url_id,"AVG SENTENCE LENGTH"] = average_sentence_length

    ### Percentage of Complex Words
    def syllable_count(word):
        if word.lower() in d:
            return max([len(list(y for y in x if y[-1].isdigit())) for x in cumdict[word.lower()]])
        else:
            return 0

    words = filtered_tokens
    complex_word_count = sum(1 for word in words if syllable_count(word) > 2)
    percentage_complex_words = (complex_word_count / len(words)) * 100

    output_df.loc[url_id,"PERCENTAGE OF COMPLEX WORDS"] = percentage_complex_words

    # Fog Index
    fog_index = 0.4 * (average_sentence_length + percentage_complex_words)

    output_df.loc[url_id,"FOG INDEX"] = fog_index

    # Average Number of Words Per Sentence
    average_words_per_sentence = len(words) / len(sentences)

    output_df.loc[url_id,"AVG NUMBER OF WORDS PER SENTENCE"] = average_words_per_sentence

    # Complex Word Count
    complex_word_count = sum(1 for word in words if syllable_count(word) > 2)

    output_df.loc[url_id,"COMPLEX WORD COUNT"] = complex_word_count

    # Total Word Count
    total_word_count = len([
        word for word in words if word not in custom_stopwords and word not in english_stop_words and not all(char in string.punctuation for char in word)
        ])

    output_df.loc[url_id,"WORD COUNT"] = total_word_count

    # Syllable Count Per Word
    def count_syllables(word):
        exceptions = ["es", "ed"]
        for ending in exceptions:
            if word.endswith(ending):
                word = word[:-len(ending)]

        vowels = "aeiouAEIOU"
        syllable_count = sum(1 for char in word if char in vowels)
        return max(1, syllable_count)

    syllables_per_word = [count_syllables(word) for word in words]
    average_syllables_per_word = sum(syllables_per_word) / len(words)

    output_df.loc[url_id,"SYLLABLE PER WORD"] = average_syllables_per_word

    # Calculate personal pronoun count
    personal_pronouns = re.findall(
        pattern = pattern,
        string = article
        )
    personal_pronoun_count = len(personal_pronouns)

    output_df.loc[url_id,"PERSONAL PRONOUNS"] = personal_pronoun_count

    ### Average Word Length
    total_characters = sum(len(word) for word in words)
    average_word_length = total_characters / len(words)

    output_df.loc[url_id,"AVG WORD LENGTH"] = average_word_length

print("Process Completed...")
print(output_df)

outputs_path = Path("./outputs")
outputs_path.drop("file_name", axis=1, inplace=True)
print(outputs_path)
output_df.to_excel(outputs_path/"output.xlsx", index = False)