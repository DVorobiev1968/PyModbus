#!/usr/bin/env python
# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
from pymodbus.server.asynchronous import StartTcpServer
#from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
# --------------------------------------------------------------------------- #
# import the twisted libraries we need
# --------------------------------------------------------------------------- #
from twisted.internet.task import LoopingCall
# --------------------------------------------------------------------------- #
# import the payload builder
# --------------------------------------------------------------------------- #
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from collections import OrderedDict

from pymodbus.transaction import ModbusRtuFramer, ModbusBinaryFramer
# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
import logging

FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.WARNING)


def update_reads(a):
    log.debug("updating the context")
    context = a[0]
    fx = 0x6
    slave_id = 0x00
    address = 0x0
    for i in range(0,9):
        address=i
        values = context[slave_id].getValues(fx, address, 4)
        decoder = BinaryPayloadDecoder.fromRegisters(values,
                                                 byteorder=Endian.Little,
                                                 wordorder=Endian.Little)
        value_64float=decoder.decode_64bit_float()
        print("{0};{1};{2}".format(slave_id,address,value_64float))


def run_server():
    # ----------------------------------------------------------------------- #
    # build your payload
    # ----------------------------------------------------------------------- #
    builder = BinaryPayloadBuilder(byteorder=Endian.Little,
                                   wordorder=Endian.Little)
    for i in range(0,9):
        builder.add_64bit_float(100.0)
    # ----------------------------------------------------------------------- #
    # use that payload in the data store
    # ----------------------------------------------------------------------- #
    # Here we use the same reference block for each underlying store.
    # ----------------------------------------------------------------------- #
    block = ModbusSequentialDataBlock(1, builder.to_registers())
    store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
    context = ModbusServerContext(slaves=store,single=True)
    # ----------------------------------------------------------------------- #
    # initialize the server information
    # ----------------------------------------------------------------------- #
    # If you don't set this or any fields, they are defaulted to empty strings.
    # ----------------------------------------------------------------------- #
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '2.3.0'
    # ----------------------------------------------------------------------- #
    # run the server you want
    # ----------------------------------------------------------------------- #
    time = 3  # 5 seconds delay
    loop = LoopingCall(f=update_reads, a=(context,))
    loop.start(time, now=False)  # initially delay by time
    print("slave_id;addr;value_64float\n")
    StartTcpServer(context, identity=identity, address=("localhost", 5020))


if __name__ == "__main__":
    run_server()
