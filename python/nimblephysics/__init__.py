import os
import ctypes
import re
import types


def _prepend_runtime_library_paths():
    dep_root = "/tmp/nimblephysics-deps"
    paths = []
    if os.path.isdir(dep_root):
        for dep_name in os.listdir(dep_root):
            lib_path = os.path.join(dep_root, dep_name, "usr", "lib", "x86_64-linux-gnu")
            if os.path.isdir(lib_path):
                paths.append(lib_path)
    if paths:
        current = os.environ.get("LD_LIBRARY_PATH")
        os.environ["LD_LIBRARY_PATH"] = os.pathsep.join(paths + ([current] if current else []))


def _preload_runtime_libraries():
    dep_root = "/tmp/nimblephysics-deps"
    if not os.path.isdir(dep_root):
        return
    library_files = []
    for dep_name in os.listdir(dep_root):
        lib_path = os.path.join(dep_root, dep_name, "usr", "lib", "x86_64-linux-gnu")
        if not os.path.isdir(lib_path):
            continue
        for file_name in os.listdir(lib_path):
            if ".so" not in file_name:
                continue
            library_files.append(os.path.join(lib_path, file_name))

    def preload_priority(path):
        name = os.path.basename(path)
        if "mumps_common" in name:
            return 0
        if name.startswith("libc") and "mumps" in name:
            return 1
        if name.startswith("libd") and "mumps" in name:
            return 2
        if name.startswith("libs") and "mumps" in name:
            return 3
        if name.startswith("libz") and "mumps" in name:
            return 4
        if "esmumps" in name:
            return 5
        return 10

    for path in sorted(library_files, key=preload_priority):
        try:
            ctypes.CDLL(path, mode=ctypes.RTLD_GLOBAL)
        except OSError:
            pass


def _fix_runtime_sonames():
    dep_root = "/tmp/nimblephysics-deps"
    if not os.path.isdir(dep_root):
        return
    pattern = re.compile(r"^(.*?)-(\d+)\.(\d+)\.(\d+)\.so$")
    for dep_name in os.listdir(dep_root):
        lib_path = os.path.join(dep_root, dep_name, "usr", "lib", "x86_64-linux-gnu")
        if not os.path.isdir(lib_path):
            continue
        for file_name in os.listdir(lib_path):
            match = pattern.match(file_name)
            if not match:
                continue
            link_name = f"{match.group(1)}-{match.group(2)}.{match.group(3)}.so"
            link_path = os.path.join(lib_path, link_name)
            target_path = os.path.join(lib_path, file_name)
            if not os.path.exists(link_path):
                try:
                    os.symlink(target_path, link_path)
                except FileExistsError:
                    pass


_prepend_runtime_library_paths()
_fix_runtime_sonames()
_preload_runtime_libraries()

import nimblephysics_libs._nimblephysics as _nimblephysics
from nimblephysics_libs._nimblephysics import *
server = types.SimpleNamespace()
from .timestep import timestep
from .get_height import get_height
from .get_lowest_point import get_lowest_point
from .get_anthropometric_log_pdf import get_anthropometric_log_pdf
from .get_marker_dist_to_nearest_vertex import get_marker_dist_to_nearest_vertex
from .native_trajectory_support import *
from .mapping import map_to_pos, map_to_vel
from .loader import loadWorld, absPath
from .models import *
from .motion_dynamics_dataset import MotionDynamicsDataset

# This requires additional dependencies on `imageio` and `pybullet`, and
# can be imported separately as `from nimblephysics.bullet_rendered import BulletRenderer`
# from .bullet_renderer import BulletRenderer

__doc__ = "Python bindings from Nimble"
