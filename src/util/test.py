#!/usr/bin/env python
import FeatureApi

api = FeatureApi.FeatureApi()

rows = api.query_simap("7cefd1d9450809b30c462f4c2c1b595a", "", "");
for row in rows:
	print row

