#!/usr/bin/env python3
import csv
import requests
from bs4 import BeautifulSoup
import re
from re import search, sub

# Updated the items list with categories
items = [
    {"itemName": "Sony a1", "firmwareLink": "https://www.sony.com/electronics/support/e-mount-body-ilce-1-series/ilce-1/downloads", "category": "Sony Camera"},
    {"itemName": "Sony a7 III", "firmwareLink": "https://www.sony.com/electronics/support/e-mount-body-ilce-7-series/ilce-7m3/downloads", "category": "Sony Camera"},
    {"itemName": "Sony a7 IV", "firmwareLink": "https://www.sony.com/electronics/support/e-mount-body-ilce-7-series/ilce-7m4/downloads", "category": "Sony Camera"},
    {"itemName": "Sony a7C", "firmwareLink": "https://www.sony.com/electronics/support/e-mount-body-ilce-7-series/ilce-7c/downloads", "category": "Sony Camera"},
    {"itemName": "Sony a7R IIIa", "firmwareLink": "https://www.sony.com/electronics/support/e-mount-body-ilce-7-series/ilce-7rm3/downloads", "category": "Sony Camera"},
    {"itemName": "Sony a7R IV", "firmwareLink": "https://www.sony.com/electronics/support/e-mount-body-ilce-7-series/ilce-7rm4/downloads", "category": "Sony Camera"},
    {"itemName": "Sony a7R V", "firmwareLink": "https://www.sony.com/electronics/support/e-mount-body-ilce-7-series/ilce-7rm5/downloads", "category": "Sony Camera"},
    {"itemName": "Sony a7S III", "firmwareLink": "https://www.sony.com/electronics/support/e-mount-body-ilce-7-series/ilce-7sm3/downloads", "category": "Sony Camera"},
    {"itemName": "Sony 6600", "firmwareLink": "https://www.sony.com/electronics/support/e-mount-body-ilce-6000-series/ilce-6600/downloads", "category": "Sony Camera"},
    {"itemName": "Sony 6700", "firmwareLink": "https://www.sony.com/electronics/support/e-mount-body-ilce-6000-series/ilce-6700/downloads", "category": "Sony Camera"},
    {"itemName": "Sony FX3", "firmwareLink": "https://www.sony.com/electronics/support/camcorders-and-video-cameras-interchangeable-lens-camcorders/ilme-fx3/downloads", "category": "Sony Camera"},
    {"itemName": "Sony FX6", "firmwareLink": "https://www.sony.com/electronics/support/camcorders-and-video-cameras-interchangeable-lens-camcorders/ilme-fx6v/downloads", "category": "Sony Camera"},
    {"itemName": "Sony FX30", "firmwareLink": "https://www.sony.com/electronics/support/camcorders-and-video-cameras-interchangeable-lens-camcorders/ilme-fx30/downloads", "category": "Sony Camera"},
    {"itemName": "Sony RX10 IV", "firmwareLink": "https://www.sony.com/electronics/support/compact-cameras-dsc-rx-series/dsc-rx10m4/downloads", "category": "Sony Camera"},
    {"itemName": "Sony RX100 VII", "firmwareLink": "https://www.sony.com/electronics/support/compact-cameras-dsc-rx-series/dsc-rx100m7/downloads", "category": "Sony Camera"},
    {"itemName": "Sony E 16-55mm F2.8 G", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel1655g/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 100-400mm F4.5-5.6 GM OSS", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel100400gm/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 12-24mm F2.8 GM", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel1224gm/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 12-24mm F4 G", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel1224g/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 135mm F1.8 GM", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel135f18gm/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 14mm F1.8 GM", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel14f18gm/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 16-35mm F2.8 GM", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel1635gm/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 200-600mm F5.6-6.3 G OSS", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel200600g/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 20mm F1.8 G", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel20f18g/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 24-105mm F4 G OSS", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel24105g/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 24-70mm F2.8 GM", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel2470gm/downloads/", "category": "Sony Lenses"},
    {"itemName": "Sony FE 24-70mm F2.8 GM II", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel2470gm2/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 24mm F1.4 GM", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel24f14gm/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 28-60mm F4-5.6", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel2860/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 35mm F1.4 GM", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel35f14gm/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 35mm F1.8", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel35f18f/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 400mm F2.8 GM OSS", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel400f28gm/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 50mm F1.2 GM", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel50f12gm/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 50mm F1.4 GM", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel50f14gm/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 55mm F1.8 ZA", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel55f18z/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 70-200 F2.8 GM OSS II", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel70200gm2/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 70-200mm F2.8 GM OSS", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel70200gm/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 70-300mm F4.5-5.6 G OSS", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel70300g/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 85mm F1.4 GM", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel85f14gm#downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 85mm F1.8", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel85f18/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE 90mm F2.8 Macro G OSS", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/sel90m28g/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony FE PZ 16-35mm F4 G", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/selp1635g/downloads", "category": "Sony Lenses"},
    {"itemName": "Sony PZ 28-135 F4 OSS", "firmwareLink": "https://www.sony.com/electronics/support/lenses-e-mount-lenses/selp28135g/downloads", "category": "Sony Lenses"}
]

# CSV file name for storing firmware data
file_name = "sony_firmware_data.csv"


# Function to scrape the latest firmware version and update date from a given link
def scrape_firmware_info(url):
    if url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        firmware_element = soup.find("span", class_="item-headline t6-light downloads")
        
        if firmware_element:
            firmware_text = firmware_element.text.strip()
            
            # Extract the firmware version using regular expressions
            version_match = re.search(r"Ver\.?\s*(0\.\d+|\d+(\.\d+)?)", firmware_text, re.IGNORECASE)
            if version_match:
                firmware_version = version_match.group(1)
            else:
                # If no match found, try searching for version after "version" keyword
                version_match = re.search(r"version\s*(0\.\d+|\d+(\.\d+)?)", firmware_text, re.IGNORECASE)
                if version_match:
                    firmware_version = version_match.group(1)
                else:
                    firmware_version = "0.0"
        else:
            firmware_version = "0.0"
            
        last_updated_element = soup.find("span", string=re.compile(r"Release Date: \d{2}/\d{2}/\d{4}"))
        if last_updated_element:
            last_updated_date = last_updated_element.text.split("Release Date: ")[-1].strip()
        else:
            last_updated_date = ""
    else:
        firmware_version = "0.0"
        last_updated_date = ""
        
    return firmware_version, last_updated_date


# Check if the file exists
file_exists = False

# Update the CSV file with the initial firmware data
with open(file_name, "a" if file_exists else "w", newline="") as file:
    fieldnames = ["itemName", "category", "currentFirmwareVersion", "latestFirmwareVersion", "lastUpdatedDate"]  # Added "category" to fieldnames
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    if not file_exists:
        writer.writeheader()
        
    for item in items:
        item_name = item["itemName"]
        category = item["category"]  # Added category retrieval
        firmware_link = item["firmwareLink"]
        
        # Scrape the firmware version and update date from the webpage
        firmware_version, last_updated_date = scrape_firmware_info(firmware_link)
        
        # Write the data to the CSV file
        writer.writerow({
            "itemName": item_name,
            "category": category,  # Added category to writerow
            "currentFirmwareVersion": firmware_version,
            "latestFirmwareVersion": "",
            "lastUpdatedDate": last_updated_date
        })
        
        # Print the initialized data
        print(f"Initialized {item_name}, Current firmware version: {firmware_version}, Last updated date: {last_updated_date or 'N/A'}")
        
print("Firmware data initialized.")
