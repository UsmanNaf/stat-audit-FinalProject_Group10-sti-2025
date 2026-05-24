import requests
import pandas as pd
import datetime
import time
import os

# ============================================
# KONFIGURASI
# ============================================
REPO = "pandas-dev/pandas"
TARGET_MERGED_COUNT = 500
TARGET_UNMERGED_COUNT = 500
TARGET_ISSUES_COUNT = 1700
TOKEN = 'isi_token'

# ============================================
# SETUP
# ============================================
five_years_ago = datetime.datetime.now() - datetime.timedelta(days=5 * 365)
since_date = five_years_ago.strftime("%Y-%m-%d")

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

# Buat folder kalau belum ada
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/clean", exist_ok=True)

# ============================================
# 1. FUNGSI AMBIL MERGED PR
# ============================================
def get_merged_prs():
    """Mengambil Pull Request yang sudah di-merge"""
    print(f"\n{'='*60}")
    print(f"MENGAMBIL PR YANG SUDAH DI-MERGE sejak {since_date}")
    print(f"{'='*60}")

    query = f"is:pr repo:{REPO} is:merged merged:>={since_date}"
    all_merged_pulls = []
    page = 1

    while len(all_merged_pulls) < TARGET_MERGED_COUNT:
        url = "https://api.github.com/search/issues"
        params = {"q": query, "per_page": 100, "page": page}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 403:
            print("Rate limit! Menunggu 60 detik...")
            time.sleep(60)
            continue

        data = response.json()
        items = data.get("items", [])
        if not items:
            break

        for item in items:
            all_merged_pulls.append({
                "id": item["id"],
                "number": item["number"],
                "title": item["title"],
                "status": "merged",
                "state": item["state"],
                "created_at": item["created_at"],
                "updated_at": item["updated_at"],
                "closed_at": item.get("closed_at"),
                "user": item["user"]["login"],
                "comments": item["comments"]
            })

            if len(all_merged_pulls) >= TARGET_MERGED_COUNT:
                break

        print(f"Halaman {page}: {len(all_merged_pulls)} merged PR terkumpul")
        page += 1
        time.sleep(2)

    return all_merged_pulls[:TARGET_MERGED_COUNT]

# ============================================
# 2. FUNGSI AMBIL UNMERGED PR
# ============================================
def get_unmerged_prs():
    """Mengambil Pull Request yang belum di-merge"""
    print(f"\n{'='*60}")
    print(f"MENGAMBIL PR YANG BELUM DI-MERGE sejak {since_date}")
    print(f"{'='*60}")

    query = f"is:pr repo:{REPO} is:open created:>={since_date}"
    all_unmerged_pulls = []
    page = 1

    while len(all_unmerged_pulls) < TARGET_UNMERGED_COUNT:
        url = "https://api.github.com/search/issues"
        params = {"q": query, "per_page": 100, "page": page}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 403:
            print("Rate limit! Menunggu 60 detik...")
            time.sleep(60)
            continue

        data = response.json()
        items = data.get("items", [])
        if not items:
            break

        for item in items:
            all_unmerged_pulls.append({
                "id": item["id"],
                "number": item["number"],
                "title": item["title"],
                "status": "unmerged",
                "state": item["state"],
                "created_at": item["created_at"],
                "updated_at": item["updated_at"],
                "closed_at": item.get("closed_at"),
                "user": item["user"]["login"],
                "comments": item["comments"]
            })

            if len(all_unmerged_pulls) >= TARGET_UNMERGED_COUNT:
                break

        print(f"Halaman {page}: {len(all_unmerged_pulls)} unmerged PR terkumpul")
        page += 1
        time.sleep(2)

    return all_unmerged_pulls[:TARGET_UNMERGED_COUNT]

# ============================================
# 3. FUNGSI AMBIL ISSUES
# ============================================
def get_issues():
    """Mengambil Issues dari repo"""
    print(f"\n{'='*60}")
    print(f"MENGAMBIL ISSUES sejak {since_date}")
    print(f"{'='*60}")

    since_date_iso = (datetime.datetime.now() - datetime.timedelta(days=5 * 365)).strftime("%Y-%m-%dT%H:%M:%SZ")
    all_issues = []
    page = 1

    while len(all_issues) < TARGET_ISSUES_COUNT:
        url = f"https://api.github.com/repos/{REPO}/issues"
        params = {
            "state": "all",
            "per_page": 100,
            "page": page,
            "since": since_date_iso
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 403:
            print("Rate limit! Menunggu 60 detik...")
            time.sleep(60)
            continue

        data = response.json()
        if not data:
            break

        all_issues.extend(data)
        print(f"Halaman {page}: {len(all_issues)} issues terkumpul")
        page += 1
        time.sleep(1)

    return all_issues[:TARGET_ISSUES_COUNT]

# ============================================
# EKSEKUSI — LANGSUNG JALAN TANPA INPUT
# ============================================
if __name__ == "__main__":
    # Ambil merged PR
    merged_prs = get_merged_prs()
    df_merged = pd.DataFrame(merged_prs)

    # Ambil unmerged PR
    unmerged_prs = get_unmerged_prs()
    df_unmerged = pd.DataFrame(unmerged_prs)

    # Gabungkan
    df_all_prs = pd.concat([df_merged, df_unmerged], ignore_index=True)

    # Simpan ke data/raw/
    df_merged.to_csv("data/raw/pr_merged.csv", index=False)
    df_unmerged.to_csv("data/raw/pr_unmerged.csv", index=False)
    df_all_prs.to_csv("data/raw/pr_all.csv", index=False)
    print("\nData PR disimpan ke data/raw/")

    # Ambil issues
    issues = get_issues()
    df_issues = pd.DataFrame(issues)
    df_issues.to_csv("data/raw/issues.csv", index=False)
    print("Data issues disimpan ke data/raw/")

    print(f"\n{'='*60}")
    print("RINGKASAN DATA")
    print(f"{'='*60}")
    print(f"Merged PR   : {len(df_merged)}")
    print(f"Unmerged PR : {len(df_unmerged)}")
    print(f"Total PR    : {len(df_all_prs)}")
    print(f"Issues      : {len(df_issues)}")