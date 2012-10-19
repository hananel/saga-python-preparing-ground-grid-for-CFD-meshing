import saga_api, sys, os

##########################################
def grid_contour(fGrid, fLines):
#   fmlb    = '/usr/local/lib/saga/libshapes_grid.so' # Linux
    fmlb    = os.environ['SAGA'] + '/bin/saga_vc_Win32/modules/shapes_grid.dll' # Windows
    mlb     = saga_api.CSG_Module_Library()

    print 'load module library: ' + fmlb
    if mlb.Create(saga_api.CSG_String(fmlb)) == 0:
        print '... failed'
        return 0
    print '... success'

    m       = mlb.Get_Module_Grid('Contour Lines from Grid')
    p       = m.Get_Parameters()
    Grid    = saga_api.SG_Create_Grid()
    
    print 'load grid file: ' + fGrid
    if Grid.Create(saga_api.CSG_String(fGrid)) == 0:
        print '... failed'
        return 0
    print '... success'

    Lines   = saga_api.SG_Create_Shapes()

    m.Get_System().Assign(Grid.Get_System()) # module needs to use conformant grid system!
    p('INPUT')  .Set_Value(Grid)
    p('CONTOUR').Set_Value(Lines)
    p('ZSTEP')  .Set_Value(25.0)

    print 'execute module: ' + m.Get_Name()
    if m.Execute() == 0:
        print '... failed'
        return 0
    print '... success'

    Lines.Save(saga_api.CSG_String(fLines))
    
    return 1

##########################################
if __name__ == '__main__':
    print 'Python - Version ' + sys.version
    print saga_api.SAGA_API_Get_Version()
    print

    if len( sys.argv ) != 4:
        print 'Usage: grid_contour.py <in: grid> <out: contour>'
        fGrid   = './test.sgrd'
        fLines  = './contour'
    else:
        fGrid   = sys.argv[1]
        if os.path.split(fGrid)[0] == '':
            fGrid   = './' + fGrid

        fLines  = sys.argv[2]
        if os.path.split(fLines)[0] == '':
            fLines  = './' + fLines

    grid_contour(fGrid, fLines)
