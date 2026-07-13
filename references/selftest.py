#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selftest.py — 验证预览+验证工作流可启动（教备神器 · 工具模块）
不依赖 selenium：启动 preview-server.js 静态服务，用 urllib 确认首页/资源可访问。
运行：python selftest.py
"""
import os
import sys
import time
import shutil
import subprocess
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))


def find_node():
    cands = [
        r"C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2/node.exe",
        r"C:/Users/Administrator/.workbuddy/binaries/node/versions/25.2.1/node.exe",
    ]
    for c in cands:
        if os.path.exists(c):
            return c
    return shutil.which("node") or "node"


def main():
    node = find_node()
    port = 9123
    server = subprocess.Popen(
        [node, os.path.join(HERE, "preview-server.js"), HERE, str(port)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    pass_n = fail_n = 0

    def check(name, cond, extra=""):
        nonlocal pass_n, fail_n
        if cond:
            pass_n += 1
        else:
            fail_n += 1
            print("  [FAIL] " + name + ("  (" + extra + ")" if extra else ""))

    try:
        time.sleep(1.5)
        # 1) 示例预览页可访问（确认服务已起 + 能托管 html）
        try:
            with urllib.request.urlopen("http://127.0.0.1:%d/sample-preview.html" % port, timeout=5) as r:
                sp = r.read().decode("utf-8", "ignore")
            check("sample-preview.html HTTP 200", r.status == 200)
            check("预览页含 canvas", "<canvas" in sp and "getContext" in sp)
        except Exception as e:
            check("sample-preview.html HTTP 200", False, str(e))

        # 2) 静态资源（server 脚本自身）可访问
        try:
            with urllib.request.urlopen("http://127.0.0.1:%d/preview-server.js" % port, timeout=5) as r:
                js = r.read().decode("utf-8", "ignore")
            check("preview-server.js 可访问", r.status == 200 and "http.createServer" in js)
        except Exception as e:
            check("preview-server.js 可访问", False, str(e))

        # 3) 场景配置可访问
        try:
            with urllib.request.urlopen("http://127.0.0.1:%d/snap1.yml" % port, timeout=5) as r:
                yml = r.read().decode("utf-8", "ignore")
            check("snap1.yml 可访问", r.status == 200 and "练字字帖" in yml)
        except Exception as e:
            check("snap1.yml 可访问", False, str(e))
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except Exception:
            server.kill()

    print("\nminiprogram-canvas-verify 自测: " + ("PASS" if fail_n == 0 else "FAIL")
          + "  (%d/%d 通过)" % (pass_n, pass_n + fail_n))
    sys.exit(0 if fail_n == 0 else 1)


if __name__ == "__main__":
    main()
