# Arc is copyright 2009-2011 the Arc team and other contributors.
# Arc is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSING" file in the "docs" folder of the Arc Package.

import os, shutil
from ConfigParser import RawConfigParser as ConfigParser

class PlayerData():
    def __init__(self, client):
        "Initialises the class with the client's protocol object."
        self.logger = client.factory.logger # Get ourselves a logger
        # We're going to take a few things from the client, so we'll save it.
        self.client = client
        # Create a RawConfigParser instance and data dict
        self.dataReader = ConfigParser()
        self.data = {}
        # Obviously, we need to load the data right away.
        success = self.loadData()
        if not success:
            self.loadDataFallback() # If it failed, fall back.
        else:
            self.saving = True

    def loadData(self):
        "Loads the player's data file"
        if os.path.isfile("data/players/%s.ini" % self.username): # Check if the file exists ( Much more efficient than x in os.listdir() )
            try:
                self.dataReader.read("data/players/%s.ini" % self.username) # Have ConfigParser read it
            except Exception as a: # If we can't read it, say that
                self.logger.error("Unable to read player data for %s!" % self.username)
                self.logger.error("Error: %s" % a)
                return False # Return false to show it failed
            else:
                self.logger.debug("Parsing data/players/%s.ini" % self.username)
        else: # If we have no file, copy it from the template
            self.logger.debug("No player data file for %s found." % self.username)
            self.logger.info("Creating data file data/players/%s.ini using template data/DEFAULT_TEMPLATE_PLAYER.ini" % self.username)
            shutil.copy("data/DEFAULT_TEMPLATE_PLAYER.ini", "data/players/%s.ini" % self.username)
            try:
                self.dataReader.read("data/players/%s.ini" % self.username) # Have ConfigParser read it
            except Exception as a: # If we can't read it, say that
                self.logger.error("Unable to read player data for %s!" % self.username)
                self.logger.error("Error: %s" % a)
                return False
        sections = self.dataReader.sections()
        try:
            for element in sections:
                data = self.dataReader.items(element) # This gives us name, value pairs for the secion
                self.data[element] = {}
                for part in data:
                    name, value = part
                    self.data[element][name] = value
            self.logger.debug("Player data dictionary:")
            self.logger.debug(str(self.data))
        except Exception as a:
            self.logger.error("Unable to read player data for %s!" % self.username)
            self.logger.error("Error: %s" % a)
            return False
        self.logger.info("Parsed data file for %s." % self.username)
        return True

    def loadDataFallback(self):
        "Called when loading data fails. Prevents data saving and loads the default data values."
        self.factory.logger.warn("Settings will not be saved. Default data being used.")
        self.dataReader.read("data/DEFAULT_TEMPLATE_PLAYER.ini")
        sections = self.dataReader.sections()
        try:
            for element in sections:
                data = self.dataReader.items(element) # This gives us named items for the secion
                self.data[element] = {}
                for part in data:
                    name, value = part # This gives us name, value pairs from the named items in the section
                    self.data[element][name] = value
            self.logger.debug("Player data dictionary:")
            self.logger.debug(str(self.data))
        except Exception as a:
            self.logger.error("Unable to read default player data for %s!" % self.username)
            self.logger.error("Error: %s" % a)
            return False
        self.logger.info("Parsed default data file for %s." % self.username)
        self.saving = False
        return True

    def saveData(self, username=self.username):
        "Saves the player's data file, possibly cloning it to another player"
        if self.saving:
            self.logger.debug("Saving data/players/%s.ini..." % self.username)
            try:
                fp = open("data/players/%s.ini" % self.username, "w")
            except Exception as a:
                self.logger.error("Unable to open data/players/%s.ini for writing!" % self.username)
                self.logger.error("%s" % a)
            else:
                for section in self.data.keys():
                    if not self.dataReader.has_section(section):
                        self.dataReader.add_section(section)
                    for element in section.items():
                        self.dataReader.set(section, element[0], str(element[1]))
                try:
                    self.dataReader.write(fp)
                    fp.flush()
                    fp.close()
        else:
            self.logger.warn("Unable to write player data for %s as it was unreadable." % self.username)
            self.logger.warn("Check the log for when they joined for more information.")
    
    # Convenience functions
    # These are here so that plugin authors can get and set data to the internal
    # data dict without interfering with it.
    
    def get(self, section, key=None):
        "Used to get data from the internal data dict"
        pass
    
    def set(self, section, key):
        "Used to set data to the internal data dict"
        pass
    
    def flush(self):
        "Saves the current data structure and reparses it."
        self.saveData()
        self.loadData()
        
    def reload(self):
        "Discards the current data structure and reparses it."
        del self.data
        self.loadData()
    
    # Properties (self.blah)
    # These are here so that plugin authors can get at the class' data variables
    # properly.
    
    @property
    def username(self):
        "Associated client's username"
        return self.client.username
    
    @property
    def canSave(self):
        "Check to see if we can save or not"
        return self.saving

class ClanData():
    pass