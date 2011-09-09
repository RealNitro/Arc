# Arc is copyright 2009-2011 the Arc team and other contributors.
# Arc is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSING" file in the "docs" folder of the Arc Package.

from ConfigParser import RawConfigParser as ConfigParser
from collections import defaultdict

from twisted.internet.task import LoopingCall

class AutoShutdownServerPlugin():

    name = "AutoShutdownPlugin"

    def gotServer(self):
        self.loop = LoopingCall(checkWorld) # TODO: Register this loop into the central loop-de-loop directory
        self.times = defaultdict(int)

    def runLoop(self):
        self.loop.start(60) # Check worlds every minute
        
    def checkWorlds(self):
        # Check the worlds
        if self.factory.worlds.keys() != list("default"): # We don't care about default :P
            for world in self.factory.worlds.keys():
                if self.factory.worlds[world].autoshutdown:
                    if self.times[world] >= self.factory.asd_delay and not self.factory.worlds[world]:
                        self.factory.unloadWorld(world)
                    else:
                        self.times[world] += 1

    hooks = {
        "configLoaded": runLoop
     }
serverPlugin = AutoShutdownServerPlugin
