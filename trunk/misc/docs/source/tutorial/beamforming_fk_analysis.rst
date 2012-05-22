=========================
Beamforming - FK Analysis
=========================

The following code shows how to do an FK Analysis with ObsPy. The data are from
the blasting of the AGFA skyscraper in Munich (:meth:`pickled <pickle.dump>` stream
object with paz attached to each :class:`~obspy.core.trace.Trace`, can also be
found `here <http://examples.obspy.org/agfa.dump>`_). We execute
:func:`~obspy.signal.array_analysis.sonic` using the following settings:

* The slowness grid is set to corner values of -3.0 to 3.0 s/km with a step
  fraction of ``sl_s = 0.03``.
* The window length is 1.0 s, using a step fraction of 0.05 s.
* The data is bandpass filtered, using corners at 1.0 and 8.0 Hz,
  prewhitening is disabled.
* ``semb_thres`` and ``vel_thres`` are set to infinitesimally small numbers
  and must not be changed.
* The ``timestamp`` will be written in ``'mlabdays'``, which can be read
  directly by our plotting routine.
* ``stime`` and ``etime`` have to be given in the UTCDateTime format.

The output will be stored in ``out``.

The second half shows how to plot the output. We use the output
``out`` produced by :func:`~obspy.signal.array_analysis.sonic`, which are
:class:`numpy ndarrays <numpy.ndarray>` containing timestamp, relative power,
absolute power, backazimuth, slowness. The colorbar corresponds to relative
power.

.. include:: beamforming_fk_analysis_1.py
   :literal:

.. plot:: source/tutorial/beamforming_fk_analysis_1.py

Another representation would be a polar plot, which sums the relative power in
gridded bins, each defined by backazimuth and slowness of the analyzed signal
part. The backazimuth is counted clockwise from north, the slowness limits can
be set by hand.

.. include:: beamforming_fk_analysis_2.py
   :literal:

.. plot:: source/tutorial/beamforming_fk_analysis_2.py
