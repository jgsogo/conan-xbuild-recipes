#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration


class NodejsInstallerConan(ConanFile):
    name = "nodejs"
    version = "10.15.0"
    description = "nodejs binaries for use in recipes"
    topics = ("conan", "node", "nodejs")
    url = "https://github.com/bincrafters/conan-nodejs_installer"
    homepage = "https://nodejs.org"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = "nodejs.patch"
    settings = "os", "arch"
    _build_subfolder = "build_subfolder"

    def configure(self):
        if self.settings.arch == "x86" and self.settings.os == "Linux":
            raise ConanInvalidConfiguration("Linux x86 is not support by nodejs 10.15.0")

    def source(self):
        arch = "x64" if self.settings.arch == "x86_64" else "x86"
        if tools.os_info.is_windows:
            platform = "win"
            extension = "zip"
        elif tools.os_info.is_macos:
            platform = "darwin"
            extension = "tar.gz"
        elif tools.os_info.is_linux:
            platform = "linux"
            extension = "tar.xz"
        else:
            raise ConanInvalidConfiguration("Actual OS is not supported.")

        filename = "node-v{}-{}-{}".format(self.version, platform, arch)
        source_url = "{}/dist/v{}/{}.{}".format(self.homepage, self.version, filename, extension)
        tools.get(source_url)
        extracted_dir = filename
        os.rename(extracted_dir, self._build_subfolder)

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._build_subfolder)
        self.copy(pattern="*", src=self._build_subfolder, dst="", keep_path=True)

    def package_info(self):
        bin_dir = self.package_folder if tools.os_info.is_windows else os.path.join(self.package_folder, "bin")
        self.env_info.PATH.append(bin_dir)
