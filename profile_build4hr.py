from treeherder.etl import buildapi
from pympler import tracker

tr = tracker.SummaryTracker()
tr.print_diff()
tr.print_diff()
tr.print_diff()
tr.print_diff()

print "-- done clearing print_diff --"
print ""

for j in range(0, 5):
    print ""
    print "<><><><><><><><><><><><><>"
    print "Pass {}".format(j)
    for i in range(0, 3):
        buildapi.Builds4hJobsProcess().run()

    tr.print_diff()