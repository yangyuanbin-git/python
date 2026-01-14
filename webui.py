import time
from playwright.sync_api import sync_playwright

# 定义循环次数
LOOP_TIMES = 10

def login_operation(page, loop_index):
    """封装单次登录操作，方便循环调用"""
    print(f"\n开始执行第 {loop_index + 1} 次登录操作")
    
    # 1. 清空输入框（避免重复输入叠加）
    page.locator("#phoneNumber").clear()
    page.locator("#password").clear()
    
    # 2. 输入账号密码
    page.locator("#phoneNumber").fill("18165531652")
    page.locator("#password").fill("123456")
    
    # 3. 点击登录按钮（如果按钮定位符不对，你需要替换成实际的）
    try:
        login_btn = page.locator("//button[@class='login']")
        # 等待按钮可点击，避免元素未加载完成
        login_btn.wait_for(state="visible", timeout=5000)
        login_btn.click()
        print(f"第 {loop_index + 1} 次：登录按钮点击成功")
    except Exception as e:
        print(f"第 {loop_index + 1} 次：点击登录按钮失败，错误：{e}")
        raise  # 抛出异常，终止循环（也可根据需要改为continue跳过）
    #点击退出按钮
    try:
        logout_btn = page.locator("//button[@id='logoutButton']")
        # 等待按钮可点击，避免元素未加载完成
        logout_btn.wait_for(state="visible", timeout=5000)
        logout_btn.click()
        print(f"第 {loop_index + 1} 次：退出按钮点击成功")
    except Exception as e:
        print(f"第 {loop_index + 1} 次：点击退出按钮失败，错误：{e}")
        raise  # 抛出异常，终止循环（也可根据需要改为continue跳过）
    # 4. 等待操作完成（可根据页面跳转/加载情况调整时间）
    time.sleep(2)
    
    # 5. 重置页面（刷新，为下一次循环做准备）
    page.reload()
    page.wait_for_load_state("networkidle")  # 等待页面加载完成
    time.sleep(1)

if __name__ == "__main__":
    with sync_playwright() as p:
        # 启动浏览器（headless=False 显示浏览器窗口，方便调试）
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # 先跳转到登录页面（替换成你的实际登录页URL）
            login_url = "http://localhost:3000/"  # ！！！替换为真实地址
            page.goto(login_url, wait_until="networkidle")
            print(f"成功打开登录页面：{login_url}")
            
            # 执行10次循环
            for i in range(LOOP_TIMES):
                login_operation(page, i)
            
            print(f"\n✅ 全部 {LOOP_TIMES} 次循环执行完成")
        
        except KeyboardInterrupt:
            print("\n⚠️ 你手动终止了脚本执行")
        except Exception as e:
            print(f"\n❌ 脚本执行出错：{e}")
        finally:
            # 关闭浏览器（也可注释掉，手动查看结果）
            print("\n正在关闭浏览器...")
            browser.close()
            print("浏览器已关闭，脚本结束")