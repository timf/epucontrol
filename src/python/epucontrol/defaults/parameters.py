import os
from ConfigParser import NoOptionError, NoSectionError

#See api/TODO.txt
#import zope.interface
#import epucontrol.api.objects

import epucontrol.main.ec_args as ec_args

# -----------------------------------------------------------------------------
# DefaultParameters 
# -----------------------------------------------------------------------------

class DefaultParameters:
    
    #See api/TODO.txt
    #zope.interface.implements(workspacecontrol.api.objects.IParameters)
    
    def __init__(self, allconfigs, opts):
        self.optdict = _create_optdict(opts)
        self.conf = allconfigs
    
    def get_arg_or_none(self, key):
        
        if not key:
            return None
            
        if isinstance(key, ec_args.ControlArg):
            key = key.name
            
        val = None
        if self.optdict and self.optdict.has_key(key):
            try:
                val = self.optdict[key]
            except:
                return None
        return val
    
    def get_conf_or_none(self, section, key):
        if not self.conf:
            return None
        if not section:
            return None
        if not key:
            return None
            
        try:
            aconf = self.conf.get(section, key)
        except NoSectionError:
            return None
        except NoOptionError:
            return None
            
        if not aconf:
            return None
            
        aconf = aconf.strip()
        if len(aconf) == 0:
            return None
            
        return aconf
        
    def all_confs_in_section(self, section):
        if not self.conf:
            return []
        if not section:
            return []
        try:
            keywords = self.conf.options(section)
        except NoSectionError:
            return []
            
        conflist = []
        for keyword in keywords:
            value = self.get_conf_or_none(section, keyword)
            if value:
                conflist.append((keyword,value))
        return conflist

def _create_optdict(opts):
    d = {}
    
    if not opts:
        return d
        
    for arg in ec_args.ALL_EC_ARGS_LIST:
        if not arg.deprecated:
            d[arg.name] = _get_one_attr(opts, arg.name)
    
    return d
    
def _get_one_attr(opts, name):
    try:
        val = getattr(opts, name)
        if not val:
            return None
        return val
    except:
        return None
    