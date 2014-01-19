import py, re, os, signal, time
from subprocess import Popen, PIPE

mod_re = (r"\bmodule\s+(", r")\s*\(\s*")
func_re = (r"\bfunction\s+(", r")\s*\(")

def extract_mod_names(fpath, name_re=r"\w+"):
    regex = name_re.join(mod_re)
    matcher = re.compile(regex)
    return (m.group(1) for m in matcher.finditer(fpath.read()))

def extract_func_names(fpath, name_re=r"\w+"):
    regex = name_re.join(func_re)
    matcher = re.compile(regex)
    return (m.group(1) for m in matcher.finditer(fpath.read()))

def collect_test_modules():
    dirpath = py.path.local("./")
    print "Collecting openscad test module names"
    
    test_files = {}
    for fpath in dirpath.visit('*.scad'):
        #print fpath
        modules = extract_mod_names(fpath, r"test\w*")
        #functions = extract_func_names(fpath, r"test\w*")
        test_files[fpath] = modules
    return test_files

collect_test_modules()

def call_openscad(path, stlpath, timeout=20):
    try:
        proc = Popen(['openscad', '-s', str(stlpath),  str(path)],
            stdout=PIPE, stderr=PIPE, close_fds=True)
        calltime = time.time()
        #print calltime
        while True:
            if proc.poll() is not None:
                break
            time.sleep(0.1)
            #print time.time()
            if time.time() > calltime + timeout:
                raise Exception("Timeout")
    finally:
        try:
            proc.terminate()
            proc.kill()
        except OSError:
            pass

    return (proc.returncode,) + proc.communicate()
