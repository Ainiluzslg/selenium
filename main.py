import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_browser():
    """初始化浏览器"""
    driver_service = Service("./msedgedriver.exe")  # 替换为你实际的驱动路径
    driver = webdriver.Edge(service=driver_service)
    driver.maximize_window()
    return driver

def perform_operations(driver):
    """执行 10 个以上的操作"""
    try:
        # 打开 Google 网站
        driver.get("https://www.google.com/")
        time.sleep(2)  # 等待页面加载

        # 2. 显式等待直到搜索框加载完成
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )

        # 3. 输入关键词
        search_box.send_keys("无畏契约")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)  # 等待搜索结果加载

        # 4. 点击第一个搜索结果
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".g a"))
        ).click()
        time.sleep(2)  # 等待页面加载

        # 5. 获取当前所有窗口句柄
        windows = driver.window_handles

        # 6. 切换到新打开的窗口（假设会打开新窗口）
        if len(windows) > 1:
            driver.switch_to.window(windows[1])  # 切换到新窗口
        else:
            print("没有新窗口打开，跳过切换窗口操作。")

        # 7. 等待页面加载完成，然后滚动
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 等待滚动完成

        # 8. 回到上一页面
        driver.back()
        # 等待返回页面加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))  # 检查搜索框是否可见
        )
        time.sleep(2)  # 也可以加一些静态等待

        # 9. 清除搜索框中的内容，然后输入 "VALORANT" 进行搜索
        search_box = driver.find_element(By.NAME, "q")
        search_box.clear()  # 清除搜索框中的内容
        search_box.send_keys("VALORANT")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        # 10. 点击第一个搜索结果
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3"))
        )
        first_result = driver.find_element(By.CSS_SELECTOR, "h3")
        first_result.click()
        time.sleep(2)  # 等待页面加载

        # 11. 在页面滚动
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)

        # 12. 点击 "最新消息"
        try:
            # 使用提供的 XPath 定位并点击“最新消息”按钮
            latest_news_button = driver.find_element(By.XPATH, "//*[@id='riotbar-center-content']/div[2]/div[3]")
            latest_news_button.click()
            time.sleep(2)  # 等待消息展开
        except Exception as e:
            print("未能点击'最新消息'按钮：", e)

        # 13. 点击最新的消息
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='news']/div/div[2]/a[1]"))
            )
            latest_news_link = driver.find_element(By.XPATH, "//*[@id='news']/div/div[2]/a[1]")
            latest_news_link.click()
            time.sleep(2)  # 等待页面加载
        except Exception as e:
            print("未能点击新闻链接：", e)

        # 14. 提取指定路径下的文本信息并写入到 hot_searches.txt 文件
        try:
            # 查找指定路径的元素
            target_element = driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div[1]/div/div[3]/div[1]")

            # 获取该元素中的文本内容
            target_text = target_element.text.strip()  # 获取并去除多余的空白

            # 打开文件并写入提取的文本
            with open('data/hot_searches.txt', 'w', encoding='utf-8') as file:
                if target_text:  # 确保内容不为空
                    file.write(f"提取的文本内容：\n{target_text}\n")

            print("文本内容已写入 hot_searches.txt")
        except Exception as e:
            print("未能提取文本内容：", e)

        print("完成 13 个操作")
    except Exception as e:
        print("操作过程中发生错误:", e)
        driver.quit()

def main():
    """主函数"""
    driver = None
    try:
        driver = setup_browser()
        perform_operations(driver)
    except Exception as e:
        print("发生错误:", e)
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
