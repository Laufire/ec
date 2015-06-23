import sys

# State
mode = None

def start():
  argv = sys.argv[1:]
  
  if not argv:
    show_usage()
    return
    
  global mode
  mode = 'd' if len(argv) == 1 else 's' # dispatch / shell mode
  
  if mode == 'd':
    import shell
    shell.init()
    
  else:
    import dispatch
    dispatch.init(argv[1:])
    
def show_usage():
  print 'private module_path <command route> [options]'
  