class SmartDevice:
    def __init__(self, name, brand):
        self.name = name
        self.brand = brand
        self.is_on = False

    def toggle_power(self):
        self.is_on = not self.is_on
        status = "ON" if self.is_on else "OFF"
        print(f"[*] {self.name} is now {status}")

    def get_status(self):
        return "Online" if self.is_on else "Offline"

# Inheritance: Light adds brightness control
class SmartLight(SmartDevice):
    def __init__(self, name, brand, color="Warm White"):
        super().__init__(name, brand)
        self.brightness = 100
        self.color = color

    def set_brightness(self, level):
        if 0 <= level <= 100:
            self.brightness = level
            print(f"[!] {self.name} brightness set to {level}%")
        else:
            print("Invalid brightness level.")

# Inheritance: Thermostat adds temperature control
class Thermostat(SmartDevice):
    def __init__(self, name, brand, temp=22):
        super().__init__(name, brand)
        self.current_temp = temp

    def set_temp(self, temp):
        self.current_temp = temp
        print(f"[!] {self.name} target temperature set to {temp}°C")

# Composition: The Hub manages all devices
class SmartHub:
    def __init__(self, location):
        self.location = location
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)
        print(f"Added {device.name} to {self.location} Hub.")

    def turn_off_all(self):
        print(f"\n--- Shutting down all devices in {self.location} ---")
        for device in self.devices:
            if device.is_on:
                device.toggle_power()

    def show_report(self):
        print(f"\n--- {self.location} Home Report ---")
        for d in self.devices:
            print(f"Device: {d.name:<15} | Brand: {d.brand:<10} | Status: {d.get_status()}")

def main():
    # Setup Hub
    my_hub = SmartHub("Main Floor")

    # Create Devices
    living_room_light = SmartLight("Main Chandelier", "Philips Hue")
    kitchen_ac = Thermostat("Kitchen AC", "Nest")
    bedroom_lamp = SmartLight("Bedside Lamp", "IKEA")

    # Add to Hub
    my_hub.add_device(living_room_light)
    my_hub.add_device(kitchen_ac)
    my_hub.add_device(bedroom_lamp)

    # Control specific device features
    living_room_light.toggle_power()
    living_room_light.set_brightness(50)
    kitchen_ac.toggle_power()
    kitchen_ac.set_temp(18)

    # Global Hub Control
    my_hub.show_report()
    my_hub.turn_off_all()

if __name__ == "__main__":
    main()