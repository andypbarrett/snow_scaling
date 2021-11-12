
# coding: utf-8

# In[14]:


parallel = True
home_dir = '/global/scratch/bolliger/tuolumne'

# variogram params
res = 3
n_lags = 100
max_dist = 1000
pts_per_lag = 10000

from sys import path
path.append('../scripts')
from ipyparallel import require

# get mapping functions
from utilities import get_apply_map_funcs, gather_files, Settings
myapply, mymap, c, dview, lview = get_apply_map_funcs(parallel)

with dview.sync_imports():
    from os.path import join
    import rasterio
    from rasterio import mask
    from matplotlib import pyplot as plt
    import fiona
    import numpy as np
    import pickle
    from os.path import dirname, exists, split
    import os
    
dview.execute("""
plt = pyplot
np = numpy
""")

# import project settings
s = Settings(home_dir)
s.local={}
s.local['res'] = res
s.local['n_lags'] = n_lags
s.local['max_dist'] = max_dist
s.local['pts_per_lag'] = pts_per_lag
dview.push({'s_local':s.local})

# double check number of engines
if parallel:
    print(len(c.ids))


# In[15]:


hs_fnames = [f for f in gather_files(join(s.data_dir,'1_resampled/global/snow_depth')) if '3m_orig3m' in f]

hs_fname = join(s.data_dir,'1_resampled','global','snow_depth',
                                  '2016','{}m_orig3m'.format(res),'20160326_snow_depth.tif')
out_fnames = [join(home_dir,'results','regional_variograms',*f.split('/')[-4:]).replace(
    '.tif','.pickle') for f in hs_fnames] 

shp_dir = join(s.data_dir,'raw','circular_regions')
circles_fname = join(shp_dir,'sample_circles1km_hex_TB.shp')

with fiona.open(circles_fname,'r') as shp:
    circles = [feature["geometry"] for feature in shp]
    circle_ids = [feature['properties']['Unique_ID'] for feature in shp]


# In[16]:


def get_valid_vals(z,x,y,ndv,include_zeros=False):
    valid_vals = z!=ndv
    
    if not include_zeros:
        valid_vals = np.logical_and(valid_vals,z!=0)
    
    return valid_vals

@require(get_valid_vals)
def calc_variogram(raster,lags,pts_per_lag,res,ndv,circular_mask=True,include_zeros=False):

    # estimate number of points needed based on points that fall outside of mask
    if circular_mask:
        pts_per_lag = (4 / np.pi) * pts_per_lag
    
    # estimate number of points needed based on number of zero vals
    n_zero = (raster==0).sum()
    n_total = (raster!=ndv).sum()
    if n_zero == n_total:
        return None,None,None
    
    if not include_zeros:
        multiplier = n_total / (n_total - n_zero)
        pts_per_lag = int(pts_per_lag * multiplier)
    
    # get sample points and directions to come up with pairs
    range_x = raster.shape[1]
    range_y = raster.shape[0]
    x_sample_ix = np.random.randint(range_x, size = pts_per_lag)
    y_sample_ix = np.random.randint(range_y, size = pts_per_lag)
    
    # get sample values for these initially selected points
    sample_vals = raster[y_sample_ix,x_sample_ix]
    
    # ignore points outside of circle mask or zero snow depth
    valid_sample = get_valid_vals(
        sample_vals,x_sample_ix,y_sample_ix,ndv,include_zeros=include_zeros)
    x_sample_ix = x_sample_ix[valid_sample]
    y_sample_ix = y_sample_ix[valid_sample]
    
    n_pts = x_sample_ix.shape[0]
    
    # get random set of directions
    dirs_sample = 2*np.pi*np.random.random(n_pts)

    
    ## loop through distances and estimate variance for pairs of that distance
    var_mean = []
    var_se = []
    n_pts = []
    for i,b in enumerate(lags):
        
        # distance in pixels
        b_ix = b / res
        
        # find comparison point
        x_compare_ix = (x_sample_ix + np.cos(dirs_sample) * b_ix).round().astype(int)
        y_compare_ix = (y_sample_ix + np.sin(dirs_sample) * b_ix).round().astype(int)

        # make sure we're not looking outside of the raster at all
        within_extent = np.logical_and(np.logical_and((x_compare_ix >= 0),(x_compare_ix < range_x)),
                                    np.logical_and((y_compare_ix >= 0),(y_compare_ix < range_y)))
        x_sample_ix_tmp = x_sample_ix[within_extent]
        y_sample_ix_tmp = y_sample_ix[within_extent]
        x_compare_ix = x_compare_ix[within_extent]
        y_compare_ix = y_compare_ix[within_extent]
        
        # make sure comparison point is not outside of circle
        compare_vals = raster[y_compare_ix,x_compare_ix]
        valid_compare = get_valid_vals(
                compare_vals,x_compare_ix,y_compare_ix,ndv,include_zeros=include_zeros)
        
        x_compare_ix = x_compare_ix[valid_compare]
        y_compare_ix = y_compare_ix[valid_compare]
        x_sample_ix_tmp = x_sample_ix_tmp[valid_compare]
        y_sample_ix_tmp = y_sample_ix_tmp[valid_compare]

        vals_sample = raster[y_sample_ix_tmp,x_sample_ix_tmp]
        vals_compare = raster[y_compare_ix,x_compare_ix]

        sq_diffs = np.square(vals_compare - vals_sample)
        var_mean.append(sq_diffs.mean())
        var_se.append(sq_diffs.std(ddof=1) / np.sqrt(len(sq_diffs)))
        n_pts.append(len(sq_diffs))

    var_mean = np.array(var_mean)
    var_se = np.array(var_se)
    n_pts = np.array(n_pts)

    return var_mean,var_se,n_pts


# In[17]:


@require(calc_variogram)
def get_all_variograms(raster_fname,out_fname):
    if not exists(dirname(out_fname)):
        os.makedirs(dirname(out_fname),exist_ok=True)
    
    rast = rasterio.open(raster_fname)
    
    variogram_vals = {'mean':[],
                 'se':[],
                 'n_pts':[],
                  'circle_ids':[],
                 'lags':lags}

    for ix,this_circ in enumerate(circles):
        try:
            out_image, out_transform = mask.mask(rast, [this_circ], crop=True)
        # if non-overlapping circles and raster, skip this circle
        except:
            continue
        var_mean,var_se,n_pts = calc_variogram(out_image[0],lags,s_local['pts_per_lag'],s_local['res'],ndv,
                                               circular_mask=True,include_zeros=False)
        if type(var_mean) != type(None):
            variogram_vals['mean'].append(var_mean)
            variogram_vals['se'].append(var_se)
            variogram_vals['n_pts'].append(n_pts)
            variogram_vals['circle_ids'].append(circle_ids[ix])

    with open(out_fname,'wb') as f_out:
        pickle.dump(variogram_vals,f_out)
    
    return None


# In[ ]:


## generate bins
min_dist = res
lags = np.logspace(np.log10(min_dist),np.log10(max_dist),n_lags)

dview.push({'circles':circles,
           'circle_ids':circle_ids,
           'lags':lags,
           'ndv':s.ndv})

n_files = len(hs_fnames)
mymap(get_all_variograms,hs_fnames,out_fnames)

