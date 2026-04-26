from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.common import AppiumOptions
import time

#（1）首次启动

# 1. 配置驱动
desired_caps = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": "sumsang",
        "appium:udid": "R5CT118J7QE",
        "appium:appPackage": "com.file.recovery.sdhay.android",
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
  isad=WebDriverWait(driver, 30,0.5).until(
     EC.element_to_be_clickable(
        (AppiumBy.XPATH,'//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View | //android.widget.ImageView[@content-desc="closeButton"] | //android.widget.RelativeLayout[@resource-id="com.file.recovery.sdhay.android:id/m75"]/android.widget.FrameLayout[5]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView')
     )
  )
  isad.click()
  # driver.quit()
except Exception as e:
  print("未弹出23000036广告 error:baga")
  # driver.quit()
allow=WebDriverWait(driver, 15,0.5).until(
    EC.element_to_be_clickable(
        (AppiumBy.ID,'com.android.permissioncontroller:id/permission_allow_button')
    )
)
allow.click()

