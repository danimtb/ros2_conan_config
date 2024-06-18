from conan.tools.files import save
from conan.tools.cmake import CMakeDeps

import os

ament_prefix_path_dsv = """\
prepend-non-duplicate;AMENT_PREFIX_PATH;
"""

ament_prefix_path_sh = """\
# copied from
# ament_cmake_core/cmake/environment_hooks/environment/ament_prefix_path.sh

ament_prepend_unique_value AMENT_PREFIX_PATH "$AMENT_CURRENT_PREFIX"
"""

library_path_dsv = """\
prepend-non-duplicate;LD_LIBRARY_PATH;lib
"""

library_path_sh = """\
# copied from ament_package/template/environment_hook/library_path.sh

# detect if running on Darwin platform
_UNAME=`uname -s`
_IS_DARWIN=0
if [ "$_UNAME" = "Darwin" ]; then
  _IS_DARWIN=1
fi
unset _UNAME

if [ $_IS_DARWIN -eq 0 ]; then
  ament_prepend_unique_value LD_LIBRARY_PATH "$AMENT_CURRENT_PREFIX/lib"
else
  ament_prepend_unique_value DYLD_LIBRARY_PATH "$AMENT_CURRENT_PREFIX/lib"
fi
unset _IS_DARWIN
"""

path_dsv = """\
prepend-non-duplicate-if-exists;PATH;bin
"""

path_sh = """\
# copied from ament_cmake_core/cmake/environment_hooks/environment/path.sh

if [ -d "$AMENT_CURRENT_PREFIX/bin" ]; then
  ament_prepend_unique_value PATH "$AMENT_CURRENT_PREFIX/bin"
fi
"""

cmake_prefix_path_dsv = """\
prepend-non-duplicate;CMAKE_PREFIX_PATH;
"""

cmake_prefix_path_ps1 = """\
# generated from colcon_powershell/shell/template/hook_prepend_value.ps1.em

colcon_prepend_unique_value CMAKE_PREFIX_PATH "$env:COLCON_CURRENT_PREFIX"
"""

cmake_prefix_path_sh = """\
# generated from colcon_core/shell/template/hook_prepend_value.sh.em

_colcon_prepend_unique_value CMAKE_PREFIX_PATH "$COLCON_CURRENT_PREFIX"
"""


class Ament(CMakeDeps):
    def __init__(self, conanfile):
        CMakeDeps.__init__(self, conanfile)
        self._conanfile = conanfile

    def generate(self):
        # conan_library-consumer\install\package_dep\share\ament_index\resource_index\package_run_dependencies\package_dep : poco;ament_lint_auto;ament_lint_common
        # conan_library-consumer\install\package_dep\share\ament_index\resource_index\packages\package_dep : 
        # conan_library-consumer\install\package_dep\share\ament_index\resource_index\parent_prefix_path\package_dep : /opt/ros/humble
        # conan_library-consumer\install\package_dep\share\colcon-core\packages\package_dep : poco
        # conan_library-consumer\install\package_dep\share\package_dep\cmake\package_depConfig.cmake
        # conanfile.output_folder
        deps_info = ""
        for dep, _ in self._conanfile.dependencies.items():
            ref_name = dep.ref.name
            paths_content = [
                (os.path.join("install", ref_name, "share", "ament_index", "resource_index", "package_run_dependencies", ref_name), ""),
                (os.path.join("install", ref_name, "share", "ament_index", "resource_index", "packages", ref_name), ""),
                (os.path.join("install", ref_name, "share", "ament_index", "resource_index", "parent_prefix_path", ref_name), "/opt/ros/humble"),
                (os.path.join("install", ref_name, "share", "colcon-core", "packages", ref_name), ""),
                # (os.path.join("install", ref_name, "share", ref_name, "cmake", f"{ref_name}Config.cmake"), ""),
                (os.path.join("install", ref_name, "share", ref_name, "environment", "ament_prefix_path.dsv"), ament_prefix_path_dsv),
                (os.path.join("install", ref_name, "share", ref_name, "environment", "ament_prefix_path.sh"), ament_prefix_path_sh),
                (os.path.join("install", ref_name, "share", ref_name, "environment", "library_path.dsv"), library_path_dsv),
                (os.path.join("install", ref_name, "share", ref_name, "environment", "library_path.sh"), library_path_sh),
                (os.path.join("install", ref_name, "share", ref_name, "environment", "path.dsv"), path_dsv),
                (os.path.join("install", ref_name, "share", ref_name, "environment", "path.sh"), path_sh),
                (os.path.join("install", ref_name, "share", ref_name, "hook", "cmake_prefix_path.dsv"), cmake_prefix_path_dsv),
                (os.path.join("install", ref_name, "share", ref_name, "hook", "cmake_prefix_path.ps1"), cmake_prefix_path_ps1),
                (os.path.join("install", ref_name, "share", ref_name, "hook", "cmake_prefix_path.sh"), cmake_prefix_path_sh),
            ]
            for path, content in paths_content:
                save(self._conanfile, path, content)
            generator_files = self.content
            for generator_file, content in generator_files.items():
                file_path = os.path.join("install", ref_name, "share", ref_name, "cmake", generator_file)
                save(self._conanfile, file_path, content)
