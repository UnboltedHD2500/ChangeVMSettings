from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import atexit
import ssl
import datetime
import time

# vCenter details
VCENTER_IP = ''
VCENTER_PORT = 443
VCENTER_USERNAME = ''
VCENTER_PASSWORD = ''
VM_NAMES = ['CIT 281 - One', 'CIT 281 - Two', 'CIT 281 - Three', 'CIT 281 - Four', 'CIT 281 - Five' ,'CIT 281 - Six', 'CIT 281 - Seven' ,'CIT 281 - Eight' ,'CIT 281 - Nine' ,'CIT 281 - Ten', 'CIT 281 - Eleven', 'CIT 281 - Twelve', 'CIT 281 - Thirteen', 'CIT 281 - Fourteen', 'CIT 281 - Fifteen', 'CIT 281 - Sixteen', 'CIT 281 - Seventeen', 'CIT 281 - Eighteen', 'CIT 281 - Nineteen', 'CIT 281 - Twenty',]  # Extend this list as needed

def connect_to_vcenter():
    """
    Connect to vCenter server.
    """
    context = ssl._create_unverified_context() if hasattr(ssl, '_create_unverified_context') else None
    si = SmartConnect(
        host=VCENTER_IP,
        port=VCENTER_PORT,
        user=VCENTER_USERNAME,
        pwd=VCENTER_PASSWORD,
        sslContext=context
    )
    atexit.register(Disconnect, si)
    return si

def get_vm_by_name(si, name):
    """
    Get VM object using name.
    """
    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for obj in container.view:
        if obj.name == name:
            return obj
    return None

def restart_vm(vm):
    """
    Restart a given VM.
    """
    if vm.runtime.powerState == 'poweredOn':
        print(f"Restarting VM: {vm.name}")
        vm.ResetVM_Task()
    else:
        print(f"VM {vm.name} is not powered on. Skipping restart.")

def restart_vms(si, vm_names):
    """
    Restart VMs based on the provided list of names.
    """
    for name in vm_names:
        vm = get_vm_by_name(si, name)
        if vm:
            restart_vm(vm)
        else:
            print(f"VM {name} not found!")

def scheduler():
    """
    Wait until next scheduled time (Monday at 2am) to run the task.
    """
    current_time = datetime.datetime.now()
    next_scheduled_time = current_time + datetime.timedelta((0-current_time.weekday() + 7) % 7)
    next_scheduled_time = next_scheduled_time.replace(hour=0, minute=25, second=0, microsecond=0)

    if current_time >= next_scheduled_time:
        next_scheduled_time += datetime.timedelta(days=7)

    seconds_till_next_schedule = (next_scheduled_time - current_time).total_seconds()
    print(f"Waiting for {seconds_till_next_schedule} seconds until next scheduled restart.")
    time.sleep(seconds_till_next_schedule)

    # Task
    si = connect_to_vcenter()
    restart_vms(si, VM_NAMES)

if __name__ == "__main__":
    scheduler()
