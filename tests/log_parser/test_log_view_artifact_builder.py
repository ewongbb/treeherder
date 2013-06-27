import json
from datadiff import diff

from treeherder.log_parser.artifactbuildercollection import ArtifactBuilderCollection
from treeherder.log_parser.artifactbuilders import BuildbotLogViewArtifactBuilder

from tests import test_utils
from ..sampledata import SampleData


def do_test(log):
    """
    Test a single log.

    ``log`` - the url prefix of the log to test.  Also searches for the
              result file with the same prefix.
    """

    url = "file://{0}".format(
        SampleData().get_log_path("{0}.txt.gz".format(log)))
    exp = test_utils.load_exp("{0}.logview.json".format(log))

    builder = BuildbotLogViewArtifactBuilder(url)
    lpc = ArtifactBuilderCollection(url, builders=builder)
    lpc.parse()
    act = lpc.artifacts[builder.name]
    # assert act == exp, diff(exp, act)
    # Use this assert when creating new tests and you want to get the actual
    # returned artifact:

    # we can't compare the "logurl" field, because it's a fully qualified url,
    # so it will be different depending on the config it's run in.
    assert "logurl" in act
    del(act["logurl"])
    # leaving the logurl in the exp files so they are a good example of the
    # expected structure.
    del(exp["logurl"])

    assert act == exp, json.dumps(act, indent=4)


def test_crashtest_passing(jm, initial_data):
    """Process a job with a single log reference."""

    do_test(
        "mozilla-central_fedora-b2g_test-crashtest-1-bm54-tests1-linux-build50"
    )


def test_mochitest_pass(jm, initial_data):
    """Process a job with a single log reference."""

    do_test(
        "mozilla-central_mountainlion_test-mochitest-2-bm77-tests1-macosx-build141"
    )


def test_mochitest_fail(jm, initial_data):
    """Process a job with a single log reference."""

    do_test(
        "mozilla-esr17_xp_test_pgo-mochitest-browser-chrome-bm74-tests1-windows-build12"
    )


def test_mochitest_process_crash(jm, initial_data):
    """Test a mochitest log that has PROCESS-CRASH """

    do_test(
        "mozilla-inbound_ubuntu64_vm-debug_test-mochitest-other-bm53-tests1-linux-build122"
    )


def test_jetpack_fail(jm, initial_data):
    """Process a job with a single log reference."""

    do_test(
        "ux_ubuntu32_vm_test-jetpack-bm67-tests1-linux-build16"
    )