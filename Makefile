.PHONY: setup baseline parse aggregate all help

PROJECT ?= collections
ORIGIN ?= developer

help:
	@echo "Targets:"
	@echo "  make setup              Clone Apache projects"
	@echo "  make baseline PROJECT=collections"
	@echo "  make metrics PROJECT=collections ORIGIN=developer"
	@echo "  make parse              Parse all raw results"
	@echo "  make aggregate          Build tables 2-4"
	@echo "  make all                Parse + aggregate (no full PIT run)"

setup:
	./scripts/00_setup.sh

baseline:
	./scripts/01_run_baseline.sh $(PROJECT)

metrics:
	./scripts/03_collect_metrics.sh $(PROJECT) $(ORIGIN)

parse:
	python3 scripts/04_parse_results.py --all

aggregate:
	python3 scripts/05_aggregate_tables.py --figures

all: parse aggregate
