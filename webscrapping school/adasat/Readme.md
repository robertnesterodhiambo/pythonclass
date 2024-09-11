# Web Scraping Project: Adasat Online Store

This project involves web scraping the [Adasat Online Store](https://adasat.online/kw-en/product-list&types=&brand=&color=&collections=&replacement_list_id=&star_list_id=&sortby=4) using Selenium and GeckoDriver (Firefox WebDriver). The goal is to extract product information from the website and save it for further analysis.

## Project Structure

- **`scraper.py`**: The main Python script that handles web scraping using Selenium.
- **`requirements.txt`**: Lists all the Python dependencies required for the project.
- **`README.md`**: This file, providing an overview of the project.
- **`data/`**: Directory to store scraped data, e.g., in CSV format.

## Getting Started

### Prerequisites

1. **Python 3.x**: Ensure that you have Python installed. You can download it from [here](https://www.python.org/downloads/).
2. **GeckoDriver**: GeckoDriver is required to interface with the Firefox browser. You can download it from [here](https://github.com/mozilla/geckodriver/releases).

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/robertnesterodhiambo/pythonclass/tree/main/webscrapping%20school
   ```

2. Navigate to the project directory:

   ```bash
   cd webscrapping%20school
   ```

3. Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. Ensure GeckoDriver is accessible in your system's PATH, or provide the path to GeckoDriver in the script.

### Usage

1. Run the `scraper.py` script to start scraping:

   ```bash
   python scraper.py
   ```

2. The script will automatically open a Firefox browser window and navigate to the Adasat website to scrape product data. The data will be saved in the `data/` directory.

### Configuration

- **GeckoDriver Path**: If GeckoDriver is not in your system's PATH, you can specify its location in the `scraper.py` script by adding the following line:

   ```python
   driver = webdriver.Firefox(executable_path='/path/to/geckodriver')
   ```

- **Scroll to Bottom**: The script includes an option to scroll to the bottom of the page to load all elements before scraping. Ensure this feature is enabled in the script if required.

### Features

- Extract product names, prices, links, and other relevant details.
- Automatically scrolls the page to load all products.
- Saves the extracted data in a structured format (e.g., CSV or JSON).

### Troubleshooting

- **GeckoDriver Issues**: Ensure that GeckoDriver is correctly installed and accessible. Check the version compatibility with your Firefox browser.
- **Selenium Timeout**: If the page takes too long to load, consider increasing the wait times in the script.

### Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to discuss potential improvements or bugs.

### License

This project is licensed under the MIT License.

### Acknowledgments

- [Selenium Documentation](https://selenium.dev/documentation/)
- [GeckoDriver Documentation](https://firefox-source-docs.mozilla.org/testing/geckodriver/)


## How to run this script

Download  a gecko driver for the computer verion you own from [https://github.com/mozilla/geckodriver/releases]
 run scrape.py after its done run fill.py then run datacleaner.py finally run category.py 
 when done copy the lates created excel file into eye power  folder and run eye2.py then datacleaner.py
