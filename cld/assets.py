from pathlib import Path

from clld.web.assets import environment

import cld


environment.append_path(
    Path(cld.__file__).parent.joinpath('static').as_posix(),
    url='/cld:static/')
environment.load_path = list(reversed(environment.load_path))
