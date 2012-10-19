import saga_api, sys, os

##########################################
def xyz2shp(fTable):
    print saga_api.SAGA_API_Get_Version()

#   fmlb    = '/usr/local/lib/saga/libshapes_points.so' # Linux
    fmlb    = os.environ['SAGA'] + '/bin/saga_vc_Win32/modules/shapes_points.dll' # Windows
    mlb     = saga_api.CSG_Module_Library()

    print 'load module library: ' + fmlb
    if mlb.Create(saga_api.CSG_String(fmlb)) == 0:
        print '... failed'
        return 0
    print '... success'

    # 1. load table from file or create a test data set
    table   = saga_api.SG_Create_Table()

    if table.Create(saga_api.CSG_String(fTable)) == 0:
        table.Add_Field('X',saga_api.TABLE_FIELDTYPE_Float)
        table.Add_Field('Y',saga_api.TABLE_FIELDTYPE_Float)
        table.Add_Field('Z',saga_api.TABLE_FIELDTYPE_Float)
        rec = table.Add_Record()
        rec.Set_Value(0,0)
        rec.Set_Value(1,0)
        rec.Set_Value(2,2)
        rec = table.Add_Record()
        rec.Set_Value(0,0)
        rec.Set_Value(1,1)
        rec.Set_Value(2,2)
        rec = table.Add_Record()
        rec.Set_Value(0,1)
        rec.Set_Value(1,1)
        rec.Set_Value(2,1)
        rec = table.Add_Record()
        rec.Set_Value(0,1)
        rec.Set_Value(1,0)
        rec.Set_Value(2,1)

    # 2. convert table to points
    m   = mlb.Get_Module(0)
    p   = m.Get_Parameters()
    p('TABLE')  .Set_Value(table)
    p('POINTS') .Set_Value(saga_api.SG_Create_Shapes(saga_api.SHAPE_TYPE_Point))
    p('X')      .Set_Value(0)
    p('Y')      .Set_Value(1)

    print 'execute module: ' + m.Get_Name()
    if m.Execute() == 0:
        print '... failed'
        return 0
    print '... success'

    p('POINTS').asShapes().Save(saga_api.CSG_String(fTable))

    return 1

##########################################
if __name__ == '__main__':
    print 'Python - Version ' + sys.version
    print saga_api.SAGA_API_Get_Version()
    print

    if len( sys.argv ) != 2:
        print 'Usage: xyz2shp.py <in: x/y/z-data as text or dbase table>'
        fTable = './test.xyz'
    else:
        fTable = sys.argv[ 1 ]
        if os.path.split(fTable)[0] == '':
            fTable = './' + fTable

    xyz2shp(fTable)
