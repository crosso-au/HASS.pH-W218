# pH-W218 Home Assistant Integration

[![Buy Me A Coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20Ryan%20a%20tasty%20coffee&emoji=☕&slug=crosso_au&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/crosso_au)


Home Assistant custom integration that reads a Tuya WiFi water tester from the Tuya Cloud and exposes **9 UI-manageable sensors** with unique IDs under one device. Works when Local Tuya cannot be used.

## What it gives you
- Sensors with names like ` pHW218 - Temperature`, ` pHW218 - pH`, ` pHW218 - TDS`, ` pHW218 - EC`, ` pHW218 - Salt`, ` pHW218 - ORP`, ` pHW218 - CF`, ` pHW218 - Proportion`, ` pHW218 - RH`
- Unique IDs so you can rename, assign Areas, and customize in the UI
- A single Device for easy Area assignment
- Configurable polling interval and name prefix from the Options panel
- Async HTTP with Tuya token caching
- Simply, another option other tha LocalTuya. Personally, I had mixed results with LocalTuya - I needed something that suited my needs and that was a bit more stable.

## The Hardware
- 8-in-1 Multifunction Water Quality Meter Digital WiFi PH EC TDS SALT SG.Temp ORP CF Tester Smart Monitor Tuya APP Control
- ![pH-W218](https://i.ibb.co/ns0LkyGs/ph-218.png)
-[![Buy on AliExpress](https://img.shields.io/badge/Buy%20on%20AliExpress-FF4747?style=for-the-badge)](https://www.aliexpress.com/item/1005008046059276.html)

---

## Prerequisites - set up Tuya Cloud and link your account

This is the most important piece. The developer platform changes often, so it can be difficult to give accurate steps on this one. I will update this as often as I can.
You need a Tuya IoT Platform account and a Cloud project that is linked to the mobile app account that owns your water tester. Steps:

1. **Create a Tuya developer account**  
   - Go to the Tuya IoT Platform and sign in or sign up.
2. **Create a Cloud Project**  
   - Cloud → Development → Create Cloud Project  
   - Select **Smart Home** as the project type.
   - Choose the **Data Center** that matches your mobile app account region.
3. **Subscribe to required APIs**  
   - In the Cloud Project, open the **API Products** or **Authorize APIs** page.  
   - Subscribe to at least **IoT Core** or the **Smart Home Device Management** set that includes:
     - Token management: `/v1.0/token`
     - Device shadow or status API: `/v2.0/cloud/thing/{device_id}/shadow/properties`
4. **Link your mobile app account**  
   - In the Cloud Project, go to **Devices** → **Link Tuya App Account**.  
   - Click **Add App Account** and scan the QR code using the **Tuya Smart** app or **Smart Life** app that you used to pair the device.  
   - After linking, the **Devices** tab in the Cloud Project should show your water tester.
5. **Find your credentials and IDs**
   - **Client ID and Client Secret**: open your Cloud Project → **Project Overview** or **Authorization** tab. Copy **Client ID** and **Client Secret**.
   - **API Endpoint by region**. Use the base URL that matches the project’s Data Center:  
     - EU: `https://openapi.tuyaeu.com`  
     - US: `https://openapi.tuyaus.com`  
     - CN: `https://openapi.tuyacn.com`  
     - IN: `https://openapi.tuyain.com`
   - **Device ID**: Cloud Project → **Devices** → your water tester → copy the **Device ID**.  
     - Optional: in **API Explorer**, call the device info endpoint to verify the ID and permissions.

> Tip: Endpoint and data center must match. A region mismatch is the number one cause of 1010/permission errors or empty results.

---

## Install

Manual install for now.

1. Copy this folder to Home Assistant:  
   `custom_components/HASS.pH-W218` so the path is:  
   `/config/custom_components/HASS.pH-W218/`
2. Restart Home Assistant.
3. Go to **Settings → Devices and services → Add Integration** and search for **TankQual Tuya Water Tester**.
4. Enter:
   - **Endpoint**: the URL from the table above
   - **Client ID**: from the Tuya Cloud Project
   - **Client Secret**: from the Tuya Cloud Project
   - **Device ID**: from the Devices tab
   - **Name Prefix**: defaults to ` pHW218`
   - **Scan interval**: defaults to 60 seconds

After setup, open the created **Device** and you will see the 9 sensors. Assign an **Area** from the device page.

---

## Configuration - change later in Options

- **Name Prefix**: default ` pHW218`. Changes the visible names only. Unique IDs stay stable.
- **Scan interval**: default 60 seconds. Respect Tuya rate limits if you reduce this.

To change: Settings → Devices and services → TankQual Tuya Water Tester → **Configure**.

---

## Data mapping and units

The integration reads the device shadow and scales raw values to human units:

| Code            | Sensor name        | Example raw | Scaled value | Unit    |
|-----------------|--------------------|-------------|--------------|---------|
| temp_current    | Temperature        | 194         | 19.4         | °C      |
| ph_current      | pH                 | 721         | 7.21         | pH      |
| tds_current     | TDS                | 71          | 71           | ppm     |
| ec_current      | EC                 | 142         | 142          | µS/cm   |
| salinity_current| Salt               | 82          | 82           | ppm     |
| orp_current     | ORP                | 216         | 216          | mV      |
| cf_current      | CF                 | 142         | 1.42         |         |
| pro_current     | Proportion         | 999         | 0.999        |         |
| rh_current      | RH                 | 45          | 45           | %       |

If your device does not support a code, the sensor will show 0 or stay unavailable.

---

## Troubleshooting

- **Cannot add integration or no data**  
  - Often Tuya API related 
  - Verify Endpoint matches your Cloud Project data center.
  - Confirm the Cloud Project is subscribed to the needed APIs.
  - Confirm the App Account is linked and the device appears under Devices.
  - Check time on the HA host. Tuya signing uses epoch ms.
- **HTTP 1010 or 1106 Too Many Requests**  
  - Increase scan interval in Options.
- **Where to see logs**  
  - Settings → System → Logs → filter `HASS.pH-W218`
  - Enable debug in `configuration.yaml`:
    ```yaml
    logger:
      default: info
      logs:
        custom_components.tankqual: debug
    ```

---

## Security

- Never commit your Client Secret or Access Token to Git.  
- This integration reads device state only. It does need write commands - In your Tuya permissions, read is fine if you're worried about least-privilege.

---

## Roadmap

- Auto-hide sensors that are not present on the device
- HACS listing
- Per-entity thresholds and Lovelace example cards
- Multi-device support

---

## Credits and license

- Created by Ryan Crossingham @ CrossboxLabs 
- Not affiliated with Analytical Intruments, Tuya or Home Assistant.  

License: GPL-3.0 license

