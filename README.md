# snow_scaling
The code in the repository documents and demonstrates a workflow for generating variograms for 
[Airborne Snow Observatory](https://www.airbornesnowobservatories.com/) (ASO) lidar data collected 
over the headwaters of the Tuolomne river basin, CA.

The repository holds original code deveopled by Ian Bolliger, UC Berkley.  Workflows developed by Ian
are documented in [notebooks/variograms_by_region_original.ipynb](https://github.com/andypbarrett/snow_scaling/blob/main/notebooks/variograms_by_region_original.ipynb).  Results of this analysis are in this 
presentation.

The original workflow was modified by Andy Barrett to use standard variogram functions from [`scikit-gstat`](https://mmaelicke.github.io/scikit-gstat/index.html), a SciPy-flavoured geostatistical toolbox written in python.  This workflow is 
documented in [notebooks/variogram_workflow.ipynb](https://github.com/andypbarrett/snow_scaling/blob/main/notebooks/variogram_workflow.ipynb).

Data are available from NSIDC **add link to dataset**.
