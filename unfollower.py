from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

USERNAME = "username"
PASSWORD = "password"
BASE_URL = "https://instagram.com"   # keep this consistent (no www)

options = Options()

# options.add_argument("-headless")
driver = webdriver.Firefox(options=options)
driver.set_window_size(1366, 900)
wait = WebDriverWait(driver, 15)

# 1) Login
driver.get(BASE_URL)
username_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
password_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']")))
username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

# wait for app shell / nav to confirm login(This might not work for some accounts since it's relying on some warning box when you're login, you can do something like sleep(5) to ensure that you've successfuly logged in)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.x1lliihq")))

#Text file of usernames to unfollow
with open("accounts.txt", "r", encoding="utf-8") as f:
    liness=f.readlines()

for eachline in liness:
    USERNAME = eachline
    # 2) Go to profile (same origin — no www.)
    driver.get(f"{BASE_URL}/{USERNAME}/")

    main_tab = driver.current_window_handle

    # wait for profile header or something unique on profile(This element strangely doesn't appear at some profiles so I passed when exception occurs if time exceeds timeout time)
    try:
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, "h2.x1lliihq > span:nth-child(1)"
        )))
    except TimeoutException:
        pass

    # 3) Click the Following link robustly
    following = (By.CSS_SELECTOR, "button[class$=' _aswp _aswr _aswv _asw_ _asx2']")
    unfollow = (By.CSS_SELECTOR, "div.x1i10hfl:nth-child(8)")
    # wait for visibility & clickability by LOCATOR (not cached element)
    wait.until(EC.visibility_of_element_located(following))
    btn = wait.until(EC.element_to_be_clickable(following))

    # bring into view (some UIs need this) and click
    driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", btn)
    try:
        btn.click()
    except Exception:
        # last-resort fallback if overlapped/intercepted
        driver.execute_script("arguments[0].click();", btn)

    print("Opened the list dialog/link successfully.")

    wait.until(EC.visibility_of_element_located(unfollow))
    btn2=wait.until(EC.element_to_be_clickable(unfollow))
    # bring into view (some UIs need this) and click
    driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", btn)
    try:
        btn2.click()
    except Exception:
        # last-resort fallback if overlapped/intercepted
        driver.execute_script("arguments[0].click();", btn2)
    sleep(2) # I added this to avoid alerting Instagram's rate limiting.


