import saga_api, sys, os

##########################################
def morphometry(fDEM, fSlope, fAspect):
#   fmlb    = '/usr/local/lib/saga/libta_morphometry.so' # Linux
    fmlb    = os.environ['SAGA'] + '/bin/saga_vc_Win32/modules/ta_morphometry.dll' # Windows
    mlb     = saga_api.CSG_Module_Library()

    print 'load module library: ' + fmlb
    if mlb.Create(saga_api.CSG_String(fmlb)) == 0:
        print '... failed'
        return 0
    print '... success'

    m       = mlb.Get_Module_Grid(0)
    p       = m.Get_Parameters()
    DEM     = saga_api.SG_Create_Grid()
    
    print 'load grid file: ' + fDEM
    if DEM.Create(saga_api.CSG_String(fDEM)) == 0:
        print '... failed'
        return 0
    print '... success'

    Slope   = saga_api.SG_Create_Grid(DEM.Get_System())
    Aspect  = saga_api.SG_Create_Grid(DEM.Get_System())

    m.Get_System().Assign(DEM.Get_System()) # module needs to use conformant grid system!
    p('ELEVATION').Set_Value(DEM)
    p('SLOPE')    .Set_Value(Slope)
    p('ASPECT')   .Set_Value(Aspect)

    print 'execute module: ' + m.Get_Name()
    if m.Execute() == 0:
        print '... failed'
        return 0
    print '... success'

    Slope .Set_Name('Slope')
    Aspect.Set_Name('Aspect')
    Slope .Save(saga_api.CSG_String(fSlope))
    Aspect.Save(saga_api.CSG_String(fAspect))
    
    return 1

##########################################
if __name__ == '__main__':
    print 'Python - Version ' + sys.version
    print saga_api.SAGA_API_Get_Version()
    print

    if len( sys.argv ) != 4:
        print 'Usage: morphometry.py <in: elevation> <out: slope> <out: aspect>'
        fDEM    = './test.sgrd'
        fSlope  = './slope'
        fAspect = './aspect'
    else:
        fDEM    = sys.argv[1]
        if os.path.split(fDEM)[0] == '':
            fDEM    = './' + fDEM

        fSlope  = sys.argv[2]
        if os.path.split(fSlope)[0] == '':
            fSlope  = './' + fSlope

        fAspect = sys.argv[3]
        if os.path.split(fAspect)[0] == '':
            fAspect = './' + fAspect

    morphometry(fDEM, fSlope, fAspect)
