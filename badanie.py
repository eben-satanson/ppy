#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TODOs:
- [x] now0
- [x] sub0
- [x] timing (clocks)
- [x] logging in PsychoPy
- [x] logging in Python
- [x] logging to file
- [ ] save data after every movie
- [x] send markers to EEG (PyParallel)
- [ ] cleanup
- [ ] final testing

"""

import os
import uuid
import json
import srsly
import time 
import random
import pathlib
import pandas as pd
from datetime import datetime as dt
from pytz import timezone as tz
from sklearn.utils import Bunch

from typing import (Dict, Mapping)

import psychopy
import psychopy.gui
import psychopy.core
import psychopy.data
import psychopy.event
import psychopy.visual
import psychopy.parallel

from psychopy.constants import (PLAYING, PAUSED)
from psychopy import logging as log0
from psychopy import plugins
from psychopy import prefs

plugins.activatePlugins()
prefs.general["audioLib"] = ["pyo"]
prefs.general["audioLib"] = ["ptb"]
prefs.hardware["audioLib"] = ["ptb"]
prefs.hardware["audioLib"] = ["sounddevice"]
prefs.hardware["audioLatencyMode"] = "3"

clock_glob = psychopy.core.monotonicClock
clock_mono = psychopy.core.MonotonicClock()
clock_main = psychopy.core.Clock()
clock_resp = psychopy.core.Clock()

log_level_term = log0.CRITICAL
log_level_term = log0.ERROR
log_level_term = log0.WARNING
# log_level_term = log0.INFO
# log_level_term = log0.DEBUG

log_level_file = log0.CRITICAL
log_level_file = log0.ERROR
log_level_file = log0.WARNING
log_level_file = log0.INFO
# log_level_file = log0.DEBUG

log0.console.setLevel(log_level_term)


def jsonable(obj: Mapping, types=False) -> Dict:
    """JSONablify."""
    def default(o):
        return f"<<non-serializable: {type(o).__qualname__}>>" if types \
            else f"{o}"

    return json.loads(json.dumps(obj, default=default))


meta0 = Bunch()
meta0.loc0 = "Europe/Berlin"
meta0.now0 = f"{dt.now(tz(meta0.loc0)).strftime('%Y%m%dT%H%M%S')}"

dlg0 = psychopy.gui.Dlg(title="Exp:TF")
dlg0.addText("Participant info")
dlg0.addField(label="Code:", initial=f"s{meta0.now0}", required=True)
dlg0.addField(label="Session:", initial="s01", required=True)
dlg0.addField(label="Run:", initial="r01", required=True)
dlg0.addField(label="Age:", initial="", required=False)
dlg0.addField(label="Gender:", initial="", required=False)
dlg0.addText("PsychoPy info")
dlg0.addFixedField(label="Version:", initial=psychopy.__version__)
list0 = dlg0.show()
log0.info(f"\n{jsonable(list0)}")
if not dlg0.OK:
    psychopy.core.quit()

meta0.sub0 = list0[0]
meta0.ses0 = list0[1]
meta0.run0 = list0[2]
meta0.age0 = list0[3]
meta0.sex0 = list0[4]
meta0.ver0 = list0[5]

meta0.dir0 = f"logs/sub-{meta0.sub0}/ses-{meta0.ses0}/run-{meta0.run0}/date-{meta0.now0}"
meta0.dir0 = pathlib.Path(meta0.dir0)
meta0.dir0.mkdir(mode=0o700, parents=True, exist_ok=True)

meta0.file0 = meta0.dir0/(
    f"sub-{meta0.sub0}"
    f"_ses-{meta0.ses0}"
    f"_run-{meta0.run0}"
    f"_date-{meta0.now0}"
    f"_uuid-{uuid.uuid4()}")

log0.info(jsonable(meta0))

log2 = log0.LogFile(
    meta0.file0.with_suffix(".log").as_posix(),
    filemode='a',
    level=log_level_file)

meta2 = Bunch()
meta2.units = "norm"
meta2.units = "deg"
meta2.units = "pix"
meta2.fullscr = False
meta2.fullscr = True
meta2.screen = 1
meta2.screen = 0
meta2.DISPLAY = ":2"
meta2.DISPLAY = ":1"
meta2.parallel = False
meta2.parallel = True

log0.info(jsonable(meta2))

log0.info("INFO")
log0.debug("DEBUG")
log0.warning("WARNING")

USING_PARPORT = False
USING_PARPORT = True
if USING_PARPORT:
    pp = psychopy.parallel.ParallelPort(address="/dev/parport0")

hand0 = psychopy.data.ExperimentHandler(
    dataFileName=str(meta0.file0), autoLog=True, savePickle=False)

os.environ["DISPLAY"] = meta2.DISPLAY

monitor = "testMonitor"
monitor = psychopy.monitors.Monitor(
    name="testMonitor",
    width=42,
    distance=62,
    gamma=None,
    notes=None,
    useBits=None,
    verbose=True,
    currentCalib=None,
    autoLog=True,
)
psychopy.event.clearEvents()
win0 = psychopy.visual.Window(
    size=(1200, 1000),
    pos=(2900, 100),
    color=(0, 0, 0),
    screen=meta2.screen,
    fullscr=meta2.fullscr,
    monitor=monitor,
    colorSpace="rgb",
    # allowGUI=False,
    # allowStencil=False,
    # blendMode="avg",
    # useFBO=True,
    units=meta2.units,
)
dir8 = pathlib.Path("movies")
files8 = sorted(dir8.glob("z*.mp4"))
assert len(files8) > 0, "WTF: No movies!"
random.shuffle(files8)
movies8 = []
for file8 in files8:
    movie8 = psychopy.visual.VlcMovieStim(
        win=win0,
        name=file8,
        filename=file8,
        size=None,
        units="pix",
        pos=(0, 0),
        loop=False,
        noAudio=False,
        flipVert=False,
        flipHoriz=False,
        volume=0.9,
        autoStart=True)
    movies8.append(movie8)

MARKERS = {}
MARKERS["RESET"] = 0
MARKERS["FIX_CROSS"] = 1
MARKERS["MOVIE"] = {}
MARKERS["MOVIE"][1] = {}
MARKERS["MOVIE"][2] = {}
MARKERS["MOVIE"][3] = {}
MARKERS["MOVIE"][4] = {}
MARKERS["MOVIE"][5] = {}
MARKERS["MOVIE"][6] = {}
MARKERS["MOVIE"][7] = {}
MARKERS["MOVIE"][8] = {}
MARKERS["MOVIE"][9] = {}
MARKERS["MOVIE"][10] = {}
MARKERS["MOVIE"][11] = {}
MARKERS["MOVIE"][12] = {}
MARKERS["MOVIE"][13] = {}
MARKERS["MOVIE"][14] = {}
MARKERS["MOVIE"][15] = {}
MARKERS["MOVIE"][16] = {}
MARKERS["MOVIE"][17] = {}
MARKERS["MOVIE"][18] = {}
MARKERS["MOVIE"][19] = {}
MARKERS["MOVIE"][20] = {}
MARKERS["MOVIE"][1]["BEG"] = 2
MARKERS["MOVIE"][1]["END"] = 3
MARKERS["MOVIE"][1]["DEC"] = 4
MARKERS["MOVIE"][1]["CON"] = 5
MARKERS["MOVIE"][2]["BEG"] = 6
MARKERS["MOVIE"][2]["END"] = 7
MARKERS["MOVIE"][2]["DEC"] = 8
MARKERS["MOVIE"][2]["CON"] = 9
MARKERS["MOVIE"][3]["BEG"] = 10
MARKERS["MOVIE"][3]["END"] = 11
MARKERS["MOVIE"][3]["DEC"] = 12
MARKERS["MOVIE"][3]["CON"] = 13
MARKERS["MOVIE"][4]["BEG"] = 14
MARKERS["MOVIE"][4]["END"] = 15
MARKERS["MOVIE"][4]["DEC"] = 16
MARKERS["MOVIE"][4]["CON"] = 17
MARKERS["MOVIE"][5]["BEG"] = 18
MARKERS["MOVIE"][5]["END"] = 19
MARKERS["MOVIE"][5]["DEC"] = 20
MARKERS["MOVIE"][5]["CON"] = 21
MARKERS["MOVIE"][6]["BEG"] = 22
MARKERS["MOVIE"][6]["END"] = 23
MARKERS["MOVIE"][6]["DEC"] = 24
MARKERS["MOVIE"][6]["CON"] = 25
MARKERS["MOVIE"][7]["BEG"] = 26
MARKERS["MOVIE"][7]["END"] = 27
MARKERS["MOVIE"][7]["DEC"] = 28
MARKERS["MOVIE"][7]["CON"] = 29
MARKERS["MOVIE"][8]["BEG"] = 30
MARKERS["MOVIE"][8]["END"] = 31
MARKERS["MOVIE"][8]["DEC"] = 32
MARKERS["MOVIE"][8]["CON"] = 33
MARKERS["MOVIE"][9]["BEG"] = 34
MARKERS["MOVIE"][9]["END"] = 35
MARKERS["MOVIE"][9]["DEC"] = 36
MARKERS["MOVIE"][9]["CON"] = 37
MARKERS["MOVIE"][10]["BEG"] = 38
MARKERS["MOVIE"][10]["END"] = 39
MARKERS["MOVIE"][10]["DEC"] = 40
MARKERS["MOVIE"][10]["CON"] = 41
MARKERS["MOVIE"][11]["BEG"] = 42
MARKERS["MOVIE"][11]["END"] = 43
MARKERS["MOVIE"][11]["DEC"] = 44
MARKERS["MOVIE"][11]["CON"] = 45
MARKERS["MOVIE"][12]["BEG"] = 46
MARKERS["MOVIE"][12]["END"] = 47
MARKERS["MOVIE"][12]["DEC"] = 48
MARKERS["MOVIE"][12]["CON"] = 49
MARKERS["MOVIE"][13]["BEG"] = 50
MARKERS["MOVIE"][13]["END"] = 51
MARKERS["MOVIE"][13]["DEC"] = 52
MARKERS["MOVIE"][13]["CON"] = 53
MARKERS["MOVIE"][14]["BEG"] = 54
MARKERS["MOVIE"][14]["END"] = 55
MARKERS["MOVIE"][14]["DEC"] = 56
MARKERS["MOVIE"][14]["CON"] = 57
MARKERS["MOVIE"][15]["BEG"] = 58
MARKERS["MOVIE"][15]["END"] = 59
MARKERS["MOVIE"][15]["DEC"] = 60
MARKERS["MOVIE"][15]["CON"] = 61
MARKERS["MOVIE"][16]["BEG"] = 62
MARKERS["MOVIE"][16]["END"] = 63
MARKERS["MOVIE"][16]["DEC"] = 64
MARKERS["MOVIE"][16]["CON"] = 65
MARKERS["MOVIE"][17]["BEG"] = 66
MARKERS["MOVIE"][17]["END"] = 67
MARKERS["MOVIE"][17]["DEC"] = 68
MARKERS["MOVIE"][17]["CON"] = 69
MARKERS["MOVIE"][18]["BEG"] = 70
MARKERS["MOVIE"][18]["END"] = 71
MARKERS["MOVIE"][18]["DEC"] = 72
MARKERS["MOVIE"][18]["CON"] = 73
MARKERS["MOVIE"][19]["BEG"] = 74
MARKERS["MOVIE"][19]["END"] = 75
MARKERS["MOVIE"][19]["DEC"] = 76
MARKERS["MOVIE"][19]["CON"] = 77
MARKERS["MOVIE"][20]["BEG"] = 78
MARKERS["MOVIE"][20]["END"] = 79
MARKERS["MOVIE"][20]["DEC"] = 80
MARKERS["MOVIE"][20]["CON"] = 81


D1 = 0.20
D2 = 2.00
cross2v = psychopy.visual.GratingStim(win=win0, size=[D1, D2], pos=(0.0, 0.0), sf=0, color=(0.5, -1, -1))
cross2h = psychopy.visual.GratingStim(win=win0, size=[D2, D1], pos=(0.0, 0.0), sf=0, color=(0.5, -1, -1))


def fixation_cross(duration_sec):
    """Display fixation cross."""
    cross2v.setColor((-1, -1, -1))
    cross2h.setColor((-1, -1, -1))
    clock_here = psychopy.core.Clock()
    while clock_here.getTime() < duration_sec:
        cross2v.draw()
        cross2h.draw()
        win0.flip()


# hand0.nextEntry()
hand0.addData("clock_mono", clock_mono.getTime())
hand0.addData("clock_glob", clock_glob.getTime())
hand0.addData("clock_main", clock_main.getTime())
hand0.addData("clock_resp", clock_resp.getTime())
hand0.addData("participant", meta0.sub0)
hand0.addData("session", meta0.ses0)
hand0.addData("session", meta0.ses0)
hand0.addData("run", meta0.run0)
hand0.addData("date", meta0.now0)
hand0.addData("event", "experiment_start")


def next_entry(handler, event):
    """Data handler."""
    handler.nextEntry()
    handler.addData("participant", meta0.sub0)
    handler.addData("session", meta0.ses0)
    handler.addData("session", meta0.ses0)
    handler.addData("run", meta0.run0)
    handler.addData("date", meta0.now0)
    handler.addData("event", event)


text0 = (
    "p: Play/Pause/Resume\n"
    "s: Stop\n"
    "q: Stop and Close\n")
ctrls0 = psychopy.visual.TextStim(
    win=win0, text=text0,
    pos=(0.0, 0.0), height=0.08,
    units="norm", wrapWidth=1.9)

text0 = (
    "Za chwilę zobaczą Państwo krótkie wypowiedzi 20 osób. "
    "\n\n"
    "Po obejrzeniu każdej z nich, Państwa zadaniem będzie zdecydowanie "
    "czy dana osoba mówiła PRAWDĘ czy KŁAMAŁA. "
    "\n\n"
    "Odpowiedzi proszę zaznaczać klikając LEWYM przyciskiem myszki na wybraną przez siebie opcję. "
    "\n\n"
    "Po każdej wypowiedzi będą Państwo również proszeni o oszacowanie na 7-stopniowej skali, "
    "na ile są Państwo pewni podjętej decyzji. "
    "Wartość 1 oznacza - „całkowity brak pewności”, "
    "a wartość 7 - „całkowitą pewność”. "
    "\n\n"
    "Proszę o uważne obejrzenie każdego filmu i spontaniczną ocenę bez długiego namysłu. "
    "\n\n"
    "Aby rozpocząć badanie proszę nacisnąć SPACJĘ.")
instr0 = psychopy.visual.TextStim(
    win=win0, text=text0,
    pos=(0.0, 0.0), height=0.08,
    units="norm", wrapWidth=1.9)


if USING_PARPORT:
    pp.setData(0)
    time.sleep(0.100)

fixation_cross(2)

next_entry(hand0, event="instruction_start")
win0.callOnFlip(hand0.addData, "clock_mono", clock_mono.getTime())
win0.callOnFlip(hand0.addData, "clock_glob", clock_glob.getTime())
win0.callOnFlip(hand0.addData, "clock_main", clock_main.getTime())
win0.callOnFlip(hand0.addData, "clock_resp", clock_resp.getTime())

begin0 = False
psychopy.event.clearEvents()
while not begin0:
    instr0.draw()
    win0.flip()
    keys0 = psychopy.event.getKeys(
        keyList=["q", "escape", "space"])
    if len(keys0) > 0:
        for key in keys0:
            if key in ["escape", "q"]:
                win0.close()
                psychopy.core.quit()
            elif key in ["space"]:
                begin0 = True
            else:
                raise RuntimeError("WTF: Invalid key in the instruction block!")


choices = ["KŁAMSTWO", "PRAWDA"]
random.shuffle(choices)

if USING_PARPORT:
    win0.callOnFlip(pp.setData, MARKERS["FIX_CROSS"])


acceptPreText = "Proszę wybrać"
acceptText = "Dalej"
acceptSize = 1.5
psychopy.event.clearEvents()

for idx, movie8 in enumerate(movies8):
    idx += 1
    if USING_PARPORT:
        pp.setData(0)
        time.sleep(0.100)

    next_entry(hand0, event="fixation")
    fix_dur = 2
    hand0.addData("duration", fix_dur)
    fixation_cross(fix_dur)

    next_entry(hand0, event="movie_start")
    hand0.addData("movie8.name", movie8.name)
    hand0.addData("movie8.width", movie8.width)
    hand0.addData("movie8.videoSize", movie8.videoSize)
    hand0.addData("movie8.duration", movie8.duration)
    win0.callOnFlip(hand0.addData, "clock_mono", clock_mono.getTime())
    win0.callOnFlip(hand0.addData, "clock_glob", clock_glob.getTime())
    win0.callOnFlip(hand0.addData, "clock_main", clock_main.getTime())
    win0.callOnFlip(hand0.addData, "clock_resp", clock_resp.getTime())
    if USING_PARPORT:
        win0.callOnFlip(pp.setData, MARKERS["MOVIE"][idx]["BEG"])

    psychopy.event.clearEvents()
    while not movie8.isFinished:
        movie8.draw()
        # ctrls0.draw()
        win0.flip()
        key_list = ["p", "q", "s", "escape", "space"]
        key_list = ["p", "q", "escape", "space"]
        key_list = ["p", "q", "escape"]
        keys0 = psychopy.event.getKeys(
            keyList=key_list)
        if len(keys0) > 0:
            for key in keys0:
                if key in ["escape", "q"]:
                    win0.close()
                    psychopy.core.quit()
                elif key in ["s"]:
                    movie8.stop()
                elif key in ["space", "p"]:
                    if movie8.status == PLAYING:
                        print("PAUSE")
                        movie8.pause()
                    elif movie8.status == PAUSED:
                        print("RESUME")
                        movie8.play()
                    else:
                        raise RuntimeError("WTF: Movie status is neither PLAY nor PAUSE!")

                else:
                    raise RuntimeError("WTF: Invalid key in the movie display block!")

    if USING_PARPORT:
        pp.setData(0)
        time.sleep(0.100)

    next_entry(hand0, event="movie_eval")
    hand0.addData("movie8.name", movie8.name)
    hand0.addData("movie8.width", movie8.width)
    hand0.addData("movie8.videoSize", movie8.videoSize)
    hand0.addData("movie8.duration", movie8.duration)
    win0.callOnFlip(hand0.addData, "clock_mono", clock_mono.getTime())
    win0.callOnFlip(hand0.addData, "clock_glob", clock_glob.getTime())
    win0.callOnFlip(hand0.addData, "clock_main", clock_main.getTime())
    win0.callOnFlip(hand0.addData, "clock_resp", clock_resp.getTime())
    if USING_PARPORT:
        win0.callOnFlip(pp.setData, MARKERS["MOVIE"][idx]["END"])


    myRatingScale = psychopy.visual.RatingScale(
        win=win0, choices=choices,
        marker="triangle", stretch=1.5, tickHeight=1.5,
        acceptSize=acceptSize,
        acceptPreText=acceptPreText, acceptText=acceptText,
        showValue=False, singleClick=False)
    text0 = (
        "PRAWDA czy KŁAMSTWO?\n\n"
        "Prosze wybrać klikając na poniższą skalę.")
    scale_TF_instr = psychopy.visual.TextStim(win=win0, text=text0, pos=(0.0, 0.0), height=0.08, units="norm", wrapWidth=1.9)
    psychopy.event.clearEvents()
    while myRatingScale.noResponse:
        scale_TF_instr.draw()
        myRatingScale.draw()
        win0.flip()
        if psychopy.event.getKeys(["q", "escape"]):
            win0.close()
            psychopy.core.quit()

    if USING_PARPORT:
        pp.setData(0)
        time.sleep(0.100)


    hand0.addData("myRatingScale.getRT", myRatingScale.getRT())
    hand0.addData("myRatingScale.getRating", myRatingScale.getRating())
    hand0.addData("myRatingScale.getHistory", myRatingScale.getHistory())
    log0.info(f"{myRatingScale.getRT() = }")
    log0.info(f"{myRatingScale.getRating() = }")
    log0.info(f"{myRatingScale.getHistory() = }")
    if USING_PARPORT:
        win0.callOnFlip(pp.setData, MARKERS["MOVIE"][idx]["DEC"])

    next_entry(hand0, event="conf_eval")
    hand0.addData("movie8.name", movie8.name)
    hand0.addData("movie8.width", movie8.width)
    hand0.addData("movie8.videoSize", movie8.videoSize)
    hand0.addData("movie8.duration", movie8.duration)
    win0.callOnFlip(hand0.addData, "clock_mono", clock_mono.getTime())
    win0.callOnFlip(hand0.addData, "clock_glob", clock_glob.getTime())
    win0.callOnFlip(hand0.addData, "clock_main", clock_main.getTime())
    win0.callOnFlip(hand0.addData, "clock_resp", clock_resp.getTime())
    myRatingScale = psychopy.visual.RatingScale(
        win=win0, low=1, high=7,
        marker="triangle", stretch=1.5, tickHeight=1.5,
        tickMarks=[1, 2, 3, 4, 5, 6, 7],
        labels=["całkowity brak pewności", "", "", "", "", "", "całkowita pewność"],
        acceptSize=acceptSize,
        acceptPreText=acceptPreText, acceptText=acceptText,
        showValue=False, singleClick=False)
    text0 = (
        "Pewność dokonanej oceny.\n\n"
        "Prosze wybrać klikając na poniższą skalę.")
    scale_CF_instr = psychopy.visual.TextStim(win=win0, text=text0, pos=(0.0, 0.0), height=0.08, units="norm", wrapWidth=1.9)
    psychopy.event.clearEvents()
    while myRatingScale.noResponse:
        scale_CF_instr.draw()
        myRatingScale.draw()
        win0.flip()
        if psychopy.event.getKeys(["q", "escape"]):
            win0.close()
            psychopy.core.quit()

    hand0.addData("myRatingScale.getRT", myRatingScale.getRT())
    hand0.addData("myRatingScale.getRating", myRatingScale.getRating())
    hand0.addData("myRatingScale.getHistory", myRatingScale.getHistory())
    log0.info(f"{myRatingScale.getRT() = }")
    log0.info(f"{myRatingScale.getRating() = }")
    log0.info(f"{myRatingScale.getHistory() = }")
    if USING_PARPORT:
        win0.callOnFlip(pp.setData, MARKERS["MOVIE"][idx]["DEC"])
        time.sleep(0.100)

    if USING_PARPORT:
        pp.setData(0)
        time.sleep(0.100)


if USING_PARPORT:
    pp.setData(0)
    time.sleep(0.100)

next_entry(hand0, event="experiment_ended")
if USING_PARPORT:
    pp.setData(214)
    time.sleep(0.100)
    pp.setData(214)
    time.sleep(0.100)
    pp.setData(0)
    time.sleep(0.100)

srsly.write_yaml(meta0.file0.with_suffix(".meta0.yaml"), jsonable(meta0))
srsly.write_yaml(meta0.file0.with_suffix(".meta2.yaml"), jsonable(meta2))
srsly.write_yaml(meta0.file0.with_suffix(".hand0.yaml"), jsonable(hand0.entries))
hand0.saveAsWideText(
    meta0.file0.with_suffix(".hand0.csv"), delim=",", matrixOnly=False, appendFile=None,
    encoding='utf-8-sig', fileCollisionMethod='rename', sortColumns=None)

df0 = pd.DataFrame(hand0.entries)
df0.to_csv("last-run.csv", index=False)
df0.to_csv(meta0.file0.with_suffix(".data0.csv"), index=False)

text0 = ("Dziekuję za udział w badaniu.")
instr0 = psychopy.visual.TextStim(
    win=win0, text=text0,
    pos=(0.0, 0.0), height=0.08,
    units="norm", wrapWidth=1.9)

next_entry(hand0, event="thanks_start")
win0.callOnFlip(hand0.addData, "clock_mono", clock_mono.getTime())
win0.callOnFlip(hand0.addData, "clock_glob", clock_glob.getTime())
win0.callOnFlip(hand0.addData, "clock_main", clock_main.getTime())
win0.callOnFlip(hand0.addData, "clock_resp", clock_resp.getTime())

begin0 = False
psychopy.event.clearEvents()
while not begin0:
    instr0.draw()
    win0.flip()
    keys0 = psychopy.event.getKeys(
        keyList=["q", "escape", "space"])
    if len(keys0) > 0:
        for key in keys0:
            if key in ["escape", "q"]:
                win0.close()
                psychopy.core.quit()
            elif key in ["space"]:
                begin0 = True
            else:
                raise RuntimeError("WTF: Invalid key in the instruction block!")


if USING_PARPORT:
    pp.setData(214)
    time.sleep(0.100)
    pp.setData(214)
    time.sleep(0.100)
    pp.setData(0)
    time.sleep(0.100)
            
win0.close()
psychopy.core.quit()
