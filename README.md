# tccprofile
Scan the TCC databases and generate a PPPCP profile.

## Clone
`git clone https://github.com/carlashley/tccprofile`

## What it does
Scans the system and current user `Library/Application Support/com.apple.TCC/TCC.db` files for all of the apps/binaries that have been added to the `Security & Privacy` preferences pane by the user.
- Excludes the `Camera` and `Microphone` entries as these are `Deny` only payloads.
- Converts any `ListenEvent` and `ScreenRecording` entries over to `AllowStandardUserToSetSystemService` values.
- Converts the `csreq` blob value in the TCC database to a proper codesign identity value.
- Automatically creates the appropriate `AppleEvents` payload.

Generated profiles are only suitable for deploying to macOS 11+ systems - the `Allowed` value used prior to macOS 11 has been deprecated by Apple and is not supported in this utility. Deploying profiles to versions of macOS older than macOS 11 will likely result in disappointment.

## What it does not do
- Target specific applications that have not been added to the `Security & Privacy` preferences pane by the user.
- Implement the ability to `Deny` the `Camera` and `Microphone` services for specific apps.

## Usage
To properly scan the TCC databases, full disk access may need to be provided to the relevant terminal application (for example, Terminal, iTerm, etc).

```
[jappleseed@infiniteloop]:tccprofile # ./tccprofile -h
usage: tccprofile [-h] [--scan] [-t [[template] [[template] ...]]] [-o [path]]
                  [--description [description]]
                  [--display-name [display-name]] [--identifier [identifier]]
                  [--organization [organization]] [--remove-profile]
                  [--services [services] [[services] ...]] [--list-services]
                  [-v]
optional arguments:
  -h, --help            show this help message and exit
  --scan                Scan the TCC configuration (system and current user)
                        on this device.
  -t [[template] [[template] ...]], --template [[template] [[template] ...]]
                        Specify a template to generate a profile from.
  -o [path], --output [path]
                        Save mobileconfig profile to specified path.
  --description [description]
                        Payload description.
  --display-name [display-name]
                        Payload display name.
  --identifier [identifier]
                        Payload identifier. Recommend bundle-id style, for
                        example: 'org.example.foo'.
  --organization [organization]
                        Payload organization.
  --remove-profile      Allow the profile to be removed. Default is disallow
                        removal.
  --services [services] [[services] ...]
                        Services to include in profile if found in TCC
                        databases. Uses the service names as per Apple's PPPCP
                        payloads.
  --list-services       Lists supported services found in the TCC database.
  -v, --version         Display version number and license and exit.
```

## Templates
The `-t/--template` argument takes a template name (the basename of files in the `templates/included` or `templates/overrides` folder minus the file extension) and uses the template to generate a PPPCP profile.

If the application/binary path specified in the `path` and/or `receiver_path` keys is present on the system, then the codesign requirements will be generated from that path.
If either of the path values for these keys are not present, then it falls back to using the supplied codesign requirements specified in the template.

To override any included template, simply copy the template from `templates/included` and place it in `templates/overrides` and update the values for the keys you want to override.

Each template file must be prefixed with 'com.github.carlashley.tccprofile.' and it is recommended to use the application/binary name and `.yaml` (for example `vmware-fusion.yaml`) for the suffix and extension.

Each template file must consist of these `key: value` pairs:
```
ServiceName:
 - path: /Application/Path
   csreq: [output from codesign -dr - /Application/Path]
   identifier: [identifier value]
   identifier_type: [path or bundleID]
   allowed: [Allow/Deny/AllowStandardUserToSetSystemService]
   receiver_path: [AppleEvents receiver app path]
   apple_events_csreq: [output from codesign -dr - /Applications/Path for the AppleEvents receiver app]
   apple_events_identifier: [AppleEvents receiver app identifier value]
   apple_events_identifier_type: [path or bundleID]
```

