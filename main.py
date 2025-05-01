from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time

# ---------- CONFIG ----------
URL = "https://txaustinweb.myvscloud.com/webtrac/web/search.html?display=detail&module=GR&secondarycode=3"
SLOT_TEXT_KEYWORD = "Open"
MIN_SLOTS = 4
HEADLESS = False  # Change to True to run in headless mode

# ---------- SETUP ----------
def get_upcoming_saturday():
    today = datetime.today()
    days_ahead = 5 - today.weekday()  # Saturday is 5 (Mon=0)
    if days_ahead < 0:
        days_ahead += 7
    return today + timedelta(days=days_ahead)

def setup_driver():
    options = Options()
    if HEADLESS:
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver

# ---------- MAIN ----------
def book_earliest_tee_time():
    driver = setup_driver()
    driver.get(URL)
    time.sleep(5)  # Wait for page to load fully

    # Scroll if needed
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    saturday = get_upcoming_saturday()
    saturday_str = saturday.strftime("%m/%d/%Y")
    
    driver.execute_script("""
        const input = document.getElementById('begindate');
        input.value = arguments[0];
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
    """, saturday_str)

    print("Updated search date:", driver.execute_script("return document.getElementById('begindate').value"))

    # Click the Search button to update the results
    # Then click the search button to reload results
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "grwebsearch_buttonsearch"))
    )
    search_button.click()

    # Wait for new table rows to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#grwebsearch_output_table tbody tr"))
    )
    print(f"Saturday date chosen: {saturday}. Saturdaystr = {saturday_str}")

    #tee_times = driver.find_elements(By.CSS_SELECTOR, ".detailListRow")  # May vary based on DOM

###############
    WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#grwebsearch_output_table tbody tr"))
)

    rows = driver.find_elements(By.CSS_SELECTOR, "#grwebsearch_output_table tbody tr")

    # Build a list of (parsed_time, add_to_cart_button) tuples
    tee_times = []

    for row in rows:
        try:
            time_cell = row.find_element(By.CSS_SELECTOR, 'td[data-title="Time"]')
            time_str = time_cell.text.strip()

            # Parse time, e.g. "6:20 pm" => datetime object
            tee_time = datetime.strptime(time_str, "%I:%M %p")

            # Find the "Add to Cart" link in the same row
            add_to_cart_button = row.find_element(By.CSS_SELECTOR, 'a.cart-button')
            tee_times.append((tee_time, add_to_cart_button))
        except Exception as e:
            print(f"Skipping row due to error: {e}")
            continue

    # Sort by earliest time and click the first one
    if tee_times:
        tee_times.sort(key=lambda x: x[0])
        earliest_time, button = tee_times[0]
        print(f"Selecting earliest tee time: {earliest_time.strftime('%I:%M %p')}")
        button.click()
        print(f"Add to cart button clicked!")

                # Wait for redirect to form page
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "processingprompts_dailyfirstname")))

        # Fill in the form details
        driver.find_element(By.NAME, "processingprompts_dailyfirstname").send_keys("Steven")
        driver.find_element(By.NAME, "processingprompts_dailylastname").send_keys("Riley")
        driver.find_element(By.NAME, "processingprompts_dailyphone").send_keys("5016801312")
        driver.find_element(By.NAME, "processingprompts_dailyemail").send_keys("rileystevend@gmail.com")

        # --- Step 3: Click the "Continue" button ---
        continue_button = driver.find_element(By.ID, "processingprompts_buttononeclicktofinish")
        continue_button.click()

        # --- Step 4: Wait for the "Proceed To Checkout" button to be clickable ---
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "webcart_buttoncheckout"))
        )

        # --- Step 5: Click the checkout button ---
        checkout_button = driver.find_element(By.ID, "webcart_buttoncheckout")
        checkout_button.click()

        # --- Step 6: Wait for the checkout form to appear ---
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "webcheckout_buttoncontinue"))
        )

       # --- Step 7: Fill in the form fields (clear first) ---
        driver.find_element(By.NAME, "webcheckout_billfirstname").clear()
        driver.find_element(By.NAME, "webcheckout_billfirstname").send_keys("Steven")

        driver.find_element(By.NAME, "webcheckout_billlastname").clear()
        driver.find_element(By.NAME, "webcheckout_billlastname").send_keys("Riley")

        driver.find_element(By.NAME, "webcheckout_billaddress1").clear()
        driver.find_element(By.NAME, "webcheckout_billaddress1").send_keys("4802 PLUM PEACH BND")

        driver.find_element(By.NAME, "webcheckout_billcity").clear()
        driver.find_element(By.NAME, "webcheckout_billcity").send_keys("AUSTIN")

        driver.find_element(By.NAME, "webcheckout_billstate").clear()
        driver.find_element(By.NAME, "webcheckout_billstate").send_keys("Texas")

        driver.find_element(By.NAME, "webcheckout_billzip").clear()
        driver.find_element(By.NAME, "webcheckout_billzip").send_keys("78723")

        driver.find_element(By.NAME, "webcheckout_billphone").clear()
        driver.find_element(By.NAME, "webcheckout_billphone").send_keys("(501)680-1312")

        driver.find_element(By.NAME, "webcheckout_billemail").clear()
        driver.find_element(By.NAME, "webcheckout_billemail").send_keys("rileystevend@gmail.com")

        driver.find_element(By.NAME, "webcheckout_billemail_2").clear()
        driver.find_element(By.NAME, "webcheckout_billemail_2").send_keys("rileystevend@gmail.com")

        # --- Step 8: Click the final Continue button ---
        driver.find_element(By.ID, "webcheckout_buttoncontinue").click()
        print(f"We have clicked submit final!")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "webconfirmation_emailtext"))
        )
        print(f"We've reached the Confirmation page!")
    else:
        print("No valid tee times found.")

#########
    #print(f"teetimelist: {tee_times}")
 #   earliest_time = None
 #   booking_button = None
#
 #   for row in tee_times:
  #      try:
   #         text = row.text
    #        if saturday_str in text and SLOT_TEXT_KEYWORD in text:
     #           available = int([s for s in text.split() if s.isdigit()][-1])
     #           if available >= MIN_SLOTS:
      #              # Save this as the earliest time
      #              earliest_time = text
      #              booking_button = row.find_element(By.CSS_SELECTOR, "input[type='submit']")
      #              print(f"Available:{available}; booking_button: {booking_button}; earliest_time= {earliest_time}")
      #              break
      #  except Exception as e:
       #     print(f"Error reading row: {e}")
       #     continue
    #print(f"Earliest tee time: {earliest_time}")
    #if booking_button:
     #   print(f"Booking earliest tee time on Saturday: {earliest_time}")
      #  booking_button.click()
       # time.sleep(5)
        # You may need to click a 'confirm' button or fill out info next
        # Add that logic here as needed
        # Add selected tee time to cart (assumes you have a reference to the right button)
       # add_to_cart_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Add to Cart')]")
       # add_to_cart_button.click()

        # Wait for redirect to form page
       # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName")))

        # Fill in the form details
       # driver.find_element(By.NAME, "firstName").send_keys("Steven")
       # driver.find_element(By.NAME, "lastName").send_keys("Riley")
       # driver.find_element(By.NAME, "phone").send_keys("5016801312")
       # driver.find_element(By.NAME, "email").send_keys("rileystevend@gmail.com")
    #else:
     #   print("No suitable tee times found.")

    #driver.quit()

if __name__ == "__main__":
    book_earliest_tee_time()