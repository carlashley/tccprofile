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
usage: tccprofile [-h] [--scan] [-o [path]] [--description [description]]
                  [--display-name [display-name]] [--identifier [identifier]]
                  [--organization [organization]] [--remove-profile]
                  [--services [services] [[services] ...]] [--list-services]
                  [-v]

optional arguments:
  -h, --help            show this help message and exit
  --scan                Scan the TCC configuration (system and current user)
                        on this device.
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
  --remove-profile      Allow the profile to be removed.
  --services [services] [[services] ...]
                        Services to include in profile if found in TCC
                        databases. Uses the service names as per Apple's PPPCP
                        payloads.
  --list-services       Lists supported services found in the TCC database.
  -v, --version         Display version number and license and exit.
```

## Example
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