### Example template
```
Accessibility:
  - path: /Applications/VMware Fusion.app
    csreq: identifier "com.vmware.fusion" and anchor apple generic and certificate 1[field.1.2.840.113635.100.6.2.6] /* exists */ and certificate leaf[field.1.2.840.113635.100.6.1.13] /* exists */ and certificate leaf[subject.OU] = EG7KH642X6
    identifier: com.vmware.fusion
    identifier_type: bundleID
    allowed: Allow
AppleEvents:
  - path: /Applications/VMware Fusion.app/Contents/Library/VMware Fusion Applications Menu.app
    csreq: identifier "com.vmware.fusionApplicationsMenu" and anchor apple generic and certificate 1[field.1.2.840.113635.100.6.2.6] /* exists */ and certificate leaf[field.1.2.840.113635.100.6.1.13] /* exists */ and certificate leaf[subject.OU] = EG7KH642X6
    identifier: com.vmware.fusionApplicationsMenu
    identifier_type: bundleID
    allowed: Allow
    receiver_path: /System/Library/CoreServices/System Events.app
    apple_events_csreq: identifier "com.apple.systemevents" and anchor apple
    apple_events_identifier: com.apple.systemevents
    apple_events_identifier_type: bundleID
SystemPolicyAllFiles:
  - path: /Applications/VMware Fusion.app
    csreq: identifier "com.vmware.fusion" and anchor apple generic and certificate 1[field.1.2.840.113635.100.6.2.6] /* exists */ and certificate leaf[field.1.2.840.113635.100.6.1.13] /* exists */ and certificate leaf[subject.OU] = EG7KH642X6
    identifier: com.vmware.fusion
    identifier_type: bundleID
    allowed: Allow
ScreenCapture:
  - path: /Applications/VMware Fusion.app
    csreq: identifier "com.vmware.fusion" and anchor apple generic and certificate 1[field.1.2.840.113635.100.6.2.6] /* exists */ and certificate leaf[field.1.2.840.113635.100.6.1.13] /* exists */ and certificate leaf[subject.OU] = EG7KH642X6
    identifier: com.vmware.fusion
    identifier_type: bundleID
    allowed: AllowStandardUserToSetSystemService
```

## Generating a profile based on templates
Generating a profile based on a template (or multiple templates) is done with the `-t/--template` arguments, then specifying the basic app name (the basename of the template without the file extension) as the template to use.

### Google Chrome and Discord (to file)
```
[jappleseed@infiniteloop]:tccprofile # ./tccprofile -t google-chrome discord -o googlediscord.mobileconfig
[jappleseed@infiniteloop]:tccprofile # ls -lha
total 168
drwxr-xr-x  13 jappleseed  staff   442B 12 Nov 21:05 .
drwxr-xr-x  11 jappleseed  staff   374B  7 Nov 14:00 ..
drwxr-xr-x  13 jappleseed  staff   442B 12 Nov 20:58 .git
-rw-r--r--   1 jappleseed  staff   1.8K  8 Nov 21:36 .gitignore
-rw-r--r--   1 jappleseed  staff    11K  1 Nov 20:47 LICENSE
-rw-r--r--   1 jappleseed  staff    16K 12 Nov 21:02 README.md
-rwxr-xr-x   1 jappleseed  staff   993B  1 Nov 20:47 build.sh
-rw-r--r--   1 jappleseed  staff   4.2K 12 Nov 21:05 googlediscord.mobileconfig
drwxr-xr-x   5 jappleseed  staff   170B 12 Nov 20:39 src
-rwxr-xr-x   1 jappleseed  staff    32K 12 Nov 20:43 tccprofile
drwxr-xr-x   4 jappleseed  staff   136B  8 Nov 17:43 templates
```

### Google Chrome (to standard out)
```
[jappleseed@infiniteloop]:tccprofile # ./tccprofile -t google-chrome
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>PayloadContent</key>
	<array>
		<dict>
			<key>PayloadDescription</key>
			<string>PPPCP profile</string>
			<key>PayloadDisplayName</key>
			<string>PPPCP profile</string>
			<key>PayloadIdentifier</key>
			<string>com.github.carlashley.tccprofile.8184B1CE-24D6-11EB-BCC4-ACDE48001122</string>
			<key>PayloadOrganization</key>
			<string>com.github.carlashley.tccprofile</string>
			<key>PayloadType</key>
			<string>com.apple.TCC.configuration-profile-policy</string>
			<key>PayloadUUID</key>
			<string>8184B1CE-24D6-11EB-BCC4-ACDE48001122</string>
			<key>PayloadVersion</key>
			<integer>1</integer>
			<key>Services</key>
			<dict>
				<key>ScreenCapture</key>
				<array>
					<dict>
						<key>Authorization</key>
						<string>AllowStandardUserToSetSystemService</string>
						<key>CodeRequirement</key>
						<string>(identifier "com.google.Chrome" or identifier "com.google.Chrome.beta" or identifier "com.google.Chrome.dev" or identifier "com.google.Chrome.canary") and certificate leaf = H"c9a99324ca3fcb23dbcc36bd5fd4f9753305130a"</string>
						<key>Identifier</key>
						<string>com.google.Chrome</string>
						<key>IdentifierType</key>
						<string>bundleID</string>
					</dict>
				</array>
				<key>SystemPolicyAllFiles</key>
				<array>
					<dict>
						<key>Authorization</key>
						<string>Allow</string>
						<key>CodeRequirement</key>
						<string>(identifier "com.google.Chrome" or identifier "com.google.Chrome.beta" or identifier "com.google.Chrome.dev" or identifier "com.google.Chrome.canary") and certificate leaf = H"c9a99324ca3fcb23dbcc36bd5fd4f9753305130a"</string>
						<key>Identifier</key>
						<string>com.google.Chrome</string>
						<key>IdentifierType</key>
						<string>bundleID</string>
					</dict>
				</array>
			</dict>
		</dict>
	</array>
	<key>PayloadDescription</key>
	<string>PPPCP Profile generated from TCC databases or templates.</string>
	<key>PayloadDisplayName</key>
	<string>PPPCP Profile Generated 2020-11-12-210207</string>
	<key>PayloadIdentifier</key>
	<string>com.github.carlashley.tccprofile</string>
	<key>PayloadOrganization</key>
	<string>com.github.carlashley.tccprofile</string>
	<key>PayloadRemovalDisallowed</key>
	<true/>
	<key>PayloadScope</key>
	<string>system</string>
	<key>PayloadType</key>
	<string>Configuration</string>
	<key>PayloadUUID</key>
	<string>8184B412-24D6-11EB-BCC4-ACDE48001122</string>
	<key>PayloadVersion</key>
	<integer>1</integer>
</dict>
</plist>
```

