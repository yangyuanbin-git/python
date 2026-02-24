from operator import index
import uiautomator2 as u2
import time
from datetime import datetime

d = u2.connect("192.168.0.104:9555")
#上下滑动左边导航栏界面
def scroll_left_menu(direction="up"):
    # 1. 获取屏幕分辨率 (1366 x 768)
    w, h = d.window_size()
    
    # 2. 设定左侧菜单的横坐标中心点
    # 菜单很窄，我们把手指放在屏幕横向 10% 的位置，确保在菜单内
    menu_x = w * 0.05
    
    # 3. 设定纵向滑动的起点和终点
    start_y = h * 0.8  # 下方
    end_y = h * 0.2    # 上方
    
    if direction == "up":
        # 向上滑动：手指从下往上推，查看下面的菜单项（如“初始化设置”、“返回”）
        d.swipe(menu_x, start_y, menu_x, end_y, duration=0.5)
        print("已在左侧菜单执行：向上滑动")
    else:
        # 向下滑动：手指从上往下拽
        d.swipe(menu_x, end_y, menu_x, start_y, duration=0.5)
        print("已在左侧菜单执行：向下滑动")
#上下滑动设置界面
def simple_swipe(direction="up"):
    # 获取屏幕的分辨率，例如 1366, 768
    w, h = d.window_size()
    
    # 确定中心横坐标
    center_x = w / 2
    
    if direction == "up":
        # 向上滑动：手指从屏幕下方往上方拉
        # 起点：(中心, 80%高度) -> 终点：(中心, 20%高度)
        d.swipe(center_x, h * 0.8, center_x, h * 0.2, duration=0.5)
        print("执行了：向上滑动 ↑")
    elif direction == "down":
        # 向下滑动：手指从屏幕上方往下方拉
        d.swipe(center_x, h * 0.2, center_x, h * 0.8, duration=0.5)
        print("执行了：向下滑动 ↓")
#自动画测试
def click_setting_by_coordinate():
    now = datetime.now().strftime('%H:%M:%S')
    try:
        # 1. 锁定插件大组
        plugin_group = d(packageName="com.osai.popup", className="android.widget.FrameLayout")
        if plugin_group.exists:
            # 获取该组在屏幕上的具体坐标范围 [left, top, right, bottom]
            bounds = plugin_group.info['bounds']
            left, top, right, bottom = bounds['left'], bounds['top'], bounds['right'], bounds['bottom']
            # 2. 计算“设置”按钮的相对位置
            # 根据 image_ecfed9.jpg 可视化显示，设置按钮在插件顶部的右侧区域
            # 我们取横向 85%，纵向 15% 的位置（你可以根据实际点击位置微调 0.85 和 0.15）
            target_x = left + (right - left) * 0.90
            target_y = top + (bottom - top) * 0.08
            d.click(target_x, target_y)
            print(f"[{now}] 已通过坐标点击插件组内的疑似设置区域: ({target_x}, {target_y})")
            d(resourceId="com.osai.popup:id/text", text="商品管理").click()
            simple_swipe("up")
            simple_swipe("up")
            d(text="新增商品").click()
            # 1. 输入 商品名称 (左侧第一个框)
            d(className="android.widget.EditText", instance=5).set_text("测试商品")
            time.sleep(0.5)
            # 2. 输入 PLU/编号 (右侧第一个框)
            d(className="android.widget.EditText", instance=0).set_text("789456")
            time.sleep(0.5)
            # 3. 输入 价格/单价 (假设是下面一个框)
            d(className="android.widget.EditText", instance=1).set_text("100.80")
            d(resourceId="com.osai.popup:id/saveButton",text="保存").click()
            time.sleep(1)
            d(className="android.widget.LinearLayout", resourceId="com.osai.popup:id/contentView", instance=1).click()
            d(resourceId="com.osai.popup:id/delButton",text="删除").click()
            d(text="确定").click()
            scroll_left_menu("up")
            d(resourceId="com.osai.popup:id/text", text="返回").click()
            return True
        else:
            print(f"[{now}] 未发现插件组 com.osai.popup")
            return False
    except Exception as e:
        print(f"[{now}] 点击发生异常: {e}")
        return False
while True:
    success = click_setting_by_coordinate()
    if success:
        # 如果点击成功后界面会变化（比如弹窗消失），可以考虑 break 
        pass
    time.sleep(2)