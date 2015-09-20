### Group Name: group88

### Members:
  - Penghua Zhao (phzhao)
  - Dapeng Hong (hongdp)
  - Chengwei Dai (joedai)
  

### Details:
  - [Link For Running Version](http://eecs485-09.eecs.umich.edu:5688/sksnf4gf1or/pa1/)

### Deploy: 
  - `cd pa1/python/`
  - `virtualenv venv --distribute`
  - `source venv/bin/activate` (run for every new terminal window)
  - `pip install -r requirements.txt`
  - `gunicorn -b eecs485-09.eecs.umich.edu:5688 -b eecs485-09.eecs.umich.edu:5788 -w 4 -D app:app`
  - go to link above
