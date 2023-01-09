# Performance_Check

### How to use - AMD machine
1. Install the modules
```shell
pip3 install -r requirements.txt
```

2. Execute
- Enter after `--time` how many seconds you want to save computer information every few seconds.
```shell
cd ./src/amd
python3 amd_main.py --time 30
```

3. Computer information is saved the `./data` folder

---


### How to use - ARM machine
1. Install the modules
```shell
pip3 install -r requirements.txt
```

2. Execute
- Enter after `--time` how many seconds you want to save computer information every few seconds.
```shell
cd ./src/arm
python3 arm_main.py --time 30
```