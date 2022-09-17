#
# Copyright (C) 2019 - 2022 VMware, Inc. All Rights Reserved.
#
# Licensed under the GNU General Public License v2 (the "License");
# you may not use this file except in compliance with the License. The terms
# of the License are located in the COPYING file of this distribution.
#

import pytest


@pytest.fixture(scope='module', autouse=True)
def setup_test(utils):
    yield
    teardown_test(utils)


def teardown_test(utils):
    pkgname = utils.config["mulversion_pkgname"]
    utils.run(['tdnf', 'erase', '-y', pkgname])


def test_install_no_arg(utils):
    ret = utils.run(['tdnf', 'install'])
    assert ret['retval'] == 1001


def test_install_invalid_arg(utils):
    ret = utils.run(['tdnf', 'install', 'invalid_package'])
    assert ret['retval'] == 1011


def test_install_package_with_version_suffix(utils):
    pkgname = utils.config["mulversion_pkgname"]
    pkgversion = utils.config["mulversion_lower"]
    utils.erase_package(pkgname)

    utils.run(['tdnf', 'install', '-y', '--nogpgcheck', pkgname + '-' + pkgversion])
    assert utils.check_package(pkgname)


def test_install_package_without_version_suffix(utils):
    pkgname = utils.config["mulversion_pkgname"]
    utils.erase_package(pkgname)

    utils.run(['tdnf', 'install', '-y', '--nogpgcheck', pkgname])
    assert utils.check_package(pkgname)


# -v (verbose) prints progress data
def test_install_package_verbose(utils):
    pkgname = utils.config["mulversion_pkgname"]
    utils.erase_package(pkgname)
    utils.run(['tdnf', 'install', '-y', '-v', '--nogpgcheck', pkgname])
    assert utils.check_package(pkgname)


def test_dummy_requires(utils):
    pkg = utils.config["dummy_requires_pkgname"]
    ret = utils.run(['tdnf', 'install', '-y', pkg])
    assert ' nothing provides ' in ret['stderr'][0]


def test_install_testonly(utils):
    pkgname = utils.config["mulversion_pkgname"]
    utils.erase_package(pkgname)

    utils.run(['tdnf', 'install', '-y', '--nogpgcheck', '--testonly', pkgname])
    assert not utils.check_package(pkgname)


# install multiple packages, one that doesn't exist
# expect other pkg will be installed if invoked with --skip-broken
def test_install_skip_broken_missing_pkg(utils):
    pkgname = utils.config["mulversion_pkgname"]
    utils.erase_package(pkgname)
    pkgname_missing = "missing"

    utils.run(['tdnf', 'install', '-y', '--nogpgcheck', '--skip-broken', pkgname, pkgname_missing])
    assert utils.check_package(pkgname)


# install multiple packages, one that doesn't exist
# expect fail if invoked without --skip-broken
def test_install_missing_pkg(utils):
    pkgname = utils.config["mulversion_pkgname"]
    utils.erase_package(pkgname)
    pkgname_missing = "missing"

    utils.run(['tdnf', 'install', '-y', '--nogpgcheck', pkgname, pkgname_missing])
    assert not utils.check_package(pkgname)


# install multiple packages, one with a missing dependency
# expect other pkg will be installed if invoked with --skip-broken
def test_install_skip_broken_missing_dep(utils):
    pkgname = utils.config["mulversion_pkgname"]
    utils.erase_package(pkgname)
    pkgname_missing = "tdnf-missing-dep"

    utils.run(['tdnf', 'install', '-y', '--nogpgcheck', '--skip-broken', pkgname, pkgname_missing])
    assert utils.check_package(pkgname)


# install multiple packages, one with a missing dependency
# expect fail if invoked without --skip-broken
def test_install_missing_dep(utils):
    pkgname = utils.config["mulversion_pkgname"]
    utils.erase_package(pkgname)
    pkgname_missing = "tdnf-missing-dep"

    utils.run(['tdnf', 'install', '-y', '--nogpgcheck', pkgname, pkgname_missing])
    assert not utils.check_package(pkgname)


def test_install_memcheck(utils):
    pkgname = utils.config["mulversion_pkgname"]
    utils.erase_package(pkgname)

    utils.run_memcheck(['tdnf', 'install', '-y', '--nogpgcheck', pkgname])
    assert utils.check_package(pkgname)
