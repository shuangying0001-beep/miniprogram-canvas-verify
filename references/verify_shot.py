#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_shot.py — 小程序 Canvas 视觉验证截图（教备神器 · 工具模块）
移植自项目 verify-screenshot.py，参数化便于复用。
依赖：selenium + Pillow（pip install selenium pillow）

用法：
  python verify_shot.py --url http://127.0.0.1:9099/your-preview.html \
      --out ./shots --script "ztOpenTemplate('pinyin');" --wait 5

会在 --out 下生成：整页截图 + 顶部/中部/底部裁剪图，供人工目检或回归对比。
"""
import argparse
import os
import sys
import time

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from PIL import Image
except ImportError as e:
    sys.exit("[verify_shot] 缺少依赖，请先: pip install selenium pillow\n  " + str(e))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', required=True, help='预览页 URL（本地服务起的 preview.html）')
    ap.add_argument('--out', default='./shots', help='截图输出目录')
    ap.add_argument('--script', default='', help='页面加载后执行的 JS（如切换模板/设参）')
    ap.add_argument('--wait', type=int, default=5, help='执行 JS 后等待秒数')
    ap.add_argument('--crop', action='store_true', help='是否额外裁剪 顶/中/底 三张区域图')
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    base = os.path.join(args.out, 'shot')

    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--window-size=1200,1600')
    opts.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=opts)
    try:
        driver.get(args.url)
        if args.script:
            driver.execute_script(args.script)
            time.sleep(args.wait)
        driver.save_screenshot(base + '.png')
        print('saved', base + '.png')

        if args.crop:
            img = Image.open(base + '.png')
            w, h = img.size
            img.crop((0, 0, w, h // 3)).save(base + '-top.png')
            img.crop((0, h // 4, w // 2, h // 2)).save(base + '-mid-left.png')
            img.crop((0, h * 2 // 3, w, h)).save(base + '-bottom.png')
            print('cropped top/mid-left/bottom')
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
