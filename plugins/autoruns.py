import argparse
from md.parser import *

"""
TO DO:
 - Add r"shell\open\command\*...
 - MAke Wildcard to search Microsoft\Windows\CurrentVersion\Shell\* values 
 - Review InstalledSDB (Ref: http://technet.microsoft.com/en-us/library/cc721961(v=ws.10).aspx)
 - Review ShellServiceObjectDelayLoad
 - Review regs: http://www.hexacorn.com/blog/2017/01/28/beyond-good-ol-run-key-all-parts/
 - Review again Autoruns (with option hide microsoft entires)
 
REOCCURRING:
 - When new office version is available, check for Microsoft\Office\<version>\*\Options\OPEN as long as multi-wildcard (Microsoft\Office\*\*\Options\OPEN) is not supported. 
 
"""

class autoruns(object):

    name = "autoruns"

    """ Baseline params """
    compare_fields = ["key_path", "value_name", "value_content"]

    """ Constants and global declarations: """
    QUERY_VALUE_LIST = [
        r"Software\Microsoft\Windows NT\CurrentVersion\Windows\Load",
        r"Microsoft\Windows NT\CurrentVersion\Windows\Load",
        r"Software\Microsoft\Windows NT\CurrentVersion\Windows\Run",
        r"Microsoft\Windows NT\CurrentVersion\Windows\Run",
        r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
        r"Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
        r"Software\Microsoft\Windows\CurrentVersion\Run\COM+",
        r"Microsoft\Windows\CurrentVersion\Run\COM+",
        r"ControlSet001\Control\SafeBoot\AlternateShell",
        r"ControlSet002\Control\SafeBoot\AlternateShell",
        r"ControlSet003\Control\SafeBoot\AlternateShell",
        r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon\System",
        r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon\TaskMan",
        r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon\VMApplet",
        r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit",
        r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Shell",
        r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon\UIHost",
        r"Microsoft\Windows NT\CurrentVersion\Winlogon\System",
        r"Microsoft\Windows NT\CurrentVersion\Winlogon\TaskMan",
        r"Microsoft\Windows NT\CurrentVersion\Winlogon\VMApplet",
        r"Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit",
        r"Microsoft\Windows NT\CurrentVersion\Winlogon\Shell",
        r"Microsoft\Windows NT\CurrentVersion\Winlogon\UIHost",
        r"Microsoft\Windows NT\CurrentVersion\Winlogon\Notify\Lock",
        r"Microsoft\Windows NT\CurrentVersion\Winlogon\Notify\Logoff",
        r"Microsoft\Windows NT\CurrentVersion\Winlogon\Notify\Logon",
        r"Microsoft\Windows NT\CurrentVersion\Winlogon\Notify\Shutdown",
        r"Microsoft\Windows NT\CurrentVersion\Winlogon\Notify\StartScreenSaver",
        r"Microsoft\Windows NT\CurrentVersion\Winlogon\Notify\StartShell",
        r"Microsoft\Windows NT\CurrentVersion\Winlogon\Notify\Startup",
        r"Microsoft\Windows NT\CurrentVersion\Winlogon\Notify\StopScreenSaver",
        r"Microsoft\Windows NT\CurrentVersion\Winlogon\Notify\Unlock",
        r"Microsoft\Windows\CurrentVersion\ShellServiceObjectDelayLoad",  # Need to check if value or a key
        r"Wow6432Node\Microsoft\Active Setup\Installed Components\*\StubPath",
        r"Microsoft\Active Setup\Installed Components\*\StubPath",
        r"Microsoft\Windows NT\CurrentVersion\Winlogon\Notify\*\DLLName",
        r"Microsoft\Office\11.0\*\Options\OPEN",  # https://twitter.com/william_knows/status/909788804696944642/photo/1
        r"Microsoft\Office\12.0\*\Options\OPEN",
        r"Microsoft\Office\14.0\*\Options\OPEN",
        r"Microsoft\Office\15.0\*\Options\OPEN",
        r"Software\Microsoft\Office\*\Common\AdditionalActionsDLL",
        r"Microsoft\Windows NT\CurrentVersion\Windows\AppInit_DLLs",
        r"ControlSet001\Control\Lsa\Authentication Packages",
        r"ControlSet002\Control\Lsa\Authentication Packages",
        r"ControlSet003\Control\Lsa\Authentication Packages",
        r"ControlSet001\Control\Lsa\Security Packages",
        r"ControlSet002\Control\Lsa\Security Packages",
        r"ControlSet003\Control\Lsa\Security Packages",
        r"ControlSet001\Control\Lsa\OSConfig\Security Packages",
        r"ControlSet002\Control\Lsa\OSConfig\Security Packages",
        r"ControlSet003\Control\Lsa\OSConfig\Security Packages",
        r"ControlSet001\Control\Print\Monitors\*\Driver",
        r"ControlSet002\Control\Print\Monitors\*\Driver",
        r"ControlSet003\Control\Print\Monitors\*\Driver",
        r"Microsoft\Windows NT\CurrentVersion\Image File Execution Options\*\VerifierDlls", # http://cybellum.com/doubleagentzero-day-code-injection-and-persistence-technique/
        r"Wow6432Node\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\*\VerifierDlls"
        r"Microsoft\Windows NT\CurrentVersion\Image File Execution Options\*\Debugger", # https://blog.malwarebytes.com/101/2015/12/an-introduction-to-image-file-execution-options/
        r"Wow6432Node\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\*\Debugger",
        r"Microsoft\Windows\CurrentVersion\App Paths\*\(default)"
    ]
    QUERY_KEY_LIST = [
        r"Select",
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        r"Microsoft\Windows\CurrentVersion\Run",
        r"Wow6432Node\Microsoft\Windows\CurrentVersion\Run",  # Might not exist
        r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run",
        r"Software\Microsoft\Windows NT\CurrentVersion\Run",
        r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
        r"Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
        r"Wow6432Node\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
        r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
        r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
        r"Microsoft\Windows\CurrentVersion\RunOnce",
        r"Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce",
        r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce",
        r"Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\RunOnce",
        r"Software\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\RunOnce",
        r"Wow6432Node\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\RunOnce",
        r"Software\Wow6432Node\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\RunOnce",
        r"Software\Microsoft\Windows\CurrentVersion\RunOnceEx",
        r"Microsoft\Windows\CurrentVersion\RunOnceEx",
        r"Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnceEx",
        r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnceEx",
        r"Software\Microsoft\Windows\CurrentVersion\RunServices",
        r"Microsoft\Windows\CurrentVersion\RunServices",
        r"Wow6432Node\Microsoft\Windows\CurrentVersion\RunServices",
        r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunServices",
        r"Software\Microsoft\Windows\CurrentVersion\RunServicesOnce",
        r"Microsoft\Windows\CurrentVersion\RunServicesOnce",
        r"Wow6432Node\Microsoft\Windows\CurrentVersion\RunServicesOnce",
        r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunServicesOnce",
        r"Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\Run",
        r"Software\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\Run",
        r"Wow6432Node\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\Run",
        r"Software\Wow6432Node\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\Run",
        r"Microsoft\Windows NT\CurrentVersion\WOW\boot",
        r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
        r"Microsoft\Windows\CurrentVersion\Policies\System",
        r"ControlSet001\Control\Session Manager\AppCertDlls",
        r"ControlSet002\Control\Session Manager\AppCertDlls",
        r"ControlSet003\Control\Session Manager\AppCertDlls",
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Common Startup",
        r"Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Common Startup",
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Startup",
        r"Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Startup",
        r"Microsoft\Windows\CurrentVersion\explorer\ShellExecuteHooks",
        r"Control Panel\Desktop\Scrnsave.exe",
        r"Microsoft\Windows NT\CurrentVersion\AppCompatFlags\InstalledSDB",
        r"Microsoft\NetSh",  # https://attack.mitre.org/wiki/Technique/T1128
        r"Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Custom\*",
        r"Software\Microsoft\Office test\Special\Perf\*",
        r"Software\Microsoft\Windows\Windows Error Reporting\RuntimeExceptionHelperModules",  # https://msdn.microsoft.com/en-us/library/windows/desktop/dd408167(v=vs.85).aspx
        r"Microsoft\Windows\Windows Error Reporting\RuntimeExceptionHelperModules"  # https://msdn.microsoft.com/en-us/library/windows/desktop/dd408167(v=vs.85).aspx
    ]

    def __init__(self, plugin, regparser):

        _parser = argparse.ArgumentParser(description='Plugin: "autoruns" designed to scan common ASEPs/Loadpoints', usage=argparse.SUPPRESS)
        _parser.add_argument("-d", "--disable-baseline", help="Would stop loading default baseline file: baseline/services.bl", default=True,
                             action="store_false", dest='baseline_enabled')
        _parser.add_argument("-f", "--baseline-file", help="Specify custom baseline location",
                             default="baseline/autoruns.bl", action="store", dest='baseline_file')

        _args = _parser.parse_args(args=plugin.args[1:])

        self.objects_matched = []
        self.plugin = plugin
        self.regparser = regparser
        self.args = _args
        self.baseline = None
        self.baseline_enabled = _args.baseline_enabled

        if self.baseline_enabled:
            self.baseline_file = _args.baseline_file
            """ Load the base line file """
            self.baseline = baseline(self.baseline_file, self.compare_fields)

    def format_data(self, _item_fields):
        """ Adjust _item_fields - from parser._print_item """
        return _item_fields

    def pull_data(self, keys, values, registry_hive):

        objects_matched = []

        self.regparser.debug_print(f'INFO: Pulling registry ASEPs ...')
        objects_matched.extend(self.regparser.query_value_wd(registry_hive.file_path, values, registry_hive, True))
        objects_matched.extend(self.regparser.query_key(registry_hive.file_path, keys, registry_hive, True))

        return objects_matched

    def process_data(self, item):
        if isinstance(item["values"], list):
            if item["values"]:
                for _value in item["values"]:
                    _item = self._process_item(item["key"], _value)
                    if _item:
                        self.objects_matched.append(
                            {"hive": item["hive"], "key": item["key"], "values": _value, "plugin": self})
            else:
                if self._process_item(item["key"]):
                    self.objects_matched.append({"hive": item["hive"], "key": item["key"], "values": None, "plugin": self})

        else:
            if self._process_item(item["key"]):
                self.objects_matched.append(
                    {"hive": item["hive"], "key": item["key"], "values": item["values"], "plugin": self})

    def _process_item(self, key, value=None):
        """ Return registry value according to plugin mode  """

        """ Remove the hive root """
        _root, _, _key_path = key.path().partition("\\")
        #_root, _, _key_path = _key_path.partition("\\")  # Removes ControlSetXXX string
        """ Check item type """
        if value:
            _value_name = value.name()
            try:
                _value_content = value.value()
            except UnicodeError:
                _value_content = "regparser - UnicodeError"
                print(f'ERROR: RegistryValue.__init__ -> {_key_path}\\{_value_name}')

            item = {"type": "VALUE", "key_path": _key_path, "value_name": _value_name, "value_content": _value_content, "temp_entry": True}
            item = self.format_data(item)
            item["value_content"] = str(item["value_content"])
        else:
            item = {"type": "KEY", "key_path": _key_path, "value_name": "", "value_content": "", "temp_entry": True}
            item = self.format_data(item)

        if self.baseline:
            if self.baseline.isfound(item):
                return None
            else:
                return item
        else:
                return item

    def execute(self):

        objects_matched = []

        if self.baseline_enabled:
            if self.baseline.initialized:
                self.regparser.debug_print(f'INFO: Baseline file: {self.baseline.file}')
                self.regparser.debug_print(f'INFO: Baseline items count: {len(self.baseline.items)}')
            else:
                self.regparser.debug_print(f'WARNING: Baseline not enabled')

        """ Parse all specified hive files """
        for hive_file in self.regparser.input_files:
            registry_hive = self.regparser._load_hive(hive_file)
            if not registry_hive:
                continue
            """ Pull registry data """
            objects_matched.extend(self.pull_data(self.QUERY_KEY_LIST, self.QUERY_VALUE_LIST, registry_hive))

        """ Parse data """
        for item in objects_matched:
            self.process_data(item)

        """ Print all """
        self.regparser.objects_matched.extend(self.objects_matched)
        self.regparser.debug_print(
             f'INFO: Printing results (count: {len(self.regparser.objects_matched.items)})...')
        self.regparser.print_items()

        """ Export matched registry keys/values to .reg file, if export was enabled """
        if self.regparser.search_criteria.export_file:
            self.regparser.debug_print(f'INFO: Exporting autoruns ...')
            self.regparser.export_items()
        else:
            if self.regparser.search_criteria.export_folder:
                self.regparser.debug_print(f'INFO: Exporting autoruns ...')
                self.regparser.export_items()

        self.regparser.objects_matched.clear()
