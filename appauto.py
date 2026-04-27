from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.common import AppiumOptions
import time
import threading

#（1）首次启动

TARGET_APP_NAME = "TikTok"  # 桌面上显示的应用名称（按需修改）
TARGET_APP_PACKAGE = "com.ss.android.ugc.trill"  # 目标应用包名（按需修改）
GAME_APP_PACKAGE = "com.file.recovery.sdhay.android"
AD_CLOSE_XPATH = (
    '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/'
    'android.widget.FrameLayout/android.view.View'
    ' | //android.widget.ImageView[@content-desc="closeButton"]'
    ' | //android.widget.RelativeLayout[@resource-id="com.file.recovery.sdhay.android:id/m75"]/'
    'android.widget.FrameLayout[5]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView'
    '| //android.widget.RelativeLayout[contains(@content-desc,"pageIndex:")]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ImageView'
    # '| //android.widget.RelativeLayout[@content-desc="pageIndex: 1"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ImageView'
    '| //android.widget.RelativeLayout[@content-desc="pageIndex: 3"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.ImageView'
    '| //android.widget.Button[@content-desc="Skip"]'
    '| //android.widget.ImageView[@resource-id="com.file.recovery.sdhay.android:id/tcx"]'
    '| //android.widget.RelativeLayout[@resource-id="com.file.recovery.sdhay.android:id/mbridge_video_templete_container"]/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ImageView[2]'
    '| //android.widget.Button[@content-desc="Close"]'
    '| //android.widget.RelativeLayout[@content-desc="pageIndex: 1"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ImageView'
    '| //android.widget.RelativeLayout[@resource-id="com.file.recovery.sdhay.android:id/mbridge_video_templete_container"]/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout[2]/android.widget.ImageView[2]'
    '| //android.widget.FrameLayout[@resource-id="com.file.recovery.sdhay.android:id/b45"]/android.widget.LinearLayout/android.widget.LinearLayout'
    '| //android.widget.FrameLayout[@resource-id="com.file.recovery.sdhay.android:id/dgo"]'
)

def start_global_ad_watcher(driver, app_package, interval=0.8):
    """
    全局广告关闭守护线程：
    - 只要目标应用进程还在，就持续轮询
    - 检测到固定关闭按钮就自动点击
    """
    stop_event = threading.Event()

    def _watch():
        while not stop_event.is_set():
            try:
                # 0: 未安装/未知, 1: 未运行, 2: 后台挂起, 3: 后台运行, 4: 前台运行
                app_state = driver.query_app_state(app_package)
                if app_state <= 1:
                    time.sleep(interval)
                    continue

                close_buttons = driver.find_elements(AppiumBy.XPATH, AD_CLOSE_XPATH)
                for close_button in close_buttons:
                    if close_button.is_displayed() and close_button.is_enabled():
                        close_button.click()
                        print("检测到广告弹窗，已自动关闭")
                        break
            except Exception:
                # 守护线程容错，避免偶发定位失败导致线程退出
                pass
            time.sleep(interval)

    watcher = threading.Thread(target=_watch, daemon=True)
    watcher.start()
    return stop_event

# 1. 配置驱动
desired_caps = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": "sumsang",
        "appium:udid": "VOBUF6DIS4CYWSUC",  #R5CT118J7QE
        "appium:appPackage": GAME_APP_PACKAGE,
        "appium:appActivity": "com.kmpc.jkrikfesfriurtkzmzkpi",
        "appium:noReset": True,
        "appium:dontStopAppOnReset": True
}
options = AppiumOptions()
options.load_capabilities(desired_caps)

# 2. 启动驱动
driver = webdriver.Remote(command_executor="http://127.0.0.1:4723/wd/hub",
    options=options)
print(driver.session_id)

# 启动全局广告监听（后续流程无需单独处理广告关闭）
ad_watcher_stop_event = start_global_ad_watcher(driver, GAME_APP_PACKAGE)

# 3. 显式等待（最多15秒），定位「我的」按钮并点击
try:
    # 用 UiAutomator 定位文本为「我的」的元素（精准匹配，稳定性高）
    # time.sleep(3)
    # driver.save_screenshot("script_page.png")
    my_button = WebDriverWait(driver, 15,0.5).until(
        EC.element_to_be_clickable(
             (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.file.recovery.sdhay.android:id/ymw")')
            # (AppiumBy.ID,'com.ss.android.article.news:id/f9h')
            # (AppiumBy.ID,'com.ss.android.article.news:id/dtr')
        )
    )
    my_button.click()
except Exception as e:
    print("未找到 continue 页面，非首次启动")
# finally:
#     # 4. 退出驱动（可根据需要注释掉，保留页面查看效果）
#     # driver.quit()
#     pass
# ie=WebDriverWait(driver, 10,0.5).until(
#     EC.element_to_be_clickable(
#         (AppiumBy.ID,"com.file.recovery.sdhay.android:id/zmv")
#     )
# )
# ie.click()
iq=WebDriverWait(driver, 15,0.5).until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("android:id/checkbox").instance(0)')
    )
)
iq.click()
try:
    allow=WebDriverWait(driver, 15,0.5).until(
      EC.element_to_be_clickable(
        (AppiumBy.ID,'com.android.permissioncontroller:id/permission_allow_button')
      )
    )
    allow.click()
except Exception as e:
    print("未找到 allow 页面，非首次启动")

time.sleep(1)

# 1) 点击系统 Home 键，返回桌面
driver.press_keycode(3)  # AndroidKey.HOME
print("已返回桌面")

time.sleep(5)
# 2) 在桌面点击目标应用图标
try:
    app_icon = WebDriverWait(driver, 10, 0.5).until(
        EC.element_to_be_clickable(
            (
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().text("{TARGET_APP_NAME}")'
            )
        )
    )
    app_icon.click()
    print(f"已点击桌面应用：{TARGET_APP_NAME}")
except Exception:
    # 兜底：若桌面图标文案/布局变化，直接按包名启动目标应用
    print(f"桌面未找到应用图标：{TARGET_APP_NAME}，改为包名直接启动")
    driver.activate_app(TARGET_APP_PACKAGE)
    print(f"已启动应用包名：{TARGET_APP_PACKAGE}")
time.sleep(360)
driver.quit()
