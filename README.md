# Connecting IKEA Vindriktning to Home Assistant via Raspberry Pi Pico W

This guide will show you how to connect the IKEA Vindriktning air quality sensor to Home Assistant using a Raspberry Pi Pico W.

## Hardware Connection

1. **Connecting the IKEA Vindriktning to Raspberry Pi Pico W**:

    - `GND` on Vindriktning -> `GND` on the Pico W
    - `5V` on Vindriktning -> `VBUS` on the Pico W
    - `REST` on Vindriktning -> `GP1` on the Pico W

## Setting Up Thonny

Thonny is a Python IDE that is ideal for beginners and works great with the Raspberry Pi Pico W.

1. **Download and Install**:

   - Download Thonny from [here](https://thonny.org).
   - Install Thonny on your computer.

2. **Connect the Pico and Open Thonny**:

   - Plug your Raspberry Pi Pico W into your computer via USB.
   - Open Thonny and ensure the bottom right corner of the window shows "MicroPython (Raspberry Pi Pico)".

3. **Upload Your Code**:

   - In Thonny, open the code file you want to upload to the Pico.
   - Click the "Run" button. This will both upload the code to the Pico and execute it.

## Software Configuration

1. **Update your Pico's code**:

   First, ensure your Raspberry Pi Pico W's code is set up to serve the PM2.5 readings over HTTP.

2. **Find the IP Address of your Pico W**:

   - Load the code onto your Raspberry Pi Pico W and run it.
   - Connect your Pico W to your Wi-Fi network. Update the `ssid` and `password` variables in the Pico's code with your Wi-Fi details.
   - After it's connected, the Pico will print its IP address. Note this down.

3. **Update Home Assistant Configuration**:

   Navigate to your Home Assistant's configuration file, usually located at `/config/configuration.yaml`.

   Append the following:

   ```yaml
   sensor:
     - platform: rest
       resource: http://YOUR_PICO_IP_ADDRESS/reading
       name: "Vindriktning PM2.5"
       value_template: "{{ value_json.pm25 }}"
       unit_of_measurement: "µg/m³"
       scan_interval: 60
   ```

   Replace `YOUR_PICO_IP_ADDRESS` with the IP address you noted down earlier.

4. **Restart Home Assistant**:

   After editing the `configuration.yaml`, you'll need to restart Home Assistant for the changes to take effect.

5. **Add the Sensor to Lovelace UI**:

   Once Home Assistant restarts, your new sensor should be available. You can add it to your Lovelace UI to view its value and create graphs or other visualizations.

That's it! Your IKEA Vindriktning air quality sensor should now be integrated into Home Assistant using a Raspberry Pi Pico W.
