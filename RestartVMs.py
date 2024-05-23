from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim
import atexit
import datetime
import time

# Define a method to get VM by its name
def get_vm_by_name(content, vm_name):
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in container.view:
        if vm.name == vm_name:
            obj = vm
            break
    return obj

# Define a method to restart a VM
def restart_vm(vm):
    if vm.runtime.powerState != 'poweredOn':
        print(f"{vm.name} is not powered on. Skipping.")
        return
    print(f"Restarting VM: {vm.name}")
    task = vm.ResetVM_Task()

# Connect to the vCenter Server using SmartConnectNoSSL (no SSL verification)
si = SmartConnectNoSSL(host="", user="", pwd="")
atexit.register(Disconnect, si)

content = si.RetrieveContent()

# List of VMs to restart
vm_names = [
    "LibreNMS",
    "NextCloud",
    # Add other VM names as needed
]

# Check the current time and wait until Monday 2am
while True:
    now = datetime.datetime.now()
    if now.weekday() == 0 and now.hour == 2:
        for vm_name in vm_names:
            vm = get_vm_by_name(content, vm_name)
            if vm:
                restart_vm(vm)
        break
    time.sleep(60)

print("VM restart tasks initiated.")
