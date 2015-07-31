
# Info
__author__ = 'Laufire Technologies'
__email__ = 'laufiretechnologies@gmail.com'
__version__ = '0.0.1'

# Imports
from docutils import nodes
from docutils.nodes import paragraph
from docutils.parsers.rst import Directive
from sphinx.addnodes import desc, desc_name, desc_addname, desc_content, desc_signature, desc_parameterlist, desc_parameter, desc_optional, compact_paragraph

# Helpers
def getArgDesc(Arg):
  _type = Arg.get('type')
  
  return Arg.get('desc', Arg['type_str'])

def getArgLabel(Arg):
  return (desc_parameter if not 'default' in Arg else desc_optional)('', Arg['name'])

def getArgsContent(Args):
  Container = desc('', desc_signature(text='Args'), objtype="Args")
  
  for name, Arg in Args.items():
    Content = desc_content()
    Content.append(desc_name(text='%s: ' % name))
    Content.append(compact_paragraph(text='%s.' % getArgDesc(Arg)))
    Container.append(Content)
    
  return Container

def getArgList(Args):
  return desc_parameterlist('', '', *[getArgLabel(Arg) for Arg in Args.values()])

def getMemberContent(Member, *Children):
  Config = Member.Config
  Content = desc_content(*Children)
  
  doc = Member.Underlying.__doc__
  if doc:
    Content.insert(0, paragraph(text=doc))
  
  if 'desc' in Config:
    Content.insert(0, paragraph(text=Config['desc']))
  
  return Content
  
def getMemberTitle(Config):
  return '%s%s' % (Config['name'], ', %s' % Config['alias'] if 'alias' in Config else '')
  
def getSignature(Config):
  return desc_signature(text=getMemberTitle(Config))
  
def getTaskTree(Task, id):
  Config = Task.Config
  
  Elms = [nodes.target('', '', ids=[id])]
  
  content = getMemberContent(Task)
  signature = getSignature(Config)
  signature.append(getArgList(Task.Args))
  
  if Task.Args:
    content.append(getArgsContent(Task.Args))
  
  Elms.append(desc(id, signature, content, id=id, objtype='Task'))
  
  return Elms
  
def getChildren(Parent, prefix):
  Children = []
  
  for name, Child in Parent.Members.iteritems():
    if Child.Config.get('alias') == name: # don't process aliases
      continue
      
    id = '%s.%s' % (prefix, name)
    
    if hasattr(Child, 'Members'):
      Children += desc_content(prefix, *getGroupTree(Child, id))
      
    else:
      Children += desc_content(prefix, *getTaskTree(Child, id))
  
  return Children
  
def getGroupTree(Group, prefix):
  return [
    nodes.target('', '', ids=[prefix]),
    desc(prefix,
      getSignature(Group.Config),
      getMemberContent(Group, *getChildren(Group, prefix)),
      id=prefix, objtype='Group'
    )
  ]
  
def getModuleTree(Module, prefix):
  Elms = [nodes.target('', '', ids=[prefix])]
  
  Section = nodes.section()
  Section  += nodes.title(text=getMemberTitle(Module.Config))
  Section += getChildren(Module, prefix)
  
  return Elms + [Section]
  
# Main
from ec import interface # importing this automatically makes the imported ec scripts to be configured

def setup(app):
  app.add_directive('ec_module', EcModuleDirective)

  return {'version': '0.1'}   # identifies the version of our extension
  
class EcModuleDirective(Directive):

  has_content = True # this enables content in the directive

  def run(self):
    env = self.state.document.settings.env
    
    module_name = self.content[0]
    module = __import__(module_name)
    
    return getModuleTree(module.__ec_member__, "ec-%d-%s" % (env.new_serialno('ec'), module.__ec_member__.Config['name']))
  