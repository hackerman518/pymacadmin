#!/usr/bin/env python

"""
Generates a list of OS X system events into a plist for crankd.

This is designed to create a large (but probably not comprehensive) sample
of the events generated by Mac OS X that crankd can tap into.  The generated
file will call the 'tunnel.sh' as the command for each event; said fail can
be easily edited to redirect the output to wherever you would like it to go.

"""

OUTPUT_FILE = "crankd-config.plist"

from SystemConfiguration import SCDynamicStoreCopyKeyList, SCDynamicStoreCreate

# Each event has a general event type, and a specific event
# The category is the key, and the value is a list of specific events
event_dict = {}

def AddEvent(event_category, specific_event):
    """Adds an event to the event dictionary"""
    if event_category not in event_dict:
        event_dict[event_category] = []
    event_dict[event_category].append(specific_event)

def AddCategoryOfEvents(event_category, events):
    """Adds a list of events that all belong to the same category"""
    for specific_event in events:
        AddEvent(event_category, specific_event)

def AddKnownEvents():
    """Here we add all the events that we know of to the dictionary"""
    
    # Add a bunch of dynamic events
    store = SCDynamicStoreCreate(None, "generate_event_plist", None, None)
    AddCategoryOfEvents(u"SystemConfiguration",
                        SCDynamicStoreCopyKeyList(store, ".*"))
    
    # Add some standard NSWorkspace events
    AddCategoryOfEvents(u"NSWorkspace",
                        u'''
        NSWorkspaceDidLaunchApplicationNotification
        NSWorkspaceDidMountNotification
        NSWorkspaceDidPerformFileOperationNotification
        NSWorkspaceDidTerminateApplicationNotification
        NSWorkspaceDidUnmountNotification
        NSWorkspaceDidWakeNotification
        NSWorkspaceSessionDidBecomeActiveNotification
        NSWorkspaceSessionDidResignActiveNotification
        NSWorkspaceWillLaunchApplicationNotification
        NSWorkspaceWillPowerOffNotification
        NSWorkspaceWillSleepNotification
        NSWorkspaceWillUnmountNotification
                        '''.split())

def PrintEvents():
    """Prints all the events, for debugging purposes"""
    for category in sorted(event_dict):
        
        print category
        
        for event in sorted(event_dict[category]):
            print "\t" + event

def OutputEvents():
    """Outputs all the events to a file"""
    
    # print the header for the file
    plist = open(OUTPUT_FILE, 'w')
    
    print >>plist, '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>'''
    
    for category in sorted(event_dict):
        
        # print out the category
        print >>plist, "  <key>%s</key>\n      <dict>" % category
        
        for event in sorted(event_dict[category]):
            print >>plist, """
        <key>%s</key>
        <dict>
          <key>command</key>
          <string>%s '%s' '%s'</string>
        </dict>""" % ( event, 'tunnel.sh', category, event )
        
        # end the category
        print >>plist, "  </dict>"
    
    # end the plist file
    print >>plist, '</dict>'
    print >>plist, '</plist>'
    
    plist.close()
    
def main():
    """Runs the program"""
    AddKnownEvents()
    #PrintEvents()
    OutputEvents()

main()

    
