import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import common_tools as ct
import data_generator as dg
import survey as sv
from common_tools import Kilonova

def main():

	(all_settings,
	survey_begin,
	survey_end,
	lower_declination_limit,
	upper_declination_limit,
	lower_redshift_limit,
	upper_redshift_limit,
	num_redshift_bins,
	sample_size,
	ATLAS_data_file,
	kilonova_data_file,
	lower_fit_time_limit,
	upper_fit_time_limit,
	polynomial_degree,
	do_extinction,
	plot_mode) = ct.readSurveyParameters()
	
	kilonova_df = pd.read_csv(kilonova_data_file)
	p_c, p_o = sv.fitKilonovaLightcurve(kilonova_df, lower_fit_time_limit, upper_fit_time_limit, polynomial_degree, plot_mode)
	
# 	sys.exit()
	
	full_ATLAS_df = pd.read_csv(ATLAS_data_file, sep = '\s+')
	
	shell_weights, redshift_distribution = dg.getShellWeights(lower_redshift_limit, upper_redshift_limit, num_redshift_bins)

	for i in range(0, sample_size):
		print('\n### KILONOVA %d' %i)
	
		kn = Kilonova()
		kn.setExplosionEpoch(survey_begin, survey_end)
		kn.setCoords(lower_declination_limit, upper_declination_limit)
		lower_redshift_bound, upper_redshift_bound = dg.getRedshiftBounds(shell_weights, redshift_distribution)
		kn.setRedshift(lower_redshift_bound, upper_redshift_bound)
		kn.info()
	
		partial_ATLAS_df = dg.filterAtlasDataFrameByExplosionEpoch(full_ATLAS_df, kn, lower_fit_time_limit, upper_fit_time_limit)
	
		if partial_ATLAS_df.empty:
			print('\nNo footprints temporally coincident with kilonova.')
			continue
	
		partial_ATLAS_df = dg.filterAtlasDataFrameByCoords(partial_ATLAS_df, kn, plot_mode)
# 		print(partial_ATLAS_df)

		if partial_ATLAS_df.empty:
			print('\nNo footprints at location of kilonova.')
			continue

		kn.generateLightcurve(p_c, p_o, partial_ATLAS_df, do_extinction)
# 		kn.showLightcurve()
	
		sv.recoverDetections(kn, partial_ATLAS_df, plot_mode)
	
	return None



if __name__ == '__main__':
	main()