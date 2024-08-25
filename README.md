# VIN-ID-Contact

This is a system that establishes secret communication between vehicles. Each vehicle sends their VIN (vehicle information number) values, locations and its date-time. And also each vehicle gets other vehicles' sending values.

The .ino files are written by Arduino IDE software. These codes are testing 3 vehicles' communication. It comminicates with the XBee module. And the manager system gets all vehicles' informations and gives the sends the datas to the computer. The manager system is receiving and reading the datas from the Python software.
