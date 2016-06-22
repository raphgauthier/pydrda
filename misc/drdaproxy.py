#!/usr/bin/env python3
##############################################################################
# The MIT License (MIT)
#
# Copyright (c) 2016 Hajime Nakagami
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
##############################################################################
import sys
import socket
import binascii

CODE_POINT = {
    0x1041: 'EXCSAT',
    0x1055: 'SYNCCTL',
    0x1069: 'SYNCRSY',
    0x106D: 'ACCSEC',
    0x106E: 'SECCHK',
    0x106F: 'SYNCLOG',
    0x2001: 'ACCRDB',
    0x2002: 'BGNBND',
    0x2004: 'BNDSQLSTT',
    0x2005: 'CLSQRY',
    0x2006: 'CNTQRY',
    0x2007: 'DRPPKG',
    0x2008: 'DSCSQLSTT',
    0x2009: 'ENDBND',
    0x200A: 'EXCSQLIMM',
    0x200B: 'EXCSQLSTT',
    0x2014: 'EXCSQLSET',
    0x200C: 'OPNQRY',
    0x200D: 'PRPSQLSTT',
    0x200E: 'RDBCMM',
    0x200F: 'RDBRLLBCK',
    0x2010: 'REBIND',
    0x2012: 'DSCRDBTBL',
    0x2412: 'SQLDTA',
    0x2413: 'SQLDTARD',
    0x2414: 'SQLSTT',
    0x2450: 'SQLATTR',
    0x2419: 'SQLSTTVRB',
    0x241A: 'QRYDSC',
    0x241B: 'QRYDTA',
    0x240E: 'SQLRSLRD',
    0x240B: 'SQLCINRD',
    0x14AC: 'ACCSECRD',
    0x1403: 'AGENT',
    0x000C: 'CODPNT',
    0x0064: 'CODPNTDR',
    0x2435: 'CSTMBCS',
    0x119D: 'CCSIDDBC',
    0x119E: 'CCSIDMBC',
    0x14CC: 'CCSIDMGR',
    0x1C08: 'UNICODEMGR',
    0x119C: 'CCSIDSBC',
    0x1444: 'CMNAPPC',
    0x147C: 'CMNSYNCPT',
    0x1474: 'CMNTCPIP',
    0x1C01: 'XAMGR',
    0x2135: 'CRRTKN',
    0x213B: 'TRGDFTRT',
    0x1458: 'DICTIONARY',
    0x119B: 'DEPERRCD',
    0x2101: 'DSCERRCD',
    0x1443: 'EXCSATRD',
    0x115E: 'EXTNAM',
    0x2418: 'FIXROWPRC',
    0x2410: 'FRCFIXROW',
    0x2417: 'LMTBLKPRC',
    0x1404: 'MGRLVLLS',
    0x1473: 'MGRLVLN',
    0x1900: 'MONITOR',
    0x1C00: 'MONITORRD',
    0x11DE: 'NEWPASSWORD',
    0x11A1: 'PASSWORD',
    0x2125: 'PKGDFTCST',
    0x2109: 'PKGID',
    0x2141: 'MAXBLKEXT',
    0x2140: 'MAXRSLCNT',
    0x2142: 'RSLSETFLG',
    0x2105: 'RDBCMTOK',
    0x2112: 'PKGNAMCT',
    0x2139: 'PKGSNLST',
    0x113F: 'PRCCNVCD',
    0x112E: 'PRDID',
    0x2415: 'OUTOVR',
    0x2147: 'OUTOVROPT',
    0x210D: 'PKGCNSTKN',
    0x2104: 'PRDDTA',
    0x215B: 'QRYINSID',
    0x2132: 'QRYBLKCTL',
    0x2114: 'QRYBLKSZ',
    0x2102: 'QRYPRCTYP',
    0x215D: 'QRYCLSIMP',
    0x215E: 'QRYCLSRLS',
    0x215F: 'QRYOPTVAL',
    0x213A: 'NBRROW',
    0x2111: 'OUTEXP',
    0x2138: 'PRCNAM',
    0x2150: 'QRYATTUPD',
    0x240F: 'RDB',
    0x210F: 'RDBACCCL',
    0x211A: 'RDBALWUPD',
    0x213C: 'QRYRELSCR',
    0x2152: 'QRYSCRORN',
    0x213D: 'QRYROWNBR',
    0x2153: 'QRYROWSNS',
    0x213E: 'QRYRFRTBL',
    0x2149: 'QRYATTSCR',
    0x2157: 'QRYATTSNS',
    0x2154: 'QRYBLKRST',
    0x2156: 'QRYROWSET',
    0x2155: 'QRYRTNDTA',
    0x2103: 'RDBINTTKN',
    0x2110: 'RDBNAM',
    0x2108: 'RDBCOLID',
    0x112D: 'RSCNAM',
    0x111F: 'RSCTYP',
    0x1127: 'RSNCOD',
    0x14C1: 'RSYNCMGR',
    0x2116: 'RTNSQLDA',
    0x2146: 'TYPSQLDA',
    0x11A4: 'SECCHKCD',
    0x11A2: 'SECMEC',
    0x1440: 'SECMGR',
    0x1196: 'SECMGRNM',
    0x11DC: 'SECTKN',
    0x2148: 'RTNEXTDTA',
    0x115D: 'SPVNAM',
    0x2407: 'SQLAM',
    0x2408: 'SQLCARD',
    0x211F: 'SQLCSRHLD',
    0x2411: 'SQLDARD',
    0x1147: 'SRVCLSNM',
    0x1153: 'SRVDGN',
    0x244E: 'SRVLST',
    0x116D: 'SRVNAM',
    0x115A: 'SRVRLSLV',
    0x2121: 'STTDECDEL',
    0x2120: 'STTSTRDEL',
    0x143C: 'SUPERVISOR',
    0x11B4: 'SVCERRNO',
    0x1149: 'SVRCOD',
    0x14C0: 'SYNCPTMGR',
    0x114A: 'SYNERRCD',
    0x002F: 'TYPDEFNAM',
    0x0035: 'TYPDEFOVR',
    0x2115: 'UOWDSP',
    0x11A0: 'USRID',
    0x1144: 'VRSNAM',
    0x2113: 'PKGNAMCSN',
    0x2160: 'DIAGLVL',
    0x220A: 'DSCINVRM',
    0x121C: 'CMDATHRM',
    0x1254: 'CMDCHKRM',
    0x1250: 'CMDNSPRM',
    0x1232: 'AGNPRMRM',
    0x2208: 'BGNBNDRM',
    0x220D: 'ABNUOWRM',
    0x2201: 'ACCRDBRM',
    0x124B: 'CMDCMPRM',
    0x1210: 'MGRLVLRM',
    0x1218: 'MGRDEPRM',
    0x220C: 'ENDUOWRM',
    0x1253: 'OBJNSPRM',
    0x1245: 'PRCCNVRM',
    0x1251: 'PRMNSPRM',
    0x2206: 'PKGBNARM',
    0x2209: 'PKGBPARM',
    0x2202: 'QRYNOPRM',
    0x220F: 'QRYPOPRM',
    0x2207: 'RDBACCRM',
    0x1219: 'SECCHKRM',
    0x221A: 'RDBAFLRM',
    0x22CB: 'RDBATHRM',
    0x2204: 'RDBNACRM',
    0x2211: 'RDBNFNRM',
    0x2218: 'RDBUPDRM',
    0x1233: 'RSCLMTRM',
    0x124C: 'SYNTAXRM',
    0x125F: 'TRGNSPRM',
    0x1252: 'VALNSPRM',
    0x2213: 'SQLERRRM',
    0x2205: 'OPNQRYRM',
    0x220B: 'ENDQRYRM',
    0x220E: 'DTAMCHRM',
    0x2212: 'OPNQFLRM',
    0x2219: 'RSLSETRM',
    0x221D: 'CMDVLTRM',
    0x2225: 'CMMRQSRM',
    0x146C: 'EXTDTA',
    0x0010: 'FDODSC',
    0x147A: 'FDODTA',
    0x2118: 'FDODSCOFF',
    0x212B: 'FDOPRMOFF',
    0x212A: 'FDOTRPOFF',
    0xC000: 'PBSD',
    0xC001: 'PBSD_ISO',
    0xC002: 'PBSD_SCHEMA',
    0x119F: 'RLSCONV',
    0x1248: 'SYNCCRD',
    0x1904: 'XARETVAL',
    0x1907: 'TIMEOUT',
    0x1186: 'FORGET',
    0x1187: 'SYNCTYPE',
    0x1801: 'XID',
    0x1903: 'XAFLAGS',
    0x11EA: 'RSYNCTYP',
    0x126D: 'SYNCRRD',
    0x1905: 'PRPHRCLST',
    0x1906: 'XIDCNT',
}

