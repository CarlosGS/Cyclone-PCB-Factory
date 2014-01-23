import py

from openscad_utils import *

def pytest_generate_tests(metafunc):
    if "modpath" in metafunc.funcargnames:
        if "modname" in metafunc.funcargnames:
            for fpath, modnames in collect_test_modules().items():
                for modname in modnames:
                    metafunc.addcall(funcargs=dict(modname=modname, modpath=fpath))
        else:
            dirpath = py.path.local("./")
            for fpath in dirpath.visit('*.scad'):
                metafunc.addcall(funcargs=dict(modpath=fpath))

temppath = py.test.ensuretemp('MCAD')

def test_compile(modname, modpath):
    tempname = "test_" + modpath.basename + modname
    fpath = temppath.join(tempname)
    stlpath = temppath.join(tempname + ".stl")
    f = fpath.open('w')
    f.write("""
//generated testfile
include <%s>

%s()
""" % (modpath, modname))
    f.flush
    output = call_openscad(path=fpath, stlpath=stlpath)
    print output
    assert output[0] is 0
    assert "warning" or "error" not in output[2].strip().lowercase()
    assert len(stlpath.readlines()) > 2

def test_compile_default(modpath):
    tempname = "test_" + modpath.basename
    stlpath = temppath.join(tempname + ".stl")
    output = call_openscad(path=modpath, stlpath=stlpath)
    print output
    assert output[0] is 0
    assert "warning" or "error" not in output[2].strip().lowercase()


