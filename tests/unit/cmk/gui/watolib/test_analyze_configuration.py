# Triggers plugin loading of plugins.wato which registers all the plugins
import cmk
import cmk.gui.wato  # pylint: disable=unused-import
import cmk.gui.watolib as watolib


def test_registered_ac_tests():
    expected_ac_tests = [
        'ACTestAlertHandlerEventTypes',
        'ACTestApacheNumberOfProcesses',
        'ACTestApacheProcessUsage',
        'ACTestBackupConfigured',
        'ACTestBackupNotEncryptedConfigured',
        'ACTestBrokenGUIExtension',
        'ACTestCheckMKHelperUsage',
        'ACTestESXDatasources',
        'ACTestGenericCheckHelperUsage',
        'ACTestHTTPSecured',
        'ACTestLDAPSecured',
        'ACTestLiveproxyd',
        'ACTestLivestatusUsage',
        'ACTestLivestatusSecured',
        'ACTestNumberOfUsers',
        'ACTestOldDefaultCredentials',
        'ACTestPersistentConnections',
        'ACTestRulebasedNotifications',
        'ACTestSizeOfExtensions',
        'ACTestTmpfs',
    ]

    if not cmk.is_raw_edition():
        expected_ac_tests += [
            'ACTestSecureAgentUpdaterTransport',
            'ACTestSecureNotificationSpoolerMessages',
        ]

    registered_plugins = sorted(watolib.ac_test_registry.keys())
    assert registered_plugins == sorted(expected_ac_tests)
