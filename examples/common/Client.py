#!/usr/bin/env python
"""
Pymodbus Synchronous Client Examples
--------------------------------------------------------------------------

The following is an example of how to use the synchronous modbus client
implementation from pymodbus.

It should be noted that the client can also be used with
the guard construct that is available in python 2.5 and up::

    with ModbusClient('127.0.0.1') as client:
        result = client.read_coils(1,10)
        print result
"""
# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
import random

from pymodbus.constants import Endian

from pymodbus.payload import BinaryPayloadBuilder

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
# from pymodbus.client.sync import ModbusUdpClient as ModbusClient
# from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time
# --------------------------------------------------------------------------- #
# configure the client logging
# --------------------------------------------------------------------------- #
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT = 0x0

def run_client_2():
    client = ModbusClient('localhost', port=5020)
    client.connect()
    log.debug("Read Write 32 and 64 bit value to holding registers")
    builder = BinaryPayloadBuilder(byteorder=Endian.Little,
                                   wordorder=Endian.Little)
    for i in range (0,9):
        real_value = random.randint(1, 100) / 3
        builder.add_64bit_float(real_value)
        payload = builder.to_registers()
        payload = builder.build()
        rq = client.write_registers(i, payload, skip_encode=True, unit=UNIT)
        if not rq.isError():
            time.sleep(1)
            builder.reset()
        else:
            log.error("Error write_registers:")
            break
    client.close()

def run_client_1():
    client = ModbusClient('localhost', port=5020)
    client.connect()
    log.debug("Read Write to multiple holding registers")
    for i in range (1,20):
        log.debug("Write to multiple holding registers and read back")
        real_value=i
        rq = client.write_register(i, real_value, unit=UNIT)
        assert (not rq.isError())       # test that we are not an error
        time.sleep(1)
    client.close()

def run_client():
    client = ModbusClient('localhost', port=5020)
    client.connect()
    log.debug("Read to multiple holding registers")
    for i in range (1,20):
        rr = client.read_holding_registers(1, 10, unit=UNIT)
        for j in range (1,10): print("{0:f};".format(rr.registers[j]))
        print("\n")
        time.sleep(1)
    client.close()

def run_sync_client():
    client = ModbusClient('localhost', port=5020)
    client.connect()
    log.debug("Reading Coils")
    rr = client.read_coils(1, 1, unit=UNIT)
    log.debug(rr)

    log.debug("Write to a Coil and read back")
    rq = client.write_coil(0, True, unit=UNIT)
    rr = client.read_coils(0, 1, unit=UNIT)
    assert(not rq.isError())     # test that we are not an error
    assert(rr.bits[0] == True)          # test the expected value

    log.debug("Write to multiple coils and read back- test 1")
    rq = client.write_coils(1, [True]*8, unit=UNIT)
    assert(not rq.isError())     # test that we are not an error
    rr = client.read_coils(1, 21, unit=UNIT)
    assert(not rr.isError())     # test that we are not an error
    resp = [True]*21

    # If the returned output quantity is not a multiple of eight,
    # the remaining bits in the final data byte will be padded with zeros
    # (toward the high order end of the byte).

    resp.extend([False]*3)
    assert(rr.bits == resp)         # test the expected value

    log.debug("Write to multiple coils and read back - test 2")
    rq = client.write_coils(1, [False]*8, unit=UNIT)
    rr = client.read_coils(1, 8, unit=UNIT)
    assert(not rq.isError())     # test that we are not an error
    assert(rr.bits == [False]*8)         # test the expected value

    log.debug("Read discrete inputs")
    rr = client.read_discrete_inputs(0, 8, unit=UNIT)
    assert(not rq.isError())     # test that we are not an error

    log.debug("Write to a holding register and read back")
    rq = client.write_register(1, 10, unit=UNIT)
    rr = client.read_holding_registers(1, 1, unit=UNIT)
    assert(not rq.isError())            # test that we are not an error
    assert(rr.registers[0] == 10)       # test the expected value
    print("rr:{0:f}\n".format(rr.registers[0]))

    log.debug("Write to multiple holding registers and read back")
    rq = client.write_registers(1, [10]*8, unit=UNIT)
    rr = client.read_holding_registers(1, 8, unit=UNIT)
    assert(not rq.isError())     # test that we are not an error
    assert(rr.registers == [10]*8)      # test the expected value
    for i in range (1,8): print("{0:f};".format(rr.registers[i]))
    print("\n")

    log.debug("Read input registers")
    rr = client.read_input_registers(1, 8, unit=UNIT)
    assert(not rq.isError())     # test that we are not an error

    arguments = {
        'read_address':    1,
        'read_count':      8,
        'write_address':   1,
        'write_registers': [20]*8,
    }
    log.debug("Read write registeres simulataneously")
    rq = client.readwrite_registers(unit=UNIT, **arguments)
    rr = client.read_holding_registers(1, 8, unit=UNIT)
    assert(not rq.isError())     # test that we are not an error
    assert(rq.registers == [20]*8)      # test the expected value
    assert(rr.registers == [20]*8)      # test the expected value

    # ----------------------------------------------------------------------- #
    # close the client
    # ----------------------------------------------------------------------- #
    client.close()


if __name__ == "__main__":
    # run_sync_client()

    run_client_2()
