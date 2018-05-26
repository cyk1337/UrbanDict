#!/usr/bin/env bash
source activate mlp

scrapy crawl UD
#scrapy crawl UD-API

source deactivate