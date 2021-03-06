# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from treeherder.log_parser.artifactbuildercollection import \
    ArtifactBuilderCollection

import simplejson as json
import time


class Command(BaseCommand):
    """Management command to test log parsing"""

    help = """
    Tests the artifact parser by downloading a specified URL, parsing it,
    and then printing the JSON structure representing its result
    """
    args = "<log url>"

    option_list = BaseCommand.option_list + (
        make_option('--profile',
                    action='store',
                    dest='profile',
                    type=int,
                    default=None,
                    help='Profile running command a number of times'),)

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Need to specify (only) log URL")

        if options['profile']:
            num_runs = options['profile']
        else:
            num_runs = 1

        times = []
        for i in range(num_runs):
            start = time.time()
            artifact_bc = ArtifactBuilderCollection(args[0],
                                                    check_errors=True)
            artifact_bc.parse()
            times.append(time.time() - start)

            if not options['profile']:
                for name, artifact in artifact_bc.artifacts.items():
                    print "%s, %s" % (name, json.dumps(artifact))

        if options['profile']:
            print "Timings: %s" % times
            print "Average: %s" % (sum(times)/len(times))
            print "Total: %s" % sum(times)
