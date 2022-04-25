cmake_minimum_required(VERSION 3.8)
project(py433d)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES
        py433/__init__.py
        py433/client.py
        py433/configuration.py
        py433/defaults.py
        py433/mqtt.py
        py433/receiver.py
        py433/tcp_server.py
        py433/transmitter.py
        scripts/433c.py
        scripts/433d.py
        433d.conf
        MANIFEST.in
        README.md
        requirements.txt
        setup.py)

add_executable(py433d ${SOURCE_FILES})