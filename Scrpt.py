import requests
import pandas as pd
import time

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "Show URL"
}

# Booth API
booth_url = "Booth_API_URL" #https://dema26.mapyourshow.com/8_0/exhview/02/exh-remote-proxy.cfm

booth_params = {
    "action": "getExhViewBoothResults",
    "hallID": "",
    "pavilion": "",
    "boothtypeid": "",
    "availableonly": "false",
    "boothsizefrom": "50",
    "boothsizeto": "10000",
    "propertyid": "",
    "orsearchcount": "0"
}

print("Fetching booth list...")

booths = session.get(
    booth_url,
    params=booth_params,
    headers=headers
).json()

# Keep only reserved exhibitors
booths = [b for b in booths if b.get("exhid")]

print(f"Found {len(booths)} exhibitors\n") #Companies etc...

results = []

for i, booth in enumerate(booths, start=1):

    detail = session.get(
        booth_url,
        params={
            "action": "getExhibitorInfo",
            "exhID": booth["exhid"],
            "showCustID": ""
        },
        headers=headers
    ).json()

    country = detail[0].get("country", "") if detail else ""

    results.append({
        "Exhibitor Name": booth["exhname"],
        "Booth Number": booth["boothdisplay"],
        "Stand Size": booth["boothdims"],
        "Country": country
    })

    print(f"[{i}/{len(booths)}] {booth['exhname']}")

    time.sleep(0.1)   # Helps avoid overwhelming the server

df = pd.DataFrame(results)

df.to_excel("ShowName_Exhibitors.xlsx", index=False)

print("\nDone!")
print(f"Saved {len(df)} exhibitors.")