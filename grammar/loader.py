import time
import traceback

class GrammarLoader():
    _grammars = None

    def __init__(self, grammars):
        self._grammars = grammars

    def load(self):
        init_time = time.time()
        
        for grammar in self._grammars:
            try:
                grammar.load()
                print 'Loaded grammar %s in %s seconds.' % (grammar.name, str(time.time() - init_time))
            except:
                traceback.print_exc()
                print 'Loading grammar %s failed!' % grammar.name

    def unload(self):
        for grammar in self._grammars:
            try:
                grammar.unload()
            except:
                traceback.print_exc()

