#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(debug='False', url='postgresql://dvhb:dvhba@localhost/dvhb', repository='apps/documents/db/')
