from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# File made by @SOULCARCK
# This script uses Selenium WebDriver with a proxy to interact with YouTube or ad sites.
# It automates page visits to potentially increase video or ad views by simulating human-like delays.

CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'

PROXIES = [
    "",
    "",
 
    "",
    ""
]
# File made by @SOULCARCK
# This script uses Selenium WebDriver with a proxy to interact with YouTube or ad sites.
# It automates page visits to potentially increase video or ad views by simulating human-like delays.

BASE_USER_AGENTS = [

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X {mac_version}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{firefox_rv}.0) Gecko/20100101 Firefox/{firefox_version}.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:{firefox_rv}.0) Gecko/20100101 Firefox/{firefox_version}.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:{firefox_rv}.0) Gecko/20100101 Firefox/{firefox_version}.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/{webkit_version}.1.15 (KHTML, like Gecko) Version/{safari_version}.0 Safari/{webkit_version}.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X {mac_version}) AppleWebKit/{webkit_version}.1.15 (KHTML, like Gecko) Version/{safari_version}.0 Safari/{webkit_version}.1.15",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36 Edg/{edge_version}.0.{edge_build}.{edge_patch}",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36 Edg/{edge_version}.0.{edge_build}.{edge_patch}",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36 OPR/{opera_version}.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36 OPR/{opera_version}.0.0.0",

    "Mozilla/5.0 (Linux; Android {android_version}; {device_model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Mobile Safari/537.36",

    "Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version} like Mac OS X) AppleWebKit/{webkit_version}.1.15 (KHTML, like Gecko) Version/{safari_version}.0 Mobile/15E148 Safari/604.1",
]
# File made by @SOULCARCK
# This script uses Selenium WebDriver with a proxy to interact with YouTube or ad sites.
# It automates page visits to potentially increase video or ad views by simulating human-like delays.

CHROME_VERSIONS = list(range(110, 125))  
FIREFOX_VERSIONS = list(range(110, 125))  
SAFARI_VERSIONS = list(range(15, 18))     
WEBKIT_VERSIONS = list(range(605, 610))  
EDGE_VERSIONS = list(range(110, 125))     
OPERA_VERSIONS = list(range(95, 110))    
MAC_VERSIONS = ["10_15_7", "13_0", "13_1", "13_2", "13_3", "13_4", "13_5", "13_6", "14_0", "14_1", "14_2"]
ANDROID_VERSIONS = ["11", "12", "13", "14"]
IOS_VERSIONS = ["15_0", "15_1", "16_0", "16_1", "16_6", "17_0", "17_1"]
DEVICE_MODELS = ["SM-G998B", "SM-G975F", "SM-G973F", "Pixel 6", "Pixel 7", "OnePlus 9", "OnePlus 10"]

# Global tracking for used user agents
used_user_agents = set()
user_agent_lock = threading.Lock()

def generate_unique_user_agent():
    with user_agent_lock:
        max_attempts = 1000
        attempts = 0

        while attempts < max_attempts:

            template = random.choice(BASE_USER_AGENTS)

            user_agent = template.format(
                chrome_version=random.choice(CHROME_VERSIONS),
                firefox_version=random.choice(FIREFOX_VERSIONS),
                firefox_rv=random.choice(FIREFOX_VERSIONS),
                safari_version=random.choice(SAFARI_VERSIONS),
                webkit_version=random.choice(WEBKIT_VERSIONS),
                edge_version=random.choice(EDGE_VERSIONS),
                edge_build=random.randint(2000, 2999),
                edge_patch=random.randint(10, 99),
                opera_version=random.choice(OPERA_VERSIONS),
                mac_version=random.choice(MAC_VERSIONS),
                android_version=random.choice(ANDROID_VERSIONS),
                ios_version=random.choice(IOS_VERSIONS),
                device_model=random.choice(DEVICE_MODELS)
            )


            if "Chrome" in user_agent and "Safari" in user_agent:

                chrome_version = random.choice(CHROME_VERSIONS)
                minor_version = random.randint(0, 9999)
                patch_version = random.randint(0, 999)
                user_agent = user_agent.replace(f"Chrome/{chrome_version}.0.0.0",
                                              f"Chrome/{chrome_version}.0.{minor_version}.{patch_version}")


            if user_agent not in used_user_agents:
                used_user_agents.add(user_agent)
                print(f"Generated unique user agent #{len(used_user_agents)}: {user_agent[:80]}...")
                return user_agent

            attempts += 1


        timestamp = int(time.time() * 1000)
        unique_user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(CHROME_VERSIONS)}.0.{timestamp % 10000}.{timestamp % 1000} Safari/537.36"
        used_user_agents.add(unique_user_agent)
        print(f"Generated timestamp-based unique user agent #{len(used_user_agents)}: {unique_user_agent[:80]}...")
        return unique_user_agent

def get_random_proxy():
    return random.choice(PROXIES)

def human_like_delay():
    return random.uniform(1.5, 4.5)

def random_mouse_movement(driver):

    try:
        action = ActionChains(driver)
        # Random mouse movements
        for _ in range(random.randint(2, 5)):
            x_offset = random.randint(-100, 100)
            y_offset = random.randint(-100, 100)
            action.move_by_offset(x_offset, y_offset)
            action.pause(random.uniform(0.5, 1.5))
        action.perform()
    except:
        pass

