import pygame
import operator
try:
    import json
except ImportError:
    import simplejson as json
import spyral
import os
import random
import base64
from collections import defaultdict

class Event(object):
    def __init__(self, type):
        self.type = type

class EventDict(dict):
    def __getattr__(self, attr):
        return self[attr]
        
    def __setattr__(self, attr, value):
        self[attr] = value

_event_names = ['QUIT', 'ACTIVEEVENT', 'KEYDOWN', 'KEYUP', 'MOUSEMOTION',
                'MOUSEBUTTONUP', 'JOYAXISMOTION', 'JOYBALLMOTION',
                'JOYHATMOTION', 'JOYBUTTONUP', 'JOYBUTTONDOWN',
                'VIDEORESIZE', 'VIDEOEXPOSE', 'USEREVENT', 'MOUSEBUTTONDOWN']

def init():
    global _type_to_name
    global _type_to_attrs
    _type_to_name = dict((getattr(pygame, name), name) for name in _event_names)

    _type_to_attrs = {
        pygame.QUIT: ('type', ),
        pygame.ACTIVEEVENT: ('type', 'gain', 'state'),
        pygame.KEYDOWN: ('type', 'unicode', 'key', 'mod'),
        pygame.KEYUP: ('type', 'key', 'mod'),
        pygame.MOUSEMOTION: ('type', 'pos', 'rel', 'buttons'),
        pygame.MOUSEBUTTONUP: ('type', 'pos', 'button'),
        pygame.MOUSEBUTTONDOWN: ('type', 'pos', 'button'),
        pygame.JOYAXISMOTION: ('type', 'joy', 'axis', 'value'),
        pygame.JOYBALLMOTION: ('type', 'joy', 'ball', 'rel'),
        pygame.JOYHATMOTION: ('type', 'joy', 'hat', 'value'),
        pygame.JOYBUTTONUP: ('type', 'joy', 'button'),
        pygame.JOYBUTTONDOWN: ('type', 'joy', 'button'),
        pygame.VIDEORESIZE: ('type', 'size', 'w', 'h'),
        pygame.VIDEOEXPOSE: ('type', 'none'),
        pygame.USEREVENT: ('type', 'code')
    }


def _event_to_dict(event):
    attrs = _type_to_attrs[event.type]
    d = EventDict((attr, getattr(event, attr)) for attr in attrs)
    d['type'] = _type_to_name[event.type]
    if d['type'] in ('KEYDOWN', 'KEYUP'):
        try:
            d['ascii'] = chr(d['key'])
        except ValueError:
            d['ascii'] = ''
    return d


class EventHandler(object):
    """
    Base event handler class.
    """
    def __init__(self):
        self._events = []
        self._mouse_pos = (0, 0)

    def tick(self):
        """
        Should be called at the beginning of update cycle. For the
        event handler which is part of a scene, this function will be
        called automatically. For any additional event handlers, you
        must call this function manually.
        """
        pass

    def get(self, types=[]):
        """
        Gets events from the event handler. Types is an optional
        iterable which has types which you would like to get.
        """
        try:
            types[0]
        except IndexError:
            pass
        except TypeError:
            types = (types,)

        if types == []:
            ret = self._events
            self._events = []
            return ret

        ret = [e for e in self._events if e['type'] in types]
        self._events = [e for e in self._events if e['type'] not in types]
        return ret


class LiveEventHandler(EventHandler):
    def __init__(self, output_file=None):
        """
        An event handler which pulls events from the operating system.
        
        The optional output_file argument specifies the path to a file
        where the event handler will save a custom json file that can
        be used with the `ReplayEventHandler` to show replays of a
        game in action, or be used for other clever purposes.
        
        .. note::
            
            If you use the output_file parameter, this function will
            reseed the random number generator, save the seed used. It
            will then be restored by the ReplayEventHandler.        
        """
        EventHandler.__init__(self)
        self._save = output_file is not None
        if self._save:
            self._file = open(output_file, 'w')
            seed = os.urandom(4)
            info = {'random_seed': base64.encodestring(seed)}
            random.seed(seed)
            self._file.write(json.dumps(info) + "\n")

    def tick(self):
        mouse = pygame.mouse.get_pos()
        events = [_event_to_dict(e) for e in pygame.event.get()]
        self._mouse_pos = mouse
        self._events.extend(events)
        if self._save:
            d = {'mouse': mouse, 'events': events}
            self._file.write(json.dumps(d) + "\n")

    def __del__(self):
        if self._save:
            self._file.close()