def asc_dump(bindata):
    r = ''
    for c in bindata:
        r += chr(c) if (c >= 32 and c < 128) else '.'
    if r:
        print('\t[' + r + ']')


def recv_from_sock(sock, nbytes):
    n = nbytes
    recieved = b''
    while n:
        bs = sock.recv(n)
        recieved += bs

        n -= len(bs)
    return recieved


def printSQLCARD(cp, obj):
    flag = obj[0]
    sqlcode = int.from_bytes(obj[1:5], byteorder='big')
    sqlstate = obj[5:10]
    sqlerrproc = obj[10:18]
    rest = obj[18:]
    print("\t\tflag=%d,sqlcode=%d,sqlstate=%s,sqlerrproc=%s,%s" % (
        flag,
        sqlcode,
        sqlstate.decode('ascii'),
        sqlerrproc.decode('ascii'),
        binascii.b2a_hex(rest).decode('ascii'),
    ))


def printObject(cp, obj):
    print("\t%s:%s" % (cp, binascii.b2a_hex(obj).decode('ascii')))
    if cp == 'SQLCARD':
        printSQLCARD(cp, obj)
        asc_dump(obj)
        return


def printCodePoint(cp, obj):
    print("%s:%s" % (cp, binascii.b2a_hex(obj).decode('ascii')))
    i = 0;
    while i < len(obj):
        ln = int.from_bytes(obj[i:i+2], byteorder='big')
        cp = CODE_POINT[int.from_bytes(obj[i+2:i+4], byteorder='big')]
        binary = obj[i+4:i+ln]
        if cp in (
            'EXTNAM', 'SRVNAM', 'SRVRLSLV', 'SRVCLSNM', 'SPVNAM', 'PRDDTA',
        ):
            print('\t%s:"%s"' % (cp, binary.decode('cp500')))
        elif cp in (
            'USRID'
        ):
            print('\t%s:"%s"' % (cp, binary.decode('utf-8')))
        elif cp in (
            'SECMEC', 'PBSD_ISO', 'UOWDSP', 'SVRCOD', 'SECCHKCD',
            'RDBCMTOK', 'OUTEXP', 'QRYBLKSZ', 'MAXBLKEXT', 'MAXRSLCNT',
            'RSLSETFLG', 'QRYROWSET', 'TYPSQLDA', 'QRYINSID',
        ):
            print("\t%s:%s(len=%d)" % (cp, int.from_bytes(binary, byteorder='big'), len(binary)))
        elif cp in ('MGRLVLLS', ):
            print("\t%s:[%s] " % (cp, binascii.b2a_hex(binary).decode('ascii')), end='')
            while binary:
                cp2 = CODE_POINT[int.from_bytes(binary[:2], byteorder='big')]
                v = int.from_bytes(binary[2:4], byteorder='big')
                print("%s=%d" % (cp2, v), end=' ')
                binary = binary[4:]
            print()
        elif cp in ('TYPDEFNAM', 'PBSD', 'PRDID', 'PBSD_SCHEMA'):
            print("\t%s:'%s'" % (cp, binary.decode('ascii')))
        elif cp in ('TYPDEFOVR', ):
            print("\t%s:%s" % (cp, binascii.b2a_hex(binary).decode('ascii')))
            j = 0;
            while j < len(binary):
                ln2 = int.from_bytes(binary[j:j+2], byteorder='big')
                cp2 = CODE_POINT[int.from_bytes(binary[j+2:j+4], byteorder='big')]
                binary2 = binary[j+4:j+ln2]
                print("\t\t%s:%s" % (cp2, int.from_bytes(binary2, byteorder='big')))
                j += ln2
        elif cp in ('RDBNAM', ):
            print("\t%s:" % (cp, ), end='')
            asc_dump(binary)
        elif cp in ('QRYPRCTYP', 'RDBACCCL'):
            print("\t%s:%s" % (cp, CODE_POINT[int.from_bytes(binary, byteorder='big')]))
        elif cp in ('CRRTKN', ):
            print("\t%s:%s" % (cp, binascii.b2a_hex(binary).decode('ascii')))
        elif cp in ('PKGNAMCSN', ):
            print("\t%s:RDBNAM=[%s],RDBCOLID=[%s],PKGID=[%s],PKGCNSTKN=[%s],PKGSN=[%s]" % (
                cp,
                binary[:18].decode('utf-8'),
                binary[18:36].decode('utf-8'),
                binary[36:54].decode('utf-8'),
                binary[54:62].decode('utf-8'),
                binascii.b2a_hex(binary[62:]).decode('ascii'),
            ))
        else:
            print("%s:%s" % (cp, binascii.b2a_hex(binary).decode('ascii')))
        i += ln
    assert i == len(obj)


