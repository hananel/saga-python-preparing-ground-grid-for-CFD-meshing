import saga_api, sys, os

##########################################
def shp2xyz(fshp, fxyz):
#   fmlb    = '/usr/local/lib/saga/libio_shapes.so' # Linux
    fmlb    = os.environ['SAGA'] + '/bin/saga_vc_Win32/modules/io_shapes.dll' # Windows
    mlb     = saga_api.CSG_Module_Library()
    shp     = saga_api.SG_Create_Shapes()

    print 'load module library: ' + fmlb
    if mlb.Create(saga_api.CSG_String(fmlb)) == 0:
        print '... failed'
        return 0
    print '... success'

    m   = mlb.Get_Module(2)
    p   = m.Get_Parameters()

    print 'load shape file: ' + fshp
    if shp.Create(saga_api.CSG_String(fshp)) == 0:
        print '... failed'
        return 0
    print '... success'

    p('SHAPES')     .Set_Value(shp)
    p('FILENAME')   .Set_Value(fxyz)

    print p('SHAPES'  ).Get_Name() + ' >> ' + p('SHAPES'  ).asString()
    print p('FILENAME').Get_Name() + ' >> ' + p('FILENAME').asString()

    print 'execute module: ' + m.Get_Name()
    if m.Execute() == 0:
        print '... failed'
        return 0
    print '... success'

    return 1

if __name__ == '__main__':
    print 'Python - Version ' + sys.version
    print saga_api.SAGA_API_Get_Version()
    print

    if len( sys.argv ) != 3:
        print 'Usage: shp2xyz.py <in: shape file> <out: x/y/z-data as text table>'
        fshp = './contour.shp'
        fxyz = './test.xyz'
    else:
        fshp = sys.argv[1]
        if os.path.split(fshp)[0] == '':
            fshp = './' + fshp
            fxyz = sys.argv[2]

    shp2xyz(fshp, fxyz)
