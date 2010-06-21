
import logging

logger = logging.getLogger('Plone')


PATTERN = '__PasswordStength_%s__'
def call(self, __name__, *args, **kw):
    return getattr(self, PATTERN % __name__)(*args, **kw)

WRAPPER = '__PasswordStength_is_wrapper_method__'
ORIG_NAME = '__PasswordStength_original_method_name__'
def isWrapperMethod(meth):
    return getattr(meth, WRAPPER, False)

def wrap_method(klass, name, method, pattern=PATTERN):
    old_method = getattr(klass, name, None)
    if isWrapperMethod(old_method):
        logger.info('PasswordStrength: *NOT* wrapping already wrapped method at %s.%s',
            klass.__name__, name)
        return
    else:
        logger.info('PasswordStrength: Wrapping method at %s.%s', klass.__name__, name)
    new_name = pattern % name
    setattr(klass, new_name, old_method)
    setattr(method, ORIG_NAME, new_name)
    setattr(method, WRAPPER, True)
    setattr(klass, name, method)

def unwrap_method(klass, name):
    old_method = getattr(klass, name)
    if not isWrapperMethod(old_method):
        raise ValueError, ('Trying to unwrap non-wrapped '
                           'method at %s.%s' % (klass.__name__, name))
    orig_name = getattr(old_method, ORIG_NAME)
    new_method = getattr(klass, orig_name)
    delattr(klass, orig_name)
    setattr(klass, name, new_method)

def wrapAllMethods(patch_class, target_class):
    for n,m in [(n,m) for n,m in patch_class.__dict__.items() if callable(m)]:
        wrap_method(target_class,n,m)
