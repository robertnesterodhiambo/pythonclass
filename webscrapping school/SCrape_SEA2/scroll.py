from playwright.sync_api import sync_playwright

def enter_text_submit_and_extract():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for silent execution
        page = browser.new_page()

        # Open the website
        page.goto("https://seaweb.seacoglobal.com/sap/bc/ui5_ui5/sap/zseaco_ue17/index.html",timeout=60000)

        # Wait for and enter text in the input field
        page.wait_for_selector("#idTAUnitNo", timeout=10000)
        page.locator("#idTAUnitNo").fill("segu7300009")

        # Click submit button
        page.wait_for_selector("#idBtnUnitEnqSubmit", timeout=10000)
        page.locator("#idBtnUnitEnqSubmit").click()

        # Wait for the table and scrollbar to appear
        page.wait_for_selector("#idUnitStatusPanel-table", timeout=15000)
        page.wait_for_selector("#idUnitStatusPanel-vsb", timeout=15000)

        # Scroll the scrollbar **UP** to reveal hidden content
        page.evaluate("""
            (async function() {
                let scrollDiv = document.querySelector("#idUnitStatusPanel-vsb");
                if (!scrollDiv) return;
                
                let lastScroll = -1;
                while (scrollDiv.scrollTop !== lastScroll) {
                    lastScroll = scrollDiv.scrollTop;
                    scrollDiv.scrollBy(0, -200);  // Scroll UP by 200 pixels
                    await new Promise(r => setTimeout(r, 500)); // Wait for content to load
                }
            })();
        """)

        # Wait for scrolling to complete
        page.wait_for_timeout(3000)

        # Extract all table rows (including newly revealed ones)
        table_data = page.evaluate("""
            () => {
                return Array.from(document.querySelectorAll("#idUnitStatusPanel-table tr"))
                    .map(row => row.innerText);
            }
        """)

        # Print the extracted data
        print("\n".join(table_data))

        # Wait to observe results
        page.wait_for_timeout(5000)

        # Close browser
        browser.close()

# Run the function
enter_text_submit_and_extract()
