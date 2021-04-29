# --------------------------------------------------------------------------- #
# import the payload builder
# --------------------------------------------------------------------------- #
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

def code_example():
    builder = BinaryPayloadBuilder(byteorder=Endian.Little,
                                   wordorder=Endian.Little)
    builder.add_32bit_float(2283899.40)
    payload = builder.to_registers()
    decoder = BinaryPayloadDecoder.fromRegisters(payload,
                                                 byteorder=Endian.Little,
                                                 wordorder=Endian.Little)
    value_32float = decoder.decode_32bit_float()
    builder.reset()

    builder.add_64bit_float(-1.23999999999)
    payload = builder.to_registers()
    decoder = BinaryPayloadDecoder.fromRegisters(payload,
                                                 byteorder=Endian.Little,
                                                 wordorder=Endian.Little)
    value_64float = decoder.decode_64bit_float()
    builder.reset()
    str = "Temporary String"
    builder.add_string(str)
    payload = builder.to_registers()
    decoder = BinaryPayloadDecoder.fromRegisters(payload,
                                                 byteorder=Endian.Little,
                                                 wordorder=Endian.Little)
    val_str = decoder.decode_string(len(str))
    print("value_32float: {0:10.10f}\nvalue_64float: {1:20.20f}\nval_str: {2:<30s}\n".format(value_32float, value_64float, val_str))

if __name__ == "__main__":
    code_example()