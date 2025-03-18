import datetime
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 設定全域變數：上班和下班的時間範圍
START_WORK_HOUR = 8  # 早上上班開始時間
END_WORK_HOUR = 12    # 早上上班結束時間（即上班時間範圍為 8:00 到 12:00）
START_OFF_HOUR = 18  # 下午下班開始時間
END_OFF_HOUR = 23    # 下午下班結束時間（即下班時間範圍為 18:00 到 23:00）

# ChromeDriver 路徑（請根據你的實際路徑修改）
# 如果在 Mac 或 Linux，路徑格式會不同
service = Service("C:/PythonCode/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# 開啟 NUEiP 登入頁面
driver.get("https://portal.nueip.com/login")

# 設定等待時間
wait = WebDriverWait(driver, 30)

# 填寫登入資訊（假設你已經登入）
COMPANY_ID = "YOUR_COMPANY_ID"
EMPLOYEE_ID = "YOUR_EMPLOYEE_ID"
PASSWORD = "YOUR_PASSWORD"

# 找「公司代號」輸入框（用 name 屬性定位）
company_input = wait.until(
    EC.presence_of_element_located((By.NAME, "inputCompany")))
company_input.send_keys(COMPANY_ID)

# 找「員工編號」輸入框（用 name 屬性定位）
employee_input = wait.until(
    EC.presence_of_element_located((By.NAME, "inputID")))
employee_input.send_keys(EMPLOYEE_ID)

# 找「密碼」輸入框（用 name 屬性定位）
password_input = wait.until(
    EC.presence_of_element_located((By.NAME, "inputPassword")))
password_input.send_keys(PASSWORD)

# 送出登入（按下 Enter）
password_input.send_keys("\n")  # 如果有登入按鈕，則可替代為 click()

# 獲取當前時間
current_time = datetime.datetime.now()
current_hour = current_time.hour  # 取得小時部分
current_minute = current_time.minute  # 取得分鐘部分
current_second = current_time.second  # 取得秒數部分

# 隨機選擇打卡時間
def get_random_time():
    # 隨機選擇時間
    if START_WORK_HOUR <= current_hour < END_WORK_HOUR:
        random_minute = random.randint(11, 25)
        random_second = random.randint(10, 50)
        return current_time.replace(hour=current_hour, minute=random_minute, second=random_second)
    elif START_OFF_HOUR <= current_hour < END_OFF_HOUR:
        random_minute = random.randint(1, 30)
        random_seconde = random.randint(10, 50)
        return current_time.replace(hour=current_hour, minute=random_minute, second=random_seconde)
    else:
        # 如果時間不在正確範圍內，顯示訊息
        print("現在不在打卡時間範圍內，未執行打卡。")
    return None

# 最大嘗試次數
max_retries = 5
retry_count = 0
target_time = get_random_time()

# 檢查目標時間是否有效
while target_time:
    # 計算等待時間
    wait_seconds = (target_time - current_time).total_seconds()

    # 若目標時間小於等於當前時間，重新隨機選擇時間
    if wait_seconds <= 0:
        print("目標時間已過或無效，重新選擇打卡時間...")
        retry_count += 1
        if retry_count >= max_retries:
            print("達到最大嘗試次數，程式結束。")
            break
        target_time = get_random_time()
        current_time = datetime.datetime.now()  # 重新獲取當前時間
    else:
        print(f"預計在 {target_time.strftime('%H:%M:%S')} 執行打卡操作，等待 {int(wait_seconds)} 秒...")
        time.sleep(wait_seconds)  # 等待直到目標時間

        # 根據時間進行打卡
        if START_WORK_HOUR <= target_time.hour < END_WORK_HOUR:
            # 點擊「上班」按鈕
            punch_in_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='punch-button__title']//span[text()='上班']")))
            punch_in_button.click()
            print(f"已點擊『上班』按鈕，時間：{target_time.strftime('%H:%M:%S')}")
        elif START_OFF_HOUR <= target_time.hour < END_OFF_HOUR:
            # 點擊「下班」按鈕
            punch_out_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='punch-button__title']//span[text()='下班']")))
            punch_out_button.click()
            print(f"已點擊『下班』按鈕，時間：{target_time.strftime('%H:%M:%S')}")

        break  # 執行完打卡後結束循環
        
#print("運作完成。")
# 測試結束後關閉瀏覽器
driver.quit()
