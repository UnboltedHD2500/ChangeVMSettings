from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, Disconnect
import atexit
import ssl

def main():
    # Connect to vCenter server
    s = ssl.SSLContext(ssl.PROTOCOL_SSLv23)  # For skipping certificate verification
    s.verify_mode = ssl.CERT_NONE
    si = SmartConnect(host="", user="", pwd="", sslContext=s)
    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)

    # Iterate through each VM and perform the specified tasks
    for vm in container.view:
        # Check if VM name matches pattern 'CIT 281 - One' to 'CIT 281 - Twenty'
        if vm.name.startswith('CIT 358 - '):
            # Turn off VM
            if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
                print(f"Powering off {vm.name}...")
                task = vm.PowerOffVM_Task()
                task.info.state  # waits for the task to finish

            # Change Memory allocation
            vmConfigSpec = vim.vm.ConfigSpec()
            vmConfigSpec.memoryMB = 32 * 1024  # 32 GB to MB
            print(f"Changing memory allocation for {vm.name}...")
            task = vm.ReconfigVM_Task(vmConfigSpec)
            task.info.state  # waits for the task to finish

    print("All tasks completed!")

if __name__ == "__main__":
    main()