def simulate_human_behavior(driver):

    try:
        # Random scroll behavior
        scroll_actions = [
            "window.scrollTo(0, Math.floor(Math.random() * 500));",
            "window.scrollTo(0, Math.floor(Math.random() * 1000));",
            "window.scrollTo(0, document.body.scrollHeight/4);",
            "window.scrollTo(0, document.body.scrollHeight/2);",
        ]

        for _ in range(random.randint(2, 4)):
            time.sleep(human_like_delay())
            driver.execute_script(random.choice(scroll_actions))
            time.sleep(human_like_delay())

        random_mouse_movement(driver)

        time.sleep(random.uniform(3, 8))

        try:

            clickable_elements = driver.find_elements(By.TAG_NAME, "a")[:5]
            if clickable_elements:
                element = random.choice(clickable_elements)
                if element.is_displayed() and element.is_enabled():
                    ActionChains(driver).move_to_element(element).pause(1).perform()
        except:
            pass

    except Exception as e:
        print(f"Error in human behavior simulation: {e}")

def create_driver_with_proxy():
    proxy = get_random_proxy()
    ip, port, user, password = proxy.split(":")
    user_agent = generate_unique_user_agent()

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-logging')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(f"user-agent={user_agent}")

    window_sizes = [
        "--window-size=1920,1080",
        "--window-size=1366,768",
        "--window-size=1440,900",
        "--window-size=1536,864",
        "--window-size=1600,900",
        "--window-size=1280,720",
        "--window-size=1680,1050"
    ]
    options.add_argument(random.choice(window_sizes))

    seleniumwire_options = {
        'proxy': {
            'http': f"http://{user}:{password}@{ip}:{port}",
            'https': f"https://{user}:{password}@{ip}:{port}",
            'no_proxy': 'localhost,127.0.0.1'
        }
    }

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options, seleniumwire_options=seleniumwire_options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver, user_agent

def run_single_instance(instance_id):
    """Run a single browser instance with human-like behavior"""
    driver = None
    try:
        print(f"Starting instance {instance_id}")
        driver, user_agent = create_driver_with_proxy()

        browser_info = "Unknown"
        if "Chrome" in user_agent and "Edg" in user_agent:
            browser_info = "Edge"
        elif "Chrome" in user_agent and "OPR" in user_agent:
            browser_info = "Opera"
        elif "Chrome" in user_agent and "Vivaldi" in user_agent:
            browser_info = "Vivaldi"
        elif "Chrome" in user_agent and "Brave" in user_agent:
            browser_info = "Brave"
        elif "Chrome" in user_agent:
            browser_info = "Chrome"
        elif "Firefox" in user_agent:
            browser_info = "Firefox"
        elif "Safari" in user_agent and "Chrome" not in user_agent:
            browser_info = "Safari"

        print(f"Instance {instance_id} using {browser_info}")
        print(f"Instance {instance_id} User-Agent: {user_agent}")

        time.sleep(random.uniform(2, 5))

        driver.get("https://youtube.com/shorts/Q0B5GhragnI?si=y4FJP9ArtdUGK56y")
        print(f"Instance {instance_id} loaded binclub.io successfully")

        time.sleep(human_like_delay())

        simulate_human_behavior(driver)

        stay_time = random.uniform(30, 90)
        print(f"Instance {instance_id} staying for {stay_time:.1f} seconds")
        time.sleep(stay_time)

        print(f"Instance {instance_id} completed")
        return f"Instance {instance_id} completed successfully"

    except Exception as e:
        print(f"Instance {instance_id} failed: {str(e)}")
        return f"Instance {instance_id} failed: {str(e)}"
    finally:
        if driver:
            try:
                driver.quit()
                print(f"Instance {instance_id} driver closed")
            except:
                pass

def run_batch_of_5():

    print("Starting batch of 5 instances... by @SOULCRACK")

    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit 5 tasks
        futures = [executor.submit(run_single_instance, i+1) for i in range(5)]

        # Wait for all tasks to complete
        for future in as_completed(futures):
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"Task failed with exception: {e}")

    print("Batch of 5 instances completed")

def main():
    batch_number = 1

    try:
        while True:
            print(f"\n{'='*50}")
            print(f"Starting Batch #{batch_number}")
            print(f"Total unique user agents used so far: {len(used_user_agents)}")
            print(f"{'='*50}")

            start_time = time.time()
            run_batch_of_5()
            end_time = time.time()

            print(f"Batch #{batch_number} completed in {end_time - start_time:.2f} seconds")
            print(f"Waiting 5 seconds before starting next batch...")

            time.sleep(5)
            batch_number += 1

    except KeyboardInterrupt:
        print("\nStopping the endless loop...")
        print(f"Total unique user agents generated: {len(used_user_agents)}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Restarting in 10 seconds...")
        time.sleep(10)
        main()

if __name__ == "__main__":
    print("Starting endless loop of 5 parallel browser instances... @SOULCRACK")
    print("Each instance will use a completely unique user agent @SOULCRACK")
    print("Press Ctrl+C to stop made by @SOULCRACK")
    main()


# File made by @SOULCARCK
# This script uses Selenium WebDriver with a proxy to interact with YouTube or ad sites.
# It automates page visits to potentially increase video or ad views by simulating human-like delays.
