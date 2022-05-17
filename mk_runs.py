#! /usr/bin/env python
#
#   script generator for project="2021-S1-MX-14"
#
#

import os
import sys

project="2021-S1-MX-14"

#        obsnums per source (make it negative if not added to the final combination)
on = {}
on['L1157-B1'] = [99000, 99001, 99025, 99026, 99030, 99031, 99035, 99036,                 # 4-may
                  99382, 99383, 99385, 99386, 99390, 99391, 99393, 99394, 99398, 99399,   # 10-may
                  99561, 99562, 99564, 99565, 99569, 99570, 99572, 99573, 99579, 99580,
                         99582, 99583, 99589, 99590, 99592, 99593,                        # 14-may
                         99765, 99766, 99770, 99771, 99776, 99777,-99778,
]

#        common parameters per source on the first dryrun (run1, run2)
pars1 = {}
pars1['L1157-B1'] = "dv=250 dw=400 extent=240 edge=1"
# at this setting beam 2 often has a birdie

#        common parameters per source on subsequent runs (run1a, run2a)
pars2 = {}
pars2['L1157-B1'] = "pix_list=1,3,4,6,7,8,9,10,11,12,13,14,15"
# 99286-99538 has bad beams 14,15
# birdie in beam 2

# below here no need to change code
# ========================================================================

#        helper function for populating obsnum dependant argument
def getargs(obsnum):
    """ search for <obsnum>.args
    """
    f = "%d.args" % obsnum
    if os.path.exists(f):
        lines = open(f).readlines()
        args = ""
        for line in lines:
            if line[0] == '#': continue
            args = args + line.strip() + " "
        return args
    else:
        return ""

#        specific parameters per obsnum will be in files <obsnum>.args
pars3 = {}
for s in on.keys():
    for o1 in on[s]:
        o = abs(o1)
        pars3[o] = getargs(o)


run1  = '%s.run1'  % project
run1a = '%s.run1a' % project
run2  = '%s.run2' % project
run2a = '%s.run2a' % project

fp1 = open(run1,  "w")
fp2 = open(run1a, "w")
fp3 = open(run2,  "w")
fp4 = open(run2a, "w")

#                           single obsnum
n1 = 0
for s in on.keys():
    for o1 in on[s]:
        o = abs(o1)
        cmd1 = "SLpipeline.sh obsnum=%d _s=%s %s admit=0 restart=1 " % (o,s,pars1[s])
        cmd2 = "SLpipeline.sh obsnum=%d _s=%s %s admit=0 %s" % (o,s,pars2[s], pars3[o])
        fp1.write("%s\n" % cmd1)
        fp2.write("%s\n" % cmd2)
        n1 = n1 + 1

#                           combination obsnums
n2 = 0        
for s in on.keys():
    obsnums = ""
    n3 = 0
    for o1 in on[s]:
        o = abs(o1)
        if o1 < 0: continue
        n3 = n3 + 1
        if obsnums == "":
            obsnums = "%d" % o
        else:
            obsnums = obsnums + ",%d" % o
    print('%s[%d/%d] :' % (s,n3,len(on[s])), obsnums)
    cmd3 = "SLpipeline.sh _s=%s admit=0 restart=1 obsnums=%s" % (s, obsnums)
    cmd4 = "SLpipeline.sh _s=%s admit=1 srdp=1  obsnums=%s" % (s, obsnums)
    fp3.write("%s\n" % cmd3)
    fp4.write("%s\n" % cmd4)
    n2 = n2 + 1

print("A proper re-run of %s should be in the following order:" % project)
print(run1)
print(run2)
print(run1a)
print(run2a)
print("Where there are %d single obsnum runs, and %d combination obsnums" % (n1,n2))