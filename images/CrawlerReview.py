from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time, re

flag = True

def clean_store_name(name: str) -> str:
    global flag
    name = re.sub(r'\(.*?\)', '', name)  # 괄호 안 제거
    name = re.sub(r'[^가-힣\d\s]', '', name)  # 한글 + 숫자 + 공백만 허용
    name = re.sub(r'\s+', ' ', name).strip()
    if name[-1] == '점':
        flag = False
    return name

def clean_address(address: str) -> str:
    global flag
    if not address or flag == False:
        return ""
    return re.split(r'[,(]', address)[0].strip()    

def crawl_reviews(restaurant_name: str, full_address: str, max_wait_sec=10) -> list[str]:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    #options.add_argument("--headless=new")  # 크롬 109 이상에서 권장되는 방식
    #options.add_argument("--window-size=1920,1080")  # 뷰포트 강제 설정
    #options.add_argument("--disable-gpu")
    #options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    store_name = clean_store_name(restaurant_name)
    address = clean_address(full_address)
    search_keyword = f"{store_name} {address}"
    
    if len(store_name.split()) < 1:
        print(f"❌ '{store_name}' → 검색어가 너무 짧아 스킵")
        return []
    
    reviews = []
    place_id = None

    try:
        # (1) 검색 페이지 접속
        search_url = f"https://map.naver.com/p/search/{search_keyword}?c=15.00,0,0,0,dh"
        driver.get(search_url)
        time.sleep(2)

        # (2) searchIframe 진입
        driver.switch_to.frame("searchIframe")

        # (3) 검색 결과 중 주소가 '성남'으로 시작하는 항목만 찾기
        results = driver.find_elements(By.CSS_SELECTOR, "li.VLTHu.OW9LQ, li.UEzoS.rTjJo")
        target_element = None
        try:
            for li in results:
                try:
                    addr_el = li.find_element(By.CSS_SELECTOR, "span.lWwyx span.Pb4bU")
                    address_text = addr_el.text.strip()
                    if address_text.startswith("성남"):
                        target_element = li.find_element(By.CSS_SELECTOR, "a._T0lO")
                        print(f"✅ '{search_keyword}' → 주소 '{address_text}' 선택됨")
                        break
                except:
                    continue
        except NoSuchElementException:
            return []

        # (4) 결과 클릭 또는 상세페이지 fallback
        if target_element:
            driver.execute_script("arguments[0].click();", target_element)
            time.sleep(2)
        else:
            print(f"⚠️ '{search_keyword}' → 성남 주소 검색 결과 없음, 상세페이지로 이동 시도")
            driver.switch_to.default_content()
            time.sleep(1)
            try:
                entry_iframe = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "entryIframe"))
                )
                driver.switch_to.frame(entry_iframe)
            except Exception as e:
                print(f"❌ 상세페이지 iframe 진입 실패: {search_keyword}")
                driver.quit()
                return []

        # (5) place_id 추출
        try:
            current_url = driver.current_url
            if 'directions' in current_url:
                coords = re.search(r'/directions/([^/]+)', current_url).group(1).split(',')
                if len(coords) >= 4:
                    place_id = coords[3]
            else:
                match = re.findall(r"place/(\d+)", current_url)
                if match:
                    place_id = match[0]
        except Exception as e:
            print(f"❌ place_id 추출 실패: {search_keyword} - {e}")
            driver.quit()
            return []

        if not place_id:
            print(f"❌ place_id 없음: {search_keyword}")
            driver.quit()
            return []

        print(f"🔍 place_id 추출 완료: {place_id}")

        # (6) 리뷰탭 이동
        review_url = f"https://pcmap.place.naver.com/restaurant/{place_id}/review/visitor"
        driver.switch_to.default_content()
        driver.get(review_url)
        time.sleep(2)

        # (7) 더보기 최대 20회 클릭
        more_click_count = 0
        while more_click_count < 20:
            try:
                more_btn = driver.find_element(By.CSS_SELECTOR, '.lfH3O > a.fvwqf')
                more_btn.click()
                more_click_count += 1
                print(f"더보기 {more_click_count} 클릭")
                time.sleep(1)
            except:
                break

        # (8) 리뷰 추출
        review_items = driver.find_elements(By.CSS_SELECTOR, 'li.place_apply_pui.EjjAW')
        print(f"[{store_name}] 총 수집 리뷰 개수: {len(review_items)}개")

        for i, li in enumerate(review_items, start=1):
            try:
                review_text = li.find_element(By.CSS_SELECTOR, 'div.pui__vn15t2 a').text.strip()
                reviews.append(review_text)
            except:
                continue

    finally:
        driver.quit()

    return reviews
