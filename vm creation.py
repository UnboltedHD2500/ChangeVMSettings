from pyVmomi import vim
from pyVmomi import vmodl
from pyVim.connect import SmartConnect, Disconnect
import atexit
import ssl

def main():
    # Disable SSL verification (might be necessary depending on your environment)
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE

    # Connect to the vCenter server
    si = SmartConnect(host="", user="", pwd="", sslContext=context)
    atexit.register(Disconnect, si)

    # Get the datacenter and virtual machine folder objects
    content = si.RetrieveContent()
    datacenter = content.rootFolder.childEntity[0]
    vm_folder = datacenter.vmFolder

    # Get the virtual machine template
    template = None
    for vm in vm_folder.childEntity:
        if vm.name == "Ubuntu Base":
            template = vm
            break

    if template is None:
        print("Template not found")
        return

    # Get the resource pool
    resource_pool = datacenter.hostFolder.childEntity[0].resourcePool

    # Create specification for cloning the virtual machine
    clone_spec = vim.vm.CloneSpec()
    clone_spec.location = vim.vm.RelocateSpec(pool=resource_pool)

    # Create the virtual machines
    for vm_name in ["Master", "Node 1", "Node 2"]:
        print(f"Creating VM: {vm_name}")
        clone_spec.config = vim.vm.ConfigSpec(name=vm_name)
        task = template.Clone(folder=vm_folder, name=vm_name, spec=clone_spec)
        while task.info.state == vim.TaskInfo.State.running:
            pass  # Wait for task to complete
        print(f"{vm_name} created successfully")

if __name__ == "__main__":
    main()