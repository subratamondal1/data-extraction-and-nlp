from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup

# define the path
input_file_path = Path("./data/Input.xlsx")
output_file_path = Path("./data/Output Data Structure.xlsx")

# create pandas dataframe
input_df = pd.read_excel(io=input_file_path)
output_df = pd.read_excel(io=output_file_path)

# create a directory to save the extracted articles
output_dir = Path("extracted_articles")
output_dir.mkdir(parents=True, exist_ok=True)

# create a file_name column, will help to populate the output_df
output_df['file_name'] = output_df['URL_ID'].apply(lambda x: str(float(x)) + '.txt')
output_df.index = output_df['file_name'] # for easier access while filling it with new values

def extract_and_save_article(df:pd.DataFrame, title_tag:str, text_tag:str, output_dir: Path):
  processed_url_ids = []
  # Iterate through each row in the input dataframe
  for index, row in df.iterrows():
      # Get the URL and URL_ID from the dataframe
      url = row['URL']
      url_id = row['URL_ID']

      # Check if the file with the same URL_ID already exists
      file_name = f"{url_id}.txt"
      output_file = output_dir / file_name
      if output_file.exists():
          print(f"Skipped as the file: '{file_name}' already exists at {output_file}")
          continue

      # Send an HTTP GET request to fetch the webpage content
      response = requests.get(url)

      if response.status_code == 200:
          # Parse the HTML content using BeautifulSoup
          soup = BeautifulSoup(response.text, 'html.parser')

          # Extract the article title and text
          title_element = soup.find('h1', title_tag)
          if title_element:
            title = title_element.text
          else:
            title = None
            print("Title not found, hence skipped", url_id, url)
            continue

          text_elements = soup.find_all(class_= text_tag)
          if text_elements:
            article_text = "\n".join([p.text for p in text_elements])
          else:
            article_text = None
            print("Text not found, hence skipped", url_id, url)

          if (title is not None) and (article_text is not None):
            # Save the extracted article to a text file with URL_ID as its name
            with output_file.open('w', encoding='utf-8') as file:
                file.write(title + "\n\n" + article_text)
                # To track which url_ids have been used to create the file
                processed_url_ids.append(url)


            print(f"Article from URL_ID {url_id} extracted and saved to {output_file}")
      else:
        # Save the extracted article to a text file with URL_ID as its name
        with output_file.open('w', encoding='utf-8') as file:
            file.write("NA" + "\n\n" + "NA")
            # To track which url_ids have been used to create the file
            processed_url_ids.append(url)
        print(f"Failed to fetch the URL for URL_ID {url_id}")

  print("Extraction completed.")
  return processed_url_ids

# Extracting Articles
processed_url_ids1 = extract_and_save_article(
    df = output_df,
    title_tag = "entry-title",
    text_tag = "td-post-content tagdiv-type",
    output_dir = output_dir
    )

# Extracting Articles with different tags
processed_url_ids2 = extract_and_save_article(
    df = output_df,
    title_tag = "tdb-title-text",
    text_tag = "tdb-block-inner td-fix-index",
    output_dir = output_dir
    )

# extracted articles list
extracted_files = list(output_dir.glob("*"))
print(f"Total Extracted Files: {len(extracted_files)}")

print(output_df)