# sim-analyzer 1.0.0
Tool to data recovery from sim cards dumps

## Usage:
```
simanalysis.py [-h] [--root [ROOT]] [--tree] [--iccid] [--contacts] [--messages] [--output [OUTPUT]]

optional arguments:
  -h, --help show this help message and exit
  --root [ROOT] path to dump root (this directory should contain '3F00' directory)
  --tree list contents of sim dump in a tree-like format
  --iccid read ICCID number
  --contacts read contacts
  --messages read messages
  --output [OUTPUT] select output [default, json, csv]
  ```

## Examples:

### Help
Show help message and exit<br />
Command: ```simanalysis.py --help```

### Version
Print current version
Command: ```simanalysis.py --version```

### Directory tree
Print contents of sim dump in a tree-like format<br />
Command: ```simanalysis.py --root ~/SimDump --tree```<br />
Result:
```
+-SimDump/
  +-3F00/
    +-2FA0
    +-2FE2
    +-7F10/
    | +-6F3A
```
### ICCID
Read ICCID number<br />
Command: ```simanalysis.py --root ~/SimDump --iccid```<br />
Result: ```8901262851479226992f```

### Messages
Read messages<br />
Command: ```simanalysis.py --root ~/SimDump --messages```<br />
Result:
```
Don't forget to change your clocks forward 1 hour.
LOVE  YOU
```

Command: ```simanalysis.py --root ~/SimDump --messages --output json```<br />
Result: json array with messages data

Command: ```simanalysis.py --root ~/SimDump --messages --output csv```<br />
Result: csv with messages data<br />

Available message fields (both json and csv):<br />
* \_\_type\_\_: str
* deleted: bool 
* smsc_address_type: hex (91 indicates international format of the phone number)
* service_center_number: str
* sender_number_type: hex
* sender_number: str
* tp_protocol_identifier: hex
* tp_data_coding_scheme: hex
* tp_sc_time_stamp: datetime
* user_data: str (message text)
* bulk_data: str (whole encoded record)
      
### Contacts
Command: ```simanalysis.py --root ~/SimDump --contacts```<br />
Result:
```
Customer Care::*+009360035
Voicemail::*+056315076
Home::+3064010503
David House::+4169325548
```
      
Command: ```simanalysis.py --root ~/SimDump --contacts --output json```<br />
Result: json array with contacts data<br />

Command: ```simanalysis.py --root ~/SimDump --contacts --output csv```<br />
Result: csv with contacts data<br />

Available contact fields (both json and csv):<br />
* \_\_type\_\_: str
* contact_name: str
* phone_number: str
