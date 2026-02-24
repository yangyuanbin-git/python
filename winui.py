from pywinauto.application import Application
import time
def start_osai_service(exe_path):
    """
    初始化连接并返回主窗口对象
    """
    try:
        # 建立连接 (backend="uia" 适用于 Qt 程序)
        app = Application(backend="uia").connect(path=exe_path)
        main_window = app.window(title="OSAI_POS_Plugin")
        return main_window
    except Exception as e:
        print(f"连接失败: {e}")
        return None

def click_function_button(window_obj, times):
    """
    控制点击“功能”按钮的循环次数
    :param window_obj: 已经连接的窗口对象
    :param times: 循环点击的次数 (变量控制)
    """
    if window_obj is None:
        return
    try:
        # 1. 预先定位按钮 (只找一次，确保速度)
        target_button = window_obj.child_window(auto_id="MainWidget.widget_head.pushButton_function",control_type="Button")
        print(f"开始执行循环，共计 {times} 次")
        # 2. 根据传参进行循环
        for i in range(times):
            # 使用 click() 进行静默点击，不干扰鼠标
            target_button.click() 
            print(f"第 {i+1} 次点击完成")
            # 每次点击之间稍微停顿，防止程序反应不过来
            time.sleep(5)
        print("所有任务执行完毕")
    except Exception as e:
        print(f"循环中出现错误: {e}")
# --- 实际调用演示 ---
if __name__ == "__main__":
    # 定义你的程序路径
    MY_EXE = r"D:\OSAI\OSAI POS Plugin\OSAI_POS_Plugin.exe"
    # 第一步：连接程序
    win = start_osai_service(MY_EXE)
    # 第二步：通过变量控制次数
    loop_times = 2  # 你可以随意修改这个变量
    click_function_button(win, times=loop_times)
