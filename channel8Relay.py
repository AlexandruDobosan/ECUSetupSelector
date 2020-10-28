import hid

class Relay(object):


    def __init__(self, vendorID, productID):
        self.h = hid.device()
        self.h.open(vendorID, productID)
        self.h.set_nonblocking(1)


    def uncypher(self,num):
        powers = range(1,7)
        values = []
        index = 0;
        status = [0,0,0,0,0,0,0,0]
        values = [1,2,4,8,16,32,64,128]
        i=7
        while i >= 0:
          if num >= values[i]:
            num -= values[i]
            status[i] = 1
          else:
              status[i] = 0
          i = i-1

        return status
    """Relay board status report contains a number of the form "168",composed of 128,32 and 8
       That means relays 8,6 and 4 are active.
       This function returns all 8 relay's status in a list of 1's - ACTIVE and 0's - INACTIVE
    """


    def get_status(self):
        report = self.get_feature_report()
        if report[8]:
           status = self.uncypher(report[8])
           relays =[1,2,3,4,5,6,7,8]
           i = 0
           while i < 8:
             relays[i] = bool(status[i])
             i = i+1
           return relays
        else:
            return [False,False,False,False,False,False,False,False]
        """
        Returns status of the 8 relays in boolean form in a list.
        For first relay on and last 7 off returns [True,False,False,False,False,False,False]
        """


    def get_switch_statuses_from_report(self, report):
        switch_statuses = report[7]
        switch_statuses = [int(x) for x in list('{0:08b}'.format(switch_statuses))]
        switch_statuses.reverse()
        return switch_statuses

    def get_feature_report(self):
        feature = 1
        length = 9
        return self.h.get_feature_report(feature, length)
    """ Built in hid function
        Returns a report which contains a number from which you can read the board's status"""

    def send_feature_report(self, message):
        self.h.send_feature_report(message)
    """Writes report to relay board"""

    def state(self, relay, on=None):
        """
        		Setter for the relay.

        		Setter - If a relay and on are specified, then the relay(s) status will be set.
        		Either specify the specific relay, 1-8, or 0 to change the state of all relays.
        		on=True will turn the relay on, on=False will turn them off.
        		"""

        if on != None:
            message = [0, 0, relay, 0, 0, 0, 0, 0, 0]
            if relay == 0:
                if on:
                    command = 0xFE
                else:
                    command = 0xFC

            else:
                if on:
                    command = 0xFF
                else:
                    command = 0xFD
            message[1] = command
            self.send_feature_report(message)

