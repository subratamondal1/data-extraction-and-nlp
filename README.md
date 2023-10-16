# 📚 Data Extraction and NLP
Everything is completed, for detailed solution checkout the [**`Data_Extraction_and_NLP.ipynb`**](https://github.com/subratamondal1/data-extraction-and-nlp/blob/main/Data_Extraction_and_NLP.ipynb) notebook. 
# 🛠️ Tools Used
- [**Python**](https://www.python.org/): @3.11.5
- [**Poetry**](https://python-poetry.org/): for packaging and dependency management.
- [**NLTK**](https://www.nltk.org/index.html): Natural Language Toolkit.

# ⚙️ Reproducible
To make it run on your local machine you need to first install `poetry`.

**Install poetry for MACOSX/LINUX**

```bash
1. curl -sSL https://install.python-poetry.org | python3 -
```
**Clone this repo**

```bash
2. git clone git@github.com:subratamondal1/data-extraction-and-nlp.git
```

**Move inside the folder**

```bash
3. cd data-extraction-and-nlp
```

**Install the required dependencies**
```bash
4. poetry install
```
**Run the .py scripts in the following order from the folder `data-extraction-and-nlp/data-extraction-and-nlp`**
```bash
5.1. poetry run python3 article_extractor.py 
```
this will create a folder `extracted_articles` where all the extracted files will be generated with the name of the `URL_ID.txt`, conatining a **Title** and **Text**.

```bash
5.2. poetry run python3 custom_inputs.py
5.3. poetry run python3 nlp.py
```
**Result**

`output.xlsx` file will be generated inside `outputs/` folder.