class EventManager(object):
    def __init__(self):
        """
        The event manager's task is to take events and send them to
        listeners which have registered to receive events.
        
        Events are any object which have a type attribute, which is a
        string. There are a number of built-in events.
        
        A listener is an object which has a handle_event method which
        takes one event as an argument.
        
        If handle_event returns True, the manager does not pass the
        event to any other listeners. To ensure the right listeners
        handle events, ensure that their priority is set accordingly.
        
        
        """
        self._listeners = defaultdict(lambda : [])
        self._events = []
        self._busy = False
        self._debug = 0
        
    def register_listener(self, listener, event_types, priority = 5):
        # We may switch to bisect here at some point, but for now, we'll just resort
        for event_type in event_types:
            self._listeners[event_type].append((listener, priority))
            self._listeners[event_type] = sorted(self._listeners[event_type], key=operator.itemgetter(1), reverse = True)
            
    def unregister_listener(self, listener, event_types = None, priority = None):
        """
        Remove the listener for the given event types and priority. If
        event_types is None, remove it for all event types, and if 
        priority is None, remove it for any priority.
        """
        if event_types is None:
            event_types = list(self._listeners.iterkeys())
        for e in event_types:
            self._listeners[e] = [l for l in self._listeners[e] if not (l[0] is listener and l[1] == priority)]
        
    def send_events(self, events):
        """
        Sends an event to the relevant listeners.
        
        If events are currently being processed by the manager, the
        events are added to the list of events to be sent out.
        """
        if not self._busy:
            self._busy = True
            self._events.extend(events)
            while len(self._events) > 0:
                events = self._events
                self._events = []
                for event in events:
                    if self._debug == 1:
                        print event.type
                    elif self._debug:
                        print event
                    # Make sure we avoid futzing with things while iterating
                    listeners = self._listeners[event.type][:]
                    for listener in listeners:
                        r = listener[0].handle_event(event)
                        if r is True:
                            break
            self._busy = False
        else:
           self._events.extend(events) 
        
        
    def send_event(self, event): #, immediate = False):
        """
        Sends an event to the relevant listeners.
        """
        self.send_events([event])
        
        # Old version with some potentially interesting things here
        # """
        # If events are currently being processed by the manager, the
        # event is added to the list of events to be sent out, unless
        # immediate is set to True, in which case it is sent immediately.
        # Use immediate sparingly, as it may lead to a large stack if
        # events trigger more immediate calls.
        # """
        # if not self._busy or immediate is True:
        #     print event.type
        #     # Make sure we avoid futzing with things while iterating
        #     listeners = self._listeners[event.type][:]
        #     for listener in listeners:
        #         r = listener[0].handle_event(event)
        #         if r is True:
        #             break
        # else:
        #     self._events.append(event)
        
    def set_debug(self, value):
        """
        Enables debugging output on the event manager of varying
        verbosity.
        
        "off" prints no output whatsoever.
        "on" prints only the event types as they are handled.
        "verbose" prints all full events.
        """
        
        if value not in ('off', 'on', 'verbose'):
            raise ValueError("Invalid debug mode.")
        self._debug = {'off' : 0, 'on' : 1, 'verbose' : 2}[value]
        
class ReplayEventHandler(EventHandler):
    def __init__(self, input_file):
        """
        An event handler which replays the events from a custom json
        file saved by the `LiveEventHandler`.
        """
        EventHandler.__init__(self)
        self._file = open(input_file)
        info = json.loads(self._file.readline())
        random.seed(base64.decodestring(info['random_seed']))
        self.paused = False
        
    def pause(self):
        """
        Pauses the replay of the events, making tick() a noop until
        resume is called.
        """
        self.paused = True
        
    def resume(self):
        """
        Resumes the replay of events.
        """
        self.paused = False

    def tick(self):
        if self.paused:
            return
        try:
            d = json.loads(self._file.readline())
        except ValueError:
            spyral.director.pop()
        events = d['events']
        events = [EventDict(e) for e in events]
        self._mouse_pos = d['mouse']
        self._events.extend(events)        

class Mods(object):
    def __init__(self):
        self.none = pygame.KMOD_NONE
        self.lshift = pygame.KMOD_LSHIFT
        self.rshift = pygame.KMOD_RSHIFT
        self.shift = pygame.KMOD_SHIFT
        self.caps = pygame.KMOD_CAPS
        self.ctrl = pygame.KMOD_CTRL
        self.lctrl = pygame.KMOD_LCTRL
        self.rctrl = pygame.KMOD_RCTRL
        self.lalt = pygame.KMOD_LALT
        self.ralt = pygame.KMOD_RALT
        self.alt = pygame.KMOD_ALT

class Keys(object):
        
    def __init__(self):  
      self.load_keys_from_file(spyral._get_spyral_path() + 'resources/default_key_mappings.txt')   

    def load_keys_from_file(self, filename):
        fp = open(filename)
        keys = fp.readlines()
        fp.close()
        for singleMapping in keys:
            mapping = singleMapping[:-1].split(' ')
            if len(mapping) == 2:
                if mapping[1][0:2] == '0x':
                    setattr(self, mapping[0], int(mapping[1],16))
                else:
                    setattr(self, mapping[0], int(mapping[1]))

    def add_key_mapping(self, name, number):
        setattr(self, name, number)
            
keys = Keys()
mods = Mods()
