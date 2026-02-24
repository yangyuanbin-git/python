from pywinauto.application import Application
import time

# --- 1. 连接函数 ---
def connect_app(easyconnect_path):
    try:
        # 建立连接
        app = Application(backend="uia").connect(path=easyconnect_path, timeout=10)
        main_window = app.window(title_re=".*EasyConnect.*")
        
        if main_window.exists():
            main_window.set_focus() 
            return app, main_window # 同时返回 app 和 window 方便后续重连
        return None, None
    except Exception as e:
        print(f"连接失败: {e}")
        return None, None

# --- 2. 批量处理函数 ---
def batch_create_products(app, main_window, times, item_data, exe_path):
    if main_window is None:
        return

    # 控件 ID 定义
    btn_new_id = "MainWidget.widget_content.stackedWidget.page_product.widget_tool_product.pushButton_add_product"
    base_id = "MainWidget.PopAddProduct.widget_background.stackedWidget.page_1.widget_4."
    sku_id = base_id + "lineEdit_sku"
    price_id = base_id + "lineEdit_sale_price"
    name_id = base_id + "lineEdit_name"
    save_id = "MainWidget.PopAddProduct.widget_background.widget_tool.pushButton_save"
    confirm_id = "MainWidget.PopMessageBox.widget_background.widget.pushButton_confirm"
    
    # 优化：删除按钮不建议使用超长全路径 ID，使用相对定位或后缀匹配更稳
    delete_id_end = "pushButton_delete"

    try:
        for i in range(times):
            print(f"\n>>> 正在执行第 {i+1}/{times} 组任务...")
            # --- 关键：强制刷新 UI 内存树 ---
            time.sleep(2)
            print("正在强制刷新 UI 树内存...")
            # --- 6. 坐标偏移删除逻辑 (跳过 UI 树识别难题) ---
            print("尝试通过坐标偏移定位删除按钮...")
            
            try:
                # 1. 找到“编号”这个表头作为基准点
                header_id = main_window.child_window(title="编号", control_type="Text")
                
                if header_id.exists(timeout=5):
                    # 获取“编号”表头的坐标 (left, top, right, bottom)
                    rect = header_id.rectangle()
                    print(f"基准点‘编号’坐标: {rect}")

                    # 2. 计算偏移量 (根据你的截图 image_2de0ec.png 推算)
                    # 每一行的高度大约是 50-60 像素
                    # 删除按钮在最右侧，相对于“编号”位置向右偏移约 1200 像素，向下偏移约 60 像素
                    click_x = rect.left + 1200  
                    click_y = rect.top + 60     

                    print(f"正在点击计算出的删除坐标: ({click_x}, {click_y})")
                    
                    # 3. 执行物理点击
                    import pywinauto.mouse as mouse
                    mouse.click(coords=(click_x, click_y))
                    
                    # 4. 处理确认弹窗
                    time.sleep(1.5)
                    confirm_box = main_window.child_window(title="确定", control_type="Button")
                    if confirm_box.exists(timeout=3):
                        confirm_box.click_input()
                        print("坐标点击删除成功！")
                else:
                    print("错误：连表头‘编号’都找不到了，请检查窗口是否被遮挡")

            except Exception as e:
                print(f"坐标点击失败: {e}")
        print("\n所有批量任务已完成！")

    except Exception as e:
        print(f"执行中断: {e}")

# --- 3. 主程序入口 ---
if __name__ == "__main__":
    EXE_PATH = r"D:\EasyConnect\EasyConnect.exe"
    LOOP_COUNT = 1 
    test_item = {"sku": "789456", "price": "100", "name": "测试商品"}

    # 建立连接
    app_obj, win = connect_app(EXE_PATH)
    
    if win: # 对象存在即为 True
        batch_create_products(app_obj, win, LOOP_COUNT, test_item, EXE_PATH)
    else:
        print("初始连接失败，请检查程序是否启动")