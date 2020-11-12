"""Configuration basics."""

# This is a translation of what Apple generally uses when referring to a specifc TCC component,
# to what the PPPCP Payload keys are generally called.
KTCC_MAP = {'kTCCServiceAccessibility': 'Accessibility',
            'kTCCServiceAddressBook': 'AddressBook',
            'kTCCServiceAppleEvents': 'AppleEvents',
            'kTCCServiceCalendar': 'Calendar',
            'kTCCServiceCamera': 'Camera',
            'kTCCServiceFileProviderPresence': 'FileProviderPresence',
            'kTCCServiceListenEvent': 'ListenEvent',
            'kTCCServiceMediaLibrary': 'MediaLibrary',
            'kTCCServiceMicrophone': 'Microphone',
            'kTCCServicePhotos': 'Photos',
            'kTCCServicePostEvent': 'PostEvent',
            'kTCCServiceReminders': 'Reminders',
            'kTCCServiceScreenCapture': 'ScreenCapture',
            'kTCCServiceSpeechRecognition': 'SpeechRecognition',
            'kTCCServiceSystemPolicyAllFiles': 'SystemPolicyAllFiles',
            'kTCCServiceSystemPolicyDesktopFolder': 'SystemPolicyDesktopFolder',
            'kTCCServiceSystemPolicyDocumentsFolder': 'SystemPolicyDocumentsFolder',
            'kTCCServiceSystemPolicyDownloadsFolder': 'SystemPolicyDownloadsFolder',
            'kTCCServiceSystemPolicyNetworkVolumes': 'SystemPolicyNetworkVolumes',
            'kTCCServiceSystemPolicyRemovableVolumes': 'SystemPolicyRemovableVolumes',
            'kTCCServiceSystemPolicySysAdminFiles': 'SystemPolicySysAdminFiles'}

# Only two PPPCP Payloads can be set to let a standard user account be whitelisted without
# admin privileges. Applies to macOS 11+ only.
KTCC_ALLOW_STD_USER_PAYLOADS = ['ListenEvent', 'ScreenCapture']

# These payloads can only be set to 'Deny'.
KTCC_DENY_ONLY_PAYLOADS = ['Camera', 'Microphone']

# Allow only payloads
KTCC_ALLOW_ONLY_PAYLOADS = [_v for _k, _v in KTCC_MAP.items() if _v not in KTCC_ALLOW_STD_USER_PAYLOADS + KTCC_DENY_ONLY_PAYLOADS]

# From macOS 11+ the 'Allowed = True/False' payload key has been deprecated
# in favour of the 'Authorization = Allow/Deny/AllowStandardUserToSetSystemService'
# values.
