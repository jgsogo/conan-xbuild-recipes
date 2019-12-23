#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os


class EmSDKInstallerConan(ConanFile):
    name = "emsdk"
    version = "1.38.29"

    settings = {
        "os": ['Windows', 'Linux', 'Macos'],
        "arch": ['x86_64']
    }
    short_paths = True
    requires = "nodejs/10.15.0@xbuild/testing"
    _source_subfolder = "source_subfolder"

    default_options = {"gtest:shared": True}

    #def build_requirements(self):
    #    self.build_requires("gtest/1.8.1@bincrafters/stable", context="host")

    def requirements(self):
        self.requires("gtest/1.8.1@bincrafters/stable")

    def source(self):
        print("*"*20)
        print(self.settings_host.os)
        print(self.settings_build.os)
        commit = "4eeff61368e7471ae543474e2c36869def9a29fc"
        sha256 = "cb0cce2a985c7b244f80f39be0f328ed2d68e0eb42cdf69fb5b50d68dd68a00f"
        source_url = 'https://github.com/emscripten-core/emsdk/archive/%s.tar.gz' % commit
        tools.get(source_url, sha256=sha256)
        extracted_folder = "emsdk-%s" % commit
        os.rename(extracted_folder, self._source_subfolder)

    def _run(self, command):
        self.output.info(command)
        self.run(command)

    @staticmethod
    def _create_dummy_file(directory):
        if not os.path.isdir(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, "dummy"), "w") as f:
            f.write("\n")

    @staticmethod
    def _chmod_plus_x(filename):
        if os.name == 'posix':
            os.chmod(filename, os.stat(filename).st_mode | 0o111)

    def build(self):
        with tools.chdir(self._source_subfolder):
            emsdk = 'emsdk.bat' if os.name == 'nt' else './emsdk'
            self._chmod_plus_x('emsdk')
            self._run('%s update' % emsdk)

            # skip undesired installation of tools (nodejs, java, python)
            # FIXME: if someone knows easier way to skip installation of tools, please tell me
            self._create_dummy_file(os.path.join("node", "8.9.1_64bit"))
            self._create_dummy_file(os.path.join("java", "8.152_64bit"))
            self._run('%s list' % emsdk)
            self._run('%s install sdk-%s-64bit' % (emsdk, self.version))
            self._run('%s activate sdk-%s-64bit --embedded' % (emsdk, self.version))

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern='*', dst='.', src=self._source_subfolder)

    def _define_tool_var(self, name, value):
        suffix = '.bat' if os.name == 'nt' else ''
        path = os.path.join(self.package_folder, 'emscripten', self.version, '%s%s' % (value, suffix))
        self._chmod_plus_x(path)
        self.output.info('Creating %s environment variable: %s' % (name, path))
        return path

    def package_info(self):
        emsdk = self.package_folder
        em_config = os.path.join(emsdk, '.emscripten')
        emscripten = os.path.join(emsdk, 'emscripten', self.version)
        em_cache = os.path.join(emsdk, '.emscripten_cache')
        toolchain = os.path.join(emscripten, 'cmake', 'Modules', 'Platform', 'Emscripten.cmake')

        self.output.info('Appending PATH environment variable: %s' % emsdk)
        self.env_info.PATH.append(emsdk)

        self.output.info('Appending PATH environment variable: %s' % emscripten)
        self.env_info.PATH.append(emscripten)

        self.output.info('Creating EMSDK environment variable: %s' % emsdk)
        self.env_info.EMSDK = emsdk

        self.output.info('Creating EMSCRIPTEN environment variable: %s' % emscripten)
        self.env_info.EMSCRIPTEN = emscripten

        self.output.info('Creating EM_CONFIG environment variable: %s' % em_config)
        self.env_info.EM_CONFIG = em_config

        self.output.info('Creating EM_CACHE environment variable: %s' % em_cache)
        self.env_info.EM_CACHE = em_cache

        self.output.info('Creating CONAN_CMAKE_TOOLCHAIN_FILE environment variable: %s' % toolchain)
        self.env_info.CONAN_CMAKE_TOOLCHAIN_FILE = toolchain

        self.env_info.CC = self._define_tool_var('CC', 'emcc')
        self.env_info.CXX = self._define_tool_var('CXX', 'em++')
        self.env_info.RANLIB = self._define_tool_var('RANLIB', 'emranlib')
        self.env_info.AR = self._define_tool_var('AR', 'emar')
