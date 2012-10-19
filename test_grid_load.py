#!/usr/bin/python

import saga_api, sys, os

def get_module_number(lib, mod_name):
    mlb = saga_api.CSG_Module_Library()
    if mlb.Create(saga_api.CSG_String(lib)) == 0:
        print "failed to open %s" % lib
        raise SystemExit
    for i in xrange(mlb.Get_Count()):
        cand = mlb.Get_Module(i)
        if mod_name in cand.Get_Name():
            print "found %s in number %d" % (cand.Get_Name(),i)
            return i
    print "could not find %r in %r" % (mod_name, lib)
    raise SystemExit

def test_usgs_srtm():
    lib = '/home/hanan/.local/lib/saga/libio_grid.so'
    n = get_module_number(lib, u'Import USGS SRTM Grid')
    mlb = saga_api.CSG_Module_Library()
    mlb.Create(saga_api.CSG_String(lib))
    usgs_srtm = mlb.Get_Module(n)
    p = usgs_srtm.Get_Parameters()
    return usgs_srtm, p
    # p('GRIDS') # unset, but defined in the module
    p('RESOLUTION').Set_Value(1) # 3 arc seconds. 0 is 1 arc seconds.
    p('FILE').Set_Value('/home/hanan/Download/N15W084.hgt.zip')
    if p.Execute() == 0:
        print "load failed"
    else:
        print "load succeeded"

