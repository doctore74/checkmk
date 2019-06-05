#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset: 4 -*-
import os
import pytest
import re
from local import actual_output, make_ini_config, localtest, wait_agent, write_config


class Globals(object):
    section = 'wmi_cpuload'
    alone = True


@pytest.fixture
def testfile():
    return os.path.basename(__file__)


@pytest.fixture(params=['alone', 'with_systemtime'])
def testconfig(request, make_ini_config):
    Globals.alone = request.param == 'alone'
    if Globals.alone:
        make_ini_config.set('global', 'sections', Globals.section)
    else:
        make_ini_config.set('global', 'sections', '%s systemtime' % Globals.section)
    make_ini_config.set('global', 'crash_debug', 'yes')
    return make_ini_config


@pytest.fixture
def expected_output():
    expected = [
        re.escape(r'<<<%s:sep(44)>>>' % Globals.section),
        re.escape(r'[system_perf]'),
        (r'AlignmentFixupsPersec,Caption,ContextSwitchesPersec,Description,'
         r'ExceptionDispatchesPersec,FileControlBytesPersec,'
         r'FileControlOperationsPersec,FileDataOperationsPersec,'
         r'FileReadBytesPersec,FileReadOperationsPersec,FileWriteBytesPersec,'
         r'FileWriteOperationsPersec,FloatingEmulationsPersec,Frequency_Object,'
         r'Frequency_PerfTime,Frequency_Sys100NS,Name,'
         r'PercentRegistryQuotaInUse,PercentRegistryQuotaInUse_Base,Processes,'
         r'ProcessorQueueLength,SystemCallsPersec,SystemUpTime,Threads,'
         r'Timestamp_Object,Timestamp_PerfTime,Timestamp_Sys100NS,WMIStatus'),
        (r'\d+,,\d+,,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,,\d+,'
         r'\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\b(?:OK|Timeout)\b'),
        re.escape(r'[computer_system]'),
        (r'AdminPasswordStatus,AutomaticManagedPagefile,'
         r'AutomaticResetBootOption,AutomaticResetCapability,BootOptionOnLimit,'
         r'BootOptionOnWatchDog,BootROMSupported,BootStatus,BootupState,'
         r'Caption,ChassisBootupState,ChassisSKUNumber,CreationClassName,'
         r'CurrentTimeZone,DaylightInEffect,Description,DNSHostName,Domain,'
         r'DomainRole,EnableDaylightSavingsTime,FrontPanelResetStatus,'
         r'HypervisorPresent,InfraredSupported,InitialLoadInfo,InstallDate,'
         r'KeyboardPasswordStatus,LastLoadInfo,Manufacturer,Model,Name,'
         r'NameFormat,NetworkServerModeEnabled,NumberOfLogicalProcessors,'
         r'NumberOfProcessors,OEMLogoBitmap,OEMStringArray,PartOfDomain,'
         r'PauseAfterReset,PCSystemType,PCSystemTypeEx,'
         r'PowerManagementCapabilities,PowerManagementSupported,'
         r'PowerOnPasswordStatus,PowerState,PowerSupplyState,'
         r'PrimaryOwnerContact,PrimaryOwnerName,ResetCapability,ResetCount,'
         r'ResetLimit,Roles,Status,SupportContactDescription,SystemFamily,'
         r'SystemSKUNumber,SystemStartupDelay,SystemStartupOptions,'
         r'SystemStartupSetting,SystemType,ThermalState,TotalPhysicalMemory,'
         r'UserName,WakeUpType,Workgroup,WMIStatus'),
        (r'\d+,\d+,\d+,\d+,\d*,\d*,\d+,[^,]*,[^,]+,[\w-]+,\d+,,\w+,\d+,\d+,'
         r'[^,]+,[\w-]+,[^,]+,\d+,\d+,\d+,\d+,\d+,,,\d+,,[^,]+(, [^,]+)?,[^,]+,'
         r'[\w-]+,,\d+,\d+,\d+,,[^,]+,\d+,\-?\d+,\d+,\d+,,,\d+,\d+,\d+,,[\w-]+,'
         r'\d+,\d+,\d+,[^,]+,\w+,,[^,]*,,,,,[^,]+,\d+,\d+,[^,]*,\d+,\w*,\b(?:OK|Timeout)\b')
    ]
    if not Globals.alone:
        expected += [re.escape(r'<<<systemtime>>>'), r'\d+']
    return expected


def test_section_wmi_cpuload(request, testconfig, expected_output, actual_output, testfile):
    # request.node.name gives test name
    localtest(expected_output, actual_output, testfile, request.node.name)
