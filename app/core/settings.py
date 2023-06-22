local = True

if local:
    from .local_settings import *
else:
    from .docker_settings import *
local = False

if local:
    from .local_settings import *
else:
    from .docker_settings import *
