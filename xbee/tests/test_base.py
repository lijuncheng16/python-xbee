#! /usr/bin/python
"""
test_xbee.py

By Paul Malmsten, 2010
pmalmsten@gmail.com

Tests the XBeeBase superclass module for XBee API conformance.
"""
import unittest
from xbee.base import XBeeBase
from xbee.tests.Fake import FakeDevice, FakeReadDevice

class TestWriteToDevice(unittest.TestCase):
    """
    XBeeBase class should properly write binary data in a valid API
    frame to a given serial device.
    """
    
    def test_write(self):
        """
        write method should write the expected data to the serial
        device
        """
        device = FakeDevice()
        
        xbee = XBeeBase(device)
        xbee.write('\x00')
        
        # Check resuting state of fake device
        expected_frame = '\x7E\x00\x01\x00\xFF'
        self.assertEqual(device.data, expected_frame)
        
    def test_write_again(self):
        """
        write method should write the expected data to the serial
        device
        """
        device = FakeDevice()
        
        xbee = XBeeBase(device)
        xbee.write('\x00\x01\x02')
        
        # Check resuting state of fake device
        expected_frame = '\x7E\x00\x03\x00\x01\x02\xFC'
        self.assertEqual(device.data, expected_frame)
        
class TestReadFromDevice(unittest.TestCase):
    """
    XBeeBase class should properly read and extract data from a valid
    API frame
    """
    def test_read(self):
        """
        wait_for_frame should properly read a frame of data
        """
        device = FakeReadDevice('\x7E\x00\x01\x00\xFF')
        xbee = XBeeBase(device)
        
        frame = xbee.wait_for_frame()
        self.assertEqual(frame.data, '\x00')
        
    def test_read_invalid_followed_by_valid(self):
        """
        wait_for_frame should skip invalid data
        """
        device = FakeReadDevice(
            '\x7E\x00\x01\x00\xFA' + '\x7E\x00\x01\x05\xFA')
        xbee = XBeeBase(device)
        
        frame = xbee.wait_for_frame()
        self.assertEqual(frame.data, '\x05')
        
class TestNotImplementedFeatures(unittest.TestCase):
    """
    In order to properly use the XBeeBase class for most situations,
    it must be subclassed with the proper attributes definined. If
    this is not the case, then a NotImplemented exception should be
    raised as appropriate.
    """
    
    def setUp(self):
        """
        Set up a base class XBeeBase object which does not have 
        api_commands or api_responses defined
        """
        self.xbee = XBeeBase(None)
    
    def test_build_command(self):
        """
        build_command should raise NotImplemented
        """
        self.assertRaises(NotImplementedError, self.xbee.build_command, "at")
        
    def test_split_response(self):
        """
        split_command should raise NotImplemented
        """
        self.assertRaises(NotImplementedError, self.xbee.split_response, "\00")
        
    def test_shorthand(self):
        """
        Shorthand calls should raise NotImplementedError
        """
        try:
            self.xbee.at
        except NotImplementedError:
            pass
        else:
            self.fail("Shorthand call on XBeeBase base class should raise NotImplementedError")
            
class TestAsyncCallback(unittest.TestCase):
    """
    XBeeBase constructor should accept an optional callback function 
    argument. When provided, this will put the module into a threaded
    mode, in which it will call the provided function with any API
    frame data received.
    
    As it would be very difficult to sanely test an asynchonous callback
    routine with a synchronous test process, proper callback behavior
    is not tested automatically at this time. Theoretically, the
    callback implementation logic is simple, but use it at your own risk.
    """
    
    def setUp(self):
        self.xbee = None
        self.serial = FakeReadDevice([])
        self.callback = lambda data: None
    
    def test_provide_callback(self):
        """
        XBeeBase constructor should accept a callback function
        """
        self.xbee = XBeeBase(self.serial, callback=self.callback)
        
if __name__ == '__main__':
    unittest.main()
