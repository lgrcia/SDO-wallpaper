# Solar Dynamics Observatory living wallpaper

Get a randomized one of the [Solar Dynamics Observatory](https://sdo.gsfc.nasa.gov/data/) latest images as your desktop background every time you run it.


## Installation

```bash
conda create -n sdo-osx python=3.10
conda activate sdo-osx
pip install -r requirements.txt
```
python path at `which python`

## Execution

```bash
python main.py
```
## Cron

```bash
crontab -e
*/5 * * * * <command to execute>
```