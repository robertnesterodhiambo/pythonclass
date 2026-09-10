from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.ke.sportpesa.com/en/mega-jackpot-pro/results")

    # Manually interact with the page
    input("Interact with the website, then press ENTER here...")

    # Wait for the iframe
    iframe = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.ID, "multijackpot-iframe")
        )
    )

    # Switch Selenium's context into the iframe
    driver.switch_to.frame(iframe)

    print("Switched into iframe.")

    # Now search INSIDE the iframe
    link = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "div.simple-horizontal-carousel__container > a.simple-horizontal-carousel__btn"
        ))
    )

    print("Found link:")
    print(link.get_attribute("href"))

    # Scroll it into view
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        link
    )

    # Click it
    link.click()

    print("Link clicked.")
    print("Current URL:", driver.current_url)

    input("Press ENTER to close...")

finally:
    driver.quit()