from cloudshell.networking.cisco.runners.cisco_firmware_runner import \
    CiscoFirmwareRunner as FirmwareRunner
from cloudshell.networking.cisco.flows.cisco_load_firmware_flow import CiscoLoadFirmwareFlow


class CustomCiscoIOSLoadFirmwareFlow(CiscoLoadFirmwareFlow):
    def __init__(self, cli_handler, logger, file_system=None):
        super(CustomCiscoIOSLoadFirmwareFlow, self).__init__(cli_handler, logger, file_system)
        self._file_system = file_system

    def execute_flow(self, path, vrf, timeout):
        # Copy and make all required changes from the base class, or call method from parent class:
        super(CustomCiscoIOSLoadFirmwareFlow, self).execute_flow(path, vrf, timeout)


class CustomFirmwareRunner(FirmwareRunner):
    def __init__(self, logger, cli_handler, file_system=None):
        super(CustomFirmwareRunner, self).__init__(logger, cli_handler)
        self.file_system = file_system

    @property
    def load_firmware_flow(self):
        return CustomCiscoIOSLoadFirmwareFlow(self._cli_handler,
                                              self._logger,
                                              self.file_system)
