from  funs import *
import pytest 
import sys

@pytest.mark.number
def test_add():
  assert add(2,5)==7
  assert add(5)==8

@pytest.mark.number  
def test_mul():
  assert mul(4)==8

@pytest.mark.strings
def test_add_strings():
  result=add('Hello ','World')
  assert result == 'Hello World'
  assert type(result) is str
  assert 'Heldlo' not in result

@pytest.mark.strings  
def test_product_strings():
  assert mul('Hello ',3)=='Hello Hello Hello '
  result=mul('Hello ')
  assert result == 'Hello Hello '
  assert type(result) is str
  assert 'Hello' in result


@pytest.mark.skip(reason="Dont run test_addnum")
def test_addnum():
  assert add(2,5)==7
  assert add(5)==8

@pytest.mark.skipif(sys.version_info < (3,3),reason="Not Supported on Lower Version")
def test_versionmul():
  assert mul(4,5)==20
  print (mul(2,6) ,' -----------------------------')
  
 
@pytest.mark.parametrize('x,y,res',[(7,3,10),('Hello',' World','Hello World'),(10.11,15.14,25.25)])
def test_addparam(x,y,res):
  assert add(x,y)==res

#db=None
'''
def setup_module(module):
  print('-----------setup called when programme starts----------')
  global db
  db=StudentDB()
  db.connect('data.json')

def teardown_module(module):
  print('------shutdown is called when programme ends--------')
  db.close()
'''    
def test_scott_data(db):
  scott_data=db.get_data('Scott')
  assert scott_data['id']==1
  assert scott_data['name']=='Scott'
  assert scott_data['result']=='pass'
  
def test_mark_data(db):
 mark_data=db.get_data('Mark')
 assert mark_data['id']==2
 assert mark_data['name']=='Mark'
 assert mark_data['result']=='fail'
 
@pytest.fixture(scope='module')   ##
def db():
  print('--------Called at from fixture only once at begining----')
  db=StudentDB()
  db.connect('data.json')
  yield db
  print('------------Called once at end--------')
  db.close()  