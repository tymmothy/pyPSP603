"""psp603.py

This module provides an API for controlling GW-Instek PSP-603
power supplies over a serial port.

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
import time

class PSP603(object):

    """ GW Instek PSP-603 Power Supply Interface Class.

    This class allows control of PSP-603 power supplies via serial interface.
    To use, instantiate this class with a (pySerial) serial port object.

    Example:

    >>> import serial
    >>> serial_port = serial.Serial('/dev/ttyS0', 2400)
    >>> psp603 = PSP603(serial_port)
    >>> psp603.voltage = 4.2
    >>> psp603.relay = True
    >>> print psp603.current

    would set the output voltage, close the output relay, then print the
    output current.

    Note:
        This module is not derived from the Serial class specifically to allow
        alternate methods of communication (e.g. the RFC2217Serial class).
    """

    def __init__(self, serial_port):
        """ Create a PSP603 object, binding it to the given in serial port.

        Args:
            serial_port (Serial / RFC2217Serial): Serial port instance.
        """
        self._serial = serial_port

    def send_command(self, cmd, wait = None):
        """ Send a command to the PSU.

        Args:
            cmd (str):  The command to send.
            wait (float):  Number of seconds to sleep after sending command.
        """
        self._serial.write(cmd + "\x0d")
        if wait:
            time.sleep(wait)

    def receive(self):
        """ Receive a response (terminated by new line) from the PSU.

        Note:
            This function will block until a complete line is recieved.
            Presently there is no way to specify a timeout.
        """
        response = ''
        while not response.endswith("\x0a"):
            # Read in a char from the port.
            response += self._serial.read()

        return response

    @property
    def voltage(self):
        """Output voltage, in volts.  Read/write float value."""
        self.send_command('V')
        s = self.receive()
        return float(s[1:])

    @voltage.setter
    def voltage(self, value):
        self.send_command("SV %05.2F" % (value), 0.6)

    @property
    def voltage_limit(self):
        """Voltage limit, in volts.  Read/write float value."""
        self.send_command('U')
        s = self.receive()
        return float(s[1:])

    @voltage_limit.setter
    def voltage_limit(self, value):
        self.send_command("SU %02d" % (value), 0.6)

    @property
    def current(self):
        """Output current, in amps.  Read-only float value."""
        # Note: Output current is read-only -- no setter.
        self.send_command('A')
        s = self.receive()
        return float(s[1:])

    @property
    def current_limit(self):
        """Current limit, in amps.  Read/write float value."""
        self.send_command('I')
        s = self.receive()
        return float(s[1:])

    @current_limit.setter
    def current_limit(self, value):
        self.send_command("SI %04.2F" % (value), 0.6)

    @property
    def power(self):
        """Output power, in watts. Read-only float value."""
        self.send_command('W')
        s = self.receive()
        return float(s[1:])

    @property
    def power_limit(self):
        """Power limit, in watts.  Read/write float value. """
        self.send_command("P")
        s = self.receive()
        return float(s[1:])

    @power_limit.setter
    def power_limit(self, value):
        self.send_command("SW %03d" % (value))

    @property
    def status(self):
        """Basic PSU status.  Read-only dict value.

        The dict has the following keys:
            relay        (bool) Relay status; output power is "ON" if True.
            overheated   (bool) PSU is overheating if True.
            fine_control (bool) PSU is in "fine knob control" mode if True.
            knob_locked  (bool) PSU knob is locked out if True.
            remote       (bool) PSU is in "remote" mode if True.
            locked       (bool) PSU is in "locked" mode if True.
        """
        self.send_command('F')
        s = self.receive()

        return { 'relay' : True if s[1] == '1' else False,
                 'overheated' : True if s[2] == '1' else False,
                 'fine_control' : True if s[3] == '1' else False,
                 'knob_locked' : True if s[4] == '1' else False,
                 'remote' : True if s[5] == '1' else False,
                 'locked' : True if s[6] == '1' else False }

    @property
    def full_status(self):
        """Full PSU status.  Read-only dict value.

        The dict has the following keys:
            voltage       (float) Present output voltage, in volts.
            current       (float) Present output current, in amps.
            power         (float) Present output power, in watts.
            voltage_limit (float) Voltage limit, in volts.
            current_limit (float) Current limit, in amps.
            power_limit   (float) Power limit, in watts.
            relay         (bool) Relay status; output power is "ON" if True.
            overheated    (bool) PSU is overheating if True.
            fine_control  (bool) PSU is in "fine knob control" mode if True.
            knob_locked   (bool) PSU knob is locked out if True.
            remote        (bool) PSU is in "remote" mode if True.
            locked        (bool) PSU is in "locked" mode if True.
        """
        self.send_command('L')
        s = self.receive()

        return {
            'voltage' : float(s[1:6]),
            'current' : float(s[7:12]),
            'power' : float(s[13:18]),
            'voltage_limit' : float(s[19:21]),
            'current_limit' : float(s[22:26]),
            'power_limit' : float(s[27:30]),
            'relay' : True if s[31] == '1' else False,
            'overheated' : True if s[32] == '1' else False,
            'fine_control' : True if s[33] == '1' else False,
            'knob_locked' : True if s[34] == '1' else False,
            'remote' : True if s[35] == '1' else False,
            'locked' : True if s[36] == '1' else False }

    @property
    def overheated(self):
        """True if power supply is overheating.  Read-only bool value."""
        return self.status.get('overheated')

    @property
    def fine_control(self):
        """True if knob is in fine control mode.  Read-only bool value."""
        return self.status.get('fine_control')

    @property
    def knob_locked(self):
        """True if knob is locked.  Read-only bool value."""
        return self.status.get('knob_locked')

    @property
    def remote(self):
        """True if PSU is in remote mode.  Read-only bool value. """
        return self.status.get('remote')

    @property
    def locked(self):
        """True if PSU is locked.  Read-only boolean value."""
        return self.status.get('locked')

    @property
    def relay(self):
        """When true, relay is closed.  Read/write bool value."""
        return self.status.get('relay')

    @relay.setter
    def relay(self, value):
        if value == True:
            self.send_command('KOE', 0.5)
        else:
            self.send_command('KOD', 0.5)
        # Note: Invert relay ("KO") easily emulated.

    def save_param(self):
        """ Save the current PSU parameter settings to internal EEPROM. """
        self.send_command('EEP', 1.0);
