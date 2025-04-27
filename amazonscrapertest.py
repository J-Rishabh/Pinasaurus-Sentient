from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import getpass
import time

# --- Prompt for login ---
email = ""
password = ""


# ----------- STEP 2: Setup Chrome with stealth -----------
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
)

# ----------- STEP 3: Go to login page -----------
driver.get("https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fref%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")

# Optional manual check for captchas
input("If you see a CAPTCHA or verification page, solve it manually, then press Enter...")

wait = WebDriverWait(driver, 15)

try:
    email_input = wait.until(EC.presence_of_element_located((By.ID, "ap_email")))
    email_input.send_keys(email)
    email_input.send_keys(Keys.ENTER)
except Exception as e:
    print("Failed to find email input.")
    driver.quit()
    raise

# ----------- STEP 4: Enter password -----------
try:
    password_input = wait.until(EC.presence_of_element_located((By.ID, "ap_password")))
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)
except Exception as e:
    print("Failed to find password input.")
    driver.quit()
    raise

# ----------- STEP 5: Go to product page -----------
product_url = "https://www.amazon.com/dp/B08N5WRWNW"  # replace with any ASIN or product URL
driver.get(product_url)

# Wait for potential SiteStripe iframe to load
time.sleep(5)

# ----------- STEP 6: Extract SiteStripe Link -----------
try:
    # Switch to SiteStripe iframe
    iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src*='assoc-amazon.com']")
    driver.switch_to.frame(iframe)

    # Find the affiliate link input field
    link_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
    affiliate_link = link_element.get_attribute("value")

    print("\n🎯 Your SiteStripe Affiliate Link:")
    print(affiliate_link)

except Exception as e:
    print("\n⚠️ Could not find the SiteStripe. Make sure you're logged into an Amazon Associates account.")
    print("Error:", e)

# ----------- STEP 7: Close browser when ready -----------
input("\nPress Enter to close browser...")
driver.quit()
