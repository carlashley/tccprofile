# tccprofile
Scan the TCC databases and generate a PPPCP profile.

## Clone
`git clone https://github.com/carlashley/tccprofile`

## Usage
To properly scan the TCC databases, full disk access may need to be provided to the relevant terminal application (for example, Terminal, iTerm, etc).

```
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
                        databases. Uses the service name as the argument. For
                        example 'Accessibility AppleEvents'
  --list-services       Lists supported services found in the TCC database.
  -v, --version         Display version number and license and exit.
  ```
