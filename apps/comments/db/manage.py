#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(repository='apps/comments/db/', debug='False', url='postgresql://closureuser:closurepass@localhost/closuredb')
