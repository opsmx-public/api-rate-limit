import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
driver = webdriver.Chrome()

# Step 1: Navigate to the SAML login URL
login_url = "https://<GATE_URL>/saml2/authenticate/SSO"
driver.get(login_url)

# Step 2: Wait for the login form and enter credentials
try:
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    password_field = driver.find_element(By.NAME, "password")

    # Fill out username and password
    username_field.send_keys("<USERMAIL-ID>")  # Replace with your username
    password_field.send_keys("<PASSWORD>")  # Replace with your password
    password_field.send_keys(Keys.RETURN)

    # Step 3: Wait for the redirection or target page
    WebDriverWait(driver, 10).until(EC.url_changes(login_url))
    print("Logged in successfully!")
    print("Current URL after login: ", driver.current_url)

except Exception as e:
    print("Login failed:", e)
    driver.quit()
    exit(1)

# Step 4: Get cookies from Selenium and convert to a dictionary
cookies = driver.get_cookies()
cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}


# Step 5: Make a GET request to the credentials page with cookies and headers
credentials_url = "https://<GATE_URL>gate/credentials"
response = requests.get(credentials_url, cookies=cookie_dict)

# Step 6: Check if the response is successful and parse it
if response.status_code == 200:
    print("Successfully fetched the accounts page!")
    # Assuming the accounts are in the HTML content
    # Replace with actual logic to extract account info
    print(response.text)  # For demonstration, printing raw HTML
else:
    print(f"Failed to fetch the accounts. Status code: {response.status_code}")

# Step 7: Keep the browser open for inspection if needed
print("Waiting for 5 minutes to inspect the page...")
time.sleep(300)  # Wait for 5 minutes for manual inspection

# Close the browser after the inspection
driver.quit()
