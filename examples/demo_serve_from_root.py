# An example of how to publish a simple wsgi app under isapi_wsgi and serve
# from IIS root.
# Using the ISAPISimpleHandler which will create a new instance for each incoming
# request.
#
# Executing this script (or any server config script) will install the extension
# into your web server and will create a "loader" DLL _demo.dll in the 
# current directory. As the server executes, the PyISAPI framework will load
# this module and create the Extension object.
# A Virtual Directory named "isapi-wsgi-demo" is setup. This dir has the ISAPI
# WSGI extension as the only application, mapped to file-extension '*'.  
# Therefore, isapi_wsgi extension handles *all* requests in this directory.
#
# To launch this application from a web browser use a url similar to:
#
#  http://localhost/
#
# A "Hello world!" and the WSGI environment should be displayed.

def demo_app(environ,start_response):
    """Demo app from wsgiref"""
    start_response("200 OK", [('Content-Type', 'text/plain')])
    cr = lambda s='': s + '\n'
    yield cr("Hello world!")
    yield cr()
    for item in sorted(environ.items()):
        yield cr(' = '.join(item))

import isapi_wsgi
# The entry points for the ISAPI extension.
def __ExtensionFactory__():
    return isapi_wsgi.ISAPISimpleHandler(demo_app)

if __name__=='__main__':
    # If run from the command-line, install ourselves.
    from isapi.install import *
    params = ISAPIParameters()
    # Setup the virtual directories - this is a list of directories our
    # extension uses - in this case only 1.
    # Each extension has a "script map" - this is the mapping of ISAPI
    # extensions.
    sm = [
        ScriptMapParams(Extension="*", Flags=0)
    ]
    # To serve from root, just set Name="/"
    vd = VirtualDirParameters(Name="/",
                              Description = "ISAPI-WSGI ISAPISimpleHandler root Demo",
                              ScriptMaps = sm,
                              ScriptMapUpdate = "replace"
                              )
    params.VirtualDirs = [vd]
    HandleCommandLine(params)
