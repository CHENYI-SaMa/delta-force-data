#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloud data fetcher for GitHub Actions.
Fetches data from kkrb.net and saves data.json for GitHub Pages.
No external dependencies - uses only Python standard library.
"""

import json
import os
import urllib.request
from delta_daily import KkrbAPI, fetch_all_data, format_wxpusher_message


def format_cloud_wxpusher_message(data):
    """云端微信推送格式：与本地文档一致，但不含子弹价格表格。"""
    lines = []
    lines.append(f"三角洲行动每日数据 {data['date']}")
    lines.append("")

    # 密码短名映射
    pwd_short = {
        "零号大坝": "大坝",
        "长弓溪谷": "长弓",
        "巴克什": "巴克",
        "航天基地": "航天",
        "AZ3核电站": "AZ3",
        "潮汐监狱": "监狱",
        "AZ3彩六联动房": "AZ3彩六",
    }

    # 密码
    lines.append("➤今日密码")
    if data.get("passwords"):
        pwd_order = ["零号大坝", "长弓溪谷", "巴克什", "航天基地", "AZ3核电站", "潮汐监狱", "AZ3彩六联动房"]
        for name in pwd_order:
            if name in data["passwords"]:
                short = pwd_short.get(name, name)
                lines.append(f"  {short} {data['passwords'][name]}")
    else:
        lines.append("  获取失败")
    lines.append("")

    # 制造推荐
    lines.append("➤制造推荐")
    if data.get("manufacturing"):
        for item in data["manufacturing"]:
            lines.append(f"  {item['item']}")
            lines.append(f"  (利润:{item['profit']:,.0f})")
    else:
        lines.append("  获取失败")
    lines.append("")

    # 兑换推荐
    lines.append("➤兑换推荐")
    if data.get("exchange"):
        for item in data["exchange"]:
            lines.append(f"  {item['item']}")
            lines.append(f"  (收益:{item['profit']:,.0f})")
    else:
        lines.append("  获取失败")
    lines.append("")
    lines.append(f"kkrb.net | {data['fetch_time']}")

    return "\n".join(lines)


def # push_wxpusher_cloud(data)  # Disabled - local task handles push:
    """GitHub Actions 环境下通过环境变量读取 WxPusher 配置并推送。"""
    app_token = os.environ.get("WXPUSHER_APP_TOKEN", "")
    uids_str = os.environ.get("WXPUSHER_UIDS", "")
    uids = [u.strip() for u in uids_str.split(",") if u.strip()]

    if not app_token or not uids:
        print("WxPusher: 未配置环境变量，跳过推送")
        return

    content = format_cloud_wxpusher_message(data)
    summary = f"三角洲每日数据 {data['date']}"

    body = json.dumps({
        "appToken": app_token,
        "content": content,
        "summary": summary,
        "contentType": 1,
        "uids": uids,
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            "https://wxpusher.zjiecode.com/api/send/message",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read().decode("utf-8"))
        if result.get("code") == 1000:
            print(f"WxPusher: 推送成功 ({len(uids)}人)")
        else:
            print(f"WxPusher: 推送失败 - {result.get('msg', 'unknown')}")
    except Exception as e:
        print(f"WxPusher: 推送异常 - {e}")


def main():
    print("Fetching data from kkrb.net...")
    api = KkrbAPI()
    data = fetch_all_data(api)

    # Save data.json in the current directory (repo root for GitHub Pages)
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Data saved to: {output_path}")
    print(f"Date: {data['date']}  Time: {data['fetch_time']}")

    # Quick summary
    if data.get("passwords"):
        print(f"  Passwords: {len(data['passwords'])} locations")
    if data.get("manufacturing"):
        print(f"  Manufacturing: {len(data['manufacturing'])} workbenches")
    if data.get("exchange"):
        print(f"  Exchange: {len(data['exchange'])} items")
    if data.get("tracked_ammo"):
        print(f"  Tracked ammo: {len(data['tracked_ammo'])} types")

    # 推送到微信（通过环境变量读取配置）
    push_wxpusher_cloud(data)


if __name__ == "__main__":
    main()
