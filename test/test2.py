#!/usr/bin/env python
# -*- coding: utf-8 -*-

import context

logger = context.G_LOGGER
redis_client = context.G_REDIS_CLIENT


def main():
    logger.info(redis_client.keys())


if __name__ == '__main__':
    main()
