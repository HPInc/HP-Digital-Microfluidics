from __future__ import annotations

# This is a copy of sphinx-build, put here to make it easier to run from within
# Eclipse.

import re
import sys
from opentrons.simulate import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())