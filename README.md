# Show me my salary

#### 이 프로젝트는 윈도우 피씨가 없어 급여명세서를 회사에서 보지 못했던 불편함을  만들어진 프로젝트 입니다. ~~(집에서 열기 귀찮아)~~

```bash
$ git clone https://github.com/zsaladin/show-me-my-salary
$ cd show-me-my-salary
$ virtualenv venv --python=python3.6
$ source venv/bin/activate
$ python show_me_my_salary.py '2017000012.htm' 19861212
```

위와 같은 커맨드를 사용하면 해당 htm 파일이 있던 경로에 복호화 된 명세서가 생성 됩니다.
