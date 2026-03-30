# Minimum Java version required by ROBOT and OTTR
MIN_JAVA_VERSION = 11

# Adoptium API — fetches the latest Java 21 JRE for the current platform
ADOPTIUM_API = (
    "https://api.adoptium.net/v3/binary/latest/21/ga"
    "/{os}/{arch}/jre/hotspot/normal/eclipse"
)

DEPENDENCIES = {
    "robot.jar": "https://github.com/ontodev/robot/releases/latest/download/robot.jar",
    "lutra.jar": "https://www.ottr.xyz/downloads/lutra/lutra-v0.6.20.jar"
}
