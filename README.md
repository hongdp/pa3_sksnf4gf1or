### Group Name: group88

### Members:
  - Penghua Zhao (phzhao)
  - Dapeng Hong (hongdp)
  - Chengwei Dai (joedai)


### Details:
  - [Link For Running Version](http://eecs485-09.eecs.umich.edu:5888/sksnf4gf1or/pa2/)

### Deploy:
  - `cd pa2/python/`
  - `virtualenv venv --distribute`
  - `source venv/bin/activate` (run for every new terminal window)
  - `pip install -r requirements.txt`
  - `gunicorn -b eecs485-09.eecs.umich.edu:5888 -b eecs485-09.eecs.umich.edu:5988 -w 4 -D app:app`
  - go to link above

### Details:
  - 'We did extra credit 1 and 2. So when you register for new user with a working email address, you should receiced a confirmation letter from group88eecs485@gmail.com with a link to home page '
  - 'When you hit forget password in login page, you are asked to type the username and then a email with new password will send to your email on that username.'
  - 'We also did the alignment!'
