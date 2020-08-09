import re

from cloudshell.devices.networking_utils import UrlParser
from cloudshell.networking.cisco.command_actions.system_actions import SystemActions
from cloudshell.networking.cisco.runners.cisco_firmware_runner import \
    CiscoFirmwareRunner as FirmwareRunner
from cloudshell.networking.cisco.flows.cisco_load_firmware_flow import CiscoLoadFirmwareFlow


class CustomCiscoIOSLoadFirmwareFlow(CiscoLoadFirmwareFlow):
    def __init__(self, cli_handler, logger, file_system=None):
        super(CustomCiscoIOSLoadFirmwareFlow, self).__init__(cli_handler, logger, file_system)
        self._file_system = file_system

    # def execute_flow(self, path, vrf, timeout):
    #     # Copy and make all required changes from the base class, or call method from parent class:
    #     super(CustomCiscoIOSLoadFirmwareFlow, self).execute_flow(path, vrf, timeout)

    def execute_flow(self, path, vrf, timeout):
        """Load a firmware onto the device

        :param path: The path to the firmware file, including the firmware file name
        :param vrf: Virtual Routing and Forwarding Name
        :param timeout:
        :return:
        """

        full_path_dict = UrlParser().parse_url(path)
        firmware_file_name = full_path_dict.get(UrlParser.FILENAME)
        if not firmware_file_name:
            raise Exception(self.__class__.__name__, "Unable to find firmware file")

        with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as enable_session:
            system_action = SystemActions(enable_session, self._logger)
            dst_file_system = self._file_system

            firmware_dst_path = "{0}/{1}".format(dst_file_system, firmware_file_name)

            # === Skipping search for default flash folders list ===
            # device_file_system = system_action.get_flash_folders_list()
            # self._logger.info("Discovered folders: {}".format(device_file_system))
            # if device_file_system:
            #     device_file_system.sort()
            #     for flash in device_file_system:
            #         if flash in self.BOOTFOLDER:
            #             self._logger.info("Device has a {} folder".format(flash))
            #             firmware_dst_path = "{0}/{1}".format(flash, firmware_file_name)
            #             self._logger.info("Copying {} image".format(firmware_dst_path))
            #             system_action.copy(path, firmware_dst_path, vrf=vrf,
            #                                action_map=system_action.prepare_action_map(path, firmware_dst_path))
            #             break
            #         if "flash-" in flash:
            #             firmware_dst_file_path = "{0}/{1}".format(flash, firmware_file_name)
            #             self._logger.info("Copying {} image".format(firmware_dst_file_path))
            #             system_action.copy(path, firmware_dst_file_path, vrf=vrf,
            #                                action_map=system_action.prepare_action_map(path,
            #                                                                            firmware_dst_file_path))
            # else:
            #     self._logger.info("Copying {} image".format(firmware_dst_path))
            #     system_action.copy(path, firmware_dst_path, vrf=vrf,
            #                        action_map=system_action.prepare_action_map(path, firmware_dst_path))

            # === passing in user path ===
            self._logger.info("Copying {} image".format(firmware_dst_path))
            system_action.copy(path, firmware_dst_path, vrf=vrf,
                               action_map=system_action.prepare_action_map(path, firmware_dst_path))

            self._logger.info("Get current boot configuration")
            current_boot = system_action.get_current_boot_image()
            self._logger.info("Modifying boot configuration")
            self._apply_firmware(enable_session, current_boot, firmware_dst_path)

            output = system_action.get_current_boot_config()
            new_boot_settings = re.sub("^.*boot-start-marker|boot-end-marker.*", "", output)
            self._logger.info("Boot config lines updated: {0}".format(new_boot_settings))

            if output.find(firmware_file_name) == -1:
                raise Exception(self.__class__.__name__,
                                "Can't add firmware '{}' for boot!".format(firmware_file_name))

            system_action.copy(self.RUNNING_CONFIG, self.STARTUP_CONFIG, vrf=vrf,
                               action_map=system_action.prepare_action_map(self.RUNNING_CONFIG, self.STARTUP_CONFIG))
            if "CONSOLE" in enable_session.session.SESSION_TYPE:
                system_action.reload_device_via_console(timeout)
            else:
                system_action.reload_device(timeout)

            os_version = system_action.get_current_os_version()
            if os_version.find(firmware_file_name) == -1:
                raise Exception(self.__class__.__name__, "Failed to load firmware, Please check logs")



class CustomFirmwareRunner(FirmwareRunner):
    def __init__(self, logger, cli_handler, file_system=None):
        super(CustomFirmwareRunner, self).__init__(logger, cli_handler)
        self.file_system = file_system

    @property
    def load_firmware_flow(self):
        return CustomCiscoIOSLoadFirmwareFlow(self._cli_handler,
                                              self._logger,
                                              self.file_system)