def relay_packets(indicator, read_sock, write_sock):
    DSS_type = {
        1: 'Request',
        2: 'Reply',
        3: 'Object',
        4: 'Communication',
        5: 'Request DSS where no reply is expected',
    }
    head = recv_from_sock(read_sock, 6)
    ln = int.from_bytes(head[:2], byteorder='big')
    assert head[2] == 0xD0

    same_correlator = head[3] & 0b00010000
    dss_type = DSS_type[head[3] & 0b1111]
    chained = head[3] & 0b01000000
    print("%s(%d) %s,%s,%s,%s,%d" % (
        indicator,
        ln,
        dss_type,
        'chained' if chained else 'unchained',
        'continue on error' if head[3] & 0b00100000 else '',
        'next DDS has same id' if same_correlator else '',
        int.from_bytes(head[4:6],  byteorder='big'),
        ),
    )

    write_sock.send(head)
    body = recv_from_sock(read_sock, 4)
    write_sock.send(body)
    obj = recv_from_sock(read_sock, ln-10)
    write_sock.send(obj)

    assert ln == int.from_bytes(body[:2], byteorder='big') + 6
    code_point = int.from_bytes(body[2:4], byteorder='big')

    if dss_type == 'Object':
        printObject(CODE_POINT[code_point], obj)
    else:
        printCodePoint(CODE_POINT[code_point], obj)

    return chained


def proxy_wire(server_name, server_port, listen_host, listen_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((listen_host, listen_port))
    sock.listen(1)
    client_sock, addr = sock.accept()
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect((server_name, server_port))

    while True:
        while relay_packets('C->S:', client_sock, server_sock):
            pass
        while relay_packets('S->C:', server_sock, client_sock):
            pass

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage : ' + sys.argv[0] + ' server[:port] [listen_host:]listen_port')
        sys.exit()

    server = sys.argv[1].split(':')
    server_name = server[0]
    if len(server) == 1:
        server_port = 1527
    else:
        server_port = int(server[1])

    listen = sys.argv[2].split(':')
    if len(listen) == 1:
        listen_host = 'localhost'
        listen_port = int(listen[0])
    else:
        listen_host = listen[0]
        listen_port = int(listen[1])

    proxy_wire(server_name, server_port, listen_host, listen_port)
