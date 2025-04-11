"""
This manifest allows the pyworkshopsystem code to be frozen into the micropython .uf2.
"""
include("$(PORT_DIR)/boards/manifest.py")
package("computer", base_path="src")  # will be available as "import computer"
package("connect", base_path="src")  # will be available as "import connect"