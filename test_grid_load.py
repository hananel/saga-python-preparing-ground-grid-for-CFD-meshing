#!/usr/bin/python

import sys
import os
from saga_api import CSG_Module_Library, CSG_String

def get_module_number(lib, mod_name):
    mlb = CSG_Module_Library()
    if mlb.Create(CSG_String(lib)) == 0:
        print "failed to open %s" % lib
        raise SystemExit
    for i, cand in enumerate(map(mlb.Get_Module, xrange(mlb.Get_Count()))):
        if mod_name in cand.Get_Name():
            print "found %s in number %d" % (cand.Get_Name(),i)
            return i
    print "could not find %r in %r" % (mod_name, lib)
    raise SystemExit

def test_usgs_srtm(hgt_file='N15W084.hgt'):
    lib = os.path.expanduser('~/.local/lib/saga/libio_grid.so')
    n = get_module_number(lib, u'Import USGS SRTM Grid')
    mlb = CSG_Module_Library()
    mlb.Create(CSG_String(lib))
    usgs_srtm = mlb.Get_Module(n)
    p = usgs_srtm.Get_Parameters()
    #return usgs_srtm, p
    # p('GRIDS') # unset, but defined in the module
    #p('RESOLUTION').Set_Value(1) # 3 arc seconds. 0 is 1 arc seconds.
    p('FILE').Set_Value(hgt_file)
    print usgs_srtm.Get_Name(), ":", p('FILE').asString()
    ret = usgs_srtm.Execute()
    if not ret:
        print "load failed"
    else:
        print "load succeeded"

if __name__ == '__main__':
    test_usgs_srtm()
