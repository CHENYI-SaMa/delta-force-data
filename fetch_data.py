#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloud data fetcher for GitHub Actions.
Fetches data from kkrb.net and saves data.json for GitHub Pages.
No external dependencies - uses only Python standard library.
"""

import json
import os
from delta_daily import KkrbAPI, fetch_all_data


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


if __name__ == "__main__":
    main()
