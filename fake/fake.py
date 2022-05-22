def use_fakes():
  import os, sys
  fake_dir = os.path.join(os.path.dirname(__package__), 'fake')
  assert(os.path.exists(fake_dir))
  sys.path.insert(0, fake_dir)