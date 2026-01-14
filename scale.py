import uiautomator2 as u2
import time
from datetime import datetime  # 导入日期时间模块

# 1. 连接设备
d = u2.connect("192.168.0.5:5555") 

def search_product():
    # 获取当前精确时间
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # 使用 exists(timeout=3) 增加稳定性，如果3秒内没出现会返回 False
        print(f"[{now}] 正在尝试点击数字 7...")
        if not d(resourceId="com.osai.android_ostmad:id/num7").exists(timeout=3):
            raise Exception("数字 7 按钮未出现")
        d(resourceId="com.osai.android_ostmad:id/num7").click()
        time.sleep(1)

        print(f"[{now}] 正在尝试点击商品内容区...")
        if not d(resourceId="com.osai.android_ostmad:id/contentView").exists(timeout=3):
            raise Exception("商品内容区 contentView 未出现")
        d(resourceId="com.osai.android_ostmad:id/contentView").click()
        time.sleep(1)

        print(f"[{now}] 正在尝试点击重新识别...")
        if not d(resourceId="com.osai.android_ostmad:id/reload").exists(timeout=3):
            raise Exception("重新识别按钮未出现")
        d(resourceId="com.osai.android_ostmad:id/reload").click()
        time.sleep(1)
        
        return True # 执行成功返回 True

    except Exception as e:
        # 一旦出错，记录时间并抛出详细错误
        error_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n系统停止！")
        print(f"发生时间: {error_time}")
        print(f"错误原因: {e}")
        return False # 执行失败返回 False

# 主循环
while True:
    success = search_product()
    if not success:
        print("由于上述错误，脚本已自动停止运行。")
        break # 停止循环