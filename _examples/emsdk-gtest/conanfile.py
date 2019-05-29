from conans import ConanFile, CMake


class Testing(ConanFile):
    name = "emsdk-gtest"
    version = "1.0"

    settings = {"os": ["Emscripten"]}
    requires = "zlib/1.2.11@conan/stable"
    exports_sources = ["CMakeLists.txt", "main.cpp"]
    generators = ["cmake"]

    def build_requirements(self):
        self.build_requires("gtest/1.8.1@bincrafters/stable", context="host")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
