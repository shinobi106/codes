// Initialize system
MAX_CAPACITY = 92
MAX_DEVICE_CAPACITY = 40
allocated_power = 0 // Total allocated power at any moment
devices = [] // List of active devices (each device is a tuple of (timestamp, device_id, power_consumed))

// Function to allocate power to a new device
function allocatePower(device_id, requested_power):
    if requested_power > MAX_DEVICE_CAPACITY:
        requested_power = MAX_DEVICE_CAPACITY  // Limit power to max device capacity
    if allocated_power + requested_power <= MAX_CAPACITY:
        allocated_power += requested_power
        addDeviceToQueue(device_id, requested_power)
    else:
        // Allocate power based on available capacity with FIFO
        available_power = MAX_CAPACITY - allocated_power
        if available_power > 0:
            allocated_power += available_power
            adjustPowerQueue(device_id, available_power)
        else:
            // No available power
            rejectDeviceConnection(device_id)

// Function to remove a device
function removeDevice(device_id):
    for device in devices:
        if device.device_id == device_id:
            allocated_power -= device.power_consumed
            devices.remove(device)
            break

// Function to handle power consumption change
function changePowerConsumption(device_id, new_power):
    for device in devices:
        if device.device_id == device_id:
            // Adjust the total allocated power
            allocated_power -= device.power_consumed
            device.power_consumed = new_power
            if allocated_power + new_power <= MAX_CAPACITY:
                allocated_power += new_power
                updateDevicePower(device_id, new_power)
            else:
                // If the new power exceeds capacity, adjust the consumption based on FIFO
                available_power = MAX_CAPACITY - allocated_power
                if available_power > 0:
                    allocated_power += available_power
                    device.power_consumed = available_power
                    updateDevicePower(device_id, available_power)
                else:
                    // Power adjustment not possible, reject or handle error
                    rejectPowerChange(device_id)

// Helper function to add a new device to the queue
function addDeviceToQueue(device_id, requested_power):
    devices.append({
        "device_id": device_id,
        "power_consumed": requested_power,
        "timestamp": current_time() // Add timestamp of connection
    })

// Helper function to update power consumption of a device
function updateDevicePower(device_id, new_power):
    for device in devices:
        if device.device_id == device_id:
            device.power_consumed = new_power
            break

// Helper function to adjust power of the queue when adding a new device
function adjustPowerQueue(device_id, available_power):
    // Adjust power based on FIFO (older devices keep their allocation)
    for device in devices:
        if device.device_id != device_id:
            if device.power_consumed + available_power <= MAX_DEVICE_CAPACITY:
                device.power_consumed += available_power
                break
        else:
            device.power_consumed = available_power

// Helper function to reject device connection (not enough power)
function rejectDeviceConnection(device_id):
    // Log the rejection or handle failure
    print("Not enough power for device: " + device_id)

// Helper function to reject power change (not enough power)
function rejectPowerChange(device_id):
    // Log the rejection or handle failure
    print("Not enough power to change consumption for device: " + device_id)
