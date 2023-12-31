"""

Define TropCyclone class.
"""

__all__ = ['TCRain']

import itertools
import logging
import datetime as dt
import numpy as np
import numba
from scipy import sparse

from pinar.hazard.base import Hazard
from pinar.hazard.trop_cyclone import TropCyclone
from pinar.hazard.tag import Tag as TagHazard
from pinar.hazard.centroids.centr import Centroids

LOGGER = logging.getLogger(__name__)

HAZ_TYPE = 'TR'

class TCRain(Hazard):
    """Contains rainfall from tropical cyclone events."""

    intensity_thres = .1
    """intensity threshold for storage in mm"""

    def __init__(self, pool=None):
        """Empty constructor."""
        Hazard.__init__(self, HAZ_TYPE)
        self.category = np.array([], int)
        self.basin = list()
        if pool:
            self.pool = pool
            LOGGER.info('Using %s CPUs.', self.pool.ncpus)
        else:
            self.pool = None

    def set_from_tracks(self, *args, **kwargs):
        """This function is deprecated, use TCRain.from_tracks instead."""
        LOGGER.warning("The use of TCRain.set_from_tracks is deprecated."
                       "Use TCRain.from_tracks instead.")
        if "intensity_thres" not in kwargs:
            # some users modify the threshold attribute before calling `set_from_tracks`
            kwargs["intensity_thres"] = self.intensity_thres
        if self.pool is not None and 'pool' not in kwargs:
            kwargs['pool'] = self.pool
        self.__dict__ = TCRain.from_tracks(*args, **kwargs).__dict__

    @classmethod
    def from_tracks(cls, tracks, centroids=None, dist_degree=3, description='', pool=None,
                    intensity_thres=None):
        """Computes rainfield from tracks based on the RCLIPER model.
        Parallel process.

        Parameters
        ----------
        tracks : TCTracks
            tracks of events
        centroids : Centroids, optional
            Centroids where to model TC.
            Default: global centroids.
        disr_degree : int
            distance (in degrees) from node within which
            the rainfield is processed (default 3 deg,~300km)
        description : str, optional
            description of the events
        pool : pathos.pool, optional
            Pool that will be used for parallel computation of wind fields. Default: None
        intensity_thres : float, optional
            Wind speeds (in mm) below this threshold are stored as 0. Default: .1

        Returns
        -------
        haz : TCRain
            New TCRain object with data from tracks.
        """
        intensity_thres = cls.intensity_thres if intensity_thres is None else intensity_thres
        num_tracks = tracks.size
        if centroids is None:
            centroids = Centroids.from_base_grid(res_as=360, land=True)

        if not centroids.coord.size:
            centroids.set_meta_to_lat_lon()

        LOGGER.info('Mapping %s tracks to %s centroids.', str(tracks.size),
                    str(centroids.size))
        if pool:
            chunksize = min(num_tracks // pool.ncpus, 1000)
            tc_haz = pool.map(cls._from_track, tracks.data,
                              itertools.repeat(centroids, num_tracks),
                              itertools.repeat(dist_degree, num_tracks),
                              itertools.repeat(intensity_thres, num_tracks),
                              chunksize=chunksize)
        else:
            tc_haz = [cls._from_track(track, centroids, dist_degree=dist_degree,
                                      intensity_thres=intensity_thres)
                      for track in tracks.data]
        LOGGER.debug('Append events.')
        haz = cls.concat(tc_haz)
        LOGGER.debug('Compute frequency.')
        TropCyclone.frequency_from_tracks(haz, tracks.data)
        haz.tag.description = description
        return haz

    @staticmethod
    @numba.jit(forceobj=True)
    def _from_track(track, centroids, dist_degree=3, intensity_thres=0.1):
        """Set hazard from track and centroids.

        Parameters
        ----------
        track : xr.Dataset
            tropical cyclone track.
        centroids : Centroids
            Centroids instance.
        disr_degree : int
            distance (in degrees) from node within which
            the rainfield is processed (default 3 deg,~300km)
        intensity_thres : float
            min intensity threshold below which values are not considered

        Returns
        -------
        haz : TCRain
            New TCRain object with data from track.
        """
        new_haz = TCRain()
        new_haz.tag = TagHazard(HAZ_TYPE, 'IBTrACS: ' + track.name)
        new_haz.intensity = rainfield_from_track(track, centroids, dist_degree, intensity_thres)
        new_haz.units = 'mm'
        new_haz.centroids = centroids
        new_haz.event_id = np.array([1])
        # frequency set when all tracks available
        new_haz.frequency = np.array([1])
        new_haz.event_name = [track.sid]
        new_haz.fraction = new_haz.intensity.copy()
        new_haz.fraction.data.fill(1)
        # store date of start
        new_haz.date = np.array([dt.datetime(
            track.time.dt.year[0], track.time.dt.month[0],
            track.time.dt.day[0]).toordinal()])
        new_haz.orig = np.array([track.orig_event_flag])
        new_haz.category = np.array([track.category])
        new_haz.basin = [str(track.basin.values[0])]
        return new_haz

def rainfield_from_track(track, centroids, dist_degree=3, intensity=0.1):
    """Compute rainfield for track at centroids.
    Parameters
    ----------
    track : xr.Dataset
        tropical cyclone track.
    centroids : Centroids
        Centroids instance.
    disr_degree : int
        distance (in degrees) from node within which
        the rainfield is processed (default 3 deg,~300km)
    intensity : int
        min intensity threshold below which values are not
        considered
    """
    dlon, dlat = dist_degree, dist_degree

    n_track_nodes = len(track.lat)
    n_centroids = len(centroids.lat)
    cos_centroids_lat = np.cos(centroids.lat / 180 * np.pi)

    rainsum = np.zeros(n_centroids)

    # transform wind speed in knots
    if track.max_sustained_wind_unit == 'kn':
        pass
    elif track.max_sustained_wind_unit == 'km/h':
        track.max_sustained_wind /= 1.852
    elif track.max_sustained_wind_unit == 'mph':
        track.max_sustained_wind /= 1.151
    elif track.max_sustained_wind_unit == 'm/s':
        track.max_sustained_wind /= (1000 * 60 * 60)
        track.max_sustained_wind /= 1.852

    track.attrs['max_sustained_wind_unit'] = 'kn'

    lats = track.lat.values
    lons = track.lon.values

    for node in range(n_track_nodes):
        inreach = (np.abs(centroids.lat - lats[node]) < dlat) \
                & (np.abs(centroids.lon - lons[node]) < dlon)

        if inreach.any():
            pos = np.where(inreach)[0]

            fradius_km = np.zeros(n_centroids)
            dd = ((lons[node] - centroids.lon[pos]) * cos_centroids_lat[pos])**2 \
                + (lats[node] - centroids.lat[pos])**2

            fradius_km[pos] = np.sqrt(dd) * 111.12

            rainsum += _RCLIPER(track.max_sustained_wind.values[node],
                                inreach, fradius_km) * track.time_step.values[node]

    rainsum[rainsum < intensity] = 0

    return sparse.csr_matrix(rainsum)

def _RCLIPER(fmaxwind_kn, inreach, radius_km):
    """Calculate rainrate in mm/h based on RCLIPER given windspeed (kn) at
    a specific node
    Parameters
    ----------
    fmaxwind_kn : float
        maximum sustained wind at specific node
    inreach : np.array, boolean
        1 if centroid is within dist_degree,
        0 otherwise
    radius_km : np.array
        distance to node for every centroid
    """

    rainrate = np.zeros(len(inreach))

    # Define Coefficients (CLIPER NHC bias adjusted (Tuleya, 2007))
    a1 = -1.1  # inch per day
    a2 = -1.6  # inch per day
    a3 = 64.   # km
    a4 = 150.  # km

    b1 = 3.96  # inch per day
    b2 = 4.8  # inch per day
    b3 = -13.  # km
    b4 = -16.  # km

    u_norm_kn = 1. + (fmaxwind_kn - 35.) / 33.

    T0 = a1 + b1 * u_norm_kn
    Tm = a2 + b2 * u_norm_kn
    rm = a3 + b3 * u_norm_kn
    r0 = a4 + b4 * u_norm_kn

    i = (radius_km <= rm) & inreach
    ii = (radius_km > rm) & inreach

    # Calculate R-Cliper symmetric rain rate in mm/h
    rainrate[i] = (T0 + (Tm - T0) * (radius_km[i] / rm)) / 24. * 25.4
    rainrate[ii] = (Tm * np.exp(-(radius_km[ii] - rm) / r0)) / 24. * 25.4

    rainrate[np.isnan(rainrate)] = 0
    rainrate[rainrate < 0] = 0

    return rainrate
