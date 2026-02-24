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
        print(f"[{now}] 正在尝试点击数字 1...")
        if not d(resourceId="com.osai.android_ostmad:id/num7").exists(timeout=3):
                raise Exception(f"[{now}] 数字 1 按钮未出现")
        d(resourceId="com.osai.android_ostmad:id/num7").click()
        time.sleep(1)

        print(f"[{now}] 正在尝试点击商品内容区...")
        if not d(resourceId="com.osai.android_ostmad:id/contentView").exists(timeout=3):
            raise Exception(f"[{now}] 商品内容区 contentView 未出现")
        d(resourceId="com.osai.android_ostmad:id/contentView").long_click(2)
        time.sleep(1)

        print(f"[{now}] 正在尝试点击编辑商品...")
        if not d(resourceId="com.osai.android_ostmad:id/editProduct").exists(timeout=3):
            raise Exception(f"[{now}] 编辑商品按钮未出现")
        d(resourceId="com.osai.android_ostmad:id/editProduct").click()
        time.sleep(1)
        
        # 逻辑：找到文本包含“销售单价”的元素，然后找到它同层级下的 EditText
        # 这种方式即便价格变了（不再是 9.90），依然能准确定位到对应的输入框
        # 修改价格保存
       # instance(0) 表示找页面中第一个出现的 EditText 类组件
        if d(className="android.widget.EditText", instance=1).get_text() == "12.50":
            d(className="android.widget.EditText", instance=1).set_text("7.5")
        else:
            d(className="android.widget.EditText", instance=1).set_text("12.50")
        time.sleep(1)
        print(f"[{now}] 正在尝试点击保存...")
        if not d(resourceId="com.osai.android_ostmad:id/saveButton").exists(timeout=3):
            raise Exception(f"[{now}] 保存按钮未出现")
        d(resourceId="com.osai.android_ostmad:id/saveButton").click()
        time.sleep(1)
        print(f"[{now}] 正在尝试点击清除...")
        if not d(resourceId="com.osai.android_ostmad:id/clearButton").exists(timeout=3):
            raise Exception(f"[{now}] 清除按钮未出现")
        d(resourceId="com.osai.android_ostmad:id/clearButton").click()
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