## Scanning
The `--scan` mode builds a list of installed applications as reported by `system_profiler`, as well as checking the `/System/Applications` and `/Applications` folders, and checks some common binary paths such as `/bin/`, `/usr/local/bin` and checks the code signature requirements for each item found.
This particular process can take several minutes to run.

The TCC databases are then checked for entries that have a service type that corresponds to the PPPCP services, and then creates the relevant information required to create a profile for each of those items found in the TCC databases.

If no code signature is found in the TCC database but the app is installed on the system, then the code signature requirements are used based on the information found from scanning for apps installed.


## Examples
### List Services
```
[jappleseed@infiniteloop]:tccprofile # ./tccprofile --list-services
Supported services found in TCC databases:
  Accessibility
  AppleEvents
  SystemPolicyAllFiles
  SystemPolicyDownloadsFolder
```
### Scan for AppleEvents
```
[jappleseed@infiniteloop]:tccprofile # ./tccprofile --scan --services AppleEvents
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>PayloadContent</key>
	<array>
		<dict>
			<key>PayloadDescription</key>
			<string>PPPCP profile</string>
			<key>PayloadDisplayName</key>
			<string>PPPCP profile</string>
			<key>PayloadIdentifier</key>
			<string>com.github.carlashley.tccprofile.A3F5F550-1C2B-11EB-B35D-ACDE48001122</string>
			<key>PayloadOrganization</key>
			<string>com.github.carlashley.tccprofile</string>
			<key>PayloadType</key>
			<string>com.apple.TCC.configuration-profile-policy</string>
			<key>PayloadUUID</key>
			<string>A3F5F550-1C2B-11EB-B35D-ACDE48001122</string>
			<key>PayloadVersion</key>
			<integer>1</integer>
			<key>Services</key>
			<dict>
				<key>AppleEvents</key>
				<array>
					<dict>
						<key>AEReceiverCodeRequirement</key>
						<string>identifier "com.apple.systemevents" and anchor apple</string>
						<key>AEReceiverIdentifier</key>
						<string>com.apple.systemevents</string>
						<key>AEReceiverIdentifierType</key>
						<string>bundleID</string>
						<key>Authorization</key>
						<string>Allow</string>
						<key>CodeRequirement</key>
						<string>identifier "com.vmware.fusionApplicationsMenu" and anchor apple generic and certificate 1[field.1.2.840.113635.100.6.2.6] /* exists */ and certificate leaf[field.1.2.840.113635.100.6.1.13] /* exists */ and certificate leaf[subject.OU] = EG7KH642X6</string>
						<key>Identifier</key>
						<string>com.vmware.fusionApplicationsMenu</string>
						<key>IdentifierType</key>
						<string>bundleID</string>
					</dict>
				</array>
			</dict>
		</dict>
	</array>
	<key>PayloadDescription</key>
	<string>PPPCP Profile generated from the System and Current user TCC databases.</string>
	<key>PayloadDisplayName</key>
	<string>PPPCP Profile Generated 2020-11-01-201852</string>
	<key>PayloadIdentifier</key>
	<string>com.github.carlashley.tccprofile</string>
	<key>PayloadOrganization</key>
	<string>com.github.carlashley.tccprofile</string>
	<key>PayloadRemovalDisallowed</key>
	<true/>
	<key>PayloadScope</key>
	<string>system</string>
	<key>PayloadType</key>
	<string>Configuration</string>
	<key>PayloadUUID</key>
	<string>A3F5F7DA-1C2B-11EB-B35D-ACDE48001122</string>
	<key>PayloadVersion</key>
	<integer>1</integer>
</dict>
</plist
```
### Scan for AppleEvents and write to file
```
[jappleseed@infiniteloop]:tccprofile # ./tccprofile --scan --services AppleEvents -o ~/Desktop/AppleEvents.mobileconfig
[jappleseed@infiniteloop]:tccprofile # ls -lha ~/Desktop
total 24
drwx------@  7 jappleseed  staff   224B  1 Nov 20:19 .
drwxr-xr-x+ 50 jappleseed  staff   1.6K  1 Nov 16:59 ..
-rw-r--r--@  1 jappleseed  staff   2.3K  1 Nov 20:19 AppleEvents.mobileconfig
```
### Scan for all services and write to file
```
[jappleseed@infiniteloop]:tccprofile # ./tccprofile --scan -o ~/Desktop/AllServices.mobileconfig
[jappleseed@infiniteloop]:tccprofile # ls -lha ~/Desktop
total 24
drwx------@  7 jappleseed  staff   224B  1 Nov 20:19 .
drwxr-xr-x+ 50 jappleseed  staff   1.6K  1 Nov 16:59 ..
-rw-r--r--@  1 jappleseed  staff   2.3K  1 Nov 20:21 AllServices.mobileconfig
```
### Override default values
```
[jappleseed@infiniteloop]:tccprofile # ./tccprofile --scan --services AppleEvents \
    --description "Full PPPCP configuration for macOS 11" \
    --display-name "PPPCP Config for macOS 11" \
    --identifier org.example.profile.pppcp.macos11 \
    --organization "Bag End Computing"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>PayloadContent</key>
	<array>
		<dict>
			<key>PayloadDescription</key>
			<string>PPPCP profile</string>
			<key>PayloadDisplayName</key>
			<string>PPPCP profile</string>
			<key>PayloadIdentifier</key>
			<string>org.example.profile.pppcp.macos11.FB279A88-1C2E-11EB-A6A0-ACDE48001122</string>
			<key>PayloadOrganization</key>
			<string>Bag End Computing</string>
			<key>PayloadType</key>
			<string>com.apple.TCC.configuration-profile-policy</string>
			<key>PayloadUUID</key>
			<string>FB279A88-1C2E-11EB-A6A0-ACDE48001122</string>
			<key>PayloadVersion</key>
			<integer>1</integer>
			<key>Services</key>
			<dict>
				<key>AppleEvents</key>
				<array>
					<dict>
						<key>AEReceiverCodeRequirement</key>
						<string>identifier "com.apple.systemevents" and anchor apple</string>
						<key>AEReceiverIdentifier</key>
						<string>com.apple.systemevents</string>
						<key>AEReceiverIdentifierType</key>
						<string>bundleID</string>
						<key>Authorization</key>
						<string>Allow</string>
						<key>CodeRequirement</key>
						<string>identifier "com.vmware.fusionApplicationsMenu" and anchor apple generic and certificate 1[field.1.2.840.113635.100.6.2.6] /* exists */ and certificate leaf[field.1.2.840.113635.100.6.1.13] /* exists */ and certificate leaf[subject.OU] = EG7KH642X6</string>
						<key>Identifier</key>
						<string>com.vmware.fusionApplicationsMenu</string>
						<key>IdentifierType</key>
						<string>bundleID</string>
					</dict>
				</array>
			</dict>
		</dict>
	</array>
	<key>PayloadDescription</key>
	<string>Full PPPCP configuration for macOS 11</string>
	<key>PayloadDisplayName</key>
	<string>PPPCP Config for macOS 11</string>
	<key>PayloadIdentifier</key>
	<string>org.example.profile.pppcp.macos11</string>
	<key>PayloadOrganization</key>
	<string>Bag End Computing</string>
	<key>PayloadRemovalDisallowed</key>
	<true/>
	<key>PayloadScope</key>
	<string>system</string>
	<key>PayloadType</key>
	<string>Configuration</string>
	<key>PayloadUUID</key>
	<string>FB279D1C-1C2E-11EB-A6A0-ACDE48001122</string>
	<key>PayloadVersion</key>
	<integer>1</integer>
</dict>
</plist>
```
