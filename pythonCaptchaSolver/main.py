from solver import launch_browser, is_captcha_present, solve_once
import time

MAX_RETRIES = 5

def run_solver():
    page, browser, p = launch_browser()
    retries = 0
    start = time.time()

    try:
        while is_captcha_present(page):
            print(f"\n[!] CAPTCHA detected - attempt #{retries + 1}")
            success = solve_once(page)
            retries += 1
            if retries >= MAX_RETRIES:
                print("[x] Max retries reached. Exiting.")
                break
            time.sleep(2)

        if not is_captcha_present(page):
            print("[✓] CAPTCHA solved or bypassed.")
        else:
            print("[x] CAPTCHA still present after max retries.")

    except Exception as e:
        print(f"[!] Unexpected error: {e}")
    finally:
        browser.close()
        p.stop()
        end = time.time()
        print(f"\n[✓] Total time: {round(end - start, 2)}s")
        print(f"[✓] Total attempts: {retries}")

if __name__ == "__main__":
    run_solver()
