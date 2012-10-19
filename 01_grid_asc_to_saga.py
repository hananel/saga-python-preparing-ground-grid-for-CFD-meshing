import saga_api, sys, os

##########################################
def grid_asc2sgrd(fASC):
    fmlb    = '/usr/local/lib/saga/libio_grid.so'     # Linux
#   fmlb    = os.environ['SAGA'] + '/bin/saga_vc_Win32/modules/io_grid.dll' # Windows
    mlb     = saga_api.CSG_Module_Library()

    import pdb; pdb.set_trace()
    print 'load module library: ' + fmlb
    if mlb.Create(saga_api.CSG_String(fmlb)) == 0:
        print '... failed'
        return 0
    print '... success'

    m       = mlb.Get_Module(1)
    p       = m.Get_Parameters()
    p('FILE').Set_Value(fASC)

    print m.Get_Name() + ': ' + p('FILE').asString()
    if m.Execute() == 0:
        print '... failed'
        return 0
    print '... success'

    print 'save as SAGA grid'
    if p('GRID').asGrid().Save(saga_api.CSG_String(fASC)) == 0:
        print '... failed'
        return 0
    print '... success'
    
    return 1

##########################################
if __name__ == '__main__':
    import pdb; pdb.set_trace()
    print 'Python - Version ' + sys.version
    print saga_api.SAGA_API_Get_Version()
    if len(sys.argv) != 2:
        print 'Usage: grid_asc_to_saga.py <in: ascii grid file>'
        fASC    = './test.asc'
        fASC    = os.path.abspath(fASC)
    else:
        fASC    = sys.argv[1]
        if os.path.split(fASC)[0] == '':
            fASC    = './' + fASC
	
    grid_asc2sgrd(fASC)
