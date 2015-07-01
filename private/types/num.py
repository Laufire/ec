class between(CustomType):
  """
  Used to get a number within two numbers.
  """
  def __init__(self, min, max, num_type=int):
    self.min = min
    self.max = max
    self.num_type = num_type
    
  def __call__(self, val):
    value = self.num_type(val)
    
    if value < self.min or value > self.max:
      raise ValueError('Invalid value.')
    
    return value
    
  def __str__(self):
    return 'a number between %s and %s' % (self.min, self.max)
