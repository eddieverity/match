class OrderedDictionary(object):
  def __init__(self):
    self.keys = []
    self.data = {}

  def __str__(self):
    return str(self.keys) + "\n" + str(self.data)

  def put(self, key, value):
    self.keys.append(key)
    self.data[key] = value

  def get_by_index(self, index):
    try:
      return self.data[self.keys[index]]
    except:
      return None

  def get_by_key(self, key):
    return self.data[key]

  def transform(self):
    t = []
    for k in self.keys:
      t.append(self.data[k])



test = OrderedDictionary()
test.put('hello1', 'edward')
test.put('hello2', 'peter')
test.put('hello3', 'fiaz')

# print test

# print test.get_by_index(5)