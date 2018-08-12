from pysnmp.hlapi import *

hostname  = ''
user_name = ''
auth_key = ''
priv_key = ''

mode = ''

def snmpget(oid):

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               UsmUserData(user_name, auth_key, priv_key, authProtocol=usmHMACMD5AuthProtocol, privProtocol=usmAesCfb128Protocol),
               UdpTransportTarget((hostname, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)
                #.addAsn1MibSource('file:///usr/share/snmp', 'http://mibs.snmplabs.com/asn1/@mib@')
                ))
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))
            return x.prettyPrint()

if mode == 'load':
    load1 = str(float(snmpget('1.3.6.1.4.1.2021.10.1.5.1'))/100)
    load5 = str(float(snmpget('1.3.6.1.4.1.2021.10.1.5.2'))/100)
    load15 = str(float(snmpget('1.3.6.1.4.1.2021.10.1.5.3'))/100)

    print 'OK - load average: %s, %s, %s' % (load1, load5, load15), '|load1=%sc, load5=%sc, load15=%sc' % (load1, load5, load15)

if mode == 'memory':
    memory_total = float(snmpget('1.3.6.1.4.1.2021.4.5.0'))
    memory_unused = float(snmpget('1.3.6.1.4.1.2021.4.6.0'))
    memory_percent = 100 / memory_total * memory_unused

    print 'OK - {:0.1f}% '.format(memory_percent) + 'free ({0:0.1f} MB out of {1:0.1f} MB)'.format((memory_unused / 1024), (memory_total / 1024)), '|memory_total=%dc, memory_unused=%dc, memory_percent=%d' % (memory_total, memory_unused, memory_percent) + '%'

