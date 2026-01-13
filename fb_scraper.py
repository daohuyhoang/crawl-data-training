from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import re
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def is_junk(text):
    # 1. Lọc các dòng chỉ có ký tự đặc biệt hoặc quá nhiều ký tự lạ
    if not text or len(text.strip()) < 10:
        return True
    
    # Ký tự lạ/spam như 웃➫, ♫♯, [r]
    junk_patterns = [r'웃➫', r'♫♯', r'\[r\]', r'♗', r'➫']
    for p in junk_patterns:
        if re.search(p, text):
            return True
            
    # 2. Lọc quảng cáo (số điện thoại, Hotline, Zalo)
    if re.search(r'0\d{9,10}', text) or "Hotline" in text or "Zalo" in text or "MIỄN PHÍ" in text:
        return True
        
    # 3. Lọc các câu có quá nhiều ký tự đặc biệt (> 30% nội dung)
    special_chars = len(re.sub(r'[\w\s,.]', '', text))
    if special_chars / len(text) > 0.3:
        return True
        
    return False

def crawl_fb_comments(post_url, max_comments=5000):
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    comments_data = set()
    
    try:
        driver.get(post_url)
        print("--- Đang tải trang... ---")
        print("TIPS: Bạn nên ĐĂNG NHẬP để lấy được nhiều bình luận hơn.")
        print("Bạn có 30 giây để chuẩn bị...")
        time.sleep(30)
        
        # Thử chuyển sang chế độ "Tất cả bình luận"
        try:
            filters = [
                "//span[contains(text(),'Phù hợp nhất') or contains(text(),'Most relevant')]",
                "//div[@role='button']//span[contains(text(), 'Bình luận hàng đầu')]",
                "//div[@role='button']//i[contains(@class, 'x1b00660')]"
            ]
            for f in filters:
                try:
                    btn = driver.find_element(By.XPATH, f)
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(2)
                    all_opt = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Tất cả bình luận') or contains(text(),'All comments')]"))
                    )
                    all_opt.click()
                    print("=> Đã chuyển sang chế độ: Tất cả bình luận")
                    time.sleep(3)
                    break
                except:
                    continue
        except:
            pass

        last_count = 0
        no_new_retry = 0
        
        while len(comments_data) < max_comments:
            # 1. Click "Xem thêm"
            see_more_xpaths = [
                "//span[contains(text(), 'Xem thêm bình luận')]",
                "//span[contains(text(), 'View more comments')]",
                "//span[contains(text(), 'Xem các bình luận trước')]",
                "//span[contains(text(), 'View previous comments')]",
                "//span[contains(text(), 'Xem thêm trả lời')]",
                "//div[contains(text(), 'replies')]"
            ]
            
            for xpath in see_more_xpaths:
                btns = driver.find_elements(By.XPATH, xpath)
                for b in btns:
                    try:
                        driver.execute_script("arguments[0].click();", b)
                    except:
                        continue

            # 2. Cuộn dần
            driver.execute_script("window.scrollBy(0, 1500);")
            time.sleep(2)

            # 3. Lấy dữ liệu
            articles = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")
            for art in articles:
                try:
                    comment_parts = art.find_elements(By.CSS_SELECTOR, "div[dir='auto']")
                    for p in comment_parts:
                        text = p.text
                        if text and not is_junk(text):
                            comments_data.add(text.strip())
                except:
                    continue
                
            current_count = len(comments_data)
            print(f"Đang lấy bình luận mới...")
            
            if current_count == last_count:
                no_new_retry += 1
                if no_new_retry > 8: # Tăng số lần thử lên cho chắc
                    print("=> Hết bình luận có thể lấy.")
                    break
            else:
                no_new_retry = 0
                
            last_count = current_count
            
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        # Lưu vào file (Chế độ APPEND - cộng dồn)
        save_file = 'crawled_fb.csv'
        new_df = pd.DataFrame(list(comments_data), columns=['text'])
        # Không gán nhãn ở đây - sẽ gán bằng BERT sau
        
        if not os.path.isfile(save_file):
            new_df.to_csv(save_file, index=False, encoding='utf-8-sig')
        else:
            # Đọc file cũ để tránh trùng lặp khi append
            old_df = pd.read_csv(save_file)
            combined_df = pd.concat([old_df, new_df]).drop_duplicates(subset=['text'])
            combined_df.to_csv(save_file, index=False, encoding='utf-8-sig')
            
        print(f"\n--- HOÀN THÀNH ---")
        print(f"Tổng số dữ liệu mới trong {save_file}: {len(pd.read_csv(save_file))}")
        print(f"\n💡 Tiếp theo: Chạy 'python auto_label_bert.py' để gán nhãn tự động!")
        driver.quit()

if __name__ == "__main__":
    print("--- Facebook Scraper Pro (Append Mode & Junk Filter) ---")
    url_input = input("Dán link Facebook bạn muốn cào sạch: ")
    if url_input:
        crawl_fb_comments(url_input)
    else:
        print("Vui lòng nhập URL.")

