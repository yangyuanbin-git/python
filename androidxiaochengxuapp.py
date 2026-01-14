import uiautomator2 as u2
import time
from datetime import datetime

# 1. 连接设备
d = u2.connect("UMX0221126002669")

def log_action(msg):
    """通用日志打印，带时间戳"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] {msg}")

def change_product_price(target_id, price):
    """
    针对指定商品编号进行改价的函数
    """
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # --- 第一步：查找商品并点击编辑 ---
        log_action(f"正在定位商品 {target_id} 的编辑按钮...")
        # 建议使用 xpath 或 scroll.to 确保 100 在屏幕内
        edit_btn = d.xpath(f'//*[@text="{target_id}"]/following::*[@text="编辑"][1]')
        
        if not edit_btn.wait(timeout=5.0):
            raise Exception(f"未能在页面找到商品 {target_id} 或其对应的编辑按钮")
        
        edit_btn.click()
        log_action("已点击编辑")

        # --- 第二步：输入新价格 ---
        log_action(f"正在尝试修改价格为: {price}")
        price_input = d(text="商品价格").sibling(className="android.widget.EditText")
        
        if not price_input.wait(timeout=5.0):
            raise Exception("进入编辑页失败，未找到 '商品价格' 输入框")
        
        price_input.set_text(price)
        time.sleep(0.5)

        # --- 第三步：点击保存 ---
        save_btn = d(text="保存", className="android.widget.TextView")
        if not save_btn.exists:
            raise Exception("未找到 '保存' 按钮")
        
        save_btn.click()
        log_action(f"商品 {target_id} 改价 {price} 保存指令已发送")
        
        # 等待保存完成回到列表
        time.sleep(1.5) 
        return True

    except Exception as e:
        error_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n[!!!] 脚本于 {error_time} 停止运行")
        print(f"错误详情: {e}")
        # 出错时自动截屏保存，方便后期排查（可选）
        # d.screenshot(f"error_{int(time.time())}.jpg")
        return False

# --- 主程序逻辑 ---
def main():
    try:
        log_action("启动 App 并进入商品管理...")
        d.app_start("com.osai.app")
        
        # 进入商品管理并等待页面加载
        if not d(text="商品管理").wait(timeout=10.0):
            print("未能进入首页或找不到'商品管理'按钮")
            return
        
        d(text="商品管理").click()
        
        # 等待列表加载完成
        d(text="新增商品").wait(timeout=5.0)

        # 执行改价流程 1：改为 10.00
        if not change_product_price("100", "10.00"):
            return # 出错则终止

        # 执行改价流程 2：改为 7.00
        if not change_product_price("100", "7.00"):
            return

        # 完成后返回
        log_action("改价任务全部完成，正在返回首页...")
        d.press("back")
        time.sleep(0.5)

    except Exception as general_e:
        print(f"全局异常: {general_e}")

if __name__ == "__main__":
    main()