from pywinauto.application import Application
import time

def connect_app(easyconnect_path):
    """
    连接并激活 EasyConnect 窗口
    """
    try:
        app = Application(backend="uia").connect(path=easyconnect_path, timeout=10)
        main_window = app.window(title_re=".*EasyConnect.*")
        
        if main_window.exists():
            main_window.set_focus() 
            return main_window
        print("错误：无法找到窗口，请确认程序已打开。")
        return None
    except Exception as e:
        print(f"连接失败: {e}")
        return None

def batch_create_products(main_window, times, item_data):
    """
    根据传参 times 控制批量新建商品
    :param item_data: 包含商品信息的字典
    """
    if main_window is None:
        return

    # --- 1. 预定义所有控件的定位器，提高运行速度 ---
    # 主界面按钮
    btn_new_id = "MainWidget.widget_content.stackedWidget.page_product.widget_tool_product.pushButton_add_product"
    
    # 弹窗内控件 (注意这些 ID 必须在弹窗弹出后才能被检索到)
    base_id = "MainWidget.PopAddProduct.widget_background.stackedWidget.page_1.widget_4."
    sku_id = base_id + "lineEdit_sku"
    price_id = base_id + "lineEdit_sale_price"
    name_id = base_id + "lineEdit_name"
    save_id = base_id + "pushButton_save"
    confirm_id = base_id + "pushButton_confirm"

    try:
        for i in range(times):
            print(f"\n>>> 正在执行第 {i+1}/{times} 组任务...")

            # --- 2. 点击新建 ---
            main_window.child_window(auto_id=btn_new_id, control_type="Button").click_input()
            
            # --- 3. 等待弹窗出现 ---
            # 这里的 sku_input 作为弹窗加载完成的标志
            sku_input = main_window.child_window(auto_id=sku_id, control_type="Edit")
            if not sku_input.exists(timeout=5):
                print("错误：弹窗加载超时")
                break

            # --- 4. 输入商品信息 ---
            print(f"输入数据: {item_data['name']} / {item_data['sku']}")
            sku_input.set_text(item_data['sku'])
            
            main_window.child_window(auto_id=price_id, control_type="Edit").set_text(item_data['price'])
            main_window.child_window(auto_id=name_id, control_type="Edit").set_text(item_data['name'])

            # --- 5. 保存并确认 ---
            # 点击保存
            main_window.child_window(auto_id=save_id, control_type="Button").click_input()
            print("已点击保存")

            # 等待确认按钮出现并点击 (防止保存过程有延迟)
            confirm_btn = main_window.child_window(auto_id=confirm_id, control_type="Button")
            if confirm_btn.exists(timeout=3):
                confirm_btn.click_input()
                print("已点击确认")

            # 每次操作完稍微停顿，确界面刷新
            time.sleep(1)

        print("\n所有批量任务已完成！")

    except Exception as e:
        print(f"执行中断: {e}")

if __name__ == "__main__":
    # 配置路径
    EXE_PATH = r"D:\EasyConnect\EasyConnect.exe"
    
    # 配置循环次数
    LOOP_COUNT = 1 
    
    # 配置测试数据 (你可以把这里改成读取 Excel 或 列表数据)
    test_item = {
        "sku": "789456",
        "price": "100",
        "name": "测试商品"
    }

    # 执行流程
    win = connect_app(EXE_PATH)
    if win:
        batch_create_products(win, times=LOOP_COUNT, item_data=test_item)