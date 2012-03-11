#!/usr/bin/python

"""
psp603_test.py

GW-Instek PSP-603 Serial-controllable power supply class testing code.

PLEASE DISCONNECT ANYTHING FROM THE PSU THAT MIGHT BE DAMAGED BY HIGH VOLTAGE!

Usage:
    python psp603_test.py <serial port name>

Copyright (c) 2011-2012, Timothy Twillman
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY TIMOTHY TWILLMAN ''AS IS'' AND ANY EXPRESS
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN
NO EVENT SHALL TIMOTHY TWILLMAN OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are
those of the authors and should not be interpreted as representing official
policies, either expressed or implied, of Timothy Twillman.
"""

from psp603 import PSP603

if __name__ == "__main__":
    import serial
    import sys

    if len(sys.argv) < 2:
        print >> sys.stderr, __doc__
        sys.exit(1)

    serial_port = sys.argv[1]

    if serial_port.startswith("rfc2217://"):
        serial_device = serial.serial_for_url(sys.argv[1], 2400)
    else:
        serial_device = serial.Serial(sys.argv[1], 2400)

    psu = PSP603(serial_device)

    print "Output Voltage: %f V" % psu.voltage
    print "Output Current: %f A" % psu.current
    print "Output Power: %f W" % psu.power
    print "Limit Voltage: %f V" % psu.voltage_limit
    print "Limit Current: %f A" % psu.current_limit
    print "Limit Power: %f W" % psu.power_limit

    print "Relay: %s" % psu.relay
    print "Overheating: %s" % psu.overheated
    print "Fine Knob Mode: %s" % psu.fine_control
    print "Remote Mode: %s" % psu.remote
    print "Knob Locked: %s" % psu.knob_locked
    print "Locked: %s" % psu.locked

    print psu.full_status

    psu.relay = False

    for i in range (0, 10, 2):
        current = i * 0.1
        print "Setting Current Limit to %5.2f..." % current
        psu.current_limit = current

    for i in range (10, 0, -2):
        current = i * 0.1
        print "Setting Current Limit to %5.2f..." % current
        psu.current_limit = current

    current = .5
    print "Setting Current Limit to %5.2f..." % current
    psu.current_limit = current

    print "Setting Output Voltage to 0..."
    psu.voltage = 0

    for i in range (0, 60, 12):
        voltage = i
        print "Setting Voltage Limit to %5.2f..." % voltage
        psu.voltage_limit = voltage

    for i in range (60, 0, -12):
        voltage = i
        print "Setting Voltage Limit to %5.2f..." % voltage
        psu.voltage_limit = voltage

    voltage = 60
    print "Setting Voltage Limit to %5.2f..." % voltage
    psu.voltage_limit = voltage

    for i in range (0, 5):
        print "Setting Output Voltage to 0.0..."
        psu.voltage = 0.0

        while psu.voltage != 0.0:
            # Wait for output to settle
            print "Output Voltage: %f V" % psu.voltage
            print "Output Wattage: %f W" % psu.power

        for i in range (0, 60, 12):
            voltage = i
            print "Setting Output Voltage to %5.2f..." % voltage
            psu.voltage = voltage

    print "Setting Output Voltage to 0..."
    psu.voltage = 0

    while psu.voltage != 0.0:
        print "Output Voltage: %f V" % psu.voltage
        print "Output Wattage: %f W" % psu.power

    print "Inverting relay."
    psu.relay = not psu.relay
    print "Turning relay off."
    psu.relay = False
