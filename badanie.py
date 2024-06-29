#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TODOs:
- [ ] save data after every movie
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
dlg0.addText('Experiment Info')
dlg0.addField('Movies:', choices=["init", "prod", "test", "temp"])
dlg0.addField('ParPort:', choices=[True, False])
dlg0.addField('ParPortDebug:', choices=[True, False])
dlg0.addField('FullScreen:', choices=[True, False])
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
meta0.mov0 = list0[5]
meta0.par0 = list0[6]
meta0.deb0 = list0[7]
meta0.scr0 = list0[8]
meta0.ver0 = list0[9]

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

DEBUG_PARPORT = True
DEBUG_PARPORT = False
DEBUG_PARPORT = meta0.deb0

USING_PARPORT = True
USING_PARPORT = False
USING_PARPORT = meta0.par0

USING_FULLSCR = True
USING_FULLSCR = False
USING_FULLSCR = meta0.scr0

if USING_PARPORT:
    import psychopy.parallel

meta2 = Bunch()
meta2.units = "norm"
meta2.units = "deg"
meta2.units = "pix"
meta2.fullscr = USING_FULLSCR
meta2.screen = 1
meta2.screen = 0
meta2.DISPLAY = ":2"
meta2.DISPLAY = ":1"
meta2.parport = USING_PARPORT

log0.info(jsonable(meta2))

log0.info("INFO")
log0.debug("DEBUG")
log0.warning("WARNING")

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
dir8 = pathlib.Path("movies")/meta0.mov0
files8 = sorted(dir8.glob("z*.mkv"))
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
    "Aby rozpocząć badanie proszę nacisnąć LEWY PRZYCISK MYSZKI.")
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

mouse0 = psychopy.event.Mouse(win=win0)
mouse0.clickReset()

begin0 = False
psychopy.event.clearEvents()
while not begin0:
    instr0.draw()
    win0.flip()
    keys0 = psychopy.event.getKeys(
        keyList=["q", "escape", "space"])
    butt0 = mouse0.getPressed(getTime=False)
    if butt0[0] == 1:
        begin0 = True

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

if DEBUG_PARPORT:
    win0.callOnFlip(print, "PARPORT → 222")

if USING_PARPORT:
    win0.callOnFlip(pp.setData, 222)

acceptPreText = "Proszę wybrać"
acceptText = "Dalej"
acceptSize = 1.5
psychopy.event.clearEvents()
MARKER = 0

for idx, movie8 in enumerate(movies8):
    idx += 1
    if DEBUG_PARPORT:
        print("PARPORT → 0 [FIXED]")

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
    MARKER += 1
    if DEBUG_PARPORT:
        win0.callOnFlip(print, f"PARPORT → {MARKER}")

    if USING_PARPORT:
        win0.callOnFlip(pp.setData, MARKER)
        win0.callOnFlip(hand0.addData, "MRK_MOV_start", MARKER)

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

    if DEBUG_PARPORT:
        print("PARPORT → 0 [FIXED]")

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
    MARKER += 1
    if DEBUG_PARPORT:
        win0.callOnFlip(print, f"PARPORT → {MARKER}")

    if USING_PARPORT:
        win0.callOnFlip(pp.setData, MARKER)
        win0.callOnFlip(hand0.addData, "MRK_MOV_eval", MARKER)

    myRatingScale = psychopy.visual.RatingScale(
        win=win0, choices=choices,
        marker="triangle", stretch=1.5, tickHeight=1.5,
        acceptSize=acceptSize,
        acceptPreText=acceptPreText, acceptText=acceptText,
        ## lineColor=(0, 0, 0),
        ## markerColor=(1, 1, 1),
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

    if DEBUG_PARPORT:
        print("PARPORT → 0 [FIXED]")

    if USING_PARPORT:
        pp.setData(0)
        time.sleep(0.100)

    hand0.addData("myRatingScale.getRT", myRatingScale.getRT())
    hand0.addData("myRatingScale.getRating", myRatingScale.getRating())
    hand0.addData("myRatingScale.getHistory", myRatingScale.getHistory())
    log0.info(f"{myRatingScale.getRT() = }")
    log0.info(f"{myRatingScale.getRating() = }")
    log0.info(f"{myRatingScale.getHistory() = }")
    MARKER += 1
    if DEBUG_PARPORT:
        win0.callOnFlip(print, f"PARPORT → {MARKER}")

    if USING_PARPORT:
        win0.callOnFlip(pp.setData, MARKER)
        win0.callOnFlip(hand0.addData, "MRK_MOV_eval_END", MARKER)

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
        # markerColor=(1, 1, 1),
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
    if DEBUG_PARPORT:
        print("PARPORT → 0 [FIXED]")

    if USING_PARPORT:
        pp.setData(0)
        time.sleep(0.100)

    MARKER += 1
    if DEBUG_PARPORT:
        print(f"PARPORT → {MARKER} [FIXED]")

    if USING_PARPORT:
        pp.setData(MARKER)
        time.sleep(0.100)
        hand0.addData("MRK_MOV_conf_eval", MARKER)

    if DEBUG_PARPORT:
        print("PARPORT → 0 [FIXED]")

    if USING_PARPORT:
        pp.setData(0)
        time.sleep(0.100)


next_entry(hand0, event="experiment_ended")

if DEBUG_PARPORT:
    print("PARPORT → 0 [FIXED]")

if USING_PARPORT:
    pp.setData(0)
    time.sleep(0.100)

if DEBUG_PARPORT:
    print("PARPORT → 225 [FIXED]")

if USING_PARPORT:
    pp.setData(225)
    time.sleep(0.100)
    hand0.addData("MRK_MOV_conf_eval", 225)

if DEBUG_PARPORT:
    print("PARPORT → 0 [FIXED]")

if USING_PARPORT:
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

text0 = ("Dziękujemy za udział w badaniu!")
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
    pp.setData(221)
    time.sleep(0.100)
    pp.setData(221)
    time.sleep(0.100)
    pp.setData(0)
    time.sleep(0.100)
            
win0.close()
psychopy.core.quit()
