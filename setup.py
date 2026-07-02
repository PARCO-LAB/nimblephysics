import os
import shutil
import re
import sys
import platform
import subprocess

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion
from pathlib import Path

try:
    import pybind11
except ImportError:
    pybind11 = None


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir='', target=None):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)
        self.target = target


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(
                re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(
            self.get_ext_fullpath(ext.name)))

        def ensure_external_path(source_path, link_name):
            if not os.path.exists(source_path):
                return None
            if os.path.exists(link_name):
                return link_name
            os.makedirs(os.path.dirname(link_name), exist_ok=True)
            os.symlink(source_path, link_name)
            return link_name

        def ensure_deb_root(deb_name, target_root):
            source_deb = os.path.join(os.path.dirname(__file__), deb_name)
            if os.path.exists(target_root):
                return target_root
            if os.path.exists(source_deb):
                os.makedirs(target_root, exist_ok=True)
                subprocess.check_call(['dpkg-deb', '-x', source_deb, target_root])
                return target_root
            return None

        temp_dep_root = os.path.join('/tmp', 'nimblephysics-deps')
        ccd_root = ensure_deb_root('libccd-dev_2.1-2_amd64.deb', os.path.join(temp_dep_root, 'ccd-root'))
        ensure_deb_root('libccd2_2.1-2_amd64.deb', os.path.join(temp_dep_root, 'ccd-root'))
        external_prefixes = [
            ccd_root,
            ensure_external_path(os.path.join(os.path.dirname(__file__), '.deps', 'eigen-install'),
                                 os.path.join(temp_dep_root, 'eigen-install')),
            ensure_external_path(os.path.join(os.path.dirname(__file__), '.deps', 'ezc3d-install'),
                                 os.path.join(temp_dep_root, 'ezc3d-install')),
            ensure_external_path(os.path.join(os.path.dirname(__file__), '.deps', 'apt-root', 'usr'),
                                 os.path.join(temp_dep_root, 'usr')),
            ensure_external_path(os.path.join('/tmp', 'nimblephysics-deps', 'draco-root', 'usr'),
                                 os.path.join(temp_dep_root, 'draco-root', 'usr')),
        ]
        # required for auto-detection of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        add_python_path_args = os.getenv('NO_PYTHON_ARGS', 'NO') == 'NO'
        print('Add python path args: '+str(add_python_path_args))

        cmake_args = []
        existing_prefix_path = os.getenv('CMAKE_PREFIX_PATH', '')
        cmake_prefix_path = ';'.join(
            [p for p in external_prefixes if p] +
            ([existing_prefix_path] if existing_prefix_path else [])
        )
        if cmake_prefix_path:
            cmake_args += ['-DCMAKE_PREFIX_PATH=' + cmake_prefix_path]

        existing_pkg_config = os.getenv('PKG_CONFIG_PATH', '')
        local_pkg_configs = [
            os.path.join(temp_dep_root, 'ccd-root', 'usr', 'lib', 'x86_64-linux-gnu', 'pkgconfig'),
            os.path.join(temp_dep_root, 'ezc3d-install', 'lib', 'pkgconfig'),
            os.path.join(temp_dep_root, 'usr', 'lib', 'x86_64-linux-gnu', 'pkgconfig'),
        ]
        pkg_config_path = os.pathsep.join(
            [p for p in local_pkg_configs if os.path.exists(p)] +
            ([existing_pkg_config] if existing_pkg_config else [])
        )
        if pkg_config_path:
            cmake_args += ['-DPKG_CONFIG_PATH=' + pkg_config_path]
        if pybind11 is not None:
            cmake_args += ['-Dpybind11_DIR=' + pybind11.get_cmake_dir()]
        # Set our Python version, default to 3.6
        cmake_args += ['-DDARTPY_PYTHON_VERSION:STRING=' +
                       os.getenv('PYTHON_VERSION_NUMBER', '3.6')]
        cmake_args += ['-DPYBIND11_PYTHON_VERSION:STRING=' +
                       os.getenv('PYTHON_VERSION_NUMBER', '3.6')]
        cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                       '-DPYTHON_EXECUTABLE:FILEPATH=' + sys.executable]

        # TODO: We include debug info in our released binaries, because it makes
        # it easier to profile and debug in the wild, which is more valuable than
        # the small performance gain from stripping debug symbols.
        #
        # So this should be 'RelWithDebInfo', not 'Release'. But that seems
        # to causes Azure Pipelines to hang while building our binaries, so this
        # needs investigation.
        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]
        if ext.target is not None:
            build_args += ['--target', ext.target]

        print('Running system specific logic:')
        print('platform.system(): '+str(platform.system()))
        print('platform.machine(): '+str(platform.machine()))

        if platform.system() == "Windows":
            cmake_args += [
                '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            # We need this on the manylinux2010 Docker images to find the correct Python
            if platform.system() == 'Linux' and add_python_path_args:
                # Use ENV vars, and default to 3.8 if we don't specify
                PYTHON_INCLUDE_DIR = os.getenv(
                    'PYTHON_INCLUDE', '/opt/python/cp38-cp38/include/python3.8/')
                PYTHON_LIBRARY = os.getenv(
                    'PYTHON_LIB', '/opt/python/cp38-cp38/lib/python3.8/')
                print('Using PYTHON_INCLUDE_DIR='+PYTHON_INCLUDE_DIR)
                print('Using PYTHON_LIBRARY='+PYTHON_LIBRARY)
                cmake_args += ['-DPYTHON_INCLUDE_DIR:PATH='+PYTHON_INCLUDE_DIR]
                cmake_args += ['-DPYTHON_LIBRARY:FILEPATH='+PYTHON_LIBRARY]
            elif platform.system() == 'Darwin':
                machine = platform.machine()
                if machine == "x86_64":
                    cmake_args += ['-DCMAKE_OSX_ARCHITECTURES=x86_64']
            build_args += ['--', '-j2']

        env = os.environ.copy()
        library_paths = []
        for dep_name in os.listdir(temp_dep_root):
            dep_lib_path = os.path.join(temp_dep_root, dep_name, 'usr', 'lib', 'x86_64-linux-gnu')
            if os.path.isdir(dep_lib_path):
                library_paths.append(dep_lib_path)
        if library_paths:
            env['LD_LIBRARY_PATH'] = os.pathsep.join(library_paths + ([env['LD_LIBRARY_PATH']] if env.get('LD_LIBRARY_PATH') else []))
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        print('Using CMake Args: '+str(cmake_args))
        subprocess.check_call(['cmake', ext.sourcedir] +
                              cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args,
                              cwd=self.build_temp, env=env)

        # Regenerate the stubs
        dir_path = os.path.dirname(os.path.realpath(__file__))
        gen_stubs_script = os.path.join(dir_path, 'generate_pyi_stubs.sh')

        # Get the current python executable and pass it to the script
        python_executable = sys.executable
        subprocess.check_call([gen_stubs_script, extdir, python_executable],
                                cwd=dir_path, env=env)
        
        stubs_home = os.path.join(dir_path, 'stubs', '_nimblephysics-stubs')

        stub_files = os.listdir(stubs_home)
        for file_name in stub_files:
            if os.path.isdir(os.path.join(stubs_home, file_name)):
                if os.path.exists(os.path.join(extdir, file_name)):
                    shutil.rmtree(os.path.join(extdir, file_name))
                shutil.copytree(os.path.join(stubs_home, file_name),
                                os.path.join(extdir, file_name))
            elif os.path.isfile(os.path.join(stubs_home, file_name)):
                if os.path.exists(os.path.join(extdir, file_name)):
                    os.remove(os.path.join(extdir, file_name))
                shutil.copy(os.path.join(stubs_home, file_name),
                            os.path.join(extdir, file_name))

        # Create the __init__.py in the library folder, so that delocate-wheel works properly
        Path(extdir+"/__init__.py").touch()


try:
    with open('VERSION.txt', 'r') as file:
        VERSION = file.read().strip()  # .strip() is safer than .replace()
except FileNotFoundError:
    raise RuntimeError("VERSION.txt not found. This file is required to build the package.")

if not VERSION:
    raise RuntimeError("VERSION.txt is empty. It must contain the package version.")

print("VERSION: " + VERSION)

setup(
    name='nimblephysics-parco',
    version=VERSION,
    author='Keenon Werling',
    author_email='keenonwerling@gmail.com',
    description='A differentiable fully featured physics engine',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    package_dir={'': 'python'},
    packages=['nimblephysics', 'dartpy', 'dartpy.common'],
    package_data={'nimblephysics': ['web_gui/*', 'web_gui/*/*',
                                    'web_gui/*/*/*', 'models/*', 'models/*/*', 'models/*/*/*']},
    ext_package='nimblephysics_libs',
    ext_modules=[CMakeExtension('_nimblephysics', target='_nimblephysics')],
    install_requires=[
        'torch',
        'numpy'
    ],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
)
