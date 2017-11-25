#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(repository='apps/auth/db/', url='postgresql://dvhb:dvhba@localhost/dvhb', debug='False')
