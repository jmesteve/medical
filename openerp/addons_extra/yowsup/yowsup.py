from osv import fields, osv

import argparse, sys, os, csv
from Common.utilities import Utilities
from EchoClient import WhatsappEchoClient
import threading,time, base64

COUNTRIES_CSV = "countries.csv"

def startDbusInterface():
    from dbus.mainloop.glib import DBusGMainLoop
    from Yowsup.Interfaces.DBus.DBusInterface import DBusInitInterface
    import gobject
    
    DBusGMainLoop(set_as_default=True)
    
    DBusInitInterface()
    
    mainloop = gobject.MainLoop()
    
    gobject.threads_init()
    print("starting")
    mainloop.run()


def resultToString(result):
    unistr = str if sys.version_info >= (3, 0) else unicode
    out = []
    for k, v in result.items():
        if v is None:
            continue
        out.append("%s: %s" %(k, v.encode("utf-8") if type(v) is unistr else v))
        
    return "\n".join(out)

def getCredentials(config):
    if os.path.isfile(config):
        f = open(config)
        
        phone = ""
        idx = ""
        pw = ""
        cc = ""
        
        try:
            for l in f:
                line = l.strip()
                if len(line) and line[0] not in ('#',';'):
                    
                    prep = line.split('#', 1)[0].split(';', 1)[0].split('=', 1)
                    
                    varname = prep[0].strip()
                    val = prep[1].strip()
                    
                    if varname == "phone":
                        phone = val
                    elif varname == "id":
                        idx = val
                    elif varname =="password":
                        pw =val
                    elif varname == "cc":
                        cc = val

            return (cc, phone, idx, pw);
        except:
            pass

    return 0

def dissectPhoneNumber(phoneNumber):
    try:
        with open(COUNTRIES_CSV, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if len(row) == 3:
                    country, cc, mcc = row
                else:
                    country,cc = row
                    mcc = "000"
                try:
                    if phoneNumber.index(cc) == 0:
                        print("Detected cc: %s"%cc)
                        return (cc, phoneNumber[len(cc):])

                except ValueError:
                    continue
                
    except:
        pass
    return False


class yowsup_gateway(osv.osv):
    _name = 'yowsup.gateway'
    _columns = {
                'cc':fields.char('code region', size=3, required=True), 
                'phone':fields.char('phone number', size=15, required=True),
                'idphone':fields.char('mac emei', size=30, required=True),
                'password':fields.char('password', size=30, required=True), 
                'test_to': fields.char('test to', size=50, required=False), 
                'test_message': fields.char('test message', size=512, required=False),                
                }
    def test_gateway(self, cr, uid, ids, context=None):
        uom_obj = self.pool.get('yowsup.gateway')
        for move in self.browse(cr, uid, ids, context=context):
            identity = move.idphone
            identity = Utilities.processIdentity(identity)
                    
            phone = move.test_to.encode('utf-8')
            message = move.test_message.encode('utf-8')
            wa = WhatsappEchoClient(phone, message)
            
            login = move.phone
            countryCode = move.cc
            phoneNumber = login[len(countryCode):]
            password = move.password
            password = base64.b64decode(bytes(password.encode('utf-8')))
            wa.login(login, password)
            
yowsup_gateway()