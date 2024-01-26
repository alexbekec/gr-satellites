"""
PYTHON EMBEDDED BLOCK: INSERT LENGTH BYTES
Alexander Bekec (bekec@vzlu.cz)

Function: Insertion of 2 bytes identifying length of the PDU for correct processing inside VCOM.
Input PDU in message format is 'measured' for length and recalculated bytes are inserted in the 
front of the PDU
"""

import numpy as np
from gnuradio import gr
import pmt

class insert_length_bytes(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    def __init__(self):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='PYTHON_DEMO: Insert length bytes',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        self.message_port_register_in(pmt.intern("pdu_in"))
        self.message_port_register_out(pmt.intern("pdu_out"))
        self.set_msg_handler(pmt.intern("pdu_in"), self.handle_msg)

    def handle_msg(self, msg):
        conv_msg = (pmt.to_python(msg)[1]).tolist()
        conv_msg_len = len(conv_msg)
        conv_msg_len_msb = conv_msg_len // 256
        conv_msg_len_lsb = conv_msg_len % 256
        conv_msg_out = [conv_msg_len_msb, conv_msg_len_lsb] + conv_msg
        conv_msg_out_len = len(conv_msg_out)
        pdu = pmt.cons(pmt.PMT_NIL,pmt.init_u8vector(conv_msg_out_len,(conv_msg_out)))

        self.message_port_pub(pmt.intern('pdu_out'), pdu)

