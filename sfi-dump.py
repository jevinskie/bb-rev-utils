#!/usr/bin/env python

import sys
from array import array
from construct import *

sfi_header = Struct("sfi_header",
    ULInt32("magic"),
    ULInt32("version"),
)

section_header = Struct("section_header",
    ULInt32("id"),
    ULInt32("size"),
    ULInt32("version"),
    Array(lambda ctx: ctx.size - 0x10, ULInt8("data")),
)

sfi_file = Struct("sfi_file",
    sfi_header,
    GreedyRange(section_header),
)

bar = sfi_file.parse_stream(open(sys.argv[1]))
#print bar

i = 0

for sec in bar.section_header:
    print "id: %x" % sec.id
    print "size: %x" % sec.size
    print "version: %x" % sec.version
    f = open("section-%x-%d.bin" % (sec.id, i), 'wb')
    array('B', sec.data).tofile(f)
    f.close()
    i += 1

