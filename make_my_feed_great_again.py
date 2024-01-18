import argparse
import chromedriver_autoinstaller

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from getpass import getpass
from selenium.webdriver.chrome.options import Options
from loguru import logger

def login_to_twitter(driver, username, password):
    driver.get('https://twitter.com/i/flow/login')
    wait = WebDriverWait(driver, 10)
    logger.info("Getting username field...")
    username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete=username]')))
    logger.info("Typing username...")
    username_field.send_keys(username)

    logger.info("Clicking on login button...")
    login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role=button].r-13qz1uu')))
    login_button.click()

    try:
        logger.info("Checking if extra input field for Twitter handle is there...")
        WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid=ocfEnterTextTextInput]')))
        input_field = driver.find_element(By.CSS_SELECTOR, '[data-testid=ocfEnterTextTextInput]')
        logger.info("Found it!")
        input_field.click()
        logger.info("Typing Twitter handle again...")
        input_field.send_keys(username)

        logger.info("Clicking on the next button...")
        next_button = driver.find_element(By.XPATH, '//span[text()="Next"]')
        next_button.click()
    except TimeoutException:
        logger.info("Not found... No need to input Twitter handle again.")

    logger.info("Typing password...")
    password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[type=password]')))
    password_field.send_keys(password)

    logger.info("Clicking on login button...")
    login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid*=Login_Button]')))
    login_button.click()

def get_bot_usernames(driver):
    logger.info("Opening notifications tab...")
    wait = WebDriverWait(driver, 10)
    notifications_tab = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid=AppTabBar_Notifications_Link]')))
    notifications_tab.click()

    notifications = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid=notification]')))

    logger.info("Checking if we have bots usernames...")
    bot_usernames = set()
    for notification in notifications:
        a_elements = notification.find_elements(By.TAG_NAME, 'a')
        for a in a_elements:
            href = a.get_attribute('href')
            if href and href.startswith('https://twitter.com/'):
                twitter_handle = href.split('/')[-1]
                if twitter_handle[-5:].isdigit():
                    bot_usernames.add(twitter_handle)
    return bot_usernames

def block_bots(driver, bot_usernames):
    if len(bot_usernames) == 0:
        logger.info("No bots to block!")
    else:
        logger.info("Starting blocking automation...")
        for username in bot_usernames:
            logger.info(f"Blocking pesky bot named {username}.")
            logger.info(f"Opening {username}'s profile")
            driver.get(f'https://twitter.com/{username}')

            logger.info("Opening user actions...")
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid=userActions]')))
            user_actions_button = driver.find_element(By.CSS_SELECTOR, '[data-testid=userActions]')
            user_actions_button.click()

            logger.info("Clicking on block button...")
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid=block]')))
            block_button = driver.find_element(By.CSS_SELECTOR, '[data-testid=block]')
            block_button.click()

            logger.info("Clicking on confirm button...")
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid=confirmationSheetConfirm]')))
            confirm_block_button = driver.find_element(By.CSS_SELECTOR, '[data-testid=confirmationSheetConfirm]')
            confirm_block_button.click()
            logger.info(f"Pesky {username} is now blocked! Aaaahhhh! So refreshing, right? :D")

def main():
    chromedriver_autoinstaller.install()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

    parser = argparse.ArgumentParser(description='Twitter bot blocker - IMPORTANT! Current criterium to define a bot is: Twitter handle ends with 5 digits (sorry for the false positives but we had to start somewhere)')
    parser.add_argument('--auto', action='store_true', help='Run in automatic mode, using credentials stored in the script')
    parser.add_argument('--username', type=str, help='Twitter username')
    parser.add_argument('--password', type=str, help='Twitter password')
    args = parser.parse_args()

    try:
        if args.auto:
            # Enter here your credentials if you want to run the script in auto mode
            username = "a_username"
            password = "a_password"
        elif args.username and args.password:
            username = args.username
            password = args.password
        else:
            username = input("Please enter your Twitter handle: ")
            password = getpass("Please enter your Twitter password: ")

        driver = webdriver.Chrome(options=chrome_options)
        login_to_twitter(driver, username, password)
        bot_usernames = get_bot_usernames(driver)
        block_bots(driver, bot_usernames)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
