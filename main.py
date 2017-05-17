#!/usr/bin/env python
# -*- coding: utf-8 -*-

import context
import detect_service

logger = context.G_LOGGER


def main():
    try:
        school_id = 11
        logger.info('进出判断---start---,schoolId:%d' % school_id)
        detect_service.seq_check_in_out_by_school(school_id=school_id)
        logger.info('进出判断---end-----,schoolId:%d' % school_id)
    except Exception, e:
        logger.exception(e)
    finally:
        pass


if __name__ == '__main__':
    main()
