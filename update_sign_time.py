import json
from datetime import datetime, timedelta
import os
import sys

def calculate_sign_time():
    """
    محاسبه مقدار جدید برای signTime بر اساس زمان UTC+3:30
    """
    now = datetime.utcnow()
    offset_time = now + timedelta(hours=3, minutes=30)
    year = offset_time.year
    month = f"{offset_time.month:02}"
    day = f"{offset_time.day:02}"
    date_part = f"{year}{month}{day}"
    hours = offset_time.hour
    minutes = offset_time.minute
    seconds = offset_time.second
    time_in_seconds = hours * 3600 + minutes * 60 + seconds
    return f"{date_part}{time_in_seconds:05}"

# دریافت نام فایل از آرگومان‌های خط فرمان
if len(sys.argv) < 2:
    print("Error: No file provided to process.")
    sys.exit(1)

filename = sys.argv[1]

# بررسی اینکه فایل وجود دارد
if not os.path.isfile(filename):
    print(f"Error: File {filename} does not exist.")
    sys.exit(1)

# پردازش فایل JSON مشخص‌شده
if filename.endswith(".json"):  # فقط فایل‌های JSON
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while reading the file: {e}")
        sys.exit(1)

    # بررسی اگر داده یک Object است
    if isinstance(data, dict):  # اگر فایل یک آبجکت باشد
        if "signTime" in data:
            old_sign_time = data["signTime"]
            data["signTime"] = calculate_sign_time()  # مقدار signTime جدید
            print(f"Updated signTime in {filename}: {old_sign_time} -> {data['signTime']}")

            # بازنویسی فایل
            try:
                with open(filename, "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"Unexpected error while writing the file: {e}")
                sys.exit(1)

    elif isinstance(data, list):  # اگر فایل یک لیست از آبجکت‌ها باشد
        updated = False
        for obj in data:
            if isinstance(obj, dict) and "signTime" in obj:
                old_sign_time = obj["signTime"]
                obj["signTime"] = calculate_sign_time()
                print(f"Updated signTime in {filename}: {old_sign_time} -> {obj['signTime']}")
                updated = True

        if updated:
            try:
                with open(filename, "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"Unexpected error while writing the file: {e}")
                sys.exit(1)

    else:
        print(f"The file {filename} does not contain a valid JSON object or list.")
        sys.exit(1)

print(f"Processing completed for file: {filename}")
