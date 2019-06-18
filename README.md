# Comics publisher

The script posts random comic from [xkcd](https://xkcd.com/) on wall in your vk group.


# How to start

Python3 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

### Environment variables.

- GROUP_ID
- ACCESS_TOKEN
- API_VERSION
- PATH_TO_IMAGES

Default value of `PATH_TO_IMAGES` is `images`

.env example:

```
GROUP_ID=123456789
ACCESS_TOKEN=0ff1884291ba11e9b603f0921ce54618206c661e91ba11e984f6f0921ce54618a11e9afc4f0921ce54618
API_VERSION=5.95
PATH_TO_IMAGES=comics
```
### How to get

* Sign up [vk](https://vk.com)
* Register stand-alone app
* Follow instructions [Implicit Flow](https://vk.com/dev/implicit_flow_group)

### Run

Launch on Linux(Python 3.5) or Windows as simple. Then check vk group wall.

```bash
$ python main.py

```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)