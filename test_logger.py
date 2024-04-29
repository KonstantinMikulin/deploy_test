import logging

from logging_config_example.module_1 import main

logging.basicConfig(
    format='#%(levelname)-8s %(name)s:%(funcName)s - %(message)s'
)

main()
