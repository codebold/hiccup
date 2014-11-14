## {{{ http://code.activestate.com/recipes/573466/ (r4)
# From the recipe at http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/551761
# A backwards compatible enhancement has been made to allow full access to registry types still through the dictionary metaphor

"""Slightly magical Win32api Registry -> Dictionary-like-object wrapper"""
import win32api, win32con, cPickle

class RegistryDict(object):
    def __init__(self, keyhandle = win32con.HKEY_LOCAL_MACHINE, keypath = [], flags = None):
        """If flags=None, then it will create the key.. otherwise pass a win32con.KEY_* sam"""
        self.keyhandle = None
        self.open(keyhandle, keypath, flags)

    @staticmethod
    def massageIncomingRegistryValue((obj, objtype), bReturnType=False):
        r=None
        if objtype == win32con.REG_BINARY and obj[:8]=='PyPickle':
            obj = obj[8:]
            r = (cPickle.loads(obj), objtype)
        elif objtype == win32con.REG_NONE:
            r = (None, objtype)
        elif objtype in (win32con.REG_SZ, win32con.REG_EXPAND_SZ,
                         win32con.REG_RESOURCE_LIST, win32con.REG_LINK,
                         win32con.REG_BINARY, win32con.REG_DWORD,
                         win32con.REG_DWORD_LITTLE_ENDIAN, win32con.REG_DWORD_BIG_ENDIAN,
                         win32con.REG_MULTI_SZ):
            r = (obj,objtype)
        if r == None:
            raise NotImplementedError, "Registry type 0x%08X not supported" % (objtype,)
        if bReturnType:
            return r
        else:
            return r[0]

    def __getitem__(self, key):
        bReturnType=False
        if (type(key) is tuple) and (len(key)==1):
            key = key[0]
            bReturnType=True
        # is it data?
        try:
            return self.massageIncomingRegistryValue(win32api.RegQueryValueEx(self.keyhandle, key),bReturnType)
        except:
            if key == '':
                # Special case: this dictionary key means "default value"
                raise KeyError, key
            pass
        # it's probably a registry key then
        try:
            return RegistryDict(self.keyhandle, key, win32con.KEY_ALL_ACCESS)
        except:
            pass
        # must not be there
        raise KeyError, key
    
    def has_key(self, key):
        return self.__contains__(key)
    
    def __contains__(self, key):
        try:
            self.__getitem__(key)
            return 1
        except KeyError:
            return 0

    def copy(self):
        return dict(self.iteritems())

    def __repr__(self):
        return repr(self.copy())

    def __str__(self):
        return self.__repr__()

    def __cmp__(self, other):
        # Do the objects have the same state?
        return self.keyhandle == other.keyhandle

    def __hash__(self):
        raise TypeError, "RegistryDict objects are unhashable"
  
    def clear(self):
        keylist = list(self.iterkeys())
        # Two-step to avoid changing the set while iterating over it
        for k in keylist:
            del self[k]
    
    def iteritems_data(self):
        i = 0
        # yield data
        try:
            while 1:
                s, obj, objtype = win32api.RegEnumValue(self.keyhandle, i)
                yield s, self.massageIncomingRegistryValue((obj, objtype))
                i += 1
        except:
            pass

    def iteritems_children(self, access=win32con.KEY_ALL_ACCESS):
        i = 0
        try:
            while 1:
                s = win32api.RegEnumKey(self.keyhandle, i)
                yield s, RegistryDict(self.keyhandle, [s], access)
                i += 1
        except:
            pass
                
    def iteritems(self, access=win32con.KEY_ALL_ACCESS):
       # yield children
        for item in self.iteritems_data():
            yield item
        for item in self.iteritems_children(access):
            yield item
            
    def iterkeys_data(self):
        for key, value in self.iteritems_data():
            yield key

    def iterkeys_children(self, access=win32con.KEY_ALL_ACCESS):
        for key, value in self.iteritems_children(access):
            yield key

    def iterkeys(self):
        for key, value in self.iteritems():
            yield key

    def itervalues_data(self):
        for key, value in self.iteritems_data():
            yield value

    def itervalues_children(self, access=win32con.KEY_ALL_ACCESS):
        for key, value in self.iteritems_children(access):
            yield value

    def itervalues(self, access=win32con.KEY_ALL_ACCESS):
        for key, value in self.iteritems(access):
            yield value

    def items(self, access=win32con.KEY_ALL_ACCESS):
        return list(self.iteritems())
              
    def keys(self):
        return list(self.iterkeys())

    def values(self, access=win32con.KEY_ALL_ACCESS):
        return list(self.itervalues(access))
        
    def __delitem__(self, key):
        # Delete a string value or a subkey, depending on the type
        try:
            item = self[key]
        except:
            return  # Silently ignore bad keys
        itemtype = type(item)
        if itemtype in (str, unicode, int):
            win32api.RegDeleteValue(self.keyhandle, key)
        elif isinstance(item, RegistryDict):
            # Delete everything in the subkey, then the subkey itself
            item.clear()
            win32api.RegDeleteKey(self.keyhandle, key)
        else:
            raise ValueError, "Unknown item type in RegistryDict"
  
    def __len__(self):
        return len(self.items())

    def __iter__(self):
        return self.iterkeys()
  
    def popitem(self):
        try:
            k, v = self.iteritems().next()
            del self[k]
            return k, v
        except StopIteration:
            raise KeyError, "RegistryDict is empty"
            
    def get(self,key,default=None):
        try:
            return self.__getitem__(key)
        except:
            return default

    def setdefault(self,key,default=None):
        try:
            return self.__getitem__(key)
        except:
            self.__setitem__(key)
            return default

    def update(self,d):
        for k,v in d.items():
            self.__setitem__(k, v)

    def __setitem__(self, item, value):
        item = str(item)
        pyvalue = type(value)
        if pyvalue is tuple and len(value)==2:
            valuetype = value[1]
            value = value[0]
        else:
            if pyvalue is dict or isinstance(value, RegistryDict):
                d = RegistryDict(self.keyhandle, item)
                d.clear()
                d.update(value)
                return
            if pyvalue is str:
                valuetype = win32con.REG_SZ
            elif pyvalue is int:
                valuetype = win32con.REG_DWORD
            else:
                valuetype = win32con.REG_BINARY
                value = 'PyPickle' + cPickle.dumps(value)
        win32api.RegSetValueEx(self.keyhandle, item, 0, valuetype, value)
  
    def open(self, keyhandle, keypath, flags = None):
        if self.keyhandle:
            self.close()
        if type(keypath) is str:
            keypath = keypath.split('\\')
        if flags in (None, win32con.KEY_ALL_ACCESS):
            for subkey in keypath:
                keyhandle = win32api.RegCreateKey(keyhandle, subkey)
        else:
            for subkey in keypath:
                keyhandle = win32api.RegOpenKeyEx(keyhandle, subkey, 0, flags)
        self.keyhandle = keyhandle

    def close(self):
        try:
            win32api.RegCloseKey(self.keyhandle)
        except:
            pass

    def __del__(self):
        self.close()
## end of http://code.activestate.com/recipes/573466/ }}}

if __name__=='__main__':
    ##
    ##    try some of the functions and remove the TestRegistryDict section again.
    ##    in case of doubt, follow this in the regedit program...
    ##
    lm = RegistryDict(win32con.HKEY_LOCAL_MACHINE,"Software\TestRegistryDict", flags=None)
        
    print 'should start with empty dict: ', lm
    lm['test'] = "abcd"
    print 'should contain test/abcd: ', lm
    lm['test'] = "xxxx"
    print 'should contain test/xxxx: ', lm
    del lm['test']
    print 'should be empty again: ', lm
    del lm['dummy']
    print 'should be still empty: ', lm
    print '--- now test int values (REG_DWORD)'
    lm['test'] = 1
    print 'should contain: test/1', lm
    lm['test'] = 0
    print 'should contain: test/1', lm
    del lm['test']
    print 'should be empty again: ', lm
    ls = RegistryDict(win32con.HKEY_LOCAL_MACHINE,"Software")
    del ls['TestRegistryDict']
    
    
    
